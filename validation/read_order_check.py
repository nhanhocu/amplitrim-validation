"""Is the order of the reads of a FASTQ file random?

The first N reads of a file are a fair sample only if the order of the reads has nothing to do with what the reads are. The Revio files of Night 9 broke that rule: in one file Escherichia coli was
0.3% of the first 20,000 reads and 14% of the first 50,000. This script splits each file into blocks of consecutive reads, takes the first `--per-block` reads of each block, cuts them between the primers
(cutadapt, insertions and deletions allowed), gives each read the strain of its nearest expected variant (the FASTA of genome_amplicons.py or the refined reference), and tests whether the strains are spread evenly
over the blocks: a chi-square test of homogeneity on the strains that make at least 1% of the sample, and Cramér's V against the V that random order would give for a table of that size.
The verdict is NOT RANDOM when the chi-square statistic is more than 4 standard deviations above its expected value and V is more than twice the V of random order; the thresholds are a convention, not a law.
The mean expected errors of each block (a drift of quality along the file) are reported as well.

    python validation\\read_order_check.py --expected C:\\...\\expected_amplicons.fasta --primer-f AGRGTTYGATYMTGGCTCAG --primer-r RGYTACCTTGTTACGACTT --out C:\\data\\runs\\order  file1.fastq.gz file2.fastq.gz

Writes ORDER_CHECK.md, order_blocks.tsv and order_summary.tsv. Needs numpy, cutadapt and rapidfuzz.
"""

import argparse
import csv
import gzip
import shutil
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import longread_common as lc  # noqa: E402
import longread_filter_check as lf  # noqa: E402
from longread_describe import open_text, sample_name  # noqa: E402

MIN_SHARE = 0.01                  # strains with at least this share of the sample take part in the test
Z_LIMIT, V_FACTOR = 4.0, 2.0      # the verdict: more than 4 standard deviations above the expected chi-square, and a V more than twice that of random order


def sample_blocks(path: Path, blocks: int, per_block: int, dest: Path) -> tuple:
    """Writes the first `per_block` reads of each of `blocks` blocks of consecutive reads to dest, renamed b<block>_<k>; returns (total reads, block size, reads taken per block)."""
    total = lf.count_reads(path)
    size = max(1, total // blocks)
    take = min(per_block, size)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open_text(path) as src, gzip.open(dest, "wt", newline="") as out:
        i = 0
        while True:
            rec = [src.readline() for _ in range(4)]
            if not rec[0]:
                break
            b, k = divmod(i, size)
            if b < blocks and k < take:
                out.write(f"@b{b}_{k}\n{rec[1].rstrip()}\n+\n{rec[3].rstrip()}\n")
            i += 1
    return total, size, take


def homogeneity(counts: np.ndarray) -> dict:
    """Chi-square test of homogeneity of a table (rows: strains, columns: blocks), with Cramér's V and the V that random order gives."""
    n = float(counts.sum())
    r, c = counts.shape
    expected = counts.sum(axis=1, keepdims=True) * counts.sum(axis=0, keepdims=True) / n
    chi2 = float(((counts - expected) ** 2 / expected).sum())
    df = (r - 1) * (c - 1)
    k = min(r - 1, c - 1)
    v = (chi2 / (n * k)) ** 0.5
    null_v = (df / (n * k)) ** 0.5
    z = (chi2 - df) / (2 * df) ** 0.5
    return {"n": int(n), "strains": r, "blocks": c, "chi2": chi2, "df": df, "v": v, "null_v": null_v, "z": z, "random": not (z > Z_LIMIT and v > V_FACTOR * null_v)}


def check_file(path: Path, names: list, seqs: list, primer_f: str, primer_r: str, work: Path, blocks: int, per_block: int, error_rate: float, cap: int) -> dict:
    strains = sorted({lc.strain_of(n) for n in names})
    index = np.array([strains.index(lc.strain_of(n)) for n in names])
    wd = work / sample_name(path)
    sample, trimmed = wd / "blocks.fastq.gz", wd / "trimmed.fastq.gz"
    total, size, take = sample_blocks(path, blocks, per_block, sample)
    lf.run_cutadapt(sample, trimmed, primer_f, primer_r, error_rate, True)
    reads, block_of, ee = [], [], []
    for name, seq, qual in lc.iter_fastq(trimmed):
        reads.append(seq)
        block_of.append(int(name[1:].split("_")[0]))
        ee.append(lc.expected_errors(qual))
    if not reads:
        raise SystemExit(f"No read of {path.name} has both primers.")
    dist, idx = lc.nearest(reads, seqs, cap)
    keep = dist <= cap
    table = np.zeros((len(strains), blocks))
    mean_ee = np.full(blocks, np.nan)
    block_of, ee = np.array(block_of), np.array(ee)
    for b in range(blocks):
        sel = block_of == b
        if sel.any():
            mean_ee[b] = ee[sel].mean()
        for s in index[idx[keep & sel]]:
            table[s, b] += 1
    pooled = table.sum(axis=1) / max(1.0, table.sum())
    used = [i for i in range(len(strains)) if pooled[i] >= MIN_SHARE]
    cols = [b for b in range(blocks) if table[:, b].sum() > 0]
    stats = homogeneity(table[np.ix_(used, cols)]) if len(used) >= 2 and len(cols) >= 2 else None
    return {"file": sample_name(path), "total": total, "block_size": size, "per_block": take, "strains": strains, "table": table, "pooled": pooled, "mean_ee": mean_ee, "stats": stats}


def run(files: list, expected_fasta, primer_f: str, primer_r: str, out: Path, blocks: int = 10, per_block: int = 400, cap: int = 50, error_rate: float = 0.15, keep: bool = False, log=print) -> list:
    variants = lc.read_fasta(expected_fasta)
    if not variants:
        raise SystemExit(f"No expected variants in {expected_fasta}")
    names, seqs = [n for n, _ in variants], [s for _, s in variants]
    work = out / "work"
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for p in files:
        r = check_file(Path(p), names, seqs, primer_f, primer_r, work, blocks, per_block, error_rate, cap)
        results.append(r)
        s = r["stats"]
        log(f"{r['file']}: {r['total']:,} reads, {blocks} blocks of {r['block_size']:,}, {r['per_block']} reads taken from each; " + ("not enough strains or blocks to test" if s is None else
            f"chi-square {s['chi2']:.0f} on {s['df']} degrees of freedom, V {s['v']:.3f} against {s['null_v']:.3f} for random order: " + ("consistent with random order" if s["random"] else "NOT RANDOM")))
    write_outputs(results, out, blocks)
    if not keep:
        shutil.rmtree(work, ignore_errors=True)
    log(f"Saved: {out / 'ORDER_CHECK.md'}")
    return results


def write_outputs(results: list, out: Path, blocks: int) -> None:
    with open(out / "order_summary.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["file", "reads", "block_size", "reads_per_block", "strains_tested", "chi2", "df", "v", "v_random_order", "z", "verdict"])
        for r in results:
            s = r["stats"]
            w.writerow([r["file"], r["total"], r["block_size"], r["per_block"]] + (["", "", "", "", "", "", "not tested"] if s is None else [s["strains"], round(s["chi2"], 2), s["df"], round(s["v"], 4), round(s["null_v"], 4), round(s["z"], 2), "random" if s["random"] else "NOT RANDOM"]))
    with open(out / "order_blocks.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["file", "block", "reads_assigned", "mean_expected_errors"] + [f"share_{s}" for s in results[0]["strains"]])
        for r in results:
            for b in range(blocks):
                col = r["table"][:, b]
                w.writerow([r["file"], b + 1, int(col.sum()), "" if np.isnan(r["mean_ee"][b]) else round(float(r["mean_ee"][b]), 3)] + [round(float(x / col.sum()), 5) if col.sum() else "" for x in col])
    lines = ["# Is the order of the reads random?", "",
             "Each file is split into blocks of consecutive reads; the first reads of each block are cut between the primers and given the strain of their nearest expected variant. "
             f"A chi-square test of homogeneity on the strains with at least {100 * MIN_SHARE:.0f}% of the sample asks whether the strains are spread evenly over the blocks; V is Cramér's V, and 'V for random order' is what a table of that size gives by chance. "
             f"NOT RANDOM: the statistic is more than {Z_LIMIT:g} standard deviations above its expected value and V is more than {V_FACTOR:g} times that of random order.", ""]
    for r in results:
        s = r["stats"]
        lines += [f"## {r['file']}", "", f"{r['total']:,} reads; {blocks} blocks of {r['block_size']:,} reads; the first {r['per_block']} reads of each block."]
        lines.append("Not enough strains or blocks to test." if s is None else
                     f"Chi-square {s['chi2']:.0f} on {s['df']} degrees of freedom (z {s['z']:.1f}); V {s['v']:.3f} against {s['null_v']:.3f} for random order; **" + ("consistent with random order" if r["stats"]["random"] else "NOT RANDOM") + "**.")
        top = [i for i in np.argsort(-r["pooled"])[:6] if r["pooled"][i] > 0]
        lines += ["", "Share of the reads of each block (%) for the six most abundant strains, and the mean expected errors:", "",
                  "| block | reads | " + " | ".join(r["strains"][i].replace("_ATCC", " ").replace("_", " ")[:24] for i in top) + " | mean expected errors |", "|---|---|" + "---|" * (len(top) + 1)]
        for b in range(blocks):
            col = r["table"][:, b]
            n = col.sum()
            lines.append(f"| {b + 1} | {int(n)} | " + " | ".join(f"{100 * col[i] / n:.1f}" if n else "-" for i in top) + f" | {'-' if np.isnan(r['mean_ee'][b]) else format(r['mean_ee'][b], '.2f')} |")
        lines.append("")
    (out / "ORDER_CHECK.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="+", type=Path, help="FASTQ files (single-end, plain or gzipped)")
    ap.add_argument("--expected", type=Path, required=True, help="the FASTA of the expected variants (names STRAIN_vN|STRAIN|N_copies)")
    ap.add_argument("--primer-f", required=True)
    ap.add_argument("--primer-r", required=True)
    ap.add_argument("--out", type=Path, default=Path("order_check"))
    ap.add_argument("--blocks", type=int, default=10, help="blocks of consecutive reads per file (default 10)")
    ap.add_argument("--per-block", type=int, default=400, help="reads taken from the start of each block (default 400)")
    ap.add_argument("--error-rate", type=float, default=0.15)
    ap.add_argument("--keep", action="store_true", help="keep the intermediate files")
    a = ap.parse_args(argv)
    lc.check_cutadapt()
    run(a.files, a.expected, a.primer_f, a.primer_r, a.out, a.blocks, a.per_block, error_rate=a.error_rate, keep=a.keep)
    return 0


if __name__ == "__main__":
    sys.exit(main())
