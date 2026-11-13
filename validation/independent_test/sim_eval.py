#!/usr/bin/env python
"""Accuracy against the known truth for addendum 2. Usage: sim_eval.py WORK_DIR DESIGN_DIR"""
import gzip, json, sys
from pathlib import Path
import numpy as np, pandas as pd
W, D = Path(sys.argv[1]), Path(sys.argv[2]); MIN_READS = 10
truth = {}; k = None
for l in open(D / "truth.fa"):
    l = l.strip()
    if l.startswith(">"): k = l[1:]
    else: truth[k] = l
seq2id = {v: k for k, v in truth.items()}
import re
CHIM = re.compile(r"^C\d+x\d+_(T\d+|W\d+_\d)_(T\d+|W\d+_\d)_(\d+)$")
def chim_seq(cid):
    a, b, bp = CHIM.match(cid).groups(); return truth[a][:int(bp)] + truth[b][int(bp):]
def origins(path):
    c = {}
    with gzip.open(path, "rt") as f:
        for i, l in enumerate(f):
            if i % 4 == 0:
                lab = l[1:].split()[0].rsplit("_", 1)[0]
                if lab.startswith("C") and chim_seq(lab) in seq2id: lab = seq2id[chim_seq(lab)]   # a bimera identical to a true sequence is that sequence
                c[lab] = c.get(lab, 0) + 1
    return c
def boot(v, f=np.median, n=10000):
    v = np.asarray(v, float); rng = np.random.default_rng(1); b = f(v[rng.integers(0, len(v), (n, len(v)))], axis=1); return [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]
res = {}; per = []
for arm, draw in (("R", "a"), ("D", "a"), ("E", "a"), ("Db", "b")):
    st = pd.read_csv(W / f"{arm}_seqtab.tsv", sep="\t")
    for s in st.index:
        org = origins(W / draw / f"{s}_R1.fastq.gz")
        true = {k: v for k, v in org.items() if not k.startswith("C")}; chims = {chim_seq(k) for k in org if k.startswith("C")}
        tot = sum(true.values()); tp = {truth[k]: v / tot for k, v in true.items()}
        row = st.loc[s]; row = row[row > 0]; n = row.sum(); inf = {q: c / n for q, c in row.items()}
        tset = [k for k, v in true.items() if k.startswith("T") and v >= MIN_READS]; wset = [k for k, v in true.items() if k.startswith("W") and v >= MIN_READS]
        found = set(row.index)
        spur = sum(c for q, c in row.items() if q not in seq2id and q not in chims) / n
        chim_left = sum(c for q, c in row.items() if q in chims) / n
        allq = set(tp) | set(inf); bc = 0.5 * sum(abs(tp.get(q, 0) - inf.get(q, 0)) for q in allq)
        per.append(dict(arm=arm, sample=s, recall_T=np.mean([truth[k] in found for k in tset]) if tset else np.nan, n_T=len(tset),
                        twins_found=sum(truth[k] in found for k in wset), twins_present=len(wset), spurious_share=spur, chimera_left_share=chim_left,
                        false_asvs=int(sum(1 for q in row.index if q not in seq2id and q not in chims)), bc_truth=bc, reads=int(n)))
per = pd.DataFrame(per); per.to_csv(W / "truth_per_sample.tsv", sep="\t", index=False)
P = {a: per[per.arm == a].set_index("sample") for a in ("R", "D", "E", "Db")}
out = {"arms": {a: dict(recall_T_median=float(P[a].recall_T.median()), twin_recovery_pooled=float(P[a].twins_found.sum() / max(P[a].twins_present.sum(), 1)),
                        twins_present=int(P[a].twins_present.sum()), spurious_median_pct=100 * float(P[a].spurious_share.median()), chimera_left_median_pct=100 * float(P[a].chimera_left_share.median()),
                        false_asvs_median=float(P[a].false_asvs.median()), bc_truth_median=float(P[a].bc_truth.median())) for a in P}}
for X in ("R", "E"):
    d_rec = 100 * (P[X].recall_T - P["D"].recall_T); d_sp = 100 * (P[X].spurious_share - P["D"].spurious_share); d_bc = P[X].bc_truth - P["D"].bc_truth
    tw = lambda df: df.twins_found / df.twins_present.replace(0, np.nan)
    d_tw = 100 * (tw(P[X]) - tw(P["D"])).dropna()
    pooled_tw = 100 * (P[X].twins_found.sum() - P["D"].twins_found.sum()) / max(P["D"].twins_present.sum(), 1)
    out[f"{X}_vs_D"] = dict(T1_recall_median_diff_pts=float(d_rec.median()), T1_ci=boot(d_rec), T1_met=bool(d_rec.median() >= -2),
        T2_spurious_median_diff_pts=float(d_sp.median()), T2_ci=boot(d_sp), T2_met=bool(d_sp.median() <= 0.5),
        T3_bc_median_diff=float(d_bc.median()), T3_ci=boot(d_bc), T3_met=bool(d_bc.median() <= 0.01),
        T4_twin_pooled_diff_pts=float(pooled_tw), T4_twin_median_diff_pts=float(d_tw.median()), T4_ci=boot(d_tw), T4_met=bool(pooled_tw >= -5))
out["H2"] = dict(E_minus_D_twin_median=out["E_vs_D"]["T4_twin_median_diff_pts"], ci=out["E_vs_D"]["T4_ci"], supported=bool(out["E_vs_D"]["T4_ci"][1] < 0))
json.dump(out, open(W / "truth_results.json", "w"), indent=1); print(json.dumps(out, indent=1))
