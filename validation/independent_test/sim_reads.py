#!/usr/bin/env python
"""Simulated reads for addendum 2. Usage: sim_reads.py MODE DESIGN_DIR OUT_DIR PAIRS SEED [args]
MODE iss: args = ISS_MODEL.npz. InSilicoSeq 2.0 amplicon mode (substitutions follow the quality scores; indels from the model).
MODE tq: args = QUAL_READS_DIR ERR_DIR. Real KFS quality strings, substitutions drawn from DADA2's learned rates for that read's flow cell.
MODE nom: same arguments and the same quality strings, substitutions at exactly the rate the quality score states (10^(-Q/10)), uniform over the other three bases.
Every read name starts with its true sequence id (T..., W... twin, C... chimera)."""
import gzip, json, random, subprocess, sys, glob, os
from pathlib import Path
import numpy as np
mode, D, out, npairs, seed = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
out.mkdir(parents=True, exist_ok=True)
des = json.load(open(D / "design.json")); truth = {}; k = None
for l in open(D / "truth.fa"):
    l = l.strip()
    if l.startswith(">"): k = l[1:]
    else: truth[k] = l
RC = str.maketrans("ACGT", "TGCA"); rc = lambda s: s.translate(RC)[::-1]
def sample_seqs(si, sname, rng):
    """Composition for one sample with chimeras: 50 bimeras between abundance-weighted parents, sharing chimera_share."""
    comp = dict(des["comp"][sname]); keys = list(comp); w = np.array([comp[x] for x in keys]); w = w / w.sum()
    seqs = {x: truth[x] for x in keys}; ab = {x: comp[x] * (1 - des["chimera_share"]) for x in keys}
    nrng = np.random.default_rng(seed * 1000 + si)
    for c in range(50):
        a, b = nrng.choice(keys, 2, replace=False, p=w); sa, sb = truth[a], truth[b]
        bp = int(nrng.integers(100, min(len(sa), len(sb)) - 100)); cid = f"C{si:02d}x{c:02d}_{a}_{b}_{bp}"
        seqs[cid] = sa[:bp] + sb[bp:]; ab[cid] = des["chimera_share"] / 50
    return seqs, ab
samples = sorted(des["comp"])[:int(os.environ.get("PILOT", "999"))]
if mode == "iss":
    model = sys.argv[6]
    for si, sname in enumerate(samples):
        rng = random.Random(seed + si); seqs, ab = sample_seqs(si, sname, rng); tmp = out / f"tmp_{si}"; tmp.mkdir(exist_ok=True)
        (tmp / "g.fa").write_text("".join(f">{k}\n{v}\n" for k, v in seqs.items()))
        (tmp / "ab.txt").write_text("".join(f"{k}\t{v}\n" for k, v in ab.items()))
        subprocess.run(["iss", "generate", "--genomes", str(tmp / "g.fa"), "--abundance_file", str(tmp / "ab.txt"), "--sequence_type", "amplicon", "--model", model,
                        "--n_reads", str(2 * npairs), "--seed", str(seed + si), "--cpus", "2", "--output", str(tmp / "r"), "--quiet"], check=True)
        for r in (1, 2):
            with open(tmp / f"r_R{r}.fastq") as f, gzip.open(out / f"SIM{si+1:02d}_{r}.fastq.gz", "wt", compresslevel=3) as o:
                L = f.read().split("\n")
                for i in range(0, len(L) - 3, 4):
                    o.write(f"@{L[i][1:].split('/')[0]}\n{L[i+1]}\n+\n{L[i+3]}\n")
        subprocess.run(["rm", "-rf", str(tmp)])
elif mode in ("tq", "nom"):
    qdir, edir = Path(sys.argv[6]), Path(sys.argv[7])
    err = {}
    for f in glob.glob(str(edir / "*_eF.tsv")):
        fc = os.path.basename(f)[:-7]
        for d in ("eF", "eR"):
            P = np.zeros((4, 46, 4)); seen = set()
            for line in open(edir / f"{fc}_{d}.tsv").read().split("\n")[1:]:
                if not line: continue
                tr, q, v = line.split("\t"); q = int(q); P["ACGT".index(tr[0]), q, "ACGT".index(tr[2])] = float(v); seen.add(q)
            lo, hi = min(seen), max(seen)
            for q in range(46):
                if q not in seen: P[:, q, :] = P[:, lo if q < lo else hi, :]
            err[(fc, d)] = P / P.sum(axis=2, keepdims=True)
    pool = []
    for f1 in sorted(glob.glob(str(qdir / "*_R1.fastq.gz"))):
        with gzip.open(f1, "rt") as a, gzip.open(f1.replace("_R1.", "_R2."), "rt") as b:
            while True:
                h = a.readline()
                if not h: break
                a.readline(); a.readline(); q1 = a.readline().strip(); b.readline(); b.readline(); b.readline(); q2 = b.readline().strip()
                fc = h.split()[1].split(":")[2] if len(h.split()) > 1 and len(h.split()[1].split(":")) > 2 else h[1:].split(":")[2]
                pool.append((fc, q1, q2))
    nrng = np.random.default_rng(seed); B = np.array(list("ACGT"))
    if mode == "nom":
        NP = np.zeros((4, 46, 4))
        for q in range(46):
            pe = 10 ** (-q / 10)
            for a in range(4):
                NP[a, q, :] = pe / 3; NP[a, q, a] = 1 - pe
        err = {k: NP for k in err}
    def mutate(s, q, P):
        idx = np.array(["ACGT".index(c) if c in "ACGT" else 0 for c in s]); qa = np.array([ord(c) - 33 for c in q])
        probs = P[idx, np.minimum(qa, P.shape[1] - 1), :]; u = nrng.random(len(s))[:, None]
        new = (u > np.cumsum(probs, axis=1)).sum(axis=1); return "".join(B[np.minimum(new, 3)])
    for si, sname in enumerate(samples):
        rng = random.Random(seed + si); seqs, ab = sample_seqs(si, sname, rng); keys = list(seqs); w = np.array([ab[k] for k in keys]); w = w / w.sum()
        pick = nrng.choice(len(keys), npairs, p=w); qp = nrng.integers(0, len(pool), npairs)
        with gzip.open(out / f"SIM{si+1:02d}_1.fastq.gz", "wt", compresslevel=3) as o1, gzip.open(out / f"SIM{si+1:02d}_2.fastq.gz", "wt", compresslevel=3) as o2:
            for n, (ki, pi) in enumerate(zip(pick, qp)):
                fc, q1, q2 = pool[pi]; s = seqs[keys[ki]]; r1 = s[:len(q1)]; r2 = rc(s)[:len(q2)]
                q1, q2 = q1[:len(r1)], q2[:len(r2)]
                r1 = mutate(r1, q1, err[(fc, "eF")]); r2 = mutate(r2, q2, err[(fc, "eR")])
                h = f"{keys[ki]}_{n} 1:N:0:{fc}"
                o1.write(f"@{h}\n{r1}\n+\n{q1}\n"); o2.write(f"@{h.replace(' 1:', ' 2:')}\n{r2}\n+\n{q2}\n")
print("done", mode, len(samples), "samples")
