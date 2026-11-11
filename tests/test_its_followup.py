"""validation/its_followup.py: the exact flow of ITS pairs through DADA2 at several mismatch limits, and the length of the overlaps of the pairs that are refused.
R is a stand-in that writes the two tables."""
import csv
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / "validation"))


def load():
    spec = importlib.util.spec_from_file_location("its_followup", HERE.parent / "validation" / "its_followup.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = load()
LIMITS = M.LIMITS


def sample_row(name, inp, filt, reach, rej_short, rej_mismatch, rej_other, merged, asv):
    """merged and asv: one number per limit, in the order of LIMITS."""
    r = {"sample": name, "input": inp, "filtered": filt, "reach": reach, "rej_short": rej_short, "rej_mismatch": rej_mismatch, "rej_other": rej_other}
    for k, m, v in zip(LIMITS, merged, asv):
        r[f"merged_k{k}"], r[f"asv_k{k}"] = m, v
    return r


def write_samples(path, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(M.columns())
        for r in rows:
            w.writerow([r[c] for c in M.columns()])


def write_pairs(path, pairs, partners=None):
    """partners: one (forward, reverse) number per pair; by default every pair has its own two sequences."""
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["sample", "forward", "reverse", "abundance", "accept", "nmatch", "nmismatch", "nindel"])
        for i, (a, ok, m, mm, ind) in enumerate(pairs):
            f, r = partners[i] if partners else (i + 1, i + 1)
            w.writerow(["s", f, r, a, "TRUE" if ok else "FALSE", m, mm, ind])


# two samples of 1,000 input pairs; 500 pairs are refused for mismatches or indels at the default; allowing 2 mismatches merges 200 more of them
ROWS = [sample_row("a", 1000, 900, 600, 20, 300, 0, (100, 150, 250, 280), (10, 11, 11, 12)),
        sample_row("b", 1000, 900, 600, 30, 200, 0, (100, 120, 150, 170), (20, 21, 22, 23))]
# 900 pairs with an overlap of at least 12 nt, in three equal groups (overlaps of 100, 200 and 300 nt), and 50 refused for a short overlap (left out)
PAIRS = [(270, True, 100, 0, 0), (30, False, 95, 5, 0), (240, True, 200, 0, 0), (60, False, 190, 10, 0),
         (150, True, 300, 0, 0), (90, False, 290, 10, 0), (60, False, 280, 20, 3), (50, False, 5, 0, 0)]


def test_the_tables_are_read_back_and_a_missing_column_is_reported(tmp_path):
    write_samples(tmp_path / "s.tsv", ROWS)
    write_pairs(tmp_path / "p.tsv", PAIRS)
    rows = M.read_samples(tmp_path / "s.tsv")
    assert rows[0]["sample"] == "a" and rows[0]["merged_k2"] == 250.0
    pairs = M.read_pairs(tmp_path / "p.tsv")
    assert pairs[1] == (30.0, False, 95, 5, 0) and pairs[0][1] is True
    (tmp_path / "bad.tsv").write_text("sample\tinput\na\t1\n")
    with pytest.raises(RuntimeError, match="lacks the columns"):
        M.read_samples(tmp_path / "bad.tsv")


def test_flow_gives_shares_of_the_input_the_recovered_share_and_the_median_asvs():
    f = M.flow(ROWS)
    assert f["input"] == 2000 and f["samples"] == 2
    assert f["filtered"] == pytest.approx(0.9) and f["reach"] == pytest.approx(0.6)
    assert f["rej_mismatch"] == pytest.approx(0.25) and f["rej_short"] == pytest.approx(0.025)
    assert f["merged"][0] == pytest.approx(0.1) and f["merged"][2] == pytest.approx(0.2)
    assert f["recovered"][2] == pytest.approx(0.4)                      # (400 - 200) of the 500 pairs refused for mismatches
    assert f["recovered"][1] == pytest.approx(0.14) and f["recovered"][5] == pytest.approx(0.5)
    assert f["recovered_all"][2] == pytest.approx(200 / 550)            # of every refused pair: 50 short, 500 for mismatches or indels
    assert f["asv"][0] == 15 and f["asv"][2] == 16.5                    # medians of (10, 20) and (11, 22)
    assert M.flow([]) == {}


def test_nothing_was_refused_for_mismatches_so_the_recovered_share_is_undefined():
    f = M.flow([sample_row("a", 1000, 900, 600, 0, 0, 0, (600, 600, 600, 600), (5, 5, 5, 5))])
    assert f["recovered"] == {1: None, 2: None, 5: None} and f["recovered_all"] == {1: None, 2: None, 5: None}


def test_the_overlap_profile_splits_the_pairs_in_thirds_by_overlap_length():
    o = M.overlap_profile(PAIRS)
    assert o["pairs"] == 900                                           # the 50 pairs with an overlap shorter than 12 nt are left out
    assert o["median_overlap"] == 200
    assert o["low_share"] == pytest.approx(30 / 300) and o["high_share"] == pytest.approx(150 / 300)
    assert o["low_max_overlap"] == 100 and o["high_min_overlap"] == 300
    assert o["indel_share"] == pytest.approx(60 / 240)                 # 240 pairs refused for mismatches or indels, 60 with an indel
    assert M.overlap_profile([(5, False, 3, 0, 0)]) == {}


def test_a_pair_with_few_matching_bases_but_a_long_enough_overlap_is_refused_for_its_mismatches_not_for_a_short_overlap():
    pairs = [(100, True, 100, 0, 0), (10, False, 10, 4, 0), (7, False, 5, 3, 0), (3, False, 8, 0, 0)]
    o = M.overlap_profile(pairs)
    assert o["pairs"] == 110                                           # 10 + 100: an overlap of 14 nt counts; 8 nt and 8 nt do not
    assert o["indel_share"] == 0.0                                     # the only pair refused for mismatches has none


def result(rows, pairs=None, partners=None):
    return {"flow": M.flow(rows), "overlap": M.overlap_profile(pairs) if pairs else {}, "partners": partners,
            "alignment": M.refused_alignment(pairs) if pairs else {}}


def by_id(res):
    return {p: (txt, ok) for p, txt, ok in M.verdicts(res)}


def test_every_criterion_is_decided_when_all_datasets_are_given():
    first = [sample_row("a", 1000, 900, 600, 20, 60, 0, (300, 310, 320, 330), (10, 10, 10, 10))]
    first_pairs = [(500, True, 40, 0, 0), (60, False, 38, 2, 0), (40, True, 60, 0, 0)]       # shorter overlaps than PAIRS
    v4 = [sample_row("a", 1000, 990, 700, 50, 200, 50, (400, 400, 400, 400), (30, 30, 30, 30))]
    iso = [sample_row("a", 1000, 900, 800, 0, 100, 0, (700, 750, 780, 790), (2, 2, 2, 3))]
    res = {"its2": result(ROWS, PAIRS, 0.6), "its": result(first, first_pairs), "v4": result(v4, partners=0.7), "arfken_its2": result(iso)}
    v = by_id(res)
    assert [k for k in v] == M.IDS
    assert v["P68"][1] is False                                         # 40% of the mismatch refusals are recovered, the limit is 50%
    assert v["P69"][1] is True and "+40.0 points" in v["P69"][0]
    assert v["P70"][1] is True
    assert v["P71"][1] is True and "200 nt against 40 nt" in v["P71"][0]
    assert v["P72"][1] is True and "second ITS study +10.0%" in v["P72"][0]     # median ASVs 15 -> 16.5 is exactly the limit; the first study: 10 -> 10
    assert v["P73"][1] is True and "70.0%" in v["P73"][0]                       # 70% of the refused pairs on soil V4 have good halves
    assert v["P74"][1] is True and "arfken_its2 +0" in v["P74"][0]
    assert v["P75"][1] is True and "60.0%" in v["P75"][0]


def test_p72_is_met_at_the_limit_and_not_met_above_it():
    first = [sample_row("a", 1000, 900, 600, 20, 60, 0, (300, 310, 320, 330), (10, 10, 10, 10))]
    ok = [sample_row("a", 1000, 900, 600, 20, 300, 0, (100, 150, 250, 280), (10, 10, 11, 12))]       # 10 -> 11: +10.0%, exactly the limit
    bad = [sample_row("a", 1000, 900, 600, 20, 300, 0, (100, 150, 250, 280), (10, 10, 12, 12))]      # +20%
    assert by_id({"its2": result(ok), "its": result(first)})["P72"][1] is True
    assert by_id({"its2": result(bad), "its": result(first)})["P72"][1] is False
    zero = [sample_row("a", 1000, 900, 600, 20, 300, 0, (100, 150, 250, 280), (0, 0, 0, 0))]
    assert by_id({"its2": result(zero), "its": result(first)})["P72"][1] is None


def test_a_dataset_that_was_not_run_leaves_its_criteria_not_decided():
    v = by_id({"its2": result(ROWS, PAIRS)})
    assert v["P68"][1] is False and v["P69"][1] is True and v["P70"][1] is True
    for p in ("P71", "P72", "P73", "P74"):
        assert v[p][1] is None and v[p][0].startswith("not decided")
    v = by_id({})
    assert all(ok is None for _, ok in v.values())


def test_p73_and_p75_ask_for_at_least_half_of_the_refused_pairs_to_have_good_halves():
    v4_rows = [sample_row("a", 1000, 990, 700, 50, 200, 50, (400,) * 4, (30,) * 4)]
    for res, pid in ((lambda p: {"v4": result(v4_rows, partners=p)}, "P73"), (lambda p: {"its2": result(ROWS, PAIRS, p)}, "P75")):
        assert by_id(res(0.5))[pid][1] is True                         # exactly half is enough
        assert by_id(res(0.49))[pid][1] is False
        assert by_id(res(None))[pid][1] is None and "no pair was refused" in by_id(res(None))[pid][0]


def test_the_partner_share_counts_refused_pairs_whose_two_halves_each_merge_elsewhere():
    rows = [("s", 1, 1, 100, True), ("s", 2, 2, 50, True),              # accepted: forward 1 and 2, reverse 1 and 2
            ("s", 1, 2, 30, False),                                      # refused, both halves occur in accepted pairs: counts
            ("s", 3, 3, 20, False),                                      # refused, neither half occurs in an accepted pair
            ("s", 1, 9, 10, False)]                                      # refused, the forward half occurs, the reverse half does not
    assert M.partner_share(rows) == pytest.approx(30 / 60)
    assert M.partner_share([("s", 1, 1, 100, True)]) is None             # nothing was refused
    # the sequences are numbered within a sample: an accepted pair of sample a does not make the halves of a refused pair of sample b good
    assert M.partner_share([("a", 1, 1, 100, True), ("b", 1, 1, 40, False)]) == 0.0


def test_the_alignment_line_counts_refused_pairs_with_no_overlap_at_all():
    pairs = [(40, False, 0, 0, 0), (10, False, 5, 3, 0), (50, True, 100, 0, 0)]
    a = M.refused_alignment(pairs)
    assert a["refused"] == 50 and a["zero_share"] == pytest.approx(0.8)
    assert M.refused_alignment([(5, True, 100, 0, 0)]) == {}


def test_the_partner_rows_are_read_back(tmp_path):
    write_pairs(tmp_path / "p.tsv", PAIRS, partners=[(7, 8)] * len(PAIRS))
    rows = M.read_partners(tmp_path / "p.tsv")
    assert rows[0] == ("s", 7, 8, 270.0, True) and rows[1][4] is False and len(rows) == len(PAIRS)


def test_p74_needs_every_isolate_library_that_was_run_to_stay_within_one_asv():
    ok = [sample_row("a", 1000, 900, 800, 0, 100, 0, (700, 750, 780, 790), (3, 3, 4, 4))]        # +1
    bad = [sample_row("a", 1000, 900, 800, 0, 100, 0, (700, 750, 780, 790), (3, 3, 5, 5))]       # +2
    assert by_id({"arfken_its1": result(ok), "arfken_its2": result(ok)})["P74"][1] is True
    assert by_id({"arfken_its1": result(ok), "arfken_its2": result(bad)})["P74"][1] is False


def test_p74_counts_the_isolate_libraries_only_not_the_mixes():
    ok = [sample_row("a", 1000, 900, 800, 0, 100, 0, (700, 750, 780, 790), (3, 3, 4, 4))]        # +1
    bad = [sample_row("a", 1000, 900, 800, 0, 100, 0, (700, 750, 780, 790), (3, 3, 9, 9))]       # +6: a mix that would fail if it were counted
    v = by_id({"arfken_its1": result(ok), "arfken_mix_its1": result(bad)})
    assert v["P74"][1] is True and "arfken_mix_its1" not in v["P74"][0]
    assert by_id({"arfken_mix_its1": result(bad)})["P74"][1] is None                              # mixes alone leave P74 undecided


def test_the_report_lists_the_verdicts_and_one_section_per_dataset():
    L = "\n".join(M.report_lines({"its2": result(ROWS, PAIRS, 0.6)}, {"its2": "no truncation"}))
    assert "60.0% have a forward and a reverse sequence that each occur in an accepted pair" in L and "have no overlap at all in the alignment" in L
    assert "- **P68** NOT MET" in L and "- **P69** MET" in L and "- **P71** not decided" in L
    assert "## its2 (2 samples, 2,000 input pairs; no truncation)" in L
    assert "| 2 | 20.00% | 40.0% | 36.4% | 16.5 |" in L
    assert "Median overlap of the pairs that enter the merge step: 200 nt" in L


class FakeR:
    """Stands in for Rscript: writes the two tables the real script would write and remembers the command it was given."""

    def __init__(self, fail=False):
        self.fail, self.commands = fail, []

    def __call__(self, cmd, capture_output=True, text=True):
        self.commands.append(cmd)
        if self.fail:
            return SimpleNamespace(returncode=1, stderr="Error in library(dada2): there is no package called 'dada2'")
        write_samples(cmd[-3], ROWS)
        write_pairs(cmd[-2], PAIRS)
        Path(cmd[-1]).write_text("sample\tk\tsequence\tabundance\ns\t0\tACGT\t10\n")
        return SimpleNamespace(returncode=0, stderr="")


def thin_stub(folder, dest, pairs):
    Path(dest).mkdir(parents=True, exist_ok=True)
    return dest


def folders(tmp_path, *labels):
    out = []
    for lab in labels:
        d = tmp_path / lab
        d.mkdir()
        out += ["--dataset", f"{lab}={d}"]
    return out


def test_main_runs_r_per_dataset_passes_the_cut_and_writes_the_report(tmp_path, capsys):
    fake = FakeR()
    args = folders(tmp_path, "its2", "v4") + ["--trunc", "v4=124,115", "--out", str(tmp_path / "o")]
    assert M.main(args, run=fake, find_rscript=lambda: "Rscript", thin=thin_stub) == 0
    its2, v4 = fake.commands
    assert its2[3:8] == [str(M.MIN_LEN), "2", "12", "0", "0"]              # minLen, maxEE, minOverlap, then no truncation
    assert v4[6:8] == ["124", "115"] and v4[8] == "0,1,2,5"                 # the cut for soil V4, and the limits
    assert its2[-3:] == [str(tmp_path / "o" / "its2_samples.tsv"), str(tmp_path / "o" / "its2_pairs.tsv"), str(tmp_path / "o" / "its2_seqs.tsv")]
    report = (tmp_path / "o" / "ITS_FOLLOWUP_REPORT.md").read_text()
    assert "## v4 (2 samples, 2,000 input pairs; truncLen 124,115)" in report and "## its2" in report
    assert (tmp_path / "o" / "its2_pairs.tsv").is_file()
    assert "written:" in capsys.readouterr().out


def test_main_stops_when_r_fails_and_says_why(tmp_path, capsys):
    assert M.main(folders(tmp_path, "its2") + ["--out", str(tmp_path / "o")], run=FakeR(fail=True), find_rscript=lambda: "Rscript", thin=thin_stub) == 2
    said = capsys.readouterr().out
    assert "its2: DADA2 could not run" in said and "no package called 'dada2'" in said


def test_main_stops_without_r_without_a_folder_and_without_a_dataset(tmp_path, capsys):
    assert M.main(folders(tmp_path, "its2"), run=FakeR(), find_rscript=lambda: None, thin=thin_stub) == 2
    assert "was not found" in capsys.readouterr().out                    # the archive's rtools says it one way, the fallback another
    assert M.main(["--dataset", f"its2={tmp_path / 'nowhere'}", "--out", str(tmp_path / "o")], run=FakeR(), find_rscript=lambda: "Rscript", thin=thin_stub) == 2
    assert "its2: the folder" in capsys.readouterr().out
    assert M.main([], run=FakeR(), find_rscript=lambda: "Rscript", thin=thin_stub) == 2


@pytest.mark.parametrize("bad", [["--dataset", "its2"], ["--dataset", "=x"], ["--trunc", "v4=124"], ["--trunc", "v4=a,b"]])
def test_main_rejects_malformed_arguments(tmp_path, bad):
    with pytest.raises(SystemExit):
        M.main(bad + ["--dataset", f"v4={tmp_path}"] if bad[0] == "--trunc" else bad, run=FakeR(), find_rscript=lambda: "Rscript", thin=thin_stub)


def test_a_cut_for_a_dataset_that_is_not_given_is_refused(tmp_path):
    with pytest.raises(SystemExit, match="not given"):
        M.main(folders(tmp_path, "its2") + ["--trunc", "v4=124,115"], run=FakeR(), find_rscript=lambda: "Rscript", thin=thin_stub)


def test_the_r_script_keeps_the_default_limit_first_and_returns_the_rejected_pairs():
    r = (HERE.parent / "validation" / "its_followup.R").read_text()
    for needle in ("seq_path", "returnRejects = TRUE", "limits[1] == 0L", "truncLen = c(trunc_f, trunc_r)", "trimOverhang = FALSE", "merged_k", "asv_k", "nmismatch", "nindel"):
        assert needle in r, needle
