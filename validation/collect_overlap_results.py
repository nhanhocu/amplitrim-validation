"""Collect the runs of the minimum-overlap test (register section 27) into one table and judge the predictions.

    python collect_overlap_results.py C:\\data\\runs --out C:\\data\\runs\\overlap_results

It reads every folder named overlap_<dataset>_<T or S>_k<overlap> under the folder you give, takes the row of the fixed setting
(t12, s10, ...) from its compare_methods.tsv, and writes <out>.tsv and <out>.md. Folders without compare_methods.tsv are listed as
unfinished. The verdicts follow the rules of the register: P-O1 to P-O3 are MET only if every dataset present meets them and all four
mock communities are there; otherwise the line says how many datasets were judged.
"""
import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path

PATTERN = re.compile(r"^overlap_(?P<name>.+)_(?P<arm>[TS])_k(?P<k>\d+)$")
EXPECTED = 4


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def read_asvs(folder, tag):
    for f in sorted(Path(folder).glob("asvs_*.fasta")):
        if tag.lower() in f.stem.lower():
            seqs, cur = set(), []
            for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
                if line.startswith(">"):
                    if cur:
                        seqs.add("".join(cur).upper())
                    cur = []
                else:
                    cur.append(line.strip())
            if cur:
                seqs.add("".join(cur).upper())
            return seqs
    return None


def collect(root):
    rows, unfinished = [], []
    for d in sorted(Path(root).iterdir()):
        m = PATTERN.match(d.name)
        if not (d.is_dir() and m):
            continue
        tsv = d / "compare_methods.tsv"
        if not tsv.exists():
            unfinished.append(d.name)
            continue
        tag = f"{m['arm'].lower()}{m['k']}"
        with open(tsv, newline="", encoding="utf-8") as fh:
            found = [r for r in csv.DictReader(fh, delimiter="\t") if r["name"] == tag]
        if not found:
            unfinished.append(d.name + " (no row " + tag + ")")
            continue
        r = found[0]
        rows.append({"dataset": m["name"], "arm": m["arm"], "k": int(m["k"]), "truncF": r["truncF"], "truncR": r["truncR"], "maxEE": r["maxEE"],
                     "pass": num(r["pass"]), "merged": num(r["merged"]), "variants": num(r["found"]), "strains": r.get("strains") or "",
                     "identical": num(r["identical"]), "extra": num(r["extra"]), "asvs": num(r["asvs"]), "error": r.get("error") or "",
                     "folder": str(d)})
        rows[-1]["note"] = ""
        if rows[-1]["merged"] is None and rows[-1]["pass"] is None:
            err = rows[-1]["error"]
            if "removed all reads" in err:                   # filterAndTrim: every read is shorter than the cut
                rows[-1]["note"] = "no result: the cut is longer than the reads (DADA2 removed all reads)"
            elif err:
                rows[-1]["note"] = "no result: " + re.sub(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s]+", r"C:\\Users\\<user>", err)[:80]
            else:
                rows[-1]["note"] = "no result (DADA2 kept no reads: is the cut longer than the reads? check the log)"
    shares = [x[key] for x in rows for key in ("pass", "merged") if x[key] is not None]
    if shares and max(shares) <= 1.0:                    # fractions: show percentages
        for x in rows:
            for key in ("pass", "merged"):
                x[key] = None if x[key] is None else 100 * x[key]
    for x in rows:
        x["identical"] = None if x["identical"] is None else 100 * x["identical"] if x["identical"] <= 1.0 else x["identical"]
    return rows, unfinished


def strains_found(text):
    m = re.match(r"\s*(\d+)\s*/\s*(\d+)", text or "")
    return int(m.group(1)) if m else None


def judge(rows):
    by = {}
    for x in rows:
        if x["note"]:
            continue
        by.setdefault(x["dataset"], {})[(x["arm"], x["k"])] = x
    out = []

    def verdict(name, text, flags, descriptive=False):
        n = len(flags)
        if descriptive:
            out.append(f"- {name}: {text}: {sum(flags)} of {n} datasets (descriptive)")
        else:
            tag = "MET" if n >= EXPECTED and all(flags) else ("NOT MET" if not all(flags) else f"not judged: only {n} of {EXPECTED} datasets")
            out.append(f"- **{name} {tag}**: {text} ({sum(flags)} of {n} datasets)")

    # P-O1: with the k = 12 cut, minOverlap 10 gives the same merged share (0.1) and no ASV that is absent at 12
    flags, notes = [], []
    for ds, d in by.items():
        a, b = d.get(("S", 10)), d.get(("T", 12))
        if not (a and b and a["merged"] is not None and b["merged"] is not None):
            continue
        ok = abs(a["merged"] - b["merged"]) <= 0.1
        sa, sb = read_asvs(a["folder"], "s10"), read_asvs(b["folder"], "t12")
        if sa is not None and sb is not None:
            ok = ok and not (sa - sb)
        else:
            notes.append(f"{ds}: ASV files not found, only the merged share was compared")
        flags.append(ok)
    if flags:
        verdict("P-O1", "minOverlap 10 on the 12 cut: same merged share (0.1 points), no ASV that 12 lacks", flags)
        out.extend("  - " + n for n in notes)
    # P-O2: identical share at 12 within 1.0 point of the best k; strains equal the best
    flags = []
    for ds, d in by.items():
        t = {k: v for (arm, k), v in d.items() if arm == "T" and v["identical"] is not None}
        if 12 in t:
            best = max(v["identical"] for v in t.values())
            bs = max((strains_found(v["strains"]) or 0) for v in t.values())
            flags.append(best - t[12]["identical"] <= 1.0 and (strains_found(t[12]["strains"]) or 0) >= bs)
    if flags:
        verdict("P-O2", "k = 12: reads in exact ASVs within 1.0 point of the best k, strains equal the best", flags)
    # P-O3: unexpected ASVs at 12 <= at 20 + 2
    flags = [d[("T", 12)]["extra"] <= d[("T", 20)]["extra"] + 2 for d in by.values()
             if ("T", 12) in d and ("T", 20) in d and d[("T", 12)]["extra"] is not None and d[("T", 20)]["extra"] is not None]
    if flags:
        verdict("P-O3", "k = 12: no more than 2 unexpected ASVs more than at k = 20", flags)
    # P-O4 (descriptive): merged share lower at 25 than at 12 by at least 1 point
    for arm in ("T", "S"):
        flags = [d[("T", 12)]["merged"] - d[(arm, 25)]["merged"] >= 1.0 for d in by.values()
                 if (("T", 12) in d) and ((arm, 25) in d) and d[("T", 12)]["merged"] is not None and d[(arm, 25)]["merged"] is not None]
        if flags:
            verdict(f"P-O4 (arm {arm})", "merged share at k = 25 at least 1 point below k = 12", flags, descriptive=True)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", type=Path, help="the folder that holds the overlap_* run folders")
    ap.add_argument("--out", type=Path, default=Path("overlap_results"))
    args = ap.parse_args(argv)
    rows, unfinished = collect(args.runs)
    if not rows:
        sys.exit("no finished overlap_* runs found in " + str(args.runs))
    rows.sort(key=lambda x: (x["dataset"], x["arm"], x["k"]))
    cols = ["dataset", "arm", "k", "truncF", "truncR", "maxEE", "pass", "merged", "variants", "strains", "identical", "extra", "asvs", "error"]
    with open(str(args.out) + ".tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    def f(v, nd=1):
        return "" if v is None else (f"{v:.{nd}f}" if isinstance(v, float) else str(v))
    md = ["# Minimum-overlap test (register section 27)", "", "| dataset | arm | k | cut F/R | maxEE | pass % | merged % | variants | strains | reads in exact ASVs % | extra ASVs | ASVs | note |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in rows:
        md.append(f"| {x['dataset']} | {x['arm']} | {x['k']} | {x['truncF']}/{x['truncR']} | {x['maxEE']} | {f(x['pass'])} | {f(x['merged'])} | {f(x['variants'], 0)} | {x['strains']} | {f(x['identical'], 2)} | {f(x['extra'], 0)} | {f(x['asvs'], 0)} | {x['note']} |")
    md += ["", "Arm T: the cut follows k. Arm S: the cut of k = 12, only minOverlap changes.", "", "## Verdicts", *judge(rows)]
    if unfinished:
        md += ["", "## Unfinished or without the expected row: run these again", *[f"- {u}" for u in unfinished]]
    with open(str(args.out) + "_asv_sets.tsv", "w", newline="", encoding="utf-8") as fh:          # the archive keeps no ASV FASTA: keep a fingerprint of each set
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["dataset", "arm", "k", "asvs", "sha256_of_sorted_asvs"])
        for x in rows:
            seqs = read_asvs(x["folder"], f"{x['arm'].lower()}{x['k']}")
            w.writerow([x["dataset"], x["arm"], x["k"], "" if seqs is None else len(seqs), "" if seqs is None else hashlib.sha256("\n".join(sorted(seqs)).encode()).hexdigest()[:16]])
    md += ["", "ASV sets: see overlap_results_asv_sets.tsv; two runs with the same fingerprint have exactly the same ASVs."]
    Path(str(args.out) + ".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    print(f"\nwritten {args.out}.tsv, {args.out}.md and {args.out}_asv_sets.tsv", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
