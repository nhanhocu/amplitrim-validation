"""validation/longread_truth.py: the classification of ASVs, the metrics, the registered gates, the conditions, the command of the R script, and a whole run with stand-ins for
cutadapt and DADA2 (this sandbox has neither). The stand-in 'denoiser' keeps every sequence that at least 3 reads share after the same filter, which is enough to check the logic around it."""
import ast
import random
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "validation"))
import longread_common as lc  # noqa: E402
import longread_filter_check as lf  # noqa: E402
import longread_truth as lt  # noqa: E402
import test_longread_calibration as t_cal  # noqa: E402
import test_longread_filter_check as t4  # noqa: E402

FWD, REV, lr = t4.FWD, t4.REV, t4.lr


def seqs(n: int, length: int = 30, seed: int = 5) -> list:
    rng = random.Random(seed)
    return ["".join(rng.choice("ACGT") for _ in range(length)) for _ in range(n)]


NAMES = ["X_v1|X|2_copies", "X_v2|X|1_copies", "Y_v1|Y|1_copies", "W_v1|W|1_copies", "Z_v1|Z|1_copies"]
SEQS = seqs(5)
STRAINS = {"X": {"share": 18.0, "expected": 50.0, "tier": "A", "eligible": True}, "Y": {"share": 1.8, "expected": 30.0, "tier": "A", "eligible": True},
           "W": {"share": 0.18, "expected": 15.0, "tier": "A", "eligible": True}, "Z": {"share": 0.02, "expected": 5.0, "tier": "A (draft)", "eligible": False}}


def mutate(s: str, n: int) -> str:
    out = list(s)
    for i in range(n):
        out[i * 3] = "A" if out[i * 3] != "A" else "C"
    return "".join(out)


def asv(sequence, reads, chimera=False):
    return {"sequence": sequence, "chimera": chimera, "reads": reads, "counts": {"s": reads}}


@pytest.fixture(autouse=True)
def fast_distance(monkeypatch):
    monkeypatch.setattr(lc, "nearest", t_cal.hamming_nearest)


def test_variant_shares_follow_the_copies_of_each_strain():
    shares = lt.variant_shares(NAMES, STRAINS)
    assert shares["X_v1|X|2_copies"] == pytest.approx(50 * 2 / 3) and shares["X_v2|X|1_copies"] == pytest.approx(50 / 3) and shares["Y_v1|Y|1_copies"] == 30.0


def test_asvs_are_classed_exact_near_or_other():
    asvs = [asv(SEQS[0], 400), asv(mutate(SEQS[1], 1), 50), asv(mutate(SEQS[2], 2), 40), asv(mutate(SEQS[3], 4), 20)]
    c = {a["sequence"]: a for a in lt.classify(asvs, NAMES, SEQS)}
    assert c[SEQS[0]]["match"] == "exact" and c[SEQS[0]]["variant"] == NAMES[0] and c[SEQS[0]]["distance"] == 0
    assert c[mutate(SEQS[1], 1)]["match"] == "near" and c[mutate(SEQS[1], 1)]["variant"] == NAMES[1]
    assert c[mutate(SEQS[2], 2)]["match"] == "near"                                                    # 2 edits is still near
    other = c[mutate(SEQS[3], 4)]
    assert other["match"] == "other" and other["distance"] == 4 and other["variant"] == NAMES[3]        # the true nearest variant and distance, not the first variant of the file
    far = lt.classify([asv(mutate(SEQS[4], 6), 5)], NAMES, SEQS, cap=3)[0]
    assert far["match"] == "other" and far["distance"] == 4                                              # beyond the search limit: limit + 1


def test_metrics_count_recall_extra_reads_chimeras_and_the_correlation():
    classified = lt.classify([asv(SEQS[0], 400), asv(SEQS[2], 100), asv(mutate(SEQS[1], 1), 50), asv(mutate(SEQS[3], 5), 20),
                              asv(SEQS[4], 10, chimera=True), asv(mutate(SEQS[0], 6), 30, chimera=True)], NAMES, SEQS)
    m = lt.metrics(classified, NAMES, STRAINS, lt.variant_shares(NAMES, STRAINS))
    assert (m["asvs_final"], m["asvs_exact"], m["asvs_near"], m["asvs_other"], m["asvs_chimeric"]) == (4, 2, 1, 1, 2)
    assert m["reads_final"] == 570 and m["reads_exact"] == 500 and m["reads_near"] == 50 and m["reads_other"] == 20
    assert m["other_share"] == pytest.approx(20 / 570) and m["chimera_share"] == pytest.approx(40 / 610)
    assert m["exact_flagged"] == 1                                                                      # Z_v1 is an expected variant that DADA2 flagged as a chimera
    assert m["variants_recovered"] == 2 and m["variants_total"] == 5
    assert (m["top_total"], m["top_recovered"]) == (3, 2)                                               # X, Y and W have 0.18% or more; X and Y are recovered
    assert (m["big_total"], m["big_recovered"]) == (5, 2)
    assert m["strain_share"]["X"] == pytest.approx(450 / 570) and m["strain_share"]["Y"] == pytest.approx(100 / 570) and m["strain_share"]["W"] == 0.0
    assert m["rho_strains"] == 3 and m["rho"] == pytest.approx(1.0)                                     # X > Y > W in both the expected and the observed shares; the draft Z is left out


def metrics_stub(**kw):
    base = {"top_total": 15, "top_recovered": 15, "big_total": 20, "big_recovered": 19, "other_share": 0.01, "rho": 0.9, "rho_strains": 17, "variants_recovered": 40}
    base.update(kw)
    return base


def test_the_gates_follow_the_registered_thresholds():
    ok = lt.judge({"L": {"ee2": metrics_stub()}}, {"L": 2})["L"]
    assert {k: s for k, (s, _) in ok.items()} == {"T2": "MET", "T3": "MET", "T5": "MET", "T6": "MET"}
    bad = lt.judge({"L": {"ee2": metrics_stub(top_recovered=13, other_share=0.03, rho=0.6)}}, {"L": 2})["L"]
    assert {k: s for k, (s, _) in bad.items()} == {"T2": "NOT MET", "T3": "NOT MET", "T5": "NOT MET", "T6": "MET"}
    assert lt.judge({"L": {"ee2": metrics_stub(big_recovered=15)}}, {"L": 2})["L"]["T2"][0] == "NOT MET"        # 15 of 20 is 75%: below 80%
    assert lt.judge({"L": {"ee2": metrics_stub(big_recovered=16)}}, {"L": 2})["L"]["T2"][0] == "MET"           # 16 of 20 is exactly 80%
    assert lt.judge({"L": {"ee2": metrics_stub(top_recovered=14)}}, {"L": 2})["L"]["T2"][0] == "MET"           # 14 of 15 is enough
    assert lt.judge({"L": {"ee2": metrics_stub(rho=None)}}, {"L": 2})["L"]["T5"][0] == "NOT DECIDED"
    assert {s for s, _ in lt.judge({"L": {"ee3": metrics_stub()}}, {"L": 3})["L"].values()} == {"NOT DECIDED"}        # no ee2 condition: nothing is judged


def test_the_rule_gate_compares_with_maxee_2():
    std = metrics_stub(variants_recovered=40, other_share=0.010)
    same = {"ee2": std, "ee3": metrics_stub(variants_recovered=40, other_share=0.014)}
    assert lt.judge({"K": same}, {"K": 3})["K"]["T6"][0] == "MET"                                      # as many variants, 0.4 points more extra reads
    worse_extra = {"ee2": std, "ee3": metrics_stub(variants_recovered=41, other_share=0.016)}
    assert lt.judge({"K": worse_extra}, {"K": 3})["K"]["T6"][0] == "NOT MET"                           # 0.6 points more extra reads
    fewer = {"ee2": std, "ee3": metrics_stub(variants_recovered=39, other_share=0.010)}
    assert lt.judge({"K": fewer}, {"K": 3})["K"]["T6"][0] == "NOT MET"
    assert lt.judge({"K": {"ee2": std}}, {"K": 3})["K"]["T6"][0] == "NOT DECIDED"                      # the rule's condition was not run


def test_a_header_without_a_copy_number_counts_as_one_copy():
    shares = lt.variant_shares(["A_v1|A|3_copies", "A_v2|A|odd", "B"], {"A": {"expected": 40.0}, "B": {"expected": 5.0}})
    assert shares["A_v1|A|3_copies"] == pytest.approx(40 * 3 / 4) and shares["A_v2|A|odd"] == pytest.approx(40 / 4) and shares["B"] == 5.0


def test_the_registered_thresholds_are_the_ones_in_the_notes():
    assert lt.THRESHOLDS == {"top_strains": 14, "big_fraction": 0.8, "other_max": 0.02, "rho_min": 0.7, "rule_slack": 0.005}
    assert lt.TOP_SHARE == 0.18 and lt.BIG_VARIANT == 1.0 and lt.NEAR == 2 and lt.DEFAULT_GRID == (1, 2, 3, 5, 10)


def test_the_conditions_hold_the_grid_the_rule_and_the_two_extras():
    tags = [c["tag"] for c in lt.build_conditions((1, 2, 3, 5, 10), 3)]
    assert tags == ["ee1", "ee2", "ee3", "ee5", "ee10", "ee2_nowindow", "ee2_dada2primers"]
    assert [c["tag"] for c in lt.build_conditions((1, 2, 3, 5, 10), 4)][:6] == ["ee1", "ee2", "ee3", "ee4", "ee5", "ee10"]           # a rule value outside the grid is added
    by = {c["tag"]: c for c in lt.build_conditions((1, 2), 2)}
    assert by["ee2_nowindow"]["window"] is False and by["ee2_nowindow"]["primers"] == "cutadapt"
    assert by["ee2_dada2primers"]["primers"] == "dada2" and by["ee2_dada2primers"]["window"] is True and by["ee2_dada2primers"]["max_ee"] == 2.0


def test_the_r_command_line_and_its_failure(tmp_path, monkeypatch):
    import subprocess
    seen = []
    monkeypatch.setattr(lt, "find_rscript", lambda: "Rscript")
    monkeypatch.setattr(subprocess, "run", lambda cmd, **k: seen.append(cmd) or subprocess.CompletedProcess(cmd, 0, "", ""))
    r = lt.run_dada2([tmp_path / "a.fastq.gz", tmp_path / "b.fastq.gz"], tmp_path / "w" / "ee2", 2.0, 1310, 1620, 32, "pseudo", 0)
    cmd = seen[0]
    assert cmd[0] == "Rscript" and cmd[1].endswith("truth_dada2.R") and cmd[3:] == [str(tmp_path / "w" / "ee2"), "2", "1310", "1620", "32", "pseudo", "0", "PacBioErrfun"]
    assert Path(cmd[2]).read_text().splitlines() == [str(tmp_path / "a.fastq.gz"), str(tmp_path / "b.fastq.gz")]
    assert r["asv"].name == "ee2_asv.tsv" and r["filter"].name == "ee2_filter.tsv"
    lt.run_dada2([tmp_path / "a.fastq.gz"], tmp_path / "w" / "nw", 2.0, 0, 0, 32, "TRUE", 1, ("AGRG", "RGYT"))
    assert seen[1][5:7] == ["0", "Inf"] and seen[1][-2:] == ["AGRG", "RGYT"] and seen[1][10] == "PacBioErrfun"   # no window is written as 0 and Inf; the error function and then the primers follow
    lt.run_dada2([tmp_path / "a.fastq.gz"], tmp_path / "w" / "bn", 2.0, 0, 0, 32, "pseudo", 0, None, "binned:3,10,40")
    assert seen[2][10] == "binned:3,10,40" and len(seen[2]) == 11
    monkeypatch.setattr(subprocess, "run", lambda cmd, **k: subprocess.CompletedProcess(cmd, 1, "", "Error in learnErrors: boom"))
    with pytest.raises(RuntimeError, match="DADA2 run failed.*boom"):
        lt.run_dada2([tmp_path / "a.fastq.gz"], tmp_path / "w" / "x", 2.0, 0, 0, 32, "pseudo", 0)
    monkeypatch.setattr(lt, "find_rscript", lambda: None)
    with pytest.raises(SystemExit, match="Rscript was not found"):
        lt.run_dada2([tmp_path / "a.fastq.gz"], tmp_path / "w" / "y", 2.0, 0, 0, 32, "pseudo", 0)


def test_the_r_script_has_the_registered_settings():
    text = (Path(lt.__file__).parent / "truth_dada2.R").read_text()
    for part in ("filterAndTrim(", "truncQ = 0", "minQ = 0", "maxN = 0", "rm.phix = FALSE", "errorEstimationFunction = errfun", "makeBinnedQualErrfun(", "binned:", "PacBioErrfun", "BAND_SIZE = band", "removeBimeraDenovo(st, method = \"consensus\"",
                 "removePrimers(", "dada2:::rc(", "orient = TRUE", "_asv.tsv", "_filter.tsv", "chimera = flag"):
        assert part in text, part


def test_asv_and_filter_tables_are_read(tmp_path):
    (tmp_path / "a.tsv").write_text("sequence\tchimera\ts1\ts2\nACGT\tFALSE\t5\t3\nTTTT\tTRUE\t0\t2\n")
    (tmp_path / "f.tsv").write_text("sample\treads_in\treads_out\ns1\t100\t80\ns2\t50\t45\n")
    rows = lt.read_asv(tmp_path / "a.tsv")
    assert rows[0] == {"sequence": "ACGT", "chimera": False, "reads": 8, "counts": {"s1": 5, "s2": 3}} and rows[1]["chimera"] is True and rows[1]["reads"] == 2
    assert lt.read_filter(tmp_path / "f.tsv") == (150, 125)


# ----------------------------------------------------------------------------- a whole run with stand-ins

CHIMERAS = set()


def fake_dada2(files, prefix, max_ee, min_len, max_len, band, pool, threads, primers=None, errfun="PacBioErrfun"):
    """The same filter as DADA2's (expected errors, the length window), then every sequence that at least 3 reads share becomes an ASV."""
    prefix = Path(prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    counts, samples, n_in, n_out = {}, [], 0, 0
    for f in files:
        sample = re.sub(r"\.fastq(\.gz)?$", "", Path(f).name)                # the name that truth_dada2.R gives a sample: the file name without .fastq.gz
        samples.append(sample)
        for _, seq, qual in lc.iter_fastq(f):
            if primers:
                hit = t4.trim_hamming(seq, qual, primers[0], primers[1], 2) or t4.trim_hamming(lr.revcomp(seq), qual[::-1], primers[0], primers[1], 2)
                if not hit:
                    continue
                seq, qual = hit
            n_in += 1
            if lc.expected_errors(qual) > max_ee or (min_len and len(seq) < min_len) or (max_len and len(seq) > max_len):
                continue
            n_out += 1
            counts.setdefault(seq, {}).setdefault(sample, 0)
            counts[seq][sample] += 1
    with open(f"{prefix}_asv.tsv", "w") as fh:
        fh.write("sequence\tchimera\t" + "\t".join(samples) + "\n")
        for s, per in counts.items():
            if sum(per.values()) >= 3:
                fh.write(f"{s}\t{'TRUE' if s in CHIMERAS else 'FALSE'}\t" + "\t".join(str(per.get(x, 0)) for x in samples) + "\n")
    Path(f"{prefix}_filter.tsv").write_text(f"sample\treads_in\treads_out\nall\t{n_in}\t{n_out}\n")
    fake_dada2.calls.append({"tag": prefix.name, "files": [Path(f).parent.name for f in files], "min_len": min_len, "max_len": max_len, "primers": primers, "errfun": errfun})
    return {"asv": Path(f"{prefix}_asv.tsv"), "filter": Path(f"{prefix}_filter.tsv")}


fake_dada2.calls = []


def substitute(seq: str, n: int, start: int = 20) -> str:
    """seq with n substitutions, 3 positions apart from `start` on."""
    out = list(seq)
    for i in range(n):
        j = start + 3 * i
        out[j] = "A" if out[j] != "A" else "C"
    return "".join(out)


def plain_read(seq: str, rng, reverse: bool = False) -> tuple:
    full = t_cal.resolve(FWD, rng) + seq + lr.revcomp(t_cal.resolve(REV, rng))
    q = "I" * len(full)
    return (lr.revcomp(full), q) if reverse else (full, q)


def mock_files(tmp_path):
    """Three expected variants of 150 nt in two strains (X with two variants, Y with one); a fourth strain Z has no read at all."""
    rng = random.Random(3)
    var = [("X_v1|X|2_copies", "".join(rng.choice("ACGT") for _ in range(150))), ("X_v2|X|1_copies", "".join(rng.choice("ACGT") for _ in range(150))),
           ("Y_v1|Y|1_copies", "".join(rng.choice("ACGT") for _ in range(150))), ("Z_v1|Z|1_copies", "".join(rng.choice("ACGT") for _ in range(150)))]
    fasta = tmp_path / "expected.fasta"
    fasta.write_text("".join(f">{n}\n{s}\n" for n, s in var))
    table = tmp_path / "genome_amplicons.tsv"
    table.write_text("strain\ttier\tshare_genomic_percent\texpected_read_share_percent\nX\tA\t18\t70\nY\tA\t18\t25\nZ\tA\t0.18\t5\n")
    reads = [plain_read(var[i % 3][1], rng, reverse=(i % 4 == 0)) for i in range(150)]                         # 50 reads of each of the three variants, perfect quality
    reads += [plain_read(substitute(var[0][1], 1), rng) for _ in range(30)]                                  # a variant with one substitution: near
    spurious = substitute(var[1][1], 6, 10)
    reads += [plain_read(spurious, rng) for _ in range(12)]                                                  # six substitutions: other
    chimera = var[0][1][:75] + var[2][1][75:]
    reads += [plain_read(chimera, rng) for _ in range(9)]                                                    # flagged by the stand-in
    CHIMERAS.clear()
    CHIMERAS.add(chimera)
    folder = tmp_path / "lib"
    folder.mkdir()
    t4.write_fastq(folder / "s1.fastq.gz", reads)
    return var, fasta, table, folder


@pytest.fixture
def stand_ins(monkeypatch):
    monkeypatch.setattr(lf, "run_cutadapt", t_cal.named_stand_in_cutadapt)
    monkeypatch.setattr(lt, "run_dada2", fake_dada2)
    monkeypatch.setattr(lf, "check_tools", lambda: None)
    fake_dada2.calls.clear()


TEST_THRESHOLDS = {"top_strains": 2, "big_fraction": 0.7, "other_max": 0.02, "rho_min": 0.7, "rule_slack": 0.005}


def test_a_whole_run_classes_every_asv_and_writes_the_tables(tmp_path, stand_ins):
    var, fasta, table, folder = mock_files(tmp_path)
    r = lt.run({"Lib": folder}, fasta, table, FWD, REV, tmp_path / "out", reads=0, only=["ee2"], thresholds=TEST_THRESHOLDS, log=lambda *_: None)
    m = r["by_lib"]["Lib"]["ee2"]
    assert (m["asvs_exact"], m["asvs_near"], m["asvs_other"], m["asvs_chimeric"]) == (3, 1, 1, 1)               # three variants, the 1-substitution sequence, the 6-substitution one, the chimera
    assert m["variants_recovered"] == 3 and m["top_recovered"] == 2 and m["top_total"] == 3                      # Z (a high tier) has no read at all
    assert m["reads_other"] == 12 and m["other_share"] == pytest.approx(12 / (150 + 30 + 12))
    out = tmp_path / "out"
    assert {p.name for p in out.iterdir()} == {"truth_conditions.tsv", "truth_strains.tsv", "truth_asvs_Lib_ee2.tsv", "TRUTH.md"}
    text = (out / "TRUTH.md").read_text()
    assert "**Gate (T2): MET.**" in text and "**Gate (T3): NOT MET.**" in text and "## Lib" in text                  # 12 'other' reads of 192 are 6%: above 2%
    head = (out / "truth_asvs_Lib_ee2.tsv").read_text().splitlines()[0].split("\t")
    assert head == ["sequence", "reads", "chimera", "match", "nearest_variant", "distance", "reads_per_sample"]
    asvs = [l.split("\t") for l in (out / "truth_asvs_Lib_ee2.tsv").read_text().splitlines()[1:]]
    assert all(a[6].startswith("s1=") for a in asvs) and sum(int(a[1]) for a in asvs) == 150 + 30 + 12 + 9      # the reads of each ASV are given per sample (here one sample)
    assert sorted(a[3] for a in asvs) == ["exact", "exact", "exact", "near", "other", "other"]               # the chimera is also an 'other' sequence, flagged
    rows = [l.split("\t") for l in (out / "truth_strains.tsv").read_text().splitlines()[1:]]
    assert {x[2] for x in rows} == {"X", "Y", "Z"} and [x for x in rows if x[2] == "Z"][0][6] == "0"
    assert not (out / "work").exists()


def test_every_condition_runs_with_its_own_files_window_and_primers(tmp_path, stand_ins):
    var, fasta, table, folder = mock_files(tmp_path)
    r = lt.run({"Lib": folder}, fasta, table, FWD, REV, tmp_path / "out", reads=0, thresholds=TEST_THRESHOLDS, log=lambda *_: None, keep=True)
    tags = [c["tag"] for c in fake_dada2.calls]
    rule = r["rules"]["Lib"]
    assert tags == [c["tag"] for c in lt.build_conditions(lt.DEFAULT_GRID, rule)] and rule == 2
    by = {c["tag"]: c for c in fake_dada2.calls}
    assert by["ee2"]["files"] == ["trimmed"] and by["ee2"]["primers"] is None and by["ee2"]["min_len"] > 0 and by["ee2"]["max_len"] > by["ee2"]["min_len"]
    assert by["ee2_nowindow"]["min_len"] == 0 and by["ee2_nowindow"]["max_len"] == 0
    assert by["ee2_dada2primers"]["files"] == ["raw"] and by["ee2_dada2primers"]["primers"] == (FWD, REV)
    lo, hi = r["libraries"]["Lib"]["window"]
    assert (lo, hi) == (int(np.floor(0.9 * 150 / 10) * 10), int(np.ceil(1.1 * 150 / 10) * 10)) and by["ee2"]["min_len"] == lo
    assert (tmp_path / "out" / "work" / "Lib" / "trimmed" / "s1.fastq.gz").is_file()


def test_the_rule_and_the_window_are_computed_from_the_reads(tmp_path, stand_ins):
    rng = random.Random(21)
    v = "".join(rng.choice("ACGT") for _ in range(150))
    reads = []
    for i in range(200):                                         # 200 reads: the expected errors are 0 for 50, 1 for 50, 2 for 50 and 4 for 50: the 75th percentile is 2.something
        k = [0, 1, 2, 4][i % 4]
        full, _ = plain_read(v, rng)
        q = list("I" * len(full))
        for j in range(k):
            q[30 + j] = "!"
        reads.append((full, "".join(q)))
    folder = tmp_path / "L"
    folder.mkdir()
    t4.write_fastq(folder / "a.fastq.gz", reads)
    info = lt.prepare_library("L", folder, tmp_path / "w", FWD, REV, 0, 0, 0.15, log=lambda *_: None)
    assert info["reads"] == 200 and info["median_length"] == 150
    assert info["p75"] == pytest.approx(np.percentile([0.0, 1.0, 2.0, 4.0] * 50, 75), abs=0.02) and info["rule"] == max(2, int(info["p75"]) + 1) == 3
    assert info["window"] == (130, 170)


def test_a_library_without_reads_or_expected_variants_is_refused(tmp_path, stand_ins):
    var, fasta, table, folder = mock_files(tmp_path)
    (tmp_path / "none").mkdir()
    with pytest.raises(SystemExit, match="No FASTQ files"):
        lt.run({"X": tmp_path / "none"}, fasta, table, FWD, REV, tmp_path / "o", log=lambda *_: None)
    empty = tmp_path / "empty.fasta"
    empty.write_text("")
    with pytest.raises(SystemExit, match="No expected variants"):
        lt.run({"X": folder}, empty, table, FWD, REV, tmp_path / "o", log=lambda *_: None)


def test_the_command_line_runs_a_pilot_of_one_condition(tmp_path, stand_ins):
    var, fasta, table, folder = mock_files(tmp_path)
    rc = lt.main(["--library", f"Cli={folder}", "--expected", str(fasta), "--strains-table", str(table), "--primer-f", FWD, "--primer-r", REV, "--out", str(tmp_path / "o"), "--only", "ee2", "--threads", "1"])
    assert rc == 0 and [c["tag"] for c in fake_dada2.calls] == ["ee2"] and (tmp_path / "o" / "TRUTH.md").is_file()
    with pytest.raises(SystemExit, match="NAME=FOLDER"):
        lt.parse_libraries(["nothing"])


def test_the_error_model_follows_the_quality_scores():
    assert lt.choose_errfun(93, list(range(94))) == "PacBioErrfun"                                      # the full range of Sequel II
    assert lt.choose_errfun(40, [3, 10, 17, 22, 27, 35, 40]) == "binned:3,10,17,22,27,35,40"            # the bins of Revio
    assert lt.choose_errfun(40, [0, 3, 10, 40]) == "binned:3,10,40"                                     # a zero is not a bin
    assert lt.choose_errfun(60, list(range(61))) == "PacBioErrfun"                                      # many values and no Q93: PacBioErrfun, which then falls back (the report says so)
    assert lt.choose_errfun(None, []) == "PacBioErrfun"


def test_the_quality_scores_of_the_library_decide_its_error_model(tmp_path, stand_ins):
    rng = random.Random(41)
    v = "".join(rng.choice("ACGT") for _ in range(150))
    for tag, extra, expect in (("binned", "", "binned:40"), ("continuous", "~", "PacBioErrfun")):
        reads = []
        for i in range(60):
            full, q = plain_read(v, rng)
            if extra and i == 0:
                q = q[:60] + extra + q[61:]                                                          # one base of Q93 inside the amplicon (the primers are cut off)
            reads.append((full, q))
        folder = tmp_path / tag
        folder.mkdir()
        t4.write_fastq(folder / "a.fastq.gz", reads)
        info = lt.prepare_library(tag, folder, tmp_path / ("w" + tag), FWD, REV, 0, 0, 0.15, log=lambda *_: None)
        assert info["errfun"] == expect and info["max_q"] == (93 if extra else 40), (tag, info["errfun"], info["max_q"])
    assert lt.prepare_library("forced", tmp_path / "binned", tmp_path / "wf", FWD, REV, 0, 0, 0.15, log=lambda *_: None, errfun="PacBioErrfun")["errfun"] == "PacBioErrfun"


def test_the_naive_condition_exists_only_for_binned_reads():
    tags = lambda **kw: [c["tag"] for c in lt.build_conditions((2,), 2, **kw)]
    assert tags(extras=("dada2primers", "naive"), binned=True) == ["ee2", "ee2_dada2primers", "ee2_naive"]
    assert tags(extras=("dada2primers", "naive"), binned=False) == ["ee2", "ee2_dada2primers"]
    by = {c["tag"]: c for c in lt.build_conditions((2,), 2, extras=("naive",), binned=True)}
    assert by["ee2_naive"]["errfun"] == "naive" and by["ee2"]["errfun"] == "auto"


def test_a_variant_without_copies_is_classed_added_and_counts_in_the_metrics():
    names = NAMES + ["X_a1|X|0_copies"]
    seqs_ = SEQS + [mutate(SEQS[0], 3)]
    strains = dict(STRAINS)
    vshare = lt.variant_shares(names, strains)
    assert vshare["X_a1|X|0_copies"] == 0.0 and vshare["X_v1|X|2_copies"] == pytest.approx(50 * 2 / 3)          # an added variant takes no share from the others
    classified = lt.classify([asv(SEQS[0], 400), asv(seqs_[5], 60), asv(mutate(SEQS[2], 1), 30), asv(mutate(SEQS[3], 6), 10)], names, seqs_)
    by = {a["match"]: a for a in classified}
    assert by["added"]["variant"] == "X_a1|X|0_copies" and by["added"]["reads"] == 60
    m = lt.metrics(classified, names, strains, vshare, replicate=["X_v1|X|2_copies", "X_a1|X|0_copies", "Y_v1|Y|1_copies"])
    assert (m["asvs_exact"], m["asvs_added"], m["asvs_near"], m["asvs_other"]) == (1, 1, 1, 1) and m["reads_added"] == 60
    assert m["unexplained_share"] == pytest.approx(40 / 500) and m["variants_recovered"] == 2                    # the exact one and the added one
    assert (m["replicate_total"], m["replicated"]) == (3, 2)                                                    # Y_v1 was not found
    assert m["strain_share"]["X"] == pytest.approx(460 / 500) and m["strain_share"]["Y"] == pytest.approx(30 / 500)  # the added reads count for their strain, and so do the near ones


def refined_stub(**kw):
    base = {"top_total": 15, "top_recovered": 15, "replicate_total": 49, "replicated": 49, "unexplained_share": 0.01, "rho": 0.9, "rho_strains": 17, "variants_recovered": 49}
    base.update(kw)
    return base


def test_the_gates_of_night_9_follow_the_registered_thresholds():
    assert lt.THRESHOLDS_REFINED == {"top_strains": 14, "replicate_fraction": 0.9, "unexplained_max": 0.02, "rho_min": 0.7, "rule_slack": 0.005}
    ok = lt.judge_refined({"R": {"ee2": refined_stub()}}, {"R": 2})["R"]
    assert {k: s for k, (s, _) in ok.items()} == {"T2": "MET", "T3": "MET", "T5": "MET", "T6": "MET"}
    assert lt.judge_refined({"R": {"ee2": refined_stub(replicated=43)}}, {"R": 2})["R"]["T2"][0] == "NOT MET"        # 43 of 49 is 87.8%
    assert lt.judge_refined({"R": {"ee2": refined_stub(replicated=45)}}, {"R": 2})["R"]["T2"][0] == "MET"            # 45 of 49 is 91.8%
    assert lt.judge_refined({"R": {"ee2": refined_stub(replicated=44)}}, {"R": 2})["R"]["T2"][0] == "NOT MET"        # 44 of 49 is 89.8%: 90% of 49 is 44.1, so 45 are needed
    assert lt.judge_refined({"R": {"ee2": refined_stub(top_recovered=13)}}, {"R": 2})["R"]["T2"][0] == "NOT MET"
    assert lt.judge_refined({"R": {"ee2": refined_stub(unexplained_share=0.021)}}, {"R": 2})["R"]["T3"][0] == "NOT MET"
    assert lt.judge_refined({"R": {"ee2": refined_stub(unexplained_share=0.02)}}, {"R": 2})["R"]["T3"][0] == "MET"
    assert {s for s, _ in lt.judge_refined({"R": {"ee3": refined_stub()}}, {"R": 3})["R"].values()} == {"NOT DECIDED"}
    std = refined_stub(variants_recovered=49, unexplained_share=0.010)
    assert lt.judge_refined({"R": {"ee2": std, "ee3": refined_stub(variants_recovered=49, unexplained_share=0.014)}}, {"R": 3})["R"]["T6"][0] == "MET"
    assert lt.judge_refined({"R": {"ee2": std, "ee3": refined_stub(variants_recovered=48, unexplained_share=0.010)}}, {"R": 3})["R"]["T6"][0] == "NOT MET"
    assert lt.judge_refined({"R": {"ee2": std, "ee3": refined_stub(variants_recovered=49, unexplained_share=0.016)}}, {"R": 3})["R"]["T6"][0] == "NOT MET"


def mock_refined(tmp_path):
    """The mock of the other tests, with a variant added by the refinement rule (one base from Y_v1) that a second file carries, and a replication set."""
    var, fasta, table, folder = mock_files(tmp_path)
    rng = random.Random(77)
    added_seq = substitute(var[2][1], 1, 40)
    refined = tmp_path / "refined.fasta"
    refined.write_text(fasta.read_text() + f">Y_a1|Y|0_copies\n{added_seq}\n")
    t4.write_fastq(folder / "s2.fastq.gz", [plain_read(added_seq, rng) for _ in range(40)])
    reps = tmp_path / "replicate.txt"
    reps.write_text("# the sequences to be found again\n" + "\n".join([var[0][0], var[1][0], var[2][0], "Y_a1|Y|0_copies"]) + "\n")
    return var, fasta, table, folder, refined, reps


TOY_REFINED = {"top_strains": 2, "replicate_fraction": 0.9, "unexplained_max": 0.2, "rho_min": 0.7, "rule_slack": 0.005}


def test_a_run_against_the_refined_reference_scores_both_references_and_the_replication(tmp_path, stand_ins):
    var, fasta, table, folder, refined, reps = mock_refined(tmp_path)
    r = lt.run({"Lib": folder}, fasta, table, FWD, REV, tmp_path / "out", reads=0, grid=(2,), thresholds=TOY_REFINED, log=lambda *_: None,
               refined_fasta=refined, replicate_file=reps, extras=("dada2primers", "naive"))
    m = r["by_lib"]["Lib"]["ee2"]
    assert r["refined"] is True and (m["asvs_exact"], m["asvs_added"], m["asvs_near"], m["asvs_other"], m["asvs_chimeric"]) == (3, 1, 1, 1, 1)
    assert m["variants_recovered"] == 4 and m["variants_total"] == 5 and (m["replicated"], m["replicate_total"]) == (4, 4)
    assert m["unexplained_share"] == pytest.approx((30 + 12) / (150 + 40 + 30 + 12))
    o = m["original"]                                                                                      # against the original four variants the added sequence is only 'near'
    assert o["variants_recovered"] == 3 and o["variants_total"] == 4 and o["other_share"] == pytest.approx(12 / 232)
    g = r["gates"]["Lib"]
    assert {k: s for k, (s, _) in g.items()} == {"T2": "MET", "T3": "MET", "T5": "MET", "T6": "MET"}
    by = {c["tag"]: c for c in fake_dada2.calls}
    assert set(by) == {"ee2", "ee2_dada2primers", "ee2_naive"} and by["ee2"]["errfun"] == "binned:40" and by["ee2_dada2primers"]["errfun"] == "binned:40" and by["ee2_naive"]["errfun"] == "PacBioErrfun"
    text = (tmp_path / "out" / "TRUTH.md").read_text()
    for part in ("Quality scores: highest 40, 1 distinct values (40); error model: **binned:40**", "Scored against the original variants (no gate)", "| added |", "**Gate (T2): MET.**", "replication set recovered"):
        assert part in text, part
    rows = [l.split("\t") for l in (tmp_path / "out" / "truth_conditions.tsv").read_text().splitlines()]
    head = rows[0]
    assert head[-5:] == ["original_variants_recovered", "original_variants_total", "original_other_share", "original_top_strains_recovered", "original_big_variants_recovered"] and "error_model" in head
    row = dict(zip(head, [x for x in rows if x[1] == "ee2"][0]))
    assert row["error_model"] == "binned:40" and row["asvs_added"] == "1" and row["replicated"] == "4" and row["original_variants_recovered"] == "3"


def test_a_run_without_a_refined_reference_still_uses_the_gates_of_night_8(tmp_path, stand_ins):
    var, fasta, table, folder = mock_files(tmp_path)
    r = lt.run({"Lib": folder}, fasta, table, FWD, REV, tmp_path / "out", reads=0, only=["ee2"], thresholds=TEST_THRESHOLDS, log=lambda *_: None)
    assert r["refined"] is False and set(r["gates"]["Lib"]) == {"T2", "T3", "T5", "T6"} and r["by_lib"]["Lib"]["ee2"]["replicate_total"] == 0
    assert "Scored against the original" not in (tmp_path / "out" / "TRUTH.md").read_text()
    assert [c["tag"] for c in fake_dada2.calls] == ["ee2"] and fake_dada2.calls[0]["errfun"] == "binned:40"


def test_the_names_of_a_replication_set_are_read_without_comments_and_blank_lines(tmp_path):
    p = tmp_path / "r.txt"
    p.write_text("# a comment\nA_v1|A|1_copies\n\n  B_v1|B|2_copies  \n")
    assert lt.read_names(p) == ["A_v1|A|1_copies", "B_v1|B|2_copies"]


def test_the_command_line_takes_the_refined_reference_and_the_error_model(tmp_path, stand_ins, monkeypatch):
    monkeypatch.setattr(lf, "SAMPLING", "spread")
    var, fasta, table, folder, refined, reps = mock_refined(tmp_path)
    rc = lt.main(["--library", f"Cli={folder}", "--expected", str(fasta), "--strains-table", str(table), "--primer-f", FWD, "--primer-r", REV, "--out", str(tmp_path / "o"), "--only", "ee2,ee2_naive",
                  "--grid", "2", "--refined", str(refined), "--replicate-set", str(reps), "--extras", "naive", "--errfun", "binned:40,93", "--threads", "1", "--sampling", "first"])
    assert lf.SAMPLING == "first" and rc == 0 and {c["tag"]: c["errfun"] for c in fake_dada2.calls} == {"ee2": "binned:40,93", "ee2_naive": "PacBioErrfun"}
    assert "refined set" in (tmp_path / "o" / "TRUTH.md").read_text()


def test_the_script_parses_as_python_3_9():
    ast.parse(Path(lt.__file__).read_text(), feature_version=(3, 9))
