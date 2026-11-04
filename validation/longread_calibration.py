"""T-cal: are the expected errors of long reads calibrated?

In a mock community the sequences are known, so the number of differences between a read and the expected variant it came from is the number of errors the read really
carries. Each read is cut between its primers (cutadapt, insertions and deletions allowed, orientation corrected), its expected errors are the sum over its bases of
10^(-Q/10), and its differences are the edit distance to the nearest expected variant (the FASTA of genome_amplicons.py). The two are compared in bins of expected errors,
for each library type and for the reads that only an indel-tolerant primer search finds ("rescued": cutadapt with no indels and 2 mismatches does not find them).
A read whose nearest variant is more than 50 differences away is counted as unmatched and left out of the bins.

Gates (written in FUTURE.md on 15 October 2026, before the first run). The bins from 1 expected error upward are judged:
  T-cal-1  for each library type, in every such bin with at least 300 matched reads, the mean differences divided by the mean expected errors is between 0.5 and 2.0;
  T-cal-2  in every such bin in which two library types both have at least 300 matched reads, their ratios differ by less than a factor of 1.5;
  T-cal-3  within each library type, in every such bin in which the rescued reads and the other reads both have at least 100 matched reads, their ratios differ by less than a factor of 1.5.
A gate with no bin to judge is NOT DECIDED. Reported, not gated: the floor (the mean differences of the reads under 0.05 expected errors, which holds PCR errors, chimeras and real
divergence that no quality score can see), the unmatched share, the composition of each file by strain and its rank correlation with the expected shares, and the similarity of the
composition between library types for the same barcode pair and between replicates.

    python validation\\longread_calibration.py --expected C:\\data\\runs\\17_night7_longread\\genome_amplicons\\expected_amplicons.fasta
        --strains-table C:\\data\\runs\\17_night7_longread\\genome_amplicons\\genome_amplicons.tsv --library Monomer=C:\\...\\l4_monomer --library Kinnex=C:\\...\\sq2_kinnex_fastq
        --primer-f AGRGTTYGATYMTGGCTCAG --primer-r RGYTACCTTGTTACGACTT --out C:\\data\\runs\\18_night8\\tcal [--reads 20000] [--max-files N]

Writes tcal_bins.tsv, composition.tsv, bias.tsv and TCAL.md. Needs numpy, cutadapt and rapidfuzz.
"""

import argparse
import csv
import re
import shutil
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import longread_common as lc  # noqa: E402
import longread_filter_check as lf  # noqa: E402
from longread_describe import find_files, sample_name  # noqa: E402

EDGES = (0.0, 0.05, 0.25, 1.0, 2.0, 3.0, 5.0, 10.0, float("inf"))
LABELS = [f"{lo:g} and over" if hi == float("inf") else f"[{lo:g}, {hi:g})" for lo, hi in zip(EDGES[:-1], EDGES[1:])]
FROM_ONE = [i for i, lo in enumerate(EDGES[:-1]) if lo >= 1.0]
CAP = 50
MIN_READS = (300, 300, 100)
RATIO_LOW, RATIO_HIGH, FACTOR = 0.5, 2.0, 1.5
PAIR = re.compile(r"Fwd_\d+--Kinnex16S_Rev_\d+")


def collect_file(path: Path, work: Path, primer_f: str, primer_r: str, max_reads: int, error_rate: float, variant_seqs: list, strain_index: np.ndarray, cap: int) -> dict:
    """The reads of one file, cut between the primers, with their expected errors, their distance to the nearest expected variant and whether they were rescued."""
    wd = work / sample_name(path)
    reads = lf.subset(path, max_reads, wd / "reads.fastq.gz")
    with_indels, without = wd / "indels.fastq.gz", wd / "no_indels.fastq.gz"
    lf.run_cutadapt(reads, with_indels, primer_f, primer_r, error_rate, True)
    lf.run_cutadapt(reads, without, primer_f, primer_r, lf.NO_INDEL_MISMATCHES, False)
    found_plain = {n for n, _, _ in lc.iter_fastq(without)}
    seqs, ee, rescued = [], [], []
    for name, seq, qual in lc.iter_fastq(with_indels):
        seqs.append(seq)
        ee.append(lc.expected_errors(qual))
        rescued.append(name not in found_plain)
    dist, idx = lc.nearest(seqs, variant_seqs, cap)
    return {"name": sample_name(path), "reads": lf.count_reads(reads), "trimmed": len(seqs), "ee": np.array(ee), "dist": dist, "rescued": np.array(rescued, dtype=bool),
            "matched": dist <= cap, "strain": strain_index[idx] if len(idx) else idx}


def bin_rows(ee: np.ndarray, dist: np.ndarray, mask: np.ndarray) -> list:
    rows = []
    for i in range(len(EDGES) - 1):
        sel = mask & (ee >= EDGES[i]) & (ee < EDGES[i + 1])
        n = int(sel.sum())
        row = {"i": i, "bin": LABELS[i], "reads": n, "mean_ee": None, "mean_diff": None, "median_diff": None, "ratio": None}
        if n:
            me, md = float(ee[sel].mean()), float(dist[sel].mean())
            row.update(mean_ee=me, mean_diff=md, median_diff=float(np.median(dist[sel])), ratio=(md / me if me > 0 else None))
        rows.append(row)
    return rows


def library_stats(files: list) -> dict:
    ee = np.concatenate([f["ee"] for f in files]) if files else np.zeros(0)
    dist = np.concatenate([f["dist"] for f in files]) if files else np.zeros(0, dtype=int)
    rescued = np.concatenate([f["rescued"] for f in files]) if files else np.zeros(0, dtype=bool)
    matched = np.concatenate([f["matched"] for f in files]) if files else np.zeros(0, dtype=bool)
    low = matched & (ee < EDGES[1])
    return {"all": bin_rows(ee, dist, matched), "rescued": bin_rows(ee, dist, matched & rescued), "other": bin_rows(ee, dist, matched & ~rescued),
            "reads": int(len(ee)), "matched": int(matched.sum()), "rescued_reads": int((rescued & matched).sum()),
            "floor": float(dist[low].mean()) if low.any() else None, "floor_reads": int(low.sum())}


def _status(judged: int, failed: int) -> str:
    return "NOT DECIDED" if judged == 0 else ("NOT MET" if failed else "MET")


def evaluate(stats: dict, min_reads: tuple = MIN_READS) -> dict:
    """{gate: (status, [notes])} for T-cal-1, T-cal-2 and T-cal-3."""
    m1, m2, m3 = min_reads
    out = {}
    notes, judged, failed = [], 0, 0
    for lib, s in stats.items():
        for i in FROM_ONE:
            r = s["all"][i]
            if r["reads"] >= m1 and r["ratio"] is not None:
                ok = RATIO_LOW <= r["ratio"] <= RATIO_HIGH
                judged += 1
                failed += (not ok)
                notes.append(f"{lib}, {LABELS[i]} expected errors: differences / expected errors = {r['ratio']:.2f} ({r['reads']:,} reads): " + ("inside 0.5 to 2.0" if ok else "OUTSIDE 0.5 to 2.0"))
    out["T-cal-1"] = (_status(judged, failed), notes)
    notes, judged, failed = [], 0, 0
    for a, b in combinations(stats, 2):
        for i in FROM_ONE:
            ra, rb = stats[a]["all"][i], stats[b]["all"][i]
            if ra["reads"] >= m2 and rb["reads"] >= m2 and ra["ratio"] and rb["ratio"]:
                q = ra["ratio"] / rb["ratio"]
                ok = 1 / FACTOR < q < FACTOR
                judged += 1
                failed += (not ok)
                notes.append(f"{a} against {b}, {LABELS[i]}: ratio {ra['ratio']:.2f} against {rb['ratio']:.2f}, a factor of {max(q, 1 / q):.2f}: " + ("within 1.5" if ok else "BEYOND 1.5"))
    out["T-cal-2"] = (_status(judged, failed), notes)
    notes, judged, failed = [], 0, 0
    for lib, s in stats.items():
        for i in FROM_ONE:
            ra, ro = s["rescued"][i], s["other"][i]
            if ra["reads"] >= m3 and ro["reads"] >= m3 and ra["ratio"] and ro["ratio"]:
                q = ra["ratio"] / ro["ratio"]
                ok = 1 / FACTOR < q < FACTOR
                judged += 1
                failed += (not ok)
                notes.append(f"{lib}, {LABELS[i]}: rescued {ra['ratio']:.2f} ({ra['reads']:,} reads) against the others {ro['ratio']:.2f} ({ro['reads']:,} reads), a factor of {max(q, 1 / q):.2f}: "
                             + ("within 1.5" if ok else "BEYOND 1.5"))
    out["T-cal-3"] = (_status(judged, failed), notes)
    return out


def composition(d: dict, n_strains: int) -> np.ndarray:
    """Reads per strain among the matched reads of one file."""
    return np.bincount(d["strain"][d["matched"]], minlength=n_strains).astype(float)


def read_expected_shares(path) -> dict:
    """{strain: expected read share in percent} from the genome_amplicons.tsv written by genome_amplicons.py."""
    if not path:
        return {}
    with open(path, newline="", encoding="utf-8") as fh:
        return {r["strain"]: float(r["expected_read_share_percent"]) for r in csv.DictReader(fh, delimiter="\t") if r.get("expected_read_share_percent") not in (None, "")}


def run(libraries: dict, expected_fasta, primer_f: str, primer_r: str, out: Path, reads: int = 20000, max_files: int = 0, cap: int = CAP, error_rate: float = 0.15,
        min_reads: tuple = MIN_READS, strains_table=None, keep: bool = False, log=print) -> dict:
    variants = lc.read_fasta(expected_fasta)
    if not variants:
        raise SystemExit(f"No expected variants in {expected_fasta}")
    names, seqs = [n for n, _ in variants], [s for _, s in variants]
    strains = sorted({lc.strain_of(n) for n in names})
    strain_index = np.array([strains.index(lc.strain_of(n)) for n in names])
    work = out / "work"
    per_lib, stats, comp, order = {}, {}, {}, {}
    for lib, folder in libraries.items():
        files = lc.pick_evenly(find_files(Path(folder)), max_files)
        if not files:
            raise SystemExit(f"No FASTQ files in {folder} (library {lib})")
        data = []
        for p in files:
            d = collect_file(p, work / lib, primer_f, primer_r, reads, error_rate, seqs, strain_index, cap)
            data.append(d)
            log(f"{lib} {d['name']}: {d['reads']:,} reads, {d['trimmed']:,} cut between the primers, {int(d['matched'].sum()):,} matched, {int((d['rescued'] & d['matched']).sum()):,} rescued")
        per_lib[lib] = data
        stats[lib] = library_stats(data)
        for d in data:
            comp[(lib, d["name"])] = composition(d, len(strains))
    gates = evaluate(stats, min_reads)
    expected = read_expected_shares(strains_table)
    out.mkdir(parents=True, exist_ok=True)
    write_tables(stats, comp, strains, expected, per_lib, out)
    write_report(stats, gates, comp, strains, expected, per_lib, out, primer_f, primer_r, reads, cap, min_reads)
    if not keep:
        shutil.rmtree(work, ignore_errors=True)
    log(f"Saved: {out / 'TCAL.md'}")
    for g, (status, _) in gates.items():
        log(f"{g}: {status}")
    return {"stats": stats, "gates": gates, "composition": comp, "strains": strains}


def pooled_share(comp: dict, lib: str) -> np.ndarray:
    total = sum(v for (l, _), v in comp.items() if l == lib)
    return total / total.sum() if np.sum(total) else total


def pair_similarity(comp: dict) -> list:
    """[(barcode pair, library a, library b, Spearman)] for files that carry the same barcode pair in two library types."""
    by = {}
    for (lib, name), v in comp.items():
        m = PAIR.search(name)
        if m:
            by.setdefault(m.group(0), {})[lib] = v
    rows = []
    for key, libs in sorted(by.items()):
        for a, b in combinations(sorted(libs), 2):
            rows.append((key, a, b, lc.spearman(list(libs[a]), list(libs[b]))))
    return rows


def replicate_similarity(comp: dict) -> dict:
    """{library: mean Spearman between the compositions of its files}."""
    out = {}
    for lib in sorted({l for l, _ in comp}):
        vs = [v for (l, _), v in comp.items() if l == lib]
        rs = [lc.spearman(list(a), list(b)) for a, b in combinations(vs, 2)]
        rs = [r for r in rs if r is not None]
        out[lib] = float(np.mean(rs)) if rs else None
    return out


def write_tables(stats: dict, comp: dict, strains: list, expected: dict, per_lib: dict, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "tcal_bins.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["library", "group", "bin", "reads", "mean_expected_errors", "mean_differences", "median_differences", "ratio"])
        for lib, s in stats.items():
            for group in ("all", "rescued", "other"):
                for r in s[group]:
                    w.writerow([lib, group, r["bin"], r["reads"], r["mean_ee"], r["mean_diff"], r["median_diff"], r["ratio"]])
    with open(out / "composition.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["library", "file", "strain", "reads", "share"])
        for (lib, name), v in comp.items():
            total = v.sum()
            for s, n in zip(strains, v):
                w.writerow([lib, name, s, int(n), (n / total) if total else ""])
    with open(out / "bias.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["library", "strain", "expected_read_share_percent", "observed_read_share_percent", "observed_over_expected"])
        for lib in stats:
            obs = pooled_share(comp, lib)
            for s, o in zip(strains, obs):
                e = expected.get(s)
                w.writerow([lib, s, e if e is not None else "", 100 * o, (100 * o / e) if e else ""])


def fmt(x, digits: int = 2) -> str:
    return "-" if x is None else f"{x:.{digits}f}"


def write_report(stats: dict, gates: dict, comp: dict, strains: list, expected: dict, per_lib: dict, out: Path, primer_f: str, primer_r: str, reads: int, cap: int, min_reads: tuple) -> None:
    lines = ["# T-cal: calibration of the expected errors against the true differences", "",
             f"Primers {primer_f} and {primer_r}; the first {reads:,} reads of each file" + (" (all reads)" if not reads else "") + f"; a read whose nearest expected variant is more than {cap} differences away is unmatched. "
             f"Minimum reads for a bin to be judged: {min_reads[0]} (T-cal-1 and T-cal-2), {min_reads[1]} for both library types in T-cal-2, {min_reads[2]} per group (T-cal-3).", ""]
    for g, (status, notes) in gates.items():
        lines += [f"**Gate ({g}): {status}.**" + ("" if notes else " No bin had enough reads to be judged."), ""] + [f"- {n}" for n in notes] + ([""] if notes else [])
    lines += ["The floor is the mean number of differences of the matched reads with fewer than 0.05 expected errors: what the quality scores cannot see (PCR errors, chimeras, real divergence).", ""]
    for lib, s in stats.items():
        lines += [f"## {lib}", "",
                  f"{s['reads']:,} reads cut between the primers, {s['matched']:,} matched ({100 * s['matched'] / s['reads']:.1f}%), of which {s['rescued_reads']:,} rescued by the indel-tolerant search; "
                  f"floor {fmt(s['floor'], 3)} differences ({s['floor_reads']:,} reads).", "",
                  "| expected errors | reads | mean expected | mean differences | median | differences / expected | rescued reads | rescued ratio | other reads | other ratio |", "|---|---|---|---|---|---|---|---|---|---|"]
        for r, ra, ro in zip(s["all"], s["rescued"], s["other"]):
            lines.append(f"| {r['bin']} | {r['reads']:,} | {fmt(r['mean_ee'], 3)} | {fmt(r['mean_diff'], 3)} | {fmt(r['median_diff'], 1)} | {fmt(r['ratio'])} | {ra['reads']:,} | {fmt(ra['ratio'])} | {ro['reads']:,} | {fmt(ro['ratio'])} |")
        lines.append("")
    if expected:
        lines += ["## Composition against the expected read shares (pooled over the files of each library type)", ""]
        for lib in stats:
            obs = pooled_share(comp, lib)
            have = [(s, expected[s], 100 * o) for s, o in zip(strains, obs) if s in expected]
            rho = lc.spearman([e for _, e, _ in have], [o for _, _, o in have])
            lines += [f"**{lib}:** Spearman correlation between the expected and the observed read share over {len(have)} strains: {fmt(rho)}.", "",
                      "| strain | expected % | observed % | observed / expected |", "|---|---|---|---|"]
            for s, e, o in sorted(have, key=lambda t: -t[1]):
                lines.append(f"| {s} | {e:.3f} | {o:.3f} | {fmt(o / e if e else None)} |")
            lines.append("")
    sims = pair_similarity(comp)
    rep = replicate_similarity(comp)
    lines += ["## Similarity of the compositions", ""]
    if sims:
        lines += ["Same barcode pair in two library types (Spearman correlation of the reads per strain):", "", "| barcode pair | library a | library b | Spearman |", "|---|---|---|---|"] + [f"| {k} | {a} | {b} | {fmt(r)} |" for k, a, b, r in sims] + [""]
    lines += ["Between the files of one library type (mean Spearman): " + "; ".join(f"{l} {fmt(v)}" for l, v in rep.items()) + ".", ""]
    (out / "TCAL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_libraries(items: list) -> dict:
    libs = {}
    for it in items:
        if "=" not in it:
            raise SystemExit(f"--library needs NAME=FOLDER, not {it!r}")
        name, folder = it.split("=", 1)
        libs[name.strip()] = Path(folder.strip())
    return libs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--library", action="append", required=True, metavar="NAME=FOLDER", help="a library type and its folder of FASTQ files (repeat for each type)")
    ap.add_argument("--expected", type=Path, required=True, help="expected_amplicons.fasta from genome_amplicons.py")
    ap.add_argument("--strains-table", type=Path, help="genome_amplicons.tsv from genome_amplicons.py (for the expected read shares)")
    ap.add_argument("--primer-f", required=True)
    ap.add_argument("--primer-r", required=True)
    ap.add_argument("--out", type=Path, default=Path("tcal"))
    ap.add_argument("--reads", type=int, default=20000, help="the first N reads of each file (default 20000; 0 = all)")
    ap.add_argument("--max-files", type=int, default=0, help="at most N files per library, spread evenly (default: all)")
    ap.add_argument("--max-distance", type=int, default=CAP, help="reads farther than this from every expected variant are unmatched (default 50)")
    ap.add_argument("--error-rate", type=float, default=0.15)
    ap.add_argument("--keep", action="store_true", help="keep the intermediate files")
    ap.add_argument("--sampling", choices=["spread", "first"], default="spread", help="which reads --reads keeps: spread evenly over each file (default) or the first N (the setting of the runs up to 15 October 2026)")
    a = ap.parse_args(argv)
    lf.SAMPLING = a.sampling
    lc.check_cutadapt()
    run(parse_libraries(a.library), a.expected, a.primer_f, a.primer_r, a.out, a.reads, a.max_files, a.max_distance, a.error_rate, MIN_READS, a.strains_table, a.keep)
    return 0


if __name__ == "__main__":
    sys.exit(main())
