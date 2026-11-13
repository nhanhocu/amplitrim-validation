#!/usr/bin/env python
"""Summarise the output folder of raw_merge_refused.R. Usage: raw_merge_summary.py OUT_DIR

1. How many read pairs vsearch merges, tolerant and strict, among the pairs DADA2 refused (by the class of their denoised overlap and by whether
   both halves merged elsewhere) and among the pairs DADA2 merged (the control).
2. What the tolerant vsearch merges of each set are, per sample, against that sample's merged DADA2 sequences (merged_asvs.tsv):
   - nearest sequence: vsearch --usearch_global at 90% identity or more, counting differences (mismatches plus gap positions);
   - chimera: vsearch --uchime_ref with the sample's merged sequences as the reference.
Writes OUT_DIR/summary.tsv and OUT_DIR/summary.md."""
import collections, re, subprocess, sys, tempfile
from pathlib import Path
import pandas as pd

out = Path(sys.argv[1])


def names_fastq(p):
    with open(p) as fh:
        return [line[1:].split()[0] for i, line in enumerate(fh) if i % 4 == 0]


def fasta(p):
    recs, name, seq = [], None, []
    with open(p) as fh:
        for line in fh:
            line = line.rstrip()
            if line.startswith(">"):
                if name is not None:
                    recs.append((name, "".join(seq)))
                name, seq = line[1:].split()[0], []
            else:
                seq.append(line)
    if name is not None:
        recs.append((name, "".join(seq)))
    return recs


def tag(n):
    cls = re.search(r";cls=(\w+)", n)
    both = re.search(r";both=(\d)", n)
    return (cls.group(1) if cls else "merged", both.group(1) if both else "-")


rows = []
for w in ("refused", "merged"):
    allp = collections.Counter(tag(n) for n in names_fastq(out / f"{w}_R1.fastq"))
    for setting in ("tolerant", "strict"):
        got = collections.Counter(tag(n) for n, _ in fasta(out / f"{w}.{setting}.merged.fasta"))
        for key, n in sorted(allp.items()):
            rows.append({"set": w, "class": key[0], "both_halves_merge_elsewhere": key[1], "setting": setting, "pairs": n, "vsearch_merged": got[key],
                         "share": round(got[key] / n, 3)})
        tot = sum(allp.values())
        rows.append({"set": w, "class": "all", "both_halves_merge_elsewhere": "all", "setting": setting, "pairs": tot, "vsearch_merged": sum(got.values()),
                     "share": round(sum(got.values()) / tot, 3)})
merge_tab = pd.DataFrame(rows)

asv = pd.read_csv(out / "merged_asvs.tsv", sep="\t")
what = []
with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    for w in ("refused", "merged"):
        recs = fasta(out / f"{w}.tolerant.merged.fasta")
        by_sample = collections.defaultdict(list)
        for n, s in recs:
            by_sample[n.split("_")[0]].append((n, s))
        for sample, rs in by_sample.items():
            ref = asv[asv["sample"] == sample]
            if ref.empty:
                continue
            db = td / "db.fa"
            db.write_text("".join(f">a{i};size={int(a)}\n{s}\n" for i, (s, a) in enumerate(zip(ref["sequence"], ref["abundance"]))))
            uniq = collections.Counter(s for _, s in rs)
            q = td / "q.fa"
            q.write_text("".join(f">q{i};size={c}\n{s}\n" for i, (s, c) in enumerate(uniq.items())))
            seqs = {f"q{i}": s for i, s in enumerate(uniq)}
            size = {f"q{i}": c for i, c in enumerate(uniq.values())}
            hits = td / "hits.tsv"
            subprocess.run(["vsearch", "--usearch_global", str(q), "--db", str(db), "--id", "0.9", "--maxaccepts", "0", "--maxrejects", "0",
                            "--userout", str(hits), "--userfields", "query+mism+gaps+ql+tl", "--output_no_hits", "--threads", "2", "--quiet"], check=True)
            dist = {}
            for line in hits.read_text().splitlines():
                qn, mism, gaps, ql, tl = line.split("\t")
                qn = qn.split(";")[0]
                if tl in ("0", "*"):
                    dist.setdefault(qn, None)
                else:                                                  # all hits are written: keep the closest
                    d = int(mism) + int(gaps)
                    dist[qn] = d if dist.get(qn) is None else min(dist[qn], d)
            chim = td / "chim.fa"
            subprocess.run(["vsearch", "--uchime_ref", str(q), "--db", str(db), "--chimeras", str(chim), "--threads", "2", "--quiet"], check=True)
            chimeric = {n.split(";")[0] for n, _ in fasta(chim)}
            for qn in seqs:
                d = dist.get(qn)
                what.append({"set": w, "sample": sample, "reads": size[qn], "nearest_differences": d, "chimera": qn in chimeric})
w = pd.DataFrame(what)


def bucket(d):
    if d is None or pd.isna(d):
        return "under 90% identity"
    d = int(d)
    return "0" if d == 0 else "1 to 3" if d <= 3 else "4 to 10" if d <= 10 else "11 or more"


w["nearest"] = w["nearest_differences"].map(bucket)
nearest = (w.groupby(["set", "nearest"])["reads"].sum() / w.groupby("set")["reads"].sum()).round(3).unstack(0)
chim = (w[w["chimera"]].groupby("set")["reads"].sum() / w.groupby("set")["reads"].sum()).round(3)
chim_far = (w[w["chimera"] & w["nearest"].isin(["4 to 10", "11 or more", "under 90% identity"])].groupby("set")["reads"].sum()
            / w.groupby("set")["reads"].sum()).round(3)
merge_tab.to_csv(out / "summary.tsv", sep="\t", index=False)
w.to_csv(out / "merged_reads_vs_asvs.tsv", sep="\t", index=False)
md = ["## vsearch on the filtered reads", "", merge_tab.to_markdown(index=False), "",
      "## Tolerant vsearch merges against the sample's merged DADA2 sequences (share of merged reads)", "", nearest.to_markdown(), "",
      f"Chimera by uchime_ref: refused {chim.get('refused', 0)}, merged {chim.get('merged', 0)}. "
      f"Chimera and 4 or more differences from every merged sequence: refused {chim_far.get('refused', 0)}, merged {chim_far.get('merged', 0)}."]
(out / "summary.md").write_text("\n".join(md) + "\n")
print("\n".join(md))
