"""validation/arfken_download.py: the list of isolate runs, the ENA addresses, the resumable download and the read-count check. The network is a stand-in."""
import gzip
import importlib.util
import io
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent


def load():
    spec = importlib.util.spec_from_file_location("arfken_download", HERE.parent / "validation" / "arfken_download.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


A = load()


def test_each_marker_has_five_isolates_in_triplicate_and_the_totals_match_the_run_table():
    for key, marker, pairs in (("its1", "ITS1", 4_029_297), ("its2", "ITS2", 1_971_812)):
        runs = A.RUNS[key]
        assert len(runs) == 15 and len({r[0] for r in runs}) == 15 and len({r[1] for r in runs}) == 15
        assert sorted({r[1][0] for r in runs}) == ["C", "K", "M", "P", "T"]
        for iso in "CKMPT":
            assert sorted(r[1] for r in runs if r[1][0] == iso) == [f"{iso}-{marker}{x}" for x in "abc"]
        assert sum(r[2] for r in runs) == pairs
    assert sum(r[3] for k in ("its1", "its2") for r in A.RUNS[k]) == 2_835_704_413


def test_the_mixes_are_three_known_mixes_in_triplicate_for_each_marker():
    for key, marker in (("mix_its1", "ITS1"), ("mix_its2", "ITS2")):
        runs = A.RUNS[key]
        assert len(runs) == 9 and len({r[0] for r in runs}) == 9
        assert sorted(r[1] for r in runs) == sorted(f"Mix{m}-{marker}{x}" for m in "ABC" for x in "abc")
    assert sum(r[2] for r in A.RUNS["mix_its1"]) == 2_005_431


def test_no_two_runs_of_the_two_markers_are_the_same_data():
    """In the run table the ITS1 and ITS2 files of the mixes MixD to MixM have identical read and base counts, which looks like a duplicated deposit; the runs used here must not."""
    seen = {}
    for key, runs in A.RUNS.items():
        for run, library, pairs, bases in runs:
            assert (pairs, bases) not in seen, f"{library} has the same read and base counts as {seen[(pairs, bases)]}"
            seen[(pairs, bases)] = library
    assert len(seen) == 48                                                  # 15 + 15 isolate runs and 9 + 9 mix runs


def test_a_group_names_both_folders_of_the_isolates_or_of_the_mixes(tmp_path, capsys):
    assert A.main(["--base", str(tmp_path), "--dry-run", "--only", "mixes"]) == 0
    out = capsys.readouterr().out
    assert "MIX_ITS1: 9 runs" in out and "MIX_ITS2: 9 runs" in out and "ITS1: 15" not in out
    assert A.main(["--base", str(tmp_path), "--dry-run", "--only", "isolates"]) == 0
    assert "MIX_ITS1" not in capsys.readouterr().out
    assert A.target(tmp_path, "mix_its2", "MixB-ITS2c", 2) == tmp_path / "19_mock_ITS2_arfken_mixes_PRJNA693350" / "raw" / "MixB-ITS2c_R2.fastq.gz"


def test_the_read_length_of_the_run_table_is_bases_per_pair_halved():
    assert A.mean_read_length(100, 56_000) == 280
    its2 = [A.mean_read_length(n, b) for _, _, n, b in A.RUNS["its2"]]
    assert 269 < min(its2) and max(its2) < 280.5                         # 269.96 to 279.91 nt: longer than 250, as the run table says
    its1 = [A.mean_read_length(n, b) for _, _, n, b in A.RUNS["its1"]]
    assert 160 < min(its1) < 165 and 278 < max(its1) < 280


def test_the_addresses_follow_the_ena_folder_rule_seen_in_the_run_table():
    assert A.ena_url("SRR13489866", 1) == "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR134/066/SRR13489866/SRR13489866_1.fastq.gz"
    assert A.ena_url("SRR13496179", 2) == "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR134/079/SRR13496179/SRR13496179_2.fastq.gz"
    assert A.ena_url("SRR13489909", 1).split("/")[-3] == "009"


def test_the_files_get_the_names_that_the_follow_up_reads(tmp_path):
    p = A.target(tmp_path, "its2", "C-ITS2a", 2)
    assert p == tmp_path / "17_mock_ITS2_arfken_isolates_PRJNA693350" / "raw" / "C-ITS2a_R2.fastq.gz"
    assert A.target(tmp_path, "its1", "P-ITS1b", 1).parent.parent.name == "16_mock_ITS1_arfken_isolates_PRJNA693350"


class Net:
    """Stand-in for the network: gives the bytes for an address, after failing a set number of times."""

    def __init__(self, data=b"abc", fail=0):
        self.data, self.fail, self.calls = data, fail, []

    def __call__(self, url):
        self.calls.append(url)
        if len(self.calls) <= self.fail:
            raise OSError("connection reset")
        return io.BytesIO(self.data)


def test_a_download_is_written_whole_kept_when_present_and_retried_when_it_drops(tmp_path):
    dest = tmp_path / "x" / "f.fastq.gz"
    net = Net(fail=2)
    assert A.download("u", dest, opener=net, sleep=lambda s: None) == "downloaded"
    assert dest.read_bytes() == b"abc" and len(net.calls) == 3 and not list(dest.parent.glob("*.part"))
    assert A.download("u", dest, opener=net, sleep=lambda s: None) == "kept" and len(net.calls) == 3      # no new request
    empty = tmp_path / "e.fastq.gz"
    empty.write_bytes(b"")
    assert A.download("u", empty, opener=Net(), sleep=lambda s: None) == "downloaded"                    # an empty file is not a download


class Response(io.BytesIO):
    """A response that says how long the file should be."""

    def __init__(self, data, promised):
        super().__init__(data)
        self.headers = {"Content-Length": str(promised)}


class Sequence:
    """Stand-in for the network that gives a different answer on each request."""

    def __init__(self, *answers):
        self.answers, self.calls = list(answers), 0

    def __call__(self, url):
        a = self.answers[min(self.calls, len(self.answers) - 1)]
        self.calls += 1
        return a() if callable(a) else io.BytesIO(a)


FULL = gzip.compress(b"ACGT" * 1000)


def test_a_connection_that_closes_early_is_noticed_by_the_promised_length_and_retried(tmp_path):
    dest = tmp_path / "f.fastq.gz"
    net = Sequence(lambda: Response(FULL[:20], len(FULL)), lambda: Response(FULL, len(FULL)))
    assert A.download("u", dest, opener=net, sleep=lambda s: None) == "downloaded"
    assert dest.read_bytes() == FULL and net.calls == 2


def test_a_truncated_gzip_is_noticed_without_a_promised_length_and_retried(tmp_path):
    dest = tmp_path / "f.fastq.gz"
    net = Sequence(FULL[:-8], FULL)                                      # the first answer lacks the end marker
    assert A.download("u", dest, opener=net, sleep=lambda s: None, verify=A.verify_gzip) == "downloaded"
    assert A.verify_gzip(dest) and net.calls == 2


def test_a_file_that_is_already_there_but_cut_short_is_repaired_and_a_whole_one_is_kept(tmp_path):
    dest = tmp_path / "f.fastq.gz"
    dest.write_bytes(FULL[:-8])
    net = Sequence(FULL)
    assert A.download("u", dest, opener=net, sleep=lambda s: None, verify=A.verify_gzip) == "repaired"
    assert dest.read_bytes() == FULL and net.calls == 1
    assert A.download("u", dest, opener=net, sleep=lambda s: None, verify=A.verify_gzip) == "kept" and net.calls == 1


def test_verify_gzip_accepts_a_whole_file_and_refuses_a_cut_one_and_a_text_file(tmp_path):
    ok, cut, text = tmp_path / "ok.gz", tmp_path / "cut.gz", tmp_path / "t.gz"
    ok.write_bytes(FULL); cut.write_bytes(FULL[:-8]); text.write_bytes(b"not gzip at all")
    assert A.verify_gzip(ok) is True and A.verify_gzip(cut) is False and A.verify_gzip(text) is False


def test_a_download_gives_up_after_the_retries_and_leaves_no_part_file(tmp_path):
    dest = tmp_path / "f.fastq.gz"
    with pytest.raises(RuntimeError, match="could not download"):
        A.download("u", dest, opener=Net(fail=99), retries=2, sleep=lambda s: None)
    assert not dest.exists() and not list(tmp_path.glob("*.part"))


def fastq_gz(path, n):
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt") as fh:
        for i in range(n):
            fh.write(f"@r{i}\nACGT\n+\nIIII\n")


def test_the_check_finds_a_missing_file_and_a_wrong_read_count(tmp_path):
    runs = [("SRR1", "C-ITS1a", 3, 24), ("SRR2", "C-ITS1b", 3, 24), ("SRR3", "C-ITS1c", 3, 24)]
    fastq_gz(A.target(tmp_path, "its1", "C-ITS1a", 1), 3)
    fastq_gz(A.target(tmp_path, "its1", "C-ITS1a", 2), 3)
    fastq_gz(A.target(tmp_path, "its1", "C-ITS1b", 1), 3)
    fastq_gz(A.target(tmp_path, "its1", "C-ITS1b", 2), 2)               # one read short
    bad = A.check(tmp_path, "its1", runs=runs)
    assert "C-ITS1b mate 2: 2 reads, the run table says 3" in bad
    assert "C-ITS1c mate 1: file missing" in bad and "C-ITS1c mate 2: file missing" in bad
    assert not any(b.startswith("C-ITS1a") for b in bad) and len(bad) == 3
    broken = A.target(tmp_path, "its1", "C-ITS1a", 1)
    broken.write_bytes(b"not a gzip file")
    assert any("C-ITS1a mate 1: cannot be read" in b for b in A.check(tmp_path, "its1", runs=runs[:1]))


def test_main_dry_run_downloads_nothing_and_only_limits_the_marker(tmp_path, capsys):
    assert A.main(["--base", str(tmp_path), "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "ITS1: 15 runs, 4,029,297 read pairs" in out and "ITS2: 15 runs, 1,971,812 read pairs" in out and not list(tmp_path.iterdir())
    assert A.main(["--base", str(tmp_path), "--dry-run", "--only", "its2"]) == 0
    assert "ITS1" not in capsys.readouterr().out


def test_main_downloads_all_sixty_files_and_stops_on_a_failure(tmp_path, capsys):
    net = Net(data=FULL)
    assert A.main(["--base", str(tmp_path), "--only", "its2"], opener=net, sleep=lambda s: None) == 0
    assert len(net.calls) == 30 and len(list((tmp_path / A.DATASETS["its2"] / "raw").glob("*.fastq.gz"))) == 30
    assert "30 downloaded, 0 repaired, 0 already there and complete" in capsys.readouterr().out
    one = A.target(tmp_path, "its2", "C-ITS2a", 1)
    one.write_bytes(FULL[:-8])                                           # a file cut short is repaired by running the same command again
    assert A.main(["--base", str(tmp_path), "--only", "its2"], opener=net, sleep=lambda s: None) == 0
    assert len(net.calls) == 31 and "1 repaired" in capsys.readouterr().out and A.verify_gzip(one)
    assert A.main(["--base", str(tmp_path / "again"), "--only", "its1"], opener=Net(fail=99), sleep=lambda s: None) == 2
    assert "could not download" in capsys.readouterr().out


def test_main_check_reports_the_state_of_the_files(tmp_path, capsys):
    assert A.main(["--base", str(tmp_path), "--check", "--only", "its2"]) == 2
    assert "C-ITS2a mate 1: file missing" in capsys.readouterr().out
