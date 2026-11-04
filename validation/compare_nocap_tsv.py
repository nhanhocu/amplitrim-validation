"""Compare two nocap_check.tsv files: which datasets does the second package recommend differently?

    python compare_nocap_tsv.py OLD\\nocap_check.tsv NEW\\nocap_check.tsv

Prints one line per dataset: "same" when the cut (forward, reverse), the maxEE and the floor are identical, and the
differences when they are not. The exit code is 0 when every dataset is the same and 1 otherwise.
"""
import csv
import sys

KEYS = ["released_truncF", "released_truncR", "released_maxEE", "floor", "floor_only_F", "floor_only_R"]


def read(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return {row["dataset"]: row for row in csv.DictReader(fh, delimiter="\t")}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2:
        sys.exit(__doc__)
    old, new = read(argv[0]), read(argv[1])
    bad = 0
    for name in sorted(set(old) | set(new)):
        if name not in old or name not in new:
            print(f"{name}: only in {'the old' if name in old else 'the new'} file")
            bad += 1
            continue
        diffs = [f"{k}: {old[name].get(k, '')} -> {new[name].get(k, '')}" for k in KEYS if old[name].get(k, "") != new[name].get(k, "")]
        if diffs:
            bad += 1
            print(f"{name}: DIFFERENT ({'; '.join(diffs)})")
        else:
            cut = f"{old[name].get('released_truncF', '')}/{old[name].get('released_truncR', '')}, maxEE {old[name].get('released_maxEE', '')}"
            print(f"{name}: same ({cut})")
    print(f"\n{len(set(old) | set(new)) - bad} of {len(set(old) | set(new))} datasets identical")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
