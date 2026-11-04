"""validation/longread_calibration.py (T-cal) on simulated reads whose calibration is known exactly, with stand-ins for cutadapt (and, for speed, for the edit distance).

A read is a variant with k substitutions. Its quality line is Q40 everywhere except at the error positions: in a calibrated library each error carries Q0 (a chance of 1 of being
wrong), so the expected errors equal k; in an under-reporting library only a third of the errors are flagged, so the expected errors are about k / 3 and the ratio is about 3.
"""
import ast
import math
import random
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "validation"))
import longread_calibration as lcal  # noqa: E402
import longread_common as lc  # noqa: E402
import longread_filter_check as lf  # noqa: E402
import test_longread_filter_check as t4  # noqa: E402

FWD, REV, lr = t4.FWD, t4.REV, t4.lr


def resolve(pattern: str, rng: random.Random) -> str:
    """A concrete sequence that an IUPAC primer pattern matches."""
    return "".join(rng.choice(lr.IUPAC[c]) for c in pattern)


def make_variants(length: int = 150):
    rng = random.Random(11)
    mk = lambda: "".join(rng.choice("ACGT") for _ in range(length))
    return [("A_v1|A|1_copies", mk()), ("A_v2|A|1_copies", mk()), ("B_v1|B|1_copies", mk())]


def make_reads(variants, n, mode="calibrated", rescued_mode=None, rescued_every=0, seed=1, reverse_every=3):
    """n reads: k = 0..8 errors in turn; every `rescued_every`-th read has an insertion in its 5' primer (found only by an indel-tolerant search)."""
    rng = random.Random(seed)
    out = []
    for i in range(n):
        k = i % 9
        seq = list(variants[i % len(variants)][1])
        positions = rng.sample(range(10, len(seq) - 10), k)
        for pos in positions:
            seq[pos] = rng.choice([b for b in "ACGT" if b != seq[pos]])
        is_rescued = bool(rescued_every) and i % rescued_every == 0
        m = (rescued_mode or mode) if is_rescued else mode
        flagged = positions if m == "calibrated" else positions[: math.ceil(k / 3)]
        qual = ["I"] * len(seq)
        for pos in flagged:
            qual[pos] = "!"
        five = resolve(FWD, rng)
        if is_rescued:
            five = five[:8] + rng.choice("ACGT") + five[8:]
        full_seq = five + "".join(seq) + lr.revcomp(resolve(REV, rng))
        full_qual = "I" * len(five) + "".join(qual) + "I" * 19
        if i % reverse_every == 0:
            full_seq, full_qual = lr.revcomp(full_seq), full_qual[::-1]
        out.append((full_seq, full_qual))
    return out


def hamming_nearest(queries, targets, cap=50, chunk=0):
    """A fast stand-in for the edit distance: the reads here differ from their variant by substitutions only."""
    d, ix = [], []
    for q in queries:
        scores = [sum(a != b for a, b in zip(q, t)) + abs(len(q) - len(t)) for t in targets]
        j = int(np.argmin(scores))
        d.append(min(scores[j], cap + 1))
        ix.append(j)
    return np.array(d, dtype=np.int32), np.array(ix, dtype=np.int32)


def named_stand_in_cutadapt(src, dst, primer_f, primer_r, errors, indels):
    """The stand-in of the L4 tests renumbers the reads it writes; cutadapt keeps their names, and T-cal matches the two outputs by name, so this one keeps them too."""
    import gzip
    records = list(lc.iter_fastq(Path(src)))
    out = []
    if indels:
        loc = lr.Locator(primer_f, primer_r, 60, errors)
        for (name, seq, qual), (orientation, category, start, end) in zip(records, loc.locate_many([s for _, s, _ in records])):
            if category == "both":
                out.append((name, seq[start:end], qual[start:end]) if orientation == "+" else (name, lr.revcomp(seq[start:end]), qual[start:end][::-1]))
    else:
        for name, seq, qual in records:
            hit = t4.trim_hamming(seq, qual, primer_f, primer_r, int(errors)) or t4.trim_hamming(lr.revcomp(seq), qual[::-1], primer_f, primer_r, int(errors))
            if hit:
                out.append((name,) + hit)
    with gzip.open(Path(dst), "wt") as fh:
        for name, seq, qual in out:
            fh.write(f"@{name}\n{seq}\n+\n{qual}\n")


@pytest.fixture
def stand_ins(monkeypatch):
    monkeypatch.setattr(lf, "run_cutadapt", named_stand_in_cutadapt)
    monkeypatch.setattr(lc, "nearest", hamming_nearest)
    monkeypatch.setattr(lf, "check_tools", lambda: None)
    monkeypatch.setattr(lc, "check_cutadapt", lambda: None)


def write_library(folder: Path, name: str, reads: list) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    t4.write_fastq(folder / name, reads)
    return folder


def expected_fasta(tmp_path, variants):
    p = tmp_path / "expected.fasta"
    p.write_text("".join(f">{n}\n{s}\n" for n, s in variants))
    return p


SMALL = (5, 5, 3)


def run(tmp_path, libraries, variants, **kw):
    return lcal.run(libraries, expected_fasta(tmp_path, variants), FWD, REV, tmp_path / "out", reads=0, min_reads=kw.pop("min_reads", SMALL), log=lambda *_: None, **kw)


def test_calibrated_libraries_meet_all_three_gates(tmp_path, stand_ins):
    v = make_variants()
    libs = {"One": write_library(tmp_path / "one", "a.fastq.gz", make_reads(v, 450, rescued_every=5, seed=2)),
            "Two": write_library(tmp_path / "two", "b.fastq.gz", make_reads(v, 450, rescued_every=5, seed=3))}
    r = run(tmp_path, libs, v)
    assert {g: s for g, (s, _) in r["gates"].items()} == {"T-cal-1": "MET", "T-cal-2": "MET", "T-cal-3": "MET"}
    ratios = [b["ratio"] for b in r["stats"]["One"]["all"] if b["i"] in lcal.FROM_ONE and b["ratio"]]
    assert ratios and all(0.9 < x < 1.1 for x in ratios)
    assert r["stats"]["One"]["rescued_reads"] > 50                                   # about a fifth of the reads are found only with indels allowed


def test_a_library_that_flags_a_third_of_its_errors_fails_the_first_two_gates(tmp_path, stand_ins):
    v = make_variants()
    libs = {"Good": write_library(tmp_path / "g", "a.fastq.gz", make_reads(v, 450, "calibrated", seed=4)),
            "Hopeful": write_library(tmp_path / "h", "b.fastq.gz", make_reads(v, 450, "third", seed=5))}
    r = run(tmp_path, libs, v)
    assert r["gates"]["T-cal-1"][0] == "NOT MET" and r["gates"]["T-cal-2"][0] == "NOT MET"
    assert any("Hopeful" in n and "OUTSIDE" in n for n in r["gates"]["T-cal-1"][1]) and not any("Good" in n and "OUTSIDE" in n for n in r["gates"]["T-cal-1"][1])
    assert any("BEYOND" in n for n in r["gates"]["T-cal-2"][1])


def test_rescued_reads_with_hidden_errors_fail_the_third_gate_only(tmp_path, stand_ins):
    v = make_variants()
    libs = {"Mixed": write_library(tmp_path / "m", "a.fastq.gz", make_reads(v, 900, "calibrated", rescued_mode="third", rescued_every=3, seed=6))}
    r = run(tmp_path, libs, v)
    assert r["gates"]["T-cal-3"][0] == "NOT MET" and r["gates"]["T-cal-2"][0] == "NOT DECIDED"          # one library type only: nothing to compare
    assert any("rescued" in n and "BEYOND" in n for n in r["gates"]["T-cal-3"][1])


def test_a_gate_with_no_bin_to_judge_is_not_decided(tmp_path, stand_ins):
    v = make_variants()
    libs = {"Tiny": write_library(tmp_path / "t", "a.fastq.gz", make_reads(v, 40, seed=7))}
    r = run(tmp_path, libs, v, min_reads=lcal.MIN_READS)                               # 300 reads per bin are asked for; there are 40 reads
    assert {s for s, _ in r["gates"].values()} == {"NOT DECIDED"}
    assert "No bin had enough reads to be judged" in (tmp_path / "out" / "TCAL.md").read_text()


def test_reads_far_from_every_variant_are_unmatched_and_left_out(tmp_path, stand_ins):
    v = make_variants()
    rng = random.Random(8)
    stranger = [(resolve(FWD, rng) + "".join(rng.choice("ACGT") for _ in range(150)) + lr.revcomp(resolve(REV, rng)), "I" * 189) for _ in range(30)]
    libs = {"L": write_library(tmp_path / "l", "a.fastq.gz", make_reads(v, 90, seed=9) + stranger)}
    r = run(tmp_path, libs, v)
    s = r["stats"]["L"]
    assert s["reads"] == 120 and s["matched"] == 90                                    # the 30 strangers are more than 50 differences from every variant
    assert sum(b["reads"] for b in s["all"]) == 90


def test_bins_and_floor():
    ee = np.array([0.0, 0.01, 0.5, 1.5, 1.5, 12.0])
    dist = np.array([0, 2, 1, 1, 3, 20])
    rows = lcal.bin_rows(ee, dist, np.ones(6, dtype=bool))
    by = {r["bin"]: r for r in rows}
    assert by["[0, 0.05)"]["reads"] == 2 and by["[0.25, 1)"]["reads"] == 1 and by["[1, 2)"]["reads"] == 2 and by["10 and over"]["reads"] == 1
    assert by["[1, 2)"]["mean_ee"] == pytest.approx(1.5) and by["[1, 2)"]["mean_diff"] == pytest.approx(2.0) and by["[1, 2)"]["ratio"] == pytest.approx(2.0 / 1.5)
    assert by["[3, 5)"]["ratio"] is None and by["[3, 5)"]["reads"] == 0
    only_low = lcal.bin_rows(ee, dist, ee < 0.05)
    assert sum(r["reads"] for r in only_low) == 2


def test_the_bins_start_at_the_values_of_the_registered_gate():
    assert lcal.EDGES[:8] == (0.0, 0.05, 0.25, 1.0, 2.0, 3.0, 5.0, 10.0) and [lcal.LABELS[i] for i in lcal.FROM_ONE] == ["[1, 2)", "[2, 3)", "[3, 5)", "[5, 10)", "10 and over"]
    assert lcal.MIN_READS == (300, 300, 100) and (lcal.RATIO_LOW, lcal.RATIO_HIGH, lcal.FACTOR) == (0.5, 2.0, 1.5) and lcal.CAP == 50


def test_composition_bias_and_the_similarity_of_the_compositions(tmp_path, stand_ins):
    v = make_variants()
    shares = tmp_path / "genome_amplicons.tsv"
    shares.write_text("strain\texpected_read_share_percent\nA\t60\nB\t40\n")
    reads_a = make_reads(v, 360, seed=12)                                              # variants A_v1, A_v2, B_v1 in turn: A 2/3, B 1/3
    libs = {"Monomer": write_library(tmp_path / "m", "x.Kinnex16S_Fwd_01--Kinnex16S_Rev_13.hifi_reads.fastq.gz", reads_a),
            "Kinnex": write_library(tmp_path / "k", "y.Kinnex16S_Fwd_01--Kinnex16S_Rev_13.hifi_reads.fastq.gz", make_reads(v, 360, seed=13))}
    r = run(tmp_path, libs, v, strains_table=shares)
    rows = [l.split("\t") for l in (tmp_path / "out" / "bias.tsv").read_text().splitlines()[1:]]
    a_row = [x for x in rows if x[0] == "Monomer" and x[1] == "A"][0]
    assert float(a_row[3]) == pytest.approx(100 * 2 / 3, abs=2.0) and float(a_row[2]) == 60.0 and float(a_row[4]) == pytest.approx(1.11, abs=0.05)
    sims = lcal.pair_similarity(r["composition"])
    assert len(sims) == 1 and sims[0][0] == "Fwd_01--Kinnex16S_Rev_13" and {sims[0][1], sims[0][2]} == {"Monomer", "Kinnex"}
    text = (tmp_path / "out" / "TCAL.md").read_text()
    assert "Same barcode pair in two library types" in text and "Spearman correlation between the expected and the observed read share" in text


def test_outputs_are_written_and_the_intermediate_files_removed(tmp_path, stand_ins):
    v = make_variants()
    libs = {"One": write_library(tmp_path / "o", "a.fastq.gz", make_reads(v, 270, seed=14))}
    run(tmp_path, libs, v)
    out = tmp_path / "out"
    assert {p.name for p in out.iterdir()} == {"tcal_bins.tsv", "composition.tsv", "bias.tsv", "TCAL.md"}
    text = (out / "TCAL.md").read_text()
    assert "**Gate (T-cal-1): MET.**" in text and "## One" in text and "| expected errors | reads |" in text and "floor" in text
    head = (out / "tcal_bins.tsv").read_text().splitlines()
    assert head[0].split("\t")[:4] == ["library", "group", "bin", "reads"] and len(head) == 1 + 3 * 8
    lcal.run({"One": write_library(tmp_path / "o2", "a.fastq.gz", make_reads(v, 30, seed=15))}, expected_fasta(tmp_path, v), FWD, REV, tmp_path / "out2", reads=0, keep=True, min_reads=SMALL, log=lambda *_: None)
    assert (tmp_path / "out2" / "work" / "One").is_dir()


def test_the_real_edit_distance_path_runs_end_to_end_on_short_reads(tmp_path, monkeypatch):
    monkeypatch.setattr(lf, "run_cutadapt", named_stand_in_cutadapt)
    monkeypatch.setitem(sys.modules, "rapidfuzz", None)
    monkeypatch.setitem(sys.modules, "rapidfuzz.distance", None)
    v = make_variants(length=60)
    libs = {"S": write_library(tmp_path / "s", "a.fastq.gz", make_reads(v, 27, seed=16))}
    r = run(tmp_path, libs, v)
    assert r["stats"]["S"]["matched"] == 27 and r["stats"]["S"]["reads"] == 27


def test_library_options_are_parsed_and_checked():
    assert lcal.parse_libraries(["Monomer=C:\\data\\a", "Kinnex = /x/y"]) == {"Monomer": Path("C:\\data\\a"), "Kinnex": Path("/x/y")}
    with pytest.raises(SystemExit, match="NAME=FOLDER"):
        lcal.parse_libraries(["no-equals-sign"])


def test_an_empty_folder_and_an_empty_reference_are_refused(tmp_path, stand_ins):
    v = make_variants()
    (tmp_path / "none").mkdir()
    with pytest.raises(SystemExit, match="No FASTQ files"):
        run(tmp_path, {"X": tmp_path / "none"}, v)
    empty = tmp_path / "empty.fasta"
    empty.write_text("")
    with pytest.raises(SystemExit, match="No expected variants"):
        lcal.run({"X": tmp_path / "none"}, empty, FWD, REV, tmp_path / "o", log=lambda *_: None)


def test_the_command_line(tmp_path, stand_ins, monkeypatch):
    monkeypatch.setattr(lf, "SAMPLING", "spread")                                           # restored after the test, whatever the command line sets
    v = make_variants()
    folder = write_library(tmp_path / "c", "a.fastq.gz", make_reads(v, 90, seed=17))
    rc = lcal.main(["--library", f"Cli={folder}", "--expected", str(expected_fasta(tmp_path, v)), "--primer-f", FWD, "--primer-r", REV, "--out", str(tmp_path / "o"), "--reads", "0", "--sampling", "first"])
    assert rc == 0 and (tmp_path / "o" / "TCAL.md").is_file() and lf.SAMPLING == "first"             # --sampling reaches the shared setting


def test_the_script_parses_as_python_3_9():
    ast.parse(Path(lcal.__file__).read_text(), feature_version=(3, 9))
