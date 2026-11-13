#!/usr/bin/env python
"""Quality check, primer step and two disjoint draws per sample. Usage: prepare.py LABEL RAW_DIR OUT_DIR N_PAIRS"""
import gzip, json, random, re, subprocess, sys, zlib
from pathlib import Path
label, raw, out, npairs = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4])
PRIMERS = {"KFS": ("CCTACGGGNGGCWGCAG", "GACTACHVGGGTATCTAATCC"), "HDP": ("CCTACGGGNGGCWGCAG", "GACTACHVGGGTATCTAATCC"), "CBGS": ("CCTACGGGNGGCWGCAG", "TACNVGGGTATCTAATCC"), "NIG": ("AGMGTTYGATYMTGGCTCAG", "GCTGCCTCCCGTAGGAGT"), "SMOKE": None}
IUPAC = dict(A="A",C="C",G="G",T="T",N="[ACGT]",W="[AT]",M="[AC]",Y="[CT]",V="[ACG]",H="[ACT]")
def rx(p): return re.compile("".join(IUPAC[c] for c in p))
def recs(path):
    """Complete FASTQ records only. A truncated gzip (partial download) ends the stream quietly, and an incomplete last record is dropped."""
    fh = gzip.open(path, "rt")
    try:
        while True:
            try:
                h = fh.readline(); s = fh.readline(); p = fh.readline(); q = fh.readline()
            except (EOFError, OSError, zlib.error):
                return
            if not h or not q.endswith("\n") or len(q) != len(s) or not h.startswith("@"):
                return
            yield h, s, p, q
    finally:
        try: fh.close()
        except Exception: pass
out.mkdir(parents=True, exist_ok=True); (out/"a").mkdir(exist_ok=True); (out/"b").mkdir(exist_ok=True); (out/"trim").mkdir(exist_ok=True)
rows = []
for r1 in sorted(raw.glob("*_1.fastq.gz")):
    run = r1.name.split("_")[0]; r2 = raw/f"{run}_2.fastq.gz"
    q = set(); n = 0; flow = None; lens = {}; f_hit = r_hit = 0
    pr = PRIMERS.get(label)
    fp = rx(pr[0]) if pr else None; rp = rx(pr[1]) if pr else None
    for (h1, s1, _, q1), (h2, s2, _, q2) in zip(recs(r1), recs(r2)):
        n += 1
        if n <= 20000: q.update(q1.strip()); q.update(q2.strip())
        if flow is None:
            m = h1.split()[1].split(":") if len(h1.split()) > 1 else []
            flow = m[2] if len(m) > 2 else "NA"
        lens[len(s1)-1] = lens.get(len(s1)-1, 0) + 1
        if pr:
            if fp.match(s1): f_hit += 1
            if rp.match(s2): r_hit += 1
    row = dict(run=run, pairs_raw=n, distinct_q=len(q), flowcell=flow, read_len=max(lens, key=lens.get), f_primer=f_hit/max(n,1), r_primer=r_hit/max(n,1))
    rows.append(row)
    rep = out/"repaired"; rep.mkdir(exist_ok=True)
    s1, s2 = rep/f"{run}_1.fastq.gz", rep/f"{run}_2.fastq.gz"; kept = 0; bad_ids = 0
    with gzip.open(s1, "wt", compresslevel=3) as o1, gzip.open(s2, "wt", compresslevel=3) as o2:
        for x, y in zip(recs(r1), recs(r2)):
            if re.sub(r"/[12]$", "", x[0].split()[0]) != re.sub(r"/[12]$", "", y[0].split()[0]): bad_ids += 1; break
            o1.write("".join(x)); o2.write("".join(y)); kept += 1
    row["pairs_complete"] = kept; row["id_mismatch_stop"] = bad_ids
    r1, r2 = s1, s2
    src1, src2 = r1, r2
    if label in ("CBGS", "KFS", "HDP"):
        t1, t2 = out/"trim"/f"{run}_R1.fastq.gz", out/"trim"/f"{run}_R2.fastq.gz"
        subprocess.run(["cutadapt","-j","2","-e","0.1","--discard-untrimmed","-g","^"+pr[0],"-G","^"+pr[1],"-o",str(t1),"-p",str(t2),str(r1),str(r2)],check=True,stdout=subprocess.DEVNULL)
        src1, src2 = t1, t2
    pairs = list(zip(recs(src1), recs(src2)))
    row["pairs_ready"] = len(pairs)
    rng = random.Random(f"20261106-{run}")
    idx = list(range(len(pairs))); rng.shuffle(idx)
    draws = {"a": sorted(idx[:npairs]), "b": sorted(idx[npairs:2*npairs])}
    row["draw_a"], row["draw_b"] = len(draws["a"]), len(draws["b"])
    for d, ii in draws.items():
        with gzip.open(out/d/f"{run}_R1.fastq.gz","wt",compresslevel=3) as a, gzip.open(out/d/f"{run}_R2.fastq.gz","wt",compresslevel=3) as b:
            for i in ii:
                a.write("".join(pairs[i][0])); b.write("".join(pairs[i][1]))
    print(json.dumps(row), flush=True)
json.dump(rows, open(out/"prepare.json","w"), indent=1)
