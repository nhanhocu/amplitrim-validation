#!/usr/bin/env python
"""ITS follow-up summary: the criteria P68 to P82 in one table, from the reports of the steps, and the outcome rows of the register section.

  python validation\\its_summary.py --run C:\\data\\runs\\its_followup --run C:\\data\\runs\\its_followup_arfken --run C:\\data\\runs\\its_depth --out C:\\data\\runs\\its_followup_summary

Each --run is a folder that holds reports of validation\\its_followup.py, its_truth.py, its_estimates.py or its_depth.py (ITS_FOLLOWUP_REPORT.md, ITS_TRUTH_REPORT.md, ITS_ESTIMATES_REPORT.md,
ITS_DEPTH_REPORT.md); the numbered folders under runs\\ work too. The verdict lines ('- **P68** MET: ...') are read from them. A criterion that one step could not decide (its datasets were not
run in that step) and another decided is taken from the one that decided it; two steps that decide the same criterion differently are reported as a conflict, and nothing is chosen.
Writes ITS_FOLLOWUP_SUMMARY.md to --out. Part of TEST_REGISTER.md (the section for this follow-up). Exit code 0 when every criterion P68 to P82 has been decided or is reported as not
decided with its reason, and 2 when a criterion appears in no report at all (a step was not run) or when two reports conflict.
"""
import argparse
import re
import sys
from pathlib import Path

IDS = [f"P{n}" for n in range(68, 83)]
LINE = re.compile(r"^- \*\*(P\d+)\*\* (MET|NOT MET): (.*)$")
UNDECIDED = re.compile(r"^- \*\*(P\d+)\*\* (not decided: .*)$")
REPORTS = ("ITS_FOLLOWUP_REPORT.md", "ITS_TRUTH_REPORT.md", "ITS_ESTIMATES_REPORT.md", "ITS_DEPTH_REPORT.md")


def parse(text: str) -> dict:
    """criterion -> (verdict, text) for one report; verdict is 'MET', 'NOT MET' or 'not decided'."""
    out = {}
    for line in text.splitlines():
        m = LINE.match(line)
        if m:
            out[m.group(1)] = (m.group(2), m.group(3))
            continue
        m = UNDECIDED.match(line)
        if m:
            out[m.group(1)] = ("not decided", m.group(2))
    return out


def collect(runs) -> tuple:
    """(criterion -> (verdict, text, report path), conflicts). A decided verdict wins over 'not decided'; two different decided verdicts are a conflict."""
    merged, conflicts = {}, []
    for run in runs:
        for name in REPORTS:
            p = Path(run) / name
            if not p.is_file():
                continue
            for cid, (verdict, text) in parse(p.read_text(encoding="utf-8")).items():
                old = merged.get(cid)
                if old is None or (old[0] == "not decided" and verdict != "not decided"):
                    merged[cid] = (verdict, text, p)
                elif verdict != "not decided" and old[0] != "not decided" and old[0] != verdict:
                    conflicts.append(f"{cid}: {old[0]} in {old[2]} but {verdict} in {p}")
    return merged, conflicts


def summary_lines(merged: dict, conflicts: list) -> list:
    n = {v: sum(1 for c in IDS if merged.get(c, ("", "", ""))[0] == v) for v in ("MET", "NOT MET", "not decided")}
    absent = [c for c in IDS if c not in merged]
    L = ["# ITS follow-up: summary", "", f"{len(IDS)} criteria (P68 to P82): {n['MET']} met, {n['NOT MET']} not met, {n['not decided']} not decided, {len(absent)} in no report.", ""]
    if conflicts:
        L += ["**Conflicts (nothing was chosen):**", ""] + [f"- {c}" for c in conflicts] + [""]
    if absent:
        L += [f"**In no report (a step was not run):** {', '.join(absent)}", ""]
    L += ["## Outcome table for the register", "", "| | Outcome |", "|---|---|"]
    for c in IDS:
        v, text, src = merged.get(c, ("not run", "no report holds this criterion", None))
        L.append(f"| {c} | {v.upper() if v in ('MET', 'NOT MET') else v}: {text} |")
    L += ["", "## Where each verdict comes from", ""]
    for c in IDS:
        if c in merged:
            L.append(f"- {c}: `{merged[c][2].parent.name}/{merged[c][2].name}`")
    return L + ["", "Next: send this file."]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", action="append", required=True, metavar="FOLDER", help="a folder with reports of the steps; repeat")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    missing = [r for r in a.run if not Path(r).is_dir()]
    if missing:
        print("Not found: " + ", ".join(missing))
        return 2
    merged, conflicts = collect(a.run)
    if not merged:
        print("No ITS_*_REPORT.md with verdict lines was found in the folders given.")
        return 2
    L = summary_lines(merged, conflicts)
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "ITS_FOLLOWUP_SUMMARY.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:next(i for i, x in enumerate(L) if x.startswith("## "))]))
    print(f"written: {a.out / 'ITS_FOLLOWUP_SUMMARY.md'}")
    return 2 if conflicts or any(c not in merged for c in IDS) else 0


if __name__ == "__main__":
    sys.exit(main())
