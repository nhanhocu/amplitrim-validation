#!/usr/bin/env python
"""ITS estimates test: does AmpliTrim's ITS mode predict what DADA2 does on independent ITS1 and ITS2 libraries? (Figure 2 and Supplementary Figure S2, on new data)

  python validation\\its_estimates.py --out C:\\data\\runs\\26_its_followup_arfken --dataset arfken_its1 --dataset arfken_its2 --dataset arfken_mix_its1 --dataset arfken_mix_its2

Run validation\\its_followup.py first, with the same labels and the same --out: DADA2's numbers come from its <label>_samples.tsv, and the reads that DADA2 received are in <label>_reads.
Each --dataset gives AmpliTrim (with --its) the same thinned reads that DADA2 received, so that both sides see exactly the same pairs. This matters: the samples of a group may differ many-fold in
size and in filter pass rate, and AmpliTrim on a whole folder weights them by their reads while the thinning gives every sample the same number of pairs. AmpliTrim's summary.json gives the
predicted share of pairs that pass the filter (its.pass) and the estimated yield (recommended.estimated_yield). Compared with DADA2 at the same settings (maxEE 2, minLen 50, no truncation).
AmpliTrim is started from --out (never from the validation archive, whose own early copy of the package would shadow the installed release), its version and folder are printed in the report, and
anything but the version named in the register (0.2.0) stops the script. Optionally, --whole LABEL=FOLDER also runs AmpliTrim on the whole folder of a group, as a user would; that table is exploratory and decides nothing. Part of TEST_REGISTER.md (the section for
this follow-up; criteria P77 to P79). Writes ITS_ESTIMATES_REPORT.md and amplitrim_thinned_<label>\\ (and amplitrim_whole_<label>\\) to --out.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]

import its_followup as F                                                  # noqa: E402

FILTER_POINTS = 1.0        # P77: the predicted share of pairs that pass the filter is within this many points of DADA2's, on every group
ISOLATE_LIMIT = 17.0       # P79: on the isolates the estimate of the yield is too high by less than this many points (a quarter of the +68.1 of the second ITS study)
CALL = "import sys; from amplitrim.cli import main; sys.exit(main())"     # AmpliTrim's command line, called from this Python
EXPECTED_VERSION = "0.2.0"                                                 # the register says AmpliTrim 0.2.0: the release, not a development copy
WHO = "import amplitrim; print(amplitrim.__version__); print(amplitrim.__file__)"      # the same two lines the closing run (night10.py) uses to say which package it tests


def installed(run, cwd) -> tuple:
    """(version, folder) of the AmpliTrim that this Python imports, which is the one that the command above runs. It is asked from `cwd`, a folder that has no amplitrim folder of its own:
    the validation archive ships a copy of the early package (version 0.1.0, with other options), and python -c imports from the folder it is started in, so from the archive that copy would
    shadow the installed release."""
    p = run([sys.executable, "-c", WHO], capture_output=True, text=True, cwd=str(cwd))
    lines = (p.stdout or "").strip().splitlines()
    if p.returncode != 0 or len(lines) < 2:
        raise RuntimeError("AmpliTrim cannot be imported in this Python: " + ((p.stderr or p.stdout or "").strip()[-300:] or "no message"))
    return lines[0].strip(), str(Path(lines[1].strip()).parent)


def read_summary(path: Path) -> dict:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    try:
        return {"pass": float(d["its"]["pass"]), "yield": float(d["recommended"]["estimated_yield"]), "pairs": int(d["its"]["pairs"])}
    except (KeyError, TypeError) as e:
        raise RuntimeError(f"{path} lacks the ITS numbers (was AmpliTrim run with --its?): {e}")


def compare(summary: dict, flow: dict) -> dict:
    """Points of difference between AmpliTrim's numbers and DADA2's, as shares of the input pairs."""
    return {"predicted_pass": summary["pass"], "observed_pass": flow["filtered"], "pass_diff": (summary["pass"] - flow["filtered"]) * 100,
            "estimated_yield": summary["yield"], "merged": flow["merged"][0], "overshoot": (summary["yield"] - flow["merged"][0]) * 100,
            "pairs_analysed": summary["pairs"], "samples": flow["samples"]}


def verdicts(res: dict) -> list:
    """res: label -> compare(...). Labels are arfken_its1, arfken_its2 (isolates) and arfken_mix_its1, arfken_mix_its2 (mixes)."""
    if not res:
        return [(p, "not decided: no group was run", None) for p in ("P77", "P78", "P79")]
    worst = max(res.items(), key=lambda kv: abs(kv[1]["pass_diff"]))
    out = [("P77", f"AmpliTrim's predicted share of pairs that pass the filter is within {FILTER_POINTS:g} point of DADA2's on every group: "
                   + ", ".join(f"{l} {r['pass_diff']:+.2f}" for l, r in res.items()), all(abs(r["pass_diff"]) <= FILTER_POINTS for r in res.values()))]
    pairs = [(m, res[f"arfken_{m}"]["overshoot"], res[f"arfken_mix_{m}"]["overshoot"]) for m in ("its1", "its2") if f"arfken_{m}" in res and f"arfken_mix_{m}" in res]
    out.append(("P78", "The estimate of the yield is too high by fewer points on the isolates than on the mixes, on every marker that has both: "
                       + (", ".join(f"{m.upper()} {i:+.1f} against {x:+.1f}" for m, i, x in pairs) if pairs else "needs the isolates and the mixes of one marker"),
                None if not pairs else all(i < x for _, i, x in pairs)))
    iso = {l: r for l, r in res.items() if l.startswith("arfken_its")}
    out.append(("P79", f"On the isolates the estimate of the yield is too high by less than {ISOLATE_LIMIT:g} points: "
                       + (", ".join(f"{l} {r['overshoot']:+.1f}" for l, r in iso.items()) if iso else "the isolates were not run"),
                None if not iso else all(r["overshoot"] < ISOLATE_LIMIT for r in iso.values())))
    return out


def report_lines(res: dict, whole: dict = None, version: tuple = None) -> list:
    L = ["# ITS estimates test", "", "The criteria (P77 to P79) are in TEST_REGISTER.md and were fixed before this ran.", ""]
    if version:
        L += [f"AmpliTrim {version[0]} ({version[1]})", ""]
    L += ["## Verdicts", ""]
    for p, txt, ok in verdicts(res):
        L.append(f"- **{p}** {txt}" if ok is None else f"- **{p}** {'MET' if ok else 'NOT MET'}: {txt}")
    L += ["", "## Filter (Figure 2 on new data)", "", "| group | AmpliTrim predicts | DADA2 observes | difference (points) |", "|---|---|---|---|"]
    L += [f"| {l} | {r['predicted_pass']:.2%} | {r['observed_pass']:.2%} | {r['pass_diff']:+.2f} |" for l, r in res.items()]
    L += ["", "## Yield (Supplementary Figure S2 on new data)", "", "| group | AmpliTrim estimates | DADA2 merged | too high by (points) | pairs analysed by AmpliTrim | samples |", "|---|---|---|---|---|---|"]
    L += [f"| {l} | {r['estimated_yield']:.2%} | {r['merged']:.2%} | {r['overshoot']:+.1f} | {r['pairs_analysed']:,} | {r['samples']} |" for l, r in res.items()]
    if whole:
        L += ["", "## Exploratory: AmpliTrim on the whole folders (as a user would), against DADA2 on the thinned reads", "",
              "| group | filter: AmpliTrim predicts | DADA2 observes | difference (points) | yield: AmpliTrim estimates | DADA2 merged | too high by (points) |", "|---|---|---|---|---|---|---|"]
        L += [f"| {l} | {r['predicted_pass']:.2%} | {r['observed_pass']:.2%} | {r['pass_diff']:+.2f} | {r['estimated_yield']:.2%} | {r['merged']:.2%} | {r['overshoot']:+.1f} |" for l, r in whole.items()]
    return L + ["", "Next: send this file."]


def analyse(label, folder, rep, samples, run, rerun, cwd):
    """AmpliTrim (unless its summary.json is already there) and the comparison with DADA2. Returns (comparison, None) or (None, the message to print)."""
    if rerun or not (rep / "summary.json").is_file():
        if not Path(folder).is_dir():
            return None, f"{label}: the folder {folder} was not found."
        p = run([sys.executable, "-c", CALL, "--input-dir", str(folder), "--work-dir", str(rep / "work"), "--out-dir", str(rep), "--its"], capture_output=True, text=True, cwd=str(cwd))
        if p.returncode != 0 or not (rep / "summary.json").is_file():
            return None, f"{label}: AmpliTrim could not run: {(p.stderr or p.stdout or '').strip()[-500:]}"
    try:
        return compare(read_summary(rep / "summary.json"), F.flow(F.read_samples(samples))), None
    except RuntimeError as e:
        return None, f"{label}: {e}"


def main(argv=None, run=subprocess.run) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, required=True, help="the --out folder of validation\\its_followup.py")
    ap.add_argument("--dataset", action="append", metavar="LABEL", default=[], help="a group; AmpliTrim analyses the thinned reads that DADA2 received (<out>\\<label>_reads); repeat")
    ap.add_argument("--whole", action="append", metavar="LABEL=FOLDER", default=[], help="exploratory: AmpliTrim on the whole folder of a group; repeat")
    ap.add_argument("--rerun", action="store_true", help="run AmpliTrim again even if its summary.json is already there")
    ap.add_argument("--expect-version", default=EXPECTED_VERSION, help=f"the version of AmpliTrim that the register names (default {EXPECTED_VERSION}); 'any' lets another version run and the report says which")
    a = ap.parse_args(argv)
    if not a.dataset:
        print("Give at least one --dataset LABEL (a label that validation\\its_followup.py was run with).")
        return 2
    try:
        a.out.mkdir(parents=True, exist_ok=True)
        version = installed(run, a.out)
    except RuntimeError as e:
        print(e)
        return 2
    if a.expect_version != "any" and version[0] != a.expect_version:
        print(f"The AmpliTrim in this Python is version {version[0]} ({version[1]}), not {a.expect_version}, which the register names. Install the release in this environment "
              f"(pip install amplitrim=={a.expect_version}) or run this script with the Python that has it; --expect-version any would run this one and the report would say so.")
        return 2
    wholes = F.parse_pairs(a.whole, "--whole")
    res, whole = {}, {}
    for label in a.dataset:
        samples = a.out / f"{label}_samples.tsv"
        if not samples.is_file():
            print(f"{label}: {samples} was not found; run validation\\its_followup.py for this label first.")
            return 2
        reads = a.out / f"{label}_reads"
        if not reads.is_dir() and not (a.out / f"amplitrim_thinned_{label}" / "summary.json").is_file():
            print(f"{label}: the thinned reads {reads} were not found; validation\\its_followup.py writes them (with --pairs above 0).")
            return 2
        res[label], msg = analyse(label, reads, a.out / f"amplitrim_thinned_{label}", samples, run, a.rerun, a.out)
        if msg:
            print(msg)
            return 2
    for label, folder in wholes.items():
        samples = a.out / f"{label}_samples.tsv"
        if not samples.is_file():
            print(f"{label}: {samples} was not found; run validation\\its_followup.py for this label first.")
            return 2
        whole[label], msg = analyse(label, folder, a.out / f"amplitrim_whole_{label}", samples, run, a.rerun, a.out)
        if msg:
            print(msg)
            return 2
    L = report_lines(res, whole, version)
    (a.out / "ITS_ESTIMATES_REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:next(i for i, x in enumerate(L) if x.startswith("## ") and x != "## Verdicts")]))
    print(f"\nwritten: {a.out / 'ITS_ESTIMATES_REPORT.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
