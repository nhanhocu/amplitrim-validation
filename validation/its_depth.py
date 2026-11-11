#!/usr/bin/env python
"""ITS depth series: do the results depend on how many pairs per sample are given to DADA2?

  python validation\\its_depth.py --run 1000=C:\\data\\runs\\26_depth_1000 --run 5000=C:\\data\\runs\\26_its_followup --run 20000=C:\\data\\runs\\26_depth_20000 --out C:\\data\\runs\\26_depth

Each --run is a --out folder of validation\\its_followup.py (run it once per depth with --pairs N, the same datasets and labels). The table gives, for every label and depth, the shares of the
input pairs that pass the filter, enter the merge step, are refused (by reason) and merge at the default mismatch limit, and the share of the refused pairs that merge when 5 mismatches
are allowed. P76 (TEST_REGISTER.md, the section for this follow-up): the share of the input pairs that merge at the default is within 5 points between 5,000 and 20,000 pairs per sample, on
every label that has both. Writes ITS_DEPTH_REPORT.md to --out.
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]

import its_followup as F                                                  # noqa: E402

LABELS = ("its2", "its", "v4")
LOW, HIGH = 5000, 20000
STABLE_POINTS = 5.0       # P76


def collect(runs: dict, labels) -> dict:
    """depth -> label -> F.flow(...), for the labels whose table is in that run's folder."""
    out = {}
    for depth, folder in runs.items():
        for label in labels:
            p = Path(folder) / f"{label}_samples.tsv"
            if p.is_file():
                f = F.flow(F.read_samples(p))
                if f:
                    out.setdefault(depth, {})[label] = f
    return out


def verdict(table: dict):
    both = [l for l in LABELS if l in table.get(LOW, {}) and l in table.get(HIGH, {})]
    if not both:
        return ("P76", f"not decided: needs a run at {LOW:,} and one at {HIGH:,} pairs per sample for the same label", None)
    diffs = {l: (table[HIGH][l]["merged"][0] - table[LOW][l]["merged"][0]) * 100 for l in both}
    return ("P76", f"The share of the input pairs that merge at the default is within {STABLE_POINTS:g} points between {LOW:,} and {HIGH:,} pairs per sample, on every label that has both: "
                   + ", ".join(f"{l} {table[LOW][l]['merged'][0]:.1%} to {table[HIGH][l]['merged'][0]:.1%} ({d:+.1f} points)" for l, d in diffs.items()), all(abs(d) <= STABLE_POINTS for d in diffs.values()))


def report_lines(table: dict) -> list:
    p, txt, ok = verdict(table)
    L = ["# ITS depth series", "", "The criterion (P76) is in TEST_REGISTER.md and was fixed before this ran.", "", "## Verdict", "",
         f"- **{p}** {txt}" if ok is None else f"- **{p}** {'MET' if ok else 'NOT MET'}: {txt}"]
    for label in LABELS:
        rows = [(d, table[d][label]) for d in sorted(table) if label in table[d]]
        if not rows:
            continue
        L += ["", f"## {label}", "", "| pairs per sample | samples | pass the filter | enter the merge step | refused: short | refused: mismatches or indels | merged at the default | of the refused, merged at 5 mismatches |",
              "|---|---|---|---|---|---|---|---|"]
        for d, f in rows:
            rec = f["recovered_all"][5]
            L.append(f"| {d:,} | {f['samples']} | {f['filtered']:.2%} | {f['reach']:.2%} | {f['rej_short']:.2%} | {f['rej_mismatch']:.2%} | {f['merged'][0]:.2%} | {'' if rec is None else f'{rec:.1%}'} |")
    return L + ["", "Next: send this file."]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", action="append", metavar="PAIRS=FOLDER", required=True, help="a depth and the --out folder of its_followup.py at that depth; repeat")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    runs = {}
    for depth, folder in F.parse_pairs(a.run, "--run").items():
        if not depth.isdigit():
            raise SystemExit(f"--run wants PAIRS=FOLDER with a whole number of pairs, not {depth}={folder}")
        runs[int(depth)] = folder
    table = collect(runs, LABELS)
    if not table:
        print("No <label>_samples.tsv (its2, its or v4) was found in the folders given.")
        return 2
    a.out.mkdir(parents=True, exist_ok=True)
    L = report_lines(table)
    (a.out / "ITS_DEPTH_REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:6]))
    print(f"\nwritten: {a.out / 'ITS_DEPTH_REPORT.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
