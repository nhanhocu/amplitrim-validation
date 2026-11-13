#!/usr/bin/env python
"""Criteria of PROTOCOL.md from arm outputs. Usage: analyze.py LABEL WORK_DIR RDP_OUT"""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
label, W, rdp = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
S = json.load(open(W/"settings.json")); ARMS = ["R","D","E","Db"]
tr = {a: pd.read_csv(W/f"{a}_track.tsv", sep="\t").set_index("sample") for a in ARMS}
st = {a: pd.read_csv(W/f"{a}_seqtab.tsv", sep="\t") for a in ARMS}
samples = sorted(set.intersection(*[set(t.index) for t in tr.values()]))
tax = {}
with open(rdp) as fh:
    for l in fh:
        p = l.rstrip("\n").split("\t"); ranks = {p[i+1]: (p[i], float(p[i+2])) for i in range(2, len(p)-2, 3)}
        g = ranks.get("genus"); tax[p[0]] = g[0] if g and g[1] >= 0.8 else "Unclassified"
seqid = json.load(open(W/"asv_ids.json"))
def genus(tab):
    g = tab.T.groupby(lambda s: tax.get(seqid.get(s), "Unclassified")).sum().T
    return g
def rel(tab): return tab.div(tab.sum(axis=1), axis=0).fillna(0)
gen = {a: rel(genus(st[a])).reindex(samples) for a in ARMS}; asv = {a: rel(st[a]).reindex(samples) for a in ARMS}
def bc(x, y):
    c = x.columns.union(y.columns); return 0.5*(x.reindex(columns=c, fill_value=0).sub(y.reindex(columns=c, fill_value=0))).abs().sum(axis=1)
def boot(v, f=np.median, n=10000):
    v = np.asarray(v, float); rng = np.random.default_rng(1); b = f(v[rng.integers(0, len(v), (n, len(v)))], axis=1); return [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]
def shannon(t):
    p = t.values; return pd.Series(-(np.where(p > 0, p*np.log(np.where(p > 0, p, 1)), 0)).sum(axis=1), index=t.index)
depth = int(min(st[a].reindex(samples).sum(axis=1).min() for a in ARMS)); dep = max(depth, 1000)
def rare(t, seed=20261106):
    rng = np.random.default_rng(seed); out = {}
    for s in samples:
        v = t.loc[s].values.astype(int)
        out[s] = int((rng.multivariate_hypergeometric(v, dep) > 0).sum()) if v.sum() >= dep else np.nan
    return pd.Series(out)
out = {"label": label, "n_samples": len(samples), "settings": {a: S[a] for a in ("R","D","E","Rb")}, "rarefaction_depth": dep, "min_nonchim_any_arm": depth}
out["arms"] = {}
for a in ARMS:
    t = tr[a].loc[samples]; out["arms"][a] = dict(pass_share=float(t.filtered.sum()/t.input.sum()), merged_share=float(t.merged.sum()/t.input.sum()), nonchim_share=float(t.nonchim.sum()/t.input.sum()), chimera_share_of_merged=float(1-t.nonchim.sum()/t.merged.sum()), asvs=int((st[a].reindex(samples).sum(axis=0) > 0).sum()), flowcells=int(t.flowcell.nunique()))
# C1, C3
for a in ("R","D","E"):
    A = out["arms"][a]; A["est_pass"] = S[a]["est_pass"]; A["est_yield"] = S[a]["est_yield"]; A["C1_diff_pts"] = 100*(S[a]["est_pass"]-A["pass_share"]); A["C1_met"] = abs(A["C1_diff_pts"]) <= 2; A["C3_diff_pts"] = 100*(S[a]["est_yield"]-A["merged_share"]); A["C3_met"] = abs(A["C3_diff_pts"]) <= 5
same_RD = S["R"]["truncF"]==S["D"]["truncF"] and S["R"]["truncR"]==S["D"]["truncR"] and S["R"]["maxEE"]==S["D"]["maxEE"]
same_ED = S["E"]["truncF"]==S["D"]["truncF"] and S["E"]["truncR"]==S["D"]["truncR"] and S["E"]["maxEE"]==S["D"]["maxEE"]
relaxed = max(S["R"]["maxEE"]) > 2
m = {a: tr[a].loc[samples].merged/tr[a].loc[samples].input for a in ARMS}
d = 100*(m["R"]-m["D"])
out["C2"] = dict(applies=relaxed, relaxed=relaxed, diff_pts_pooled=100*(out["arms"]["R"]["merged_share"]-out["arms"]["D"]["merged_share"]), mean_paired=float(d.mean()), ci=boot(d, np.mean), n_up=int((d>0).sum()), n_down=int((d<0).sum()))
out["C2"]["met"] = (out["C2"]["diff_pts_pooled"] >= 2) if relaxed else None
noise_g, noise_a = bc(gen["D"], gen["Db"]), bc(asv["D"], asv["Db"])
out["noise"] = dict(genus_bc_median=float(noise_g.median()), genus_bc_ci=boot(noise_g), asv_bc_median=float(noise_a.median()), asv_bc_ci=boot(noise_a))
per = pd.DataFrame({"noise_genus_bc": noise_g, "noise_asv_bc": noise_a})
top = gen["D"].mean().sort_values(ascending=False).head(10).index.tolist(); out["top10_D"] = {g: float(gen["D"][g].mean()) for g in top}
sh_D = shannon(asv["D"]); rich_D = rare(st["D"].reindex(samples))
for X, same in (("R", same_RD), ("E", same_ED)):
    if same: out[f"{X}_vs_D"] = dict(applies=False); continue
    g, a = bc(gen[X], gen["D"]), bc(asv[X], asv["D"]); per[f"{X}_genus_bc"] = g; per[f"{X}_asv_bc"] = a
    c = gen[X].columns.union(gen["D"].columns); dg = 100*(gen[X].reindex(columns=c, fill_value=0)-gen["D"].reindex(columns=c, fill_value=0)).abs()
    tt = {t: float(dg[t].mean()) for t in top}
    ds = shannon(asv[X])-sh_D; rich = rare(st[X].reindex(samples)); dr = 100*(rich-rich_D)/rich_D; dr = dr.dropna()
    per[f"{X}_d_shannon"] = ds; per[f"{X}_d_richness_pct"] = dr
    Dset = set(st["D"].reindex(samples).columns[st["D"].reindex(samples).sum(axis=0) > 0]); T = st[X].reindex(samples); new = [s for s in T.columns if s not in Dset]
    newshare = float(T[new].sum().sum()/T.sum().sum())
    dch = 100*(out["arms"][X]["chimera_share_of_merged"]-out["arms"]["D"]["chimera_share_of_merged"])
    out[f"{X}_vs_D"] = dict(applies=True, genus_bc_median=float(g.median()), genus_bc_ci=boot(g), asv_bc_median=float(a.median()), asv_bc_ci=boot(a), C4_met=bool(g.median() <= noise_g.median()),
        top10_abs_diff_pts=tt, C5_max=max(tt.values()), C5_met=bool(max(tt.values()) <= 1), shannon_median_diff=float(ds.median()), shannon_ci=boot(ds), richness_median_diff_pct=float(dr.median()), richness_ci=boot(dr), richness_n=int(len(dr)), C6_met=bool(abs(ds.median()) <= .10 and abs(dr.median()) <= 10),
        new_asv_read_share_pct=100*newshare, new_asvs=len(new), chimera_rise_pts=dch, C7_met=bool(100*newshare <= 2 and dch <= 2), merged_mean_paired=float((100*(m[X]-m["D"])).mean()), merged_ci=boot(100*(m[X]-m["D"]), np.mean))
tot = lambda k: S[k]["truncF"]+S[k]["truncR"]
out["C8"] = dict(a=[S["R"]["truncF"],S["R"]["truncR"],S["R"]["maxEE"]], b=[S["Rb"]["truncF"],S["Rb"]["truncR"],S["Rb"]["maxEE"]], total_diff=abs(tot("R")-tot("Rb")), same_ee=S["R"]["maxEE"]==S["Rb"]["maxEE"]); out["C8"]["met"] = out["C8"]["total_diff"]<=10 and out["C8"]["same_ee"]
per.to_csv(W/"per_sample.tsv", sep="\t"); json.dump(out, open(W/"results.json","w"), indent=1); print(json.dumps(out, indent=1))
