"""validation/its_truth.py: reference sequences from the isolates, spurious sequences and recall in the mixes, at each mismatch limit."""
import csv
import importlib.util
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "validation"))


def load():
    spec = importlib.util.spec_from_file_location("its_truth", HERE.parent / "validation" / "its_truth.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


T = load()
F = T.F
REF_C, REF_C2, REF_K = "ACGTACGTACGTACGTACGT", "TTTTGGGGCCCCAAAATTTT", "GATTACAGATTACAGATTAC"
SPUR1, SPUR2 = "GGGGGGGGGGGGGGGGGGGG", "CCCCCCCCCCCCCCCCCCCC"          # far from every reference sequence


def write_seqs(path, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["sample", "k", "sequence", "abundance"])
        w.writerows(rows)


def write_samples(path, merged_by_limit, inp=100):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(F.columns())
        row = {"sample": "MixB-ITS1a", "input": inp, "filtered": inp, "reach": inp, "rej_short": 0, "rej_mismatch": 0, "rej_other": 0}
        for k in F.LIMITS:
            row[f"merged_k{k}"], row[f"asv_k{k}"] = merged_by_limit[k], 3
        w.writerow([row[c] for c in F.columns()])


ISOLATES = [("C-ITS1a", 0, REF_C, 99), ("C-ITS1a", 0, REF_C2, 1),       # C2 holds exactly 1% of C: in the reference
            ("K-ITS1a", 0, REF_K, 100), ("K-ITS1a", 0, "AAAAAAAAAAAAAAAAAAAA", 0.5),   # 0.5 of 100.5 is under 1%: left out
            ("K-ITS1a", 2, "CCCCCCCCCCCCCCCCCCCC", 7)]                  # rows at other limits do not enter the reference
# MixB holds K and C. At the default: 2 of 100 pairs are in a spurious sequence; with 2 mismatches a second spurious sequence and the second C sequence appear
MIX = [("MixB-ITS1a", 0, REF_C, 60), ("MixB-ITS1a", 0, REF_K, 38), ("MixB-ITS1a", 0, SPUR1, 2),
       ("MixB-ITS1a", 1, REF_C, 60), ("MixB-ITS1a", 1, REF_K, 38), ("MixB-ITS1a", 1, SPUR1, 2),
       ("MixB-ITS1a", 2, REF_C, 60), ("MixB-ITS1a", 2, REF_K, 38), ("MixB-ITS1a", 2, SPUR1, 2), ("MixB-ITS1a", 2, SPUR2, 3), ("MixB-ITS1a", 2, REF_C2, 1),
       ("MixB-ITS1a", 5, REF_C, 60), ("MixB-ITS1a", 5, REF_K, 38), ("MixB-ITS1a", 5, SPUR1, 2), ("MixB-ITS1a", 5, SPUR2, 3), ("MixB-ITS1a", 5, REF_C2, 1)]
MERGED = {0: 100, 1: 100, 2: 110, 5: 110}                                   # pairs merged at each limit, of 100... (shares are of the input; see below)


def test_within_edits_counts_mismatches_and_indels_up_to_the_limit():
    assert T.within_edits(REF_C, REF_C)
    assert T.within_edits(REF_C, REF_C[:5] + "T" + REF_C[6:])                # one mismatch
    assert T.within_edits(REF_C, REF_C[:5] + "TT" + REF_C[7:])               # two mismatches
    assert not T.within_edits(REF_C, REF_C[:5] + "AAA" + REF_C[8:])          # three: C, G and T all differ
    assert T.within_edits(REF_C, REF_C[:8] + REF_C[9:])                      # one deletion
    assert T.within_edits(REF_C, REF_C[:8] + "G" + REF_C[8:])                # one insertion
    assert not T.within_edits(REF_C, REF_C + "ACG")                          # length differs by three
    assert T.within_edits("", "AC") and not T.within_edits("", "ACG")


def test_the_reference_holds_the_sequences_with_at_least_one_percent_of_an_isolate_at_the_default_limit():
    ref = T.reference(ISOLATES)
    assert ref == {"C": {REF_C, REF_C2}, "K": {REF_K}}


def test_the_mix_profile_gives_the_spurious_share_the_recall_and_the_merged_share(tmp_path):
    ref = T.reference(ISOLATES)
    write_samples(tmp_path / "s.tsv", MERGED)
    prof = T.mix_profile(MIX, F.read_samples(tmp_path / "s.tsv"), ref)
    assert prof["spurious"][0] == pytest.approx(2 / 100) and prof["spurious"][1] == pytest.approx(2 / 100)
    assert prof["spurious"][2] == pytest.approx(5 / 104) and prof["spurious"][5] == pytest.approx(5 / 104)      # 60 + 38 + 2 + 3 + 1 pairs
    assert prof["recall"][0] == pytest.approx(2 / 3)                         # the second C sequence is not seen at the default
    assert prof["recall"][2] == pytest.approx(1.0)
    assert prof["merged"][0] == pytest.approx(1.0) and prof["merged"][2] == pytest.approx(1.1)
    assert prof["samples"] == 1


def test_a_sequence_within_two_edits_of_a_reference_counts_as_true():
    ref = {"C": {REF_C}}
    near = REF_C[:5] + "TT" + REF_C[7:]                                     # two mismatches: still true
    far = REF_C[:5] + "AAA" + REF_C[8:]                                     # three: spurious
    rows = [("MixB-ITS1a", 0, near, 90), ("MixB-ITS1a", 0, far, 10)]
    prof = T.mix_profile(rows, [{"input": 100, **{f"merged_k{k}": 100 for k in F.LIMITS}}], ref, limits=(0,))
    assert prof["spurious"][0] == pytest.approx(0.10)


def verdicts_for(mix_rows, merged, tmp_path):
    ref = T.reference(ISOLATES)
    write_samples(tmp_path / "s.tsv", merged)
    return {p: (txt, ok) for p, txt, ok in T.verdicts({"its1": T.mix_profile(mix_rows, F.read_samples(tmp_path / "s.tsv"), ref)})}


def test_the_criteria_are_decided_from_the_profile(tmp_path):
    v = verdicts_for(MIX, MERGED, tmp_path)
    assert v["P80"][1] is False and "its1 +2.81 points" in v["P80"][0]        # 2.00% to 4.81%
    assert v["P81"][1] is True and "66.7% to 100.0%" in v["P81"][0]
    assert v["P82"][1] is True and "+10.0 points" in v["P82"][0]


def test_p80_is_met_when_the_spurious_share_rises_by_at_most_one_point_and_p82_needs_two_points_of_gain(tmp_path):
    safe = [r for r in MIX if r[2] not in (SPUR2,)]                          # no second spurious sequence: the share stays at about 2%
    v = verdicts_for(safe, {0: 100, 1: 100, 2: 101, 5: 101}, tmp_path)
    assert v["P80"][1] is True and v["P82"][1] is False                      # +1.0 point of gain is under 2


def test_nothing_is_decided_without_the_mixes_and_a_marker_that_is_missing_does_not_block_the_other(tmp_path):
    assert all(ok is None for _, _, ok in T.verdicts({"its1": None, "its2": None}))
    ref = T.reference(ISOLATES)
    write_samples(tmp_path / "s.tsv", MERGED)
    prof = T.mix_profile(MIX, F.read_samples(tmp_path / "s.tsv"), ref)
    assert {p: ok for p, _, ok in T.verdicts({"its1": prof, "its2": None})}["P81"] is True


def test_main_writes_the_report_from_the_files_of_the_follow_up(tmp_path, capsys):
    write_seqs(tmp_path / "arfken_its1_seqs.tsv", ISOLATES)
    write_seqs(tmp_path / "arfken_mix_its1_seqs.tsv", MIX)
    write_samples(tmp_path / "arfken_mix_its1_samples.tsv", MERGED)
    assert T.main(["--out", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "**P80** NOT MET" in out and "written:" in out
    report = (tmp_path / "ITS_TRUTH_REPORT.md").read_text()
    assert "## ITS1 mixes" in report and "| 2 | 110.00% | 4.81% | 100.00% |" in report and "## ITS2 mixes\n\nNot run." in report
    assert "Reference sequences per isolate: C 2, K 1" in report


def test_main_says_what_is_missing(tmp_path, capsys):
    assert T.main(["--out", str(tmp_path)]) == 2
    assert "run validation" in capsys.readouterr().out
    write_seqs(tmp_path / "bad.tsv", [])
    (tmp_path / "bad.tsv").write_text("a\tb\n")
    with pytest.raises(RuntimeError, match="does not have the columns"):
        T.read_seqs(tmp_path / "bad.tsv")
