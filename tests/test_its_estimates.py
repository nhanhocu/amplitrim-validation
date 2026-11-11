"""validation/its_estimates.py: AmpliTrim's ITS prediction of the filter pass and the yield against DADA2. AmpliTrim is a stand-in that writes summary.json."""
import csv
import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "validation"))


def load():
    spec = importlib.util.spec_from_file_location("its_estimates", HERE.parent / "validation" / "its_estimates.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


E = load()
F = E.F


def write_samples(path, filtered=830, merged=140, inp=1000):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(F.columns())
        row = {"sample": "s", "input": inp, "filtered": filtered, "reach": filtered, "rej_short": 0, "rej_mismatch": 0, "rej_other": 0}
        for k in F.LIMITS:
            row[f"merged_k{k}"], row[f"asv_k{k}"] = merged, 2
        w.writerow([row[c] for c in F.columns()])


def summary_json(pass_=0.834, yield_=0.82, pairs=45000):
    return {"schema_version": 1, "its": {"pairs": pairs, "pass": pass_}, "recommended": {"estimated_yield": yield_}}


def test_the_numbers_are_read_from_summary_json_and_a_missing_key_is_reported(tmp_path):
    (tmp_path / "summary.json").write_text(json.dumps(summary_json()))
    assert E.read_summary(tmp_path / "summary.json") == {"pass": 0.834, "yield": 0.82, "pairs": 45000}
    (tmp_path / "plain.json").write_text(json.dumps({"schema_version": 1, "recommended": {"estimated_yield": 0.9}}))      # a run without --its has no 'its' block
    with pytest.raises(RuntimeError, match="was AmpliTrim run with --its"):
        E.read_summary(tmp_path / "plain.json")


def test_compare_gives_the_differences_in_points_of_the_input_pairs(tmp_path):
    write_samples(tmp_path / "s.tsv")
    c = E.compare({"pass": 0.834, "yield": 0.82, "pairs": 45000}, F.flow(F.read_samples(tmp_path / "s.tsv")))
    assert c["observed_pass"] == pytest.approx(0.83) and c["pass_diff"] == pytest.approx(0.4)
    assert c["merged"] == pytest.approx(0.14) and c["overshoot"] == pytest.approx(68.0)
    assert c["samples"] == 1 and c["pairs_analysed"] == 45000


def res_of(diffs, overshoots):
    keys = ("arfken_its1", "arfken_its2", "arfken_mix_its1", "arfken_mix_its2")
    return {k: {"pass_diff": d, "overshoot": o, "predicted_pass": .8, "observed_pass": .8, "estimated_yield": .9, "merged": .8, "pairs_analysed": 1, "samples": 1}
            for k, d, o in zip(keys, diffs, overshoots)}


def by_id(res):
    return {p: (txt, ok) for p, txt, ok in E.verdicts(res)}


def test_the_three_criteria_are_decided_from_the_groups():
    v = by_id(res_of([0.4, -0.9, 0.0, 1.0], [9, 2, 12, 5]))                  # isolates 9 and 2, mixes 12 and 5
    assert v["P77"][1] is True                                              # 1.0 point is the limit
    assert v["P78"][1] is True and "ITS1 +9.0 against +12.0" in v["P78"][0]
    assert v["P79"][1] is True
    v = by_id(res_of([0.4, -1.1, 0.0, 1.0], [9, 2, 12, 5]))
    assert v["P77"][1] is False and "arfken_its2 -1.10" in v["P77"][0]
    assert by_id(res_of([0, 0, 0, 0], [20, 2, 30, 5]))["P79"][1] is False     # 20 is not under 17
    assert by_id(res_of([0, 0, 0, 0], [9, 6, 12, 5]))["P78"][1] is False       # ITS2: the isolates are above the mixes


def test_a_marker_without_both_groups_leaves_p78_undecided_and_nothing_run_decides_nothing():
    r = res_of([0, 0, 0, 0], [9, 2, 12, 5])
    only_isolates = {k: v for k, v in r.items() if "mix" not in k}
    assert by_id(only_isolates)["P78"][1] is None and by_id(only_isolates)["P79"][1] is True
    mixed_only = {k: v for k, v in r.items() if "mix" in k}
    assert by_id(mixed_only)["P79"][1] is None
    assert all(ok is None for _, _, ok in E.verdicts({}))


class FakeAmpliTrim:
    """Stands in for the AmpliTrim command line: writes summary.json into the --out-dir it is given, and remembers the command."""

    def __init__(self, fail=False, plain=False, whole_pass=None):
        self.fail, self.plain, self.whole_pass, self.commands = fail, plain, whole_pass, []

    def __call__(self, cmd, capture_output=True, text=True):
        self.commands.append(cmd)
        if self.fail:
            return SimpleNamespace(returncode=1, stderr="amplitrim: error: no read pairs found", stdout="")
        out = Path(cmd[cmd.index("--out-dir") + 1])
        out.mkdir(parents=True, exist_ok=True)
        whole = self.whole_pass is not None and Path(cmd[cmd.index("--input-dir") + 1]).name == "whole"          # a different answer for the whole folder
        (out / "summary.json").write_text(json.dumps({"schema_version": 1, "recommended": {"estimated_yield": 0.9}} if self.plain
                                                      else summary_json(pass_=self.whole_pass) if whole else summary_json()))
        return SimpleNamespace(returncode=0, stderr="", stdout="")


def setup(tmp_path, *labels):
    """What validation/its_followup.py leaves in its --out folder for each label: the table of DADA2's counts and the thinned reads that DADA2 received."""
    args = []
    for lab in labels:
        (tmp_path / f"{lab}_reads").mkdir(parents=True)
        write_samples(tmp_path / f"{lab}_samples.tsv")
        args += ["--dataset", lab]
    return args


def test_main_gives_amplitrim_the_thinned_reads_that_dada2_received_and_writes_the_report(tmp_path, capsys):
    fake = FakeAmpliTrim()
    args = setup(tmp_path, "arfken_its1", "arfken_mix_its1")
    assert E.main(["--out", str(tmp_path)] + args, run=fake) == 0
    cmd = fake.commands[0]
    assert "--its" in cmd and cmd[cmd.index("--input-dir") + 1] == str(tmp_path / "arfken_its1_reads")
    assert cmd[cmd.index("--out-dir") + 1] == str(tmp_path / "amplitrim_thinned_arfken_its1") and len(fake.commands) == 2
    report = (tmp_path / "ITS_ESTIMATES_REPORT.md").read_text()
    assert "| arfken_its1 | 83.40% | 83.00% | +0.40 |" in report and "| arfken_mix_its1 | 82.00% | 14.00% | +68.0 | 45,000 | 1 |" in report
    assert "- **P77** MET" in report and "Exploratory" not in report and "written:" in capsys.readouterr().out


def test_the_whole_folder_run_is_an_exploratory_table_that_decides_nothing(tmp_path):
    fake = FakeAmpliTrim(whole_pass=0.90)                                            # the whole folder would predict 90%, 7 points above DADA2's 83%
    args = setup(tmp_path, "arfken_its1")
    (tmp_path / "whole").mkdir()
    assert E.main(["--out", str(tmp_path), "--whole", f"arfken_its1={tmp_path / 'whole'}"] + args, run=fake) == 0
    assert [c[c.index("--input-dir") + 1] for c in fake.commands] == [str(tmp_path / "arfken_its1_reads"), str(tmp_path / "whole")]
    assert fake.commands[1][fake.commands[1].index("--out-dir") + 1] == str(tmp_path / "amplitrim_whole_arfken_its1")
    report = (tmp_path / "ITS_ESTIMATES_REPORT.md").read_text()
    assert "## Exploratory: AmpliTrim on the whole folders" in report
    assert "- **P77** MET" in report                                                 # decided on the thinned reads (+0.4), not on the whole folder (+7.0)
    assert "| arfken_its1 | 90.00% | 83.00% | +7.00 |" in report.split("## Exploratory")[1]
    assert "+7.00" not in report.split("## Exploratory")[0]


def test_an_existing_summary_is_reused_unless_rerun_is_given(tmp_path):
    fake = FakeAmpliTrim()
    args = setup(tmp_path, "arfken_its1")
    assert E.main(["--out", str(tmp_path)] + args, run=fake) == 0 and len(fake.commands) == 1
    assert E.main(["--out", str(tmp_path)] + args, run=fake) == 0 and len(fake.commands) == 1       # no new run
    assert E.main(["--out", str(tmp_path), "--rerun"] + args, run=fake) == 0 and len(fake.commands) == 2


def test_main_stops_and_says_why(tmp_path, capsys):
    args = setup(tmp_path, "arfken_its1")
    assert E.main(["--out", str(tmp_path)] + args, run=FakeAmpliTrim(fail=True)) == 2
    said = capsys.readouterr().out
    assert "arfken_its1: AmpliTrim could not run" in said and "no read pairs found" in said
    assert E.main(["--out", str(tmp_path), "--rerun"] + args, run=FakeAmpliTrim(plain=True)) == 2          # a run without --its has no ITS numbers
    assert "arfken_its1:" in capsys.readouterr().out
    assert E.main(["--out", str(tmp_path), "--dataset", "arfken_its2"], run=FakeAmpliTrim()) == 2
    assert "its_followup.py for this label first" in capsys.readouterr().out
    (tmp_path / "arfken_its2_samples.tsv").write_text((tmp_path / "arfken_its1_samples.tsv").read_text())
    assert E.main(["--out", str(tmp_path), "--dataset", "arfken_its2"], run=FakeAmpliTrim()) == 2          # the table is there but the thinned reads are not
    assert "the thinned reads" in capsys.readouterr().out
    assert E.main(["--out", str(tmp_path), "--whole", f"arfken_its1={tmp_path / 'nowhere'}", "--rerun"] + args, run=FakeAmpliTrim()) == 2
    assert "was not found" in capsys.readouterr().out
    assert E.main(["--out", str(tmp_path)], run=FakeAmpliTrim()) == 2
    assert "at least one --dataset" in capsys.readouterr().out
