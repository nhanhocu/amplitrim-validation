#!/usr/bin/env python
"""Truth communities for addendum 2. Usage: sim_build.py KFS_D_SEQTAB OUT_DIR SEED
Truth sequences: the ASVs of arm D in KFS. Sample compositions: the 24 KFS sample profiles of arm D.
Near-twins: the 30 most abundant ASVs each get a variant 1, 2 or 3 substitutions away (10 each), at 10% of the parent's abundance wherever the parent occurs.
Chimeras (made at simulation time) take 4% of each sample's reads."""
import json, random, sys
from pathlib import Path
import pandas as pd
st = pd.read_csv(sys.argv[1], sep="\t"); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True); rng = random.Random(int(sys.argv[3]))
seqs = list(st.columns); ids = {s: f"T{i+1:03d}" for i, s in enumerate(seqs)}
rel = st.div(st.sum(axis=1), axis=0)
parents = rel.mean().sort_values(ascending=False).index[:30].tolist()
def hd(a, b): return sum(x != y for x, y in zip(a, b)) + abs(len(a) - len(b))
twins = {}
for k, p in enumerate(parents):
    d = 1 + k % 3
    while True:
        pos = sorted(rng.sample(range(20, len(p) - 20), d)); t = list(p)
        for i in pos: t[i] = rng.choice([b for b in "ACGT" if b != p[i]])
        t = "".join(t)
        if t not in ids and t not in twins.values() and min(hd(t, s) for s in seqs if s != p) > d: break
    twins[ids[p]] = t
seq_of = {ids[s]: s for s in seqs}; twin_ids = {}
for pid, t in twins.items():
    tid = f"W{pid[1:]}_{hd(t, seq_of[pid])}"; seq_of[tid] = t; twin_ids[tid] = pid
comp = {}
for sname, row in rel.iterrows():
    c = {ids[s]: float(v) for s, v in row.items() if v > 0}
    for tid, pid in twin_ids.items():
        if pid in c: c[tid] = 0.1 * c[pid]
    tot = sum(c.values()); comp[sname] = {k: v / tot for k, v in c.items()}
Path(out / "truth.fa").write_text("".join(f">{k}\n{v}\n" for k, v in seq_of.items()))
json.dump({"comp": comp, "twins": twin_ids, "n_truth": len(seqs), "chimera_share": 0.04}, open(out / "design.json", "w"))
print(len(seqs), "truth ASVs,", len(twin_ids), "twins,", len(comp), "samples; lengths", min(map(len, seqs)), max(map(len, seqs)))
