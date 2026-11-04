"""validation/longread_filter_check.py with stand-ins for cutadapt and DADA2, on simulated long reads whose properties are known exactly.

The stand-ins implement the documented behaviour of the real tools (cutadapt: both primers, either orientation, reads without both dropped;
DADA2: reads kept when their expected errors are at or under maxEE), so these tests check the script's own logic: the comparison, the gate,
the arms of the primer table and the files written. The real tools are checked by running the script on real data.
"""
import gzip
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "validation"))
import longread_describe as lr  # noqa: E402
import longread_filter_check as lf  # noqa: E402

FWD, REV = "AGRGTTYGATYMTGGCTCAG", "RGYTACCTTGTTACGACTT"
INSERT = 400


def choices(primer: str) -> str:
    return "".join(random.choice(lr.IUPAC[c]) for c in primer)


def qualities(n: int, k_low: int, seed: int) -> str:
    """Q93 everywhere except k_low bases of Q5 (0.316 expected errors each) inside the amplicon, so a read's expected errors are 0.316 * k_low."""
    rng = random.Random(seed)
    q = [93] * n
    for i in rng.sample(range(40, n - 40), k_low):
        q[i] = 5
    return "".join(chr(33 + v) for v in q)


def make_reads(n_fwd: int, n_rev: int, n_indel: int, n_none: int, seed: int = 1) -> list:
    random.seed(seed)
    rng = random.Random(seed)
    out = []
    for i in range(n_fwd + n_rev + n_indel + n_none):
        amp = "".join(rng.choice("ACGT") for _ in range(INSERT))
        five = choices(FWD)
        if n_fwd + n_rev <= i < n_fwd + n_rev + n_indel:
            five = five[:8] + rng.choice("ACGT") + five[8:]                    # an insertion inside the 5' primer
        seq = five + amp + lr.revcomp(choices(REV))
        if n_fwd <= i < n_fwd + n_rev:
            seq = lr.revcomp(seq)
        if i >= n_fwd + n_rev + n_indel:
            seq = "".join(rng.choice("ACGT") for _ in range(len(seq)))        # no primers at all
        qual = qualities(len(seq), rng.randint(0, 40), seed * 1000 + i)
        if n_fwd <= i < n_fwd + n_rev:
            qual = qual[::-1]
        out.append((seq, qual))
    return out


def write_fastq(path: Path, records) -> None:
    with gzip.open(path, "wt") as fh:
        for i, (seq, qual) in enumerate(records):
            fh.write(f"@r{i}\n{seq}\n+\n{qual}\n")


def read_back(path: Path) -> list:
    with gzip.open(path, "rt") as fh:
        lines = fh.read().splitlines()
    return [(lines[i + 1], lines[i + 3]) for i in range(0, len(lines), 4)]


def mismatches(seq: str, primer: lr.Primer) -> int:
    return sum(0 if c in "ACGT" and primer.allowed[i, "ACGT".index(c)] else 1 for i, c in enumerate(seq))


def trim_hamming(seq: str, qual: str, primer_f: str, primer_r: str, k: int, window: int = 60):
    f, r_rc = lr.Primer(primer_f), lr.Primer(lr.revcomp(primer_r))
    start = next((o + len(f) for o in range(window + 1) if o + len(f) <= len(seq) and mismatches(seq[o:o + len(f)], f) <= k), None)
    end = next((len(seq) - o - len(r_rc) for o in range(window + 1) if len(seq) - o - len(r_rc) >= 0
                and mismatches(seq[len(seq) - o - len(r_rc): len(seq) - o], r_rc) <= k), None)
    return (seq[start:end], qual[start:end]) if start is not None and end is not None and end > start else None


def stand_in_cutadapt(src, dst, primer_f, primer_r, errors, indels):
    reads = read_back(Path(src))
    out = []
    if indels:                                              # the edit-distance search, as the describer does it
        loc = lr.Locator(primer_f, primer_r, 60, errors)
        for (seq, qual), (orientation, category, start, end) in zip(reads, loc.locate_many([s for s, _ in reads])):
            if category == "both":
                out.append((seq[start:end], qual[start:end]) if orientation == "+" else (lr.revcomp(seq[start:end]), qual[start:end][::-1]))
    else:                                                   # mismatches only
        for seq, qual in reads:
            hit = trim_hamming(seq, qual, primer_f, primer_r, int(errors)) or trim_hamming(lr.revcomp(seq), qual[::-1], primer_f, primer_r, int(errors))
            if hit:
                out.append(hit)
    write_fastq(Path(dst), out)


def expected_errors(qual: str) -> float:
    return float(np.sum(10.0 ** (-(np.frombuffer(qual.encode("ascii"), dtype=np.uint8).astype(float) - 33) / 10)))


def stand_in_filter(reads, grid, table):
    recs = read_back(Path(reads))
    return {float(g): (len(recs), sum(1 for _, q in recs if expected_errors(q) <= g)) for g in grid}


def stand_in_remove_primers(reads, primer_f, primer_r, table):
    recs = read_back(Path(reads))
    kept = sum(1 for s, q in recs if trim_hamming(s, q, primer_f, primer_r, 2) or trim_hamming(lr.revcomp(s), q[::-1], primer_f, primer_r, 2))
    return len(recs), kept


@pytest.fixture
def folder(tmp_path):
    d = tmp_path / "reads"
    d.mkdir()
    write_fastq(d / "sampleA.fastq.gz", make_reads(120, 100, 60, 40, seed=3))
    return d


@pytest.fixture
def stand_ins(monkeypatch):
    monkeypatch.setattr(lf, "run_cutadapt", stand_in_cutadapt)
    monkeypatch.setattr(lf, "dada2_filter", stand_in_filter)
    monkeypatch.setattr(lf, "dada2_remove_primers", stand_in_remove_primers)


def test_the_gate_is_met_when_the_estimate_and_the_filter_agree(folder, tmp_path, stand_ins):
    results = lf.check_folder(folder, tmp_path / "out", FWD, REV, log=lambda *_: None)
    rows = results[0]["rows"]
    assert [r["maxEE"] for r in rows] == [1, 2, 3, 5, 10]
    assert all(r["within"] for r in rows) and all(abs(r["difference"]) < 1e-9 for r in rows)
    assert 0.05 < rows[0]["estimate"] < rows[-1]["estimate"] <= 1.0                      # a real spread across the grid
    text = (tmp_path / "out" / "FILTER_CHECK.md").read_text()
    assert "Gate (L4): MET" in text and "NOT MET" not in text


def test_the_primer_table_shows_what_indels_cost(folder, tmp_path, stand_ins):
    a = lf.check_folder(folder, tmp_path / "out", FWD, REV, log=lambda *_: None)[0]["arms"]
    assert a["reads"] == 320
    assert a["describer"] == a["cutadapt_indels"] == 280                                 # 40 reads have no primers
    assert a["cutadapt_no_indels"] == a["dada2_remove_primers"] == 220                   # the 60 reads with an insertion in a primer are lost
    text = (tmp_path / "out" / "FILTER_CHECK.md").read_text()
    assert "87.5" in text and "68.8" in text


def test_the_gate_is_not_met_when_dada2_keeps_another_share(folder, tmp_path, monkeypatch):
    monkeypatch.setattr(lf, "run_cutadapt", stand_in_cutadapt)
    monkeypatch.setattr(lf, "dada2_remove_primers", stand_in_remove_primers)

    def off_by_five_points(reads, grid, table):
        n = len(read_back(Path(reads)))
        return {float(g): (n, int(n * min(1.0, 0.5 + 0.05 * i))) for i, g in enumerate(grid)}

    monkeypatch.setattr(lf, "dada2_filter", off_by_five_points)
    results = lf.check_folder(folder, tmp_path / "out", FWD, REV, log=lambda *_: None)
    assert not all(r["within"] for r in results[0]["rows"])
    text = (tmp_path / "out" / "FILTER_CHECK.md").read_text()
    assert "Gate (L4): NOT MET" in text and "sampleA" in text and "| NO |" in text


def test_a_file_without_primers_is_reported_and_the_filter_is_not_run(tmp_path, monkeypatch):
    d = tmp_path / "reads"
    d.mkdir()
    write_fastq(d / "nothing.fastq.gz", make_reads(0, 0, 0, 30, seed=5))
    monkeypatch.setattr(lf, "run_cutadapt", stand_in_cutadapt)
    monkeypatch.setattr(lf, "dada2_remove_primers", stand_in_remove_primers)
    monkeypatch.setattr(lf, "dada2_filter", lambda *a, **k: pytest.fail("the filter must not run without reads"))
    messages = []
    results = lf.check_folder(d, tmp_path / "out", FWD, REV, log=messages.append)
    assert all(r["difference"] is None and not r["within"] for r in results[0]["rows"])
    assert any("no read has both primers" in m for m in messages)
    assert "NOT MET" in (tmp_path / "out" / "FILTER_CHECK.md").read_text()


def test_the_tables_are_written_and_the_intermediate_files_removed(folder, tmp_path, stand_ins):
    out = tmp_path / "out"
    lf.check_folder(folder, out, FWD, REV, log=lambda *_: None)
    head = (out / "filter_check.tsv").read_text().splitlines()
    assert head[0].split("\t") == ["sample", "maxEE", "estimate", "dada2", "difference", "within_tolerance", "reads_in", "reads_out"] and len(head) == 6
    assert (out / "primer_arms.tsv").read_text().splitlines()[0].startswith("sample\treads\tdescriber")
    assert not (out / "work").exists()
    lf.check_folder(folder, tmp_path / "out2", FWD, REV, keep=True, log=lambda *_: None)
    assert (tmp_path / "out2" / "work" / "sampleA" / "cutadapt_indels.fastq.gz").is_file()


def test_the_reads_option_makes_every_step_see_the_same_first_reads(folder, tmp_path, stand_ins, monkeypatch):
    monkeypatch.setattr(lf, "SAMPLING", "first")                                      # the setting of the runs up to 15 October 2026
    a = lf.check_folder(folder, tmp_path / "out", FWD, REV, max_reads=100, log=lambda *_: None)[0]["arms"]
    assert a["reads"] == 100                                                          # 100 forward reads, all with both primers
    assert a["describer"] == a["cutadapt_indels"] == a["cutadapt_no_indels"] == 100


def test_the_reads_option_keeps_n_reads_spread_over_the_file_by_default(folder, tmp_path, stand_ins):
    assert lf.SAMPLING == "spread"
    a = lf.check_folder(folder, tmp_path / "out", FWD, REV, max_reads=100, log=lambda *_: None)[0]["arms"]
    assert a["reads"] == 100 and max(a["describer"], a["cutadapt_indels"], a["cutadapt_no_indels"]) <= 100


def ordered_file(path, per_group=100):
    """Three groups of reads in a row (a stand-in for an ordered file): reads 0-99 carry an A, 100-199 a C and 200-299 a G as their sequence."""
    with open(path, "w") as fh:
        for i in range(3 * per_group):
            fh.write(f"@r{i}\n{'ACG'[i // per_group] * 20}\n+\n{'I' * 20}\n")
    return path


def test_subset_spread_takes_exactly_n_reads_evenly_over_the_file(tmp_path):
    import longread_common as lc
    path = ordered_file(tmp_path / "o.fastq")
    names = lambda p: [n for n, _, _ in lc.iter_fastq(p)]
    spread = lf.subset(path, 30, tmp_path / "s.fastq.gz", mode="spread")
    ids = [int(n[1:]) for n in names(spread)]
    assert len(ids) == 30 and ids == sorted(ids) and len(set(ids)) == 30
    groups = [sum(1 for i in ids if i // 100 == g) for g in range(3)]
    assert groups == [10, 10, 10]                                                       # each third of the file is represented equally
    assert names(lf.subset(path, 30, tmp_path / "s2.fastq.gz", mode="spread")) == names(spread)       # deterministic
    first = lf.subset(path, 30, tmp_path / "f.fastq.gz", mode="first")
    assert [int(n[1:]) for n in names(first)] == list(range(30))                        # the first reads of an ordered file are all of one kind
    assert len(names(lf.subset(path, 0, tmp_path / "a.fastq.gz"))) == 300               # 0 means all reads
    for mode in ("spread", "first"):
        assert len(names(lf.subset(path, 500, tmp_path / f"b_{mode}.fastq.gz", mode=mode))) == 300      # more than the file holds: all of it


def test_subset_follows_the_module_setting_unless_told_otherwise(tmp_path, monkeypatch):
    import longread_common as lc
    path = ordered_file(tmp_path / "o.fastq")
    monkeypatch.setattr(lf, "SAMPLING", "first")
    assert [n for n, _, _ in lc.iter_fastq(lf.subset(path, 10, tmp_path / "x.fastq.gz"))] == [f"r{i}" for i in range(10)]
    monkeypatch.setattr(lf, "SAMPLING", "spread")
    assert len({s for _, s, _ in lc.iter_fastq(lf.subset(path, 30, tmp_path / "y.fastq.gz"))}) == 3          # the three kinds of reads


def test_the_two_cutadapt_commands(tmp_path, monkeypatch):
    seen = []
    monkeypatch.setattr(subprocess, "run", lambda cmd, **k: seen.append(cmd) or subprocess.CompletedProcess(cmd, 0, "", ""))
    lf.run_cutadapt(tmp_path / "in.fastq.gz", tmp_path / "out.fastq.gz", FWD, REV, 0.15, True)
    lf.run_cutadapt(tmp_path / "in.fastq.gz", tmp_path / "out.fastq.gz", FWD, REV, 2, False)
    with_indels, without = seen
    linked = f"{FWD}...{lr.revcomp(REV)}"
    for cmd in seen:
        assert cmd[:3] == [sys.executable, "-m", "cutadapt"] and linked in cmd and "--revcomp" in cmd and "--discard-untrimmed" in cmd
    assert with_indels[with_indels.index("-e") + 1] == "0.15" and "--no-indels" not in with_indels
    assert without[without.index("-e") + 1] == "2" and "--no-indels" in without


def test_a_failing_tool_is_reported_with_its_message(tmp_path, monkeypatch):
    monkeypatch.setattr(subprocess, "run", lambda cmd, **k: subprocess.CompletedProcess(cmd, 1, "", "boom: bad adapter"))
    with pytest.raises(RuntimeError, match="cutadapt failed.*boom"):
        lf.run_cutadapt(tmp_path / "in.fastq.gz", tmp_path / "out.fastq.gz", FWD, REV, 0.15, True)
    monkeypatch.setattr(lf, "find_rscript", lambda: "Rscript")
    with pytest.raises(RuntimeError, match="DADA2 step failed.*boom"):
        lf.run_r(["filter", "x", "1", "y"])


def test_a_missing_rscript_stops_with_the_install_message(monkeypatch):
    monkeypatch.setattr(lf, "find_rscript", lambda: None)
    with pytest.raises(SystemExit, match="Rscript was not found"):
        lf.run_r(["filter", "x", "1", "y"])


def test_compare_and_verdict():
    estimate = {"keep_maxEE_1": 0.70, "keep_maxEE_2": 0.80}
    rows = lf.compare(estimate, {1.0: (1000, 705), 2.0: (1000, 830)}, (1, 2), 0.02)
    assert [r["within"] for r in rows] == [True, False] and rows[1]["difference"] == pytest.approx(0.03)
    met, worst = lf.verdict([("a", rows)], 0.02)
    assert not met and worst["sample"] == "a" and worst["maxEE"] == 2
    assert lf.verdict([], 0.02) == (False, None)


def test_the_r_script_has_both_modes_and_only_maxEE_acts():
    text = (Path(lf.__file__).parent / "filter_check.R").read_text()
    assert 'mode == "filter"' in text and 'mode == "primers"' in text
    assert "filterAndTrim(" in text and "removePrimers(" in text and "dada2:::rc(" in text
    for setting in ("truncQ = 0", "minQ = 0", "maxN = 0", "minLen = 0", "maxLen = Inf", "rm.phix = FALSE"):
        assert setting in text


def test_the_script_parses_as_python_3_9():
    import ast
    ast.parse(Path(lf.__file__).read_text(), feature_version=(3, 9))
