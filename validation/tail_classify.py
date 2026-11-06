#!/usr/bin/env python
"""What are the longest amplicons of a dataset? (register section 28, step `tail`; descriptive, no criterion)

  python validation/tail_classify.py READY --silva SILVA_SSU_NR99.fasta --out DIR [--top-share 0.01] [--min-len N] [--per-sample 5000] [--threads 4]

READY is a folder of primer-free pairs named <sample>_R1.fastq.gz and <sample>_R2.fastq.gz (the `ready` folder of real_data.py).
The pairs are thinned evenly (at most --per-sample per sample), merged with vsearch (minimum overlap 12, up to 10 differences, staggered pairs allowed:
the merge AmpliTrim uses for the amplicon lengths), and the longest --top-share of the merged sequences (or those of at least --min-len nt) are
searched against SILVA with vsearch (identity 0.6 or more, best hit). A control of the same size, with lengths within 5 nt of the median, is searched
the same way, so that a poor match of the long sequences can be told from a SILVA search that does not work on this dataset at all.

The domain of the best hit is the first field of the SILVA taxonomy (Bacteria, Archaea, Eukaryota). Writes tail_summary.md and tail_summary.tsv in --out.
The question it answers: are the long amplicons of D6300 V4-V5 (about 1% of them, 550 nt against a median of 374) 16S of bacteria or 18S of eukaryotes?
"""
import argparse
import csv
import gzip
import shutil
import statistics
import subprocess
import sys
from collections import Counter
from pathlib import Path


def find_pairs(folder):
    """[(sample, R1, R2)] for every <sample>_R1.fastq.gz that has its _R2.fastq.gz."""
    out = []
    for r1 in sorted(Path(folder).glob("*_R1.fastq.gz")):
        r2 = r1.with_name(r1.name[:-len("_R1.fastq.gz")] + "_R2.fastq.gz")
        if r2.is_file():
            out.append((r1.name[:-len("_R1.fastq.gz")], r1, r2))
    return out


def read_fastq(path):
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt") as fh:
        while True:
            head = fh.readline()
            if not head:
                return
            seq = fh.readline().rstrip("\n")
            fh.readline()
            qual = fh.readline().rstrip("\n")
            yield head.rstrip("\n"), seq, qual


def thin_pairs(pairs, per_sample, out_r1, out_r2):
    """Write at most `per_sample` evenly spaced pairs of every sample to two plain FASTQ files; names start with the sample. Returns the number of pairs."""
    total = 0
    with open(out_r1, "w", newline="\n") as o1, open(out_r2, "w", newline="\n") as o2:
        for sample, r1, r2 in pairs:
            n = sum(1 for _ in read_fastq(r1))
            step = max(1, n // per_sample) if per_sample else 1
            kept = 0
            for i, (a, b) in enumerate(zip(read_fastq(r1), read_fastq(r2))):
                if i % step or (per_sample and kept >= per_sample):
                    continue
                name = f"{sample}_{i}"
                o1.write(f"@{name}\n{a[1]}\n+\n{a[2]}\n")
                o2.write(f"@{name}\n{b[1]}\n+\n{b[2]}\n")
                kept += 1
            total += kept
    return total


def run(cmd):
    p = subprocess.run([str(c) for c in cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    if p.returncode:
        raise RuntimeError(f"{' '.join(str(c) for c in cmd[:3])} ... failed ({p.returncode}): {p.stdout[-600:]}")
    return p.stdout


def merged_sequences(fq):
    return [(h[1:].split()[0], s) for h, s, _ in read_fastq(fq)]


def choose(seqs, top_share=0.01, min_len=None):
    """(long, control, threshold): the longest share (or the sequences of at least min_len nt) and an equal number around the median length."""
    if not seqs:
        return [], [], 0
    lengths = sorted(len(s) for _, s in seqs)
    if min_len:
        thr = min_len
    else:
        k = max(1, int(round(len(lengths) * top_share)))
        thr = lengths[-k]
    long_ = [x for x in seqs if len(x[1]) >= thr]
    med = statistics.median(lengths)
    near = [x for x in seqs if abs(len(x[1]) - med) <= 5]
    step = max(1, len(near) // max(1, len(long_)))
    control = near[::step][:len(long_)]
    return long_, control, thr


def write_fasta(path, seqs):
    with open(path, "w", newline="\n") as fh:
        for name, s in seqs:
            fh.write(f">{name}\n{s}\n")


def domain_of(label):
    """SILVA headers read '<accession> Bacteria;Firmicutes;...'; vsearch keeps the whole label with --notrunclabels."""
    parts = label.split(" ", 1)
    return parts[1].split(";")[0].strip() if len(parts) > 1 and parts[1] else "unknown"


def summarise_hits(hits_tsv, n_queries):
    """hits_tsv has query, identity (percent), target label per line. Returns (domain counts including 'no hit', median identity)."""
    domains, ids = Counter(), []
    if Path(hits_tsv).is_file():
        with open(hits_tsv, encoding="utf-8") as fh:
            for row in csv.reader(fh, delimiter="\t"):
                if len(row) < 3:
                    continue
                domains[domain_of(row[2])] += 1
                ids.append(float(row[1]))
    hit = sum(domains.values())
    if n_queries > hit:
        domains["no hit"] = n_queries - hit
    return domains, (statistics.median(ids) if ids else None)


def classify(vsearch, fasta, silva, hits, threads):
    run([vsearch, "--usearch_global", fasta, "--db", silva, "--id", "0.6", "--maxaccepts", "1", "--maxrejects", "64", "--strand", "both",
         "--userout", hits, "--userfields", "query+id+target", "--notrunclabels", "--threads", str(threads), "--quiet"])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("reads", type=Path)
    ap.add_argument("--silva", type=Path, required=True, help="a SILVA SSU Ref NR99 FASTA (not gzipped) with the taxonomy in the headers")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--per-sample", type=int, default=5000)
    ap.add_argument("--top-share", type=float, default=0.01, help="the longest share of the merged sequences to classify (default 0.01)")
    ap.add_argument("--min-len", type=int, help="classify the sequences of at least this length instead")
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--vsearch", default="vsearch")
    ap.add_argument("--keep-files", action="store_true", help="keep the thinned reads and the merged reads (large) in --out")
    a = ap.parse_args(argv)
    if shutil.which(a.vsearch) is None:
        raise SystemExit(f"{a.vsearch} was not found on PATH")
    if not a.silva.is_file():
        raise SystemExit(f"{a.silva} does not exist")
    pairs = find_pairs(a.reads)
    if not pairs:
        raise SystemExit(f"no <sample>_R1.fastq.gz / _R2.fastq.gz pairs in {a.reads}")
    a.out.mkdir(parents=True, exist_ok=True)
    r1, r2, merged = a.out / "thin_R1.fq", a.out / "thin_R2.fq", a.out / "merged.fq"
    n = thin_pairs(pairs, a.per_sample, r1, r2)
    run([a.vsearch, "--fastq_mergepairs", r1, "--reverse", r2, "--fastq_minovlen", "12", "--fastq_maxdiffs", "10", "--fastq_allowmergestagger",
         "--fastq_minmergelen", "50", "--fastqout", merged, "--threads", str(a.threads), "--quiet"])
    seqs = merged_sequences(merged)
    long_, control, thr = choose(seqs, a.top_share, a.min_len)
    if not long_:
        raise SystemExit("no merged sequences: nothing to classify")
    lengths = sorted(len(s) for _, s in seqs)
    write_fasta(a.out / "long.fa", long_)
    write_fasta(a.out / "control.fa", control)
    classify(a.vsearch, a.out / "long.fa", a.silva, a.out / "long_hits.tsv", a.threads)
    classify(a.vsearch, a.out / "control.fa", a.silva, a.out / "control_hits.tsv", a.threads)
    rows = []
    for label, group, hits in (("long", long_, a.out / "long_hits.tsv"), ("control", control, a.out / "control_hits.tsv")):
        doms, med_id = summarise_hits(hits, len(group))
        for d, k in sorted(doms.items(), key=lambda x: -x[1]):
            rows.append({"group": label, "domain": d, "n": k, "share": k / len(group), "median_identity": med_id})
    with open(a.out / "tail_summary.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["group", "domain", "n", "share", "median_identity"], delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    L = [f"# The longest amplicons of {a.reads.name}", "",
         f"{n} pairs (at most {a.per_sample} per sample) gave {len(seqs)} merged sequences; lengths: median {statistics.median(lengths):.0f}, longest {lengths[-1]}.",
         f"Classified: the {len(long_)} sequences of at least {thr} nt ({'--min-len' if a.min_len else f'the longest {a.top_share:.1%}'}), against a control of {len(control)} sequences within 5 nt of the median.", "",
         "| Group | Best hit in SILVA | n | share | median identity (%) |", "| --- | --- | --- | --- | --- |"]
    for r in rows:
        mi = "-" if r["median_identity"] is None else f"{r['median_identity']:.1f}"
        L.append(f"| {r['group']} | {r['domain']} | {r['n']} | {r['share']:.1%} | {mi} |")
    L += ["", "Read it as: if the long group is mostly Eukaryota while the control is Bacteria, the long amplicons are 18S of eukaryotes amplified by the same primers; if both are Bacteria,",
          "they are long 16S. A long group with mostly 'no hit' and a control with hits says the long sequences are not in SILVA (or are not rRNA); if the control has no hits either,",
          "the search does not work on this dataset (check the SILVA file and the identity threshold)."]
    (a.out / "tail_summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    if not a.keep_files:                                            # the thinned and merged reads are large and are not results
        for big in (r1, r2, merged):
            big.unlink(missing_ok=True)
    print("\n".join(L))
    print(f"\nSaved: {a.out / 'tail_summary.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
