"""The ITS follow-up in the archive: the thresholds in the code are the ones written in the register section, the runs of the follow-up are recognised by the organiser, and the collector
leaves out the thinned reads. The register is written before the run; these tests fail if a number is changed in the code or in the register only."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "validation"))
import collect_results as cr  # noqa: E402
import its_depth  # noqa: E402
import its_estimates  # noqa: E402
import its_followup  # noqa: E402
import its_truth  # noqa: E402
import organise_data as od  # noqa: E402


def section() -> str:
    text = (ROOT / "TEST_REGISTER.md").read_text(encoding="utf-8")
    m = re.search(r"^## \d+\. ITS follow-up: why DADA2 refuses ITS pairs.*?(?=^## \d+\. |\Z)", text, re.M | re.S)
    assert m, "the register has no section 'ITS follow-up: why DADA2 refuses ITS pairs ...'"
    return m.group(0)


def predictions() -> dict:
    return {m.group(1): m.group(2) for m in re.finditer(r"^- \*\*(P\d+)[^*]*\*\* (.*)$", section(), re.M)}


def test_every_criterion_of_the_code_is_written_in_the_register():
    p = predictions()
    assert sorted(p) == [f"P{n}" for n in range(68, 83)], sorted(p)


def test_the_thresholds_of_the_code_are_the_ones_of_the_register():
    p = predictions()
    checks = [("P68", "at least 50%", its_followup.NEAR_MISS_SHARE, 0.5), ("P69", "at least 15 points", its_followup.LENGTH_POINTS, 15.0), ("P70", "at least 20%", its_followup.INDEL_SHARE, 0.20),
              ("P72", "by at most 10%", its_followup.ASV_RISE, 0.10), ("P73", "at least 50%", its_followup.PARTNERS, 0.5), ("P75", "The same as P73", its_followup.PARTNERS, 0.5),
              ("P74", "at most 1 ASV", its_followup.ISOLATE_RISE, 1), ("P76", "within 5 points", its_depth.STABLE_POINTS, 5.0), ("P77", "within 1 point", its_estimates.FILTER_POINTS, 1.0),
              ("P79", "less than 17 points", its_estimates.ISOLATE_LIMIT, 17.0), ("P80", "by at most 1 point", its_truth.SPURIOUS_RISE, 1.0), ("P82", "at least 2 points", its_truth.GAIN, 2.0)]
    for pid, phrase, value, expected in checks:
        assert phrase in p[pid], (pid, phrase)
        assert value == expected, (pid, value, expected)


def test_the_definitions_of_the_code_are_the_ones_of_the_register():
    s = section()
    assert (its_truth.REF_SHARE, its_truth.SEEN_SHARE, its_truth.EDIT) == (0.01, 0.001, 2)
    for phrase in ("at least 1% of an isolate's merged pairs", "0.1% or more of the merged pairs", "within 2 edits"):
        assert phrase in s, phrase
    assert (its_followup.MIN_LEN, its_followup.MAX_EE, its_followup.MIN_OVERLAP, its_followup.LIMITS) == (50, 2.0, 12, (0, 1, 2, 5))
    for phrase in ("`maxEE = 2`", "`minLen = 50`", "`minOverlap = 12`", "a mismatch limit of 0 (the default), 1, 2 and 5"):
        assert phrase in s, phrase
    assert (its_depth.LOW, its_depth.HIGH) == (5000, 20000) and "5,000" in predictions()["P76"] and "20,000" in predictions()["P76"]
    assert its_followup.DEFAULT_PAIRS == 5000 and "5,000 pairs per sample" in s
    assert its_estimates.EXPECTED_VERSION == "0.2.0" and "AmpliTrim 0.2.0 is run with `--its`" in s              # the release the register names is the release the script demands


def test_the_register_section_is_listed_for_the_run_of_the_follow_up():
    number = od.run_number("its_followup")
    row = [r for r in od.RUNS if r[0] == number][0]
    m = re.match(r"## (\d+)\.", section())
    assert row[2] == m.group(1) and row[1].lower() == "its follow-up"


def test_the_folders_of_the_follow_up_are_recognised_as_one_run_and_not_as_the_earlier_its_runs():
    n = od.run_number("its_followup")
    assert n is not None
    assert all(od.run_number(f) == n for f in ("its_followup", "its_followup_arfken", "its_followup_summary", "its_depth", "its_depth_1000", "its_depth_20000"))
    assert od.run_number("its_check") != n and od.run_number("its_merge_check") != n


def test_the_collector_leaves_out_the_thinned_reads_and_keeps_the_reports(tmp_path):
    root = tmp_path / "its_followup"
    files = {"ITS_FOLLOWUP_REPORT.md": True, "arfken_its1_samples.tsv": True, "arfken_its1_reads/C-ITS1a_R1.fastq.gz": False, "arfken_its1_reads/note.txt": False,
             "amplitrim_thinned_arfken_its1/summary.json": True, "amplitrim_thinned_arfken_its1/work/stage0.log": False}
    for rel, keep in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x", encoding="utf-8")
    for rel, keep in files.items():
        assert cr.wanted(root / rel, root)[0] is keep, rel
