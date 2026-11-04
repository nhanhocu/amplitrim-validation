"""Write the commands of the minimum-overlap test (register section 27) as a Windows batch file.

    python make_overlap_commands.py --template > overlap_datasets.tsv
    python make_overlap_commands.py overlap_datasets.tsv --set mockA.ready_dir=C:\\data\\x --set mockA.reference=C:\\data\\a.fasta
    python make_overlap_commands.py overlap_datasets.tsv --out C:\\data\\runs --only mockA mockB > run_first.bat
    python make_overlap_commands.py overlap_datasets.tsv --out C:\\data\\runs --only mockA mockB --slim > run_first.bat

overlap_datasets.tsv has one line per mock community (tab-separated):
    name  ready_dir  reference  F  amplicon  maxee  pairs
  ready_dir : the folder of primer-trimmed pairs that the nights gave compare_methods.py (the "ready" folder)
  reference : the FASTA of the expected sequences of the mock
  F         : truncLenF of the released cut (mock A 273, mock B 274, D6300 V3-V4 224, D6300 V4-V5 282)
  amplicon  : the longest amplicon, that is the floor of the released cut minus 12 (508, 515, 430, 550)
  maxee     : the maxEE DADA2 was run at (2,3 / 4,8 / 2 / 2,3)
  pairs     : pairs per sample given to DADA2 (0 = all; the nights used 5000, mock A not thinned)

Two arms for every overlap k in 10 12 15 20 25:
  T  the cut is tied to k: total = amplicon + k, the forward read keeps F, DADA2 merges with minOverlap = k.
  S  the cut stays at the k = 12 cut; only minOverlap changes.

--slim (little disk space): after every run that finished, all of its files are deleted except the results that the
collector needs (compare_methods.tsv/.txt, asvs_*.fasta, track_*.tsv). Only one run is on the disk at a time.
"""
import argparse
import csv
import sys
from pathlib import Path

OVERLAPS = [10, 12, 15, 20, 25]
TEMPLATE = (
    "name\tready_dir\treference\tF\tamplicon\tmaxee\tpairs\n"
    "mockA\t<FILL IN: folder of mock A pairs>\t<FILL IN: mock A expected sequences .fasta>\t273\t508\t2,3\t0\n"
    "mockB\t<FILL IN: folder of mock B pairs>\t<FILL IN: mock B expected sequences .fasta>\t274\t515\t4,8\t5000\n"
    "d6300_V3-V4\t<FILL IN>\t<FILL IN>\t224\t430\t2\t5000\n"
    "d6300_V4-V5\t<FILL IN>\t<FILL IN>\t282\t550\t2,3\t5000\n"
)
KEEP_NAMES = ("compare_methods.tsv", "compare_methods.txt")


def read_table(path):
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    fields = list(rows[0].keys()) if rows else []
    need = {"name", "ready_dir", "reference", "F", "amplicon", "maxee", "pairs"}
    if need - set(fields):
        sys.exit(f"{path}: missing columns {sorted(need - set(fields))} (is the file tab-separated? use --set, or edit it in Notepad, not Excel)")
    return rows, fields


def read_rows(path, only=None):
    rows, _ = read_table(path)
    if only:
        unknown = [n for n in only if n not in {r["name"] for r in rows}]
        if unknown:
            sys.exit(f"{path}: no line named {unknown}; the names are {[r['name'] for r in rows]}")
    for r in rows:
        if only and r["name"] not in only:
            continue                                      # lines that are not used need not be filled in
        for key in ("ready_dir", "reference"):
            if "<FILL IN" in r[key]:
                sys.exit(f"{path}: fill in {key} for {r['name']} (use --set {r['name']}.{key}=PATH)")
            if not r[key].strip():
                sys.exit(f"{path}: {key} is empty for {r['name']}")
    return rows


def set_values(path, items):
    """Write NAME.COLUMN=VALUE items into the table, keeping it tab-separated."""
    rows, fields = read_table(path)
    for item in items:
        if "=" not in item or "." not in item.split("=", 1)[0]:
            sys.exit(f"--set {item!r}: write it as NAME.COLUMN=VALUE")
        key, value = item.split("=", 1)
        name, column = key.split(".", 1)
        hit = [r for r in rows if r["name"] == name]
        if not hit:
            sys.exit(f"--set {item!r}: no line named {name}; the names are {[r['name'] for r in rows]}")
        if column not in fields:
            sys.exit(f"--set {item!r}: no column {column}; the columns are {fields}")
        hit[0][column] = value.strip().strip('"')
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"updated {path}: {len(items)} value(s) written", file=sys.stderr)
    return 0


def slim_folder(folder):
    """Delete the bulk of a finished run folder; keep what the results need."""
    root = Path(folder)
    if not (root / "compare_methods.tsv").exists():
        sys.exit(f"{root}: no compare_methods.tsv, so the run did not finish; nothing deleted")
    freed = 0
    for f in sorted(root.rglob("*"), key=lambda x: len(x.parts), reverse=True):
        if f.is_file():
            keep = f.parent == root and (f.name in KEEP_NAMES or (f.name.startswith("asvs_") and f.suffix == ".fasta")
                                         or (f.name.startswith("track_") and f.suffix == ".tsv"))
            if not keep:
                freed += f.stat().st_size
                f.unlink()
        elif f.is_dir() and not any(f.iterdir()):
            f.rmdir()
    print(f"slimmed {root}: freed {freed / 1e6:.0f} MB", file=sys.stderr)
    return 0


def commands(rows, out, overlaps, only, slim=False):
    lines = ["@echo off", "REM Minimum-overlap test, register section 27. One DADA2 comparison per line."]
    me = Path(__file__).resolve()
    for r in rows:
        if only and r["name"] not in only:
            continue
        f, amp, ee, pairs = int(r["F"]), int(r["amplicon"]), r["maxee"], int(r["pairs"])
        r12 = amp + 12 - f
        lines.append(f"REM ---- {r['name']}: longest amplicon {amp} nt, forward {f}, maxEE {ee}")
        for k in overlaps:
            arms = [("T", amp + k - f)]                      # arm T: the cut follows k
            if k != 12:
                arms.append(("S", r12))                      # arm S: the k = 12 cut, only minOverlap changes
            for arm, rr in arms:
                tag = f"{arm.lower()}{k}"
                folder = f"{out}\\overlap_{r['name']}_{arm}_k{k}"
                line = (f'python validation\\compare_methods.py "{r["ready_dir"]}" --out "{folder}" '
                        f'--amplitrim-max-ee {ee} --min-overlap {k} --setting {tag}={f},{rr},{ee} '
                        f'--reference "{r["reference"]}" --baseline {tag}' + (f" --pairs {pairs}" if pairs else ""))
                if slim:                                     # only after a run that finished (&&)
                    line += f' && python "{me}" --slim-folder "{folder}"'
                lines.append(line)
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("table", nargs="?", type=Path)
    ap.add_argument("--out", default=r"C:\data\runs")
    ap.add_argument("--overlaps", type=int, nargs="+", default=OVERLAPS)
    ap.add_argument("--only", nargs="+", help="only these dataset names")
    ap.add_argument("--template", action="store_true", help="print a template of the table and stop")
    ap.add_argument("--set", action="append", default=[], metavar="NAME.COLUMN=VALUE", help="write a value into the table (for example mockA.ready_dir=C:\\data\\x) and stop")
    ap.add_argument("--slim", action="store_true", help="after every finished run, delete all of its files except the results")
    ap.add_argument("--slim-folder", type=Path, metavar="FOLDER", help="delete the bulk of one finished run folder and stop (used by --slim)")
    args = ap.parse_args(argv)
    if args.slim_folder:
        return slim_folder(args.slim_folder)
    if args.set:
        if not args.table:
            sys.exit("give the table to change: make_overlap_commands.py TABLE --set NAME.COLUMN=VALUE")
        return set_values(args.table, args.set)
    if args.template or not args.table:
        sys.stdout.write(TEMPLATE)
        return 0
    lines = commands(read_rows(args.table, args.only), args.out, args.overlaps, args.only, args.slim)
    print("\n".join(lines))
    print(f"REM {sum(1 for x in lines if x.startswith('python'))} runs", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
