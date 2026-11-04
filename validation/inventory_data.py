"""Read-only inventory of the data drive: what is there, how big, how old, and what is not recorded in the validation archive.

    python inventory_data.py --base C:\\data --repo C:\\Users\\Admin\\OneDrive\\Documents\\GitHub\\amplitrim-validation --out C:\\data\\_reports\\inventory

It changes nothing. It writes <out>.md (to read) and <out>.tsv (to sort). For every folder of <base> and every folder of <base>\\runs it
gives the size, the number of files, the date of the newest file, and the size of the "bulk" (reads, work, trimmed, merge, filt, dada2:
what DADA2 and vsearch wrote, which can be made again) against the "results" (the .md .tsv .json .log .txt files that the archive keeps).
With --repo it also says whether a run folder has been collected into <repo>\\results.
"""
import argparse
import csv
import datetime
import os
import re
import shutil
import sys
import time
from pathlib import Path

BULK_DIRS = {"reads", "work", "trimmed", "merge", "filt", "dada2", "filtered", "subset", "explore", "stage0", "stability"}
RESULT_SUFFIXES = {".md", ".tsv", ".json", ".log", ".txt", ".csv"}
SCRATCH_WORDS = ("pypi", "test", "tmp", "temp", "sanity", "scratch", "old", "copy", "backup", "pilot")
SUPPORT = {"backup", "tools", "timing", "_reports", "_duplicates", "longread", "runs"}


def scan(folder):
    """(bytes, files, newest mtime, bulk bytes, result bytes) of a folder, walking it once."""
    total = files = bulk = results = 0
    newest = 0.0
    stack = [(str(folder), False)]
    while stack:
        path, in_bulk = stack.pop()
        try:
            with os.scandir(path) as it:
                for e in it:
                    try:
                        if e.is_dir(follow_symlinks=False):
                            stack.append((e.path, in_bulk or e.name.lower() in BULK_DIRS))
                        elif e.is_file(follow_symlinks=False):
                            st = e.stat()
                            total += st.st_size
                            files += 1
                            newest = max(newest, st.st_mtime)
                            if in_bulk or e.name.startswith("asvs_"):
                                bulk += st.st_size
                            elif Path(e.name).suffix.lower() in RESULT_SUFFIXES:
                                results += st.st_size
                    except OSError:
                        continue
        except OSError:
            continue
    return total, files, newest, bulk, results


def day(ts):
    return datetime.date.fromtimestamp(ts).isoformat() if ts else ""


def kind_of_top(name):
    low = name.lower()
    if re.match(r"^\d{2}_(mock|real)_", low):
        return "dataset"
    if low == "runs":
        return "runs"
    if low.startswith("_archive"):
        return "old archive"
    if low in SUPPORT or low.startswith("pilot"):
        return "support"
    return "UNKNOWN"


def flags_of_run(name, collected):
    out = []
    if not re.match(r"^\d{2}_", name):
        out.append("no number")
    if any(w in name.lower() for w in SCRATCH_WORDS):
        out.append("scratch?")
    if name.lower().startswith("overlap_"):
        out.append("part of the overlap test: group them")
    if collected is False:
        out.append("not in results/")
    return "; ".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", type=Path, required=True, help="the data drive folder, for example C:\\data")
    ap.add_argument("--repo", type=Path, help="the validation archive; its results folder is checked")
    ap.add_argument("--out", type=Path, default=Path("inventory"))
    args = ap.parse_args(argv)
    if not args.base.is_dir():
        sys.exit(f"{args.base} is not a folder")
    started = time.time()
    results_dir = (args.repo / "results") if args.repo else None
    collected_names = {p.name for p in results_dir.iterdir() if p.is_dir()} if results_dir and results_dir.is_dir() else None
    top, runs = [], []
    for d in sorted(p for p in args.base.iterdir() if p.is_dir()):
        t, n, newest, bulk, res = scan(d)
        top.append({"folder": d.name, "kind": kind_of_top(d.name), "gb": t / 1e9, "files": n, "newest": day(newest), "bulk_gb": bulk / 1e9, "results_mb": res / 1e6})
    rdir = args.base / "runs"
    if rdir.is_dir():
        for d in sorted(p for p in rdir.iterdir() if p.is_dir()):
            t, n, newest, bulk, res = scan(d)
            coll = None if collected_names is None else (d.name in collected_names)
            runs.append({"folder": d.name, "gb": t / 1e9, "files": n, "newest": day(newest), "bulk_gb": bulk / 1e9, "results_mb": res / 1e6, "flags": flags_of_run(d.name, coll)})
        loose = [p.name for p in rdir.iterdir() if p.is_file()]
    else:
        loose = []
    usage = shutil.disk_usage(args.base)
    rows = [("top", x) for x in top] + [("run", x) for x in runs]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(str(args.out) + ".tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["level", "folder", "kind", "gb", "files", "newest", "bulk_gb", "results_mb", "flags"])
        for lvl, x in rows:
            w.writerow([lvl, x["folder"], x.get("kind", ""), f"{x['gb']:.2f}", x["files"], x["newest"], f"{x['bulk_gb']:.2f}", f"{x['results_mb']:.1f}", x.get("flags", "")])
    md = [f"# Data inventory of {args.base}", "",
          f"Made {datetime.datetime.now():%Y-%m-%d %H:%M} in {time.time() - started:.0f} s. Nothing was changed.", "",
          f"Drive: {usage.free / 1e9:.1f} GB free of {usage.total / 1e9:.0f} GB. Folders of {args.base}: {sum(x['gb'] for x in top):.1f} GB; "
          f"of this runs\\ {sum(x['gb'] for x in runs):.1f} GB, and {sum(x['bulk_gb'] for x in runs):.1f} GB of that is bulk that can be made again.", "",
          "## Top level", "", "| folder | kind | GB | files | newest | bulk GB | results MB |", "|---|---|---|---|---|---|---|"]
    for x in sorted(top, key=lambda z: -z["gb"]):
        md.append(f"| {x['folder']} | {x['kind']} | {x['gb']:.2f} | {x['files']} | {x['newest']} | {x['bulk_gb']:.2f} | {x['results_mb']:.1f} |")
    md += ["", "## Runs (folders of runs\\)", "", "| folder | GB | files | newest | bulk GB | results MB | to look at |", "|---|---|---|---|---|---|---|"]
    for x in runs:
        md.append(f"| {x['folder']} | {x['gb']:.2f} | {x['files']} | {x['newest']} | {x['bulk_gb']:.2f} | {x['results_mb']:.1f} | {x['flags']} |")
    unknown = [x["folder"] for x in top if x["kind"] == "UNKNOWN"]
    unnum = [x["folder"] for x in runs if "no number" in x["flags"]]
    scratch = [x["folder"] for x in runs if "scratch?" in x["flags"]]
    overlap = [x["folder"] for x in runs if x["folder"].lower().startswith("overlap_")]
    notcoll = [x["folder"] for x in runs if "not in results/" in x["flags"]]
    md += ["", "## What to look at", ""]
    md.append(f"- Top-level folders of an unknown kind: {', '.join(unknown) or 'none'}.")
    md.append(f"- Run folders without a number ({len(unnum)}): {', '.join(unnum) or 'none'}.")
    md.append(f"- Run folders that look like scratch ({len(scratch)}): {', '.join(scratch) or 'none'}.")
    md.append(f"- Folders of the overlap test ({len(overlap)}): they belong together in one numbered run folder.")
    if collected_names is None:
        md.append("- Collected into the archive: not checked (give --repo, and run collect_results.py first).")
    else:
        md.append(f"- Run folders not found in the archive's results\\ ({len(notcoll)}): {', '.join(notcoll) or 'none'}.")
    if loose:
        md.append(f"- Loose files in runs\\ ({len(loose)}): {', '.join(loose[:15])}{' ...' if len(loose) > 15 else ''}.")
    Path(str(args.out) + ".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    print(f"\nwritten {args.out}.md and {args.out}.tsv", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
