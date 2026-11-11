"""validation/its_summary.py: the criteria P68 to P82 in one table, from the reports of the steps. The verdict lines are in the form the other scripts write."""
import importlib.util
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "validation"))


def load():
    spec = importlib.util.spec_from_file_location("its_summary", HERE.parent / "validation" / "its_summary.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


S = load()


def report(path, *lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# a report\n\n## Verdicts\n\n" + "\n".join(lines) + "\n\n## a table\n\n| x |\n", encoding="utf-8")


ND = "not decided: the second ITS study was not run"


def world(tmp_path):
    """Three folders as the real steps leave them: part A (second ITS, first ITS, soil V4), part B (the Arfken groups: the follow-up, the truth test, the estimates) and the depth series."""
    a, b, c = tmp_path / "its_followup", tmp_path / "its_followup_arfken", tmp_path / "its_depth"
    report(a / "ITS_FOLLOWUP_REPORT.md", "- **P68** MET: On the second ITS study, 2 mismatches merge at least 50%: 100.0%", "- **P69** NOT MET: the longest third is not higher: -11.1 points",
           "- **P70** MET: at least 20% have an indel: 100.0%", "- **P71** MET: longer on the second ITS study: 275 nt against 188 nt", "- **P72** NOT MET: the ASVs rise by more than 10%: +100.0%",
           "- **P73** NOT MET: on soil V4: 23.6%", "- **P74** not decided: the single-isolate libraries were not run", "- **P75** MET: on the second ITS study: 61.0%")
    report(b / "ITS_FOLLOWUP_REPORT.md", *[f"- **P{n}** {ND}" for n in (68, 69, 70)], "- **P71** not decided: both ITS studies are needed", "- **P72** not decided: both ITS studies are needed",
           "- **P73** not decided: soil V4 was not run", "- **P74** MET: On the single-isolate libraries: arfken_its1 +0, arfken_its2 +0", f"- **P75** {ND}")
    report(b / "ITS_TRUTH_REPORT.md", "- **P80** MET: spurious +0.00 points", "- **P81** MET: recall 77.8% to 77.8%", "- **P82** NOT MET: its1 +0.0 points, its2 +0.0 points")
    report(b / "ITS_ESTIMATES_REPORT.md", "- **P77** MET: within 1 point: arfken_its1 +0.00", "- **P78** NOT MET: ITS1 +9.7 against +0.3", "- **P79** MET: arfken_its1 +9.7, arfken_its2 +0.0")
    report(c / "ITS_DEPTH_REPORT.md", "- **P76** MET: within 5 points: its2 40.0% to 43.0% (+3.0 points)")
    return a, b, c


def test_a_report_is_read_line_by_line_and_undecided_lines_keep_their_reason():
    p = S.parse("## Verdicts\n\n- **P68** MET: a: b\n- **P69** NOT MET: c\n- **P71** not decided: both ITS studies are needed\nnot a verdict line\n- **P70** maybe: d\n")
    assert p == {"P68": ("MET", "a: b"), "P69": ("NOT MET", "c"), "P71": ("not decided", "not decided: both ITS studies are needed")}


def test_a_decided_verdict_wins_over_not_decided_wherever_it_comes_from(tmp_path):
    merged, conflicts = S.collect(world(tmp_path))
    assert conflicts == [] and sorted(merged) == sorted(S.IDS)
    assert merged["P68"][0] == "MET" and merged["P68"][2].parent.name == "its_followup"                # part B said 'not decided'
    assert merged["P74"][0] == "MET" and merged["P74"][2].parent.name == "its_followup_arfken"         # part A said 'not decided'
    assert merged["P76"][2].name == "ITS_DEPTH_REPORT.md" and merged["P80"][2].name == "ITS_TRUTH_REPORT.md" and merged["P77"][2].name == "ITS_ESTIMATES_REPORT.md"


def test_the_summary_counts_the_verdicts_and_gives_the_outcome_rows(tmp_path):
    merged, conflicts = S.collect(world(tmp_path))
    L = "\n".join(S.summary_lines(merged, conflicts))
    assert "15 criteria (P68 to P82): 10 met, 5 not met, 0 not decided, 0 in no report." in L
    assert "| P69 | NOT MET: the longest third is not higher: -11.1 points |" in L and "| P74 | MET: On the single-isolate libraries: arfken_its1 +0, arfken_its2 +0 |" in L
    assert "Conflicts" not in L and "In no report" not in L and "- P76: `its_depth/ITS_DEPTH_REPORT.md`" in L


def test_two_reports_that_decide_a_criterion_differently_are_a_conflict_and_nothing_is_chosen(tmp_path):
    a, b, c = world(tmp_path)
    report(tmp_path / "again" / "ITS_FOLLOWUP_REPORT.md", "- **P68** NOT MET: On the second ITS study, 2 mismatches merge at least 50%: 12.0%")
    merged, conflicts = S.collect([a, b, c, tmp_path / "again"])
    assert len(conflicts) == 1 and conflicts[0].startswith("P68: MET in ") and "NOT MET in " in conflicts[0]
    assert "**Conflicts (nothing was chosen):**" in "\n".join(S.summary_lines(merged, conflicts))
    same = tmp_path / "same"
    report(same / "ITS_FOLLOWUP_REPORT.md", "- **P68** MET: On the second ITS study, 2 mismatches merge at least 50%: 100.0%")        # the same verdict twice is no conflict
    assert S.collect([a, same])[1] == []


def test_a_criterion_in_no_report_is_named(tmp_path):
    a, b, c = world(tmp_path)
    merged, conflicts = S.collect([a, b])                                                          # the depth series was not run
    L = "\n".join(S.summary_lines(merged, conflicts))
    assert "14 met" not in L and "1 in no report" in L and "**In no report (a step was not run):** P76" in L
    assert "| P76 | not run: no report holds this criterion |" in L


def test_main_writes_the_summary_and_the_exit_code_says_whether_everything_is_there(tmp_path, capsys):
    a, b, c = world(tmp_path)
    assert S.main(["--run", str(a), "--run", str(b), "--run", str(c), "--out", str(tmp_path / "out")]) == 0
    assert (tmp_path / "out" / "ITS_FOLLOWUP_SUMMARY.md").is_file() and "written:" in capsys.readouterr().out
    assert S.main(["--run", str(a), "--run", str(b), "--out", str(tmp_path / "out2")]) == 2           # P76 missing
    assert S.main(["--run", str(tmp_path / "nowhere"), "--out", str(tmp_path / "o3")]) == 2
    assert "Not found" in capsys.readouterr().out
    (tmp_path / "empty").mkdir()
    assert S.main(["--run", str(tmp_path / "empty"), "--out", str(tmp_path / "o4")]) == 2
    assert "No ITS_*_REPORT.md" in capsys.readouterr().out


def test_the_lines_of_the_real_scripts_are_read(tmp_path):
    """The verdict lines are produced by the other four scripts; their form must stay readable by this one."""
    sys.path.insert(0, str(HERE.parent / "validation"))
    import its_depth, its_estimates, its_followup, its_truth
    lines = []
    lines += [f"- **{p}** {txt}" if ok is None else f"- **{p}** {'MET' if ok else 'NOT MET'}: {txt}" for p, txt, ok in its_followup.verdicts({})]
    lines += [f"- **{p}** {txt}" if ok is None else f"- **{p}** {'MET' if ok else 'NOT MET'}: {txt}" for p, txt, ok in its_truth.verdicts({"its1": None, "its2": None})]
    lines += [f"- **{p}** {txt}" if ok is None else f"- **{p}** {'MET' if ok else 'NOT MET'}: {txt}" for p, txt, ok in its_estimates.verdicts({})]
    p, txt, ok = its_depth.verdict({})
    lines.append(f"- **{p}** {txt}")
    parsed = S.parse("\n".join(lines))
    assert sorted(parsed) == sorted(S.IDS) and all(v[0] == "not decided" for v in parsed.values())
