"""validation/its_depth.py: the same datasets at several depths, and the stability criterion P76."""
import csv
import importlib.util
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "validation"))


def load():
    spec = importlib.util.spec_from_file_location("its_depth", HERE.parent / "validation" / "its_depth.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = load()
F = D.F


def write_samples(folder, label, filtered, reach, merged, inp=1000, rej_short=0, rej_mismatch=0):
    folder.mkdir(parents=True, exist_ok=True)
    with open(folder / f"{label}_samples.tsv", "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(F.columns())
        row = {"sample": "s", "input": inp, "filtered": filtered, "reach": reach, "rej_short": rej_short, "rej_mismatch": rej_mismatch, "rej_other": 0}
        for k in F.LIMITS:
            row[f"merged_k{k}"], row[f"asv_k{k}"] = merged + (20 if k == 5 else 0), 2          # 5 mismatches merge 20 more pairs
        w.writerow([row[c] for c in F.columns()])


def make(tmp_path, merged_5000, merged_20000, label="its2"):
    write_samples(tmp_path / "d1000", label, 800, 300, 100)
    write_samples(tmp_path / "d5000", label, 800, 500, merged_5000, rej_mismatch=60)
    write_samples(tmp_path / "d20000", label, 800, 600, merged_20000)
    return {1000: tmp_path / "d1000", 5000: tmp_path / "d5000", 20000: tmp_path / "d20000"}


def test_the_collected_table_has_a_flow_per_depth_and_label(tmp_path):
    t = D.collect(make(tmp_path, 400, 430), D.LABELS)
    assert sorted(t) == [1000, 5000, 20000] and list(t[5000]) == ["its2"]
    assert t[5000]["its2"]["merged"][0] == pytest.approx(0.4) and t[20000]["its2"]["reach"] == pytest.approx(0.6)


def test_p76_is_met_within_five_points_and_not_met_beyond_it(tmp_path):
    ok = D.verdict(D.collect(make(tmp_path, 400, 450), D.LABELS))               # +5.0 points: the limit
    assert ok[2] is True and "its2 40.0% to 45.0% (+5.0 points)" in ok[1]
    bad = D.verdict(D.collect(make(tmp_path / "b", 400, 451), D.LABELS))
    assert bad[2] is False
    down = D.verdict(D.collect(make(tmp_path / "c", 400, 340), D.LABELS))        # a fall of 6 points counts too
    assert down[2] is False


def test_p76_needs_both_depths_and_every_label_that_has_both_must_be_stable(tmp_path):
    only_5000 = D.collect({5000: make(tmp_path, 400, 400)[5000]}, D.LABELS)
    assert D.verdict(only_5000)[2] is None and D.verdict(only_5000)[1].startswith("not decided")
    runs = make(tmp_path / "x", 400, 410, "its2")
    write_samples(runs[5000], "v4", 990, 500, 400)
    write_samples(runs[20000], "v4", 990, 600, 520)                              # v4 moves by 12 points
    v = D.verdict(D.collect(runs, D.LABELS))
    assert v[2] is False and "v4 40.0% to 52.0% (+12.0 points)" in v[1] and "its2 40.0% to 41.0%" in v[1]


def test_the_report_has_one_table_per_label_in_order_of_depth(tmp_path):
    L = "\n".join(D.report_lines(D.collect(make(tmp_path, 400, 430), D.LABELS)))
    assert "- **P76** MET" in L and "## its2" in L and "## v4" not in L
    assert L.index("| 1,000 |") < L.index("| 5,000 |") < L.index("| 20,000 |")
    assert "| 5,000 | 1 | 80.00% | 50.00% | 0.00% | 6.00% | 40.00% |" in L          # reach 500, refused for mismatches 60, merged 400, all of 1,000 input pairs


def test_main_writes_the_report_and_rejects_a_depth_that_is_not_a_number(tmp_path, capsys):
    runs = make(tmp_path, 400, 430)
    args = [x for d, f in runs.items() for x in ("--run", f"{d}={f}")] + ["--out", str(tmp_path / "out")]
    assert D.main(args) == 0 and (tmp_path / "out" / "ITS_DEPTH_REPORT.md").is_file() and "written:" in capsys.readouterr().out
    with pytest.raises(SystemExit):
        D.main(["--run", f"many={runs[5000]}", "--out", str(tmp_path / "o2")])
    assert D.main(["--run", f"5000={tmp_path / 'empty'}", "--out", str(tmp_path / "o3")]) == 2
