#!/usr/bin/env python
"""The screen of addendum 1, step 4: on the first 250 kB of one run, distinct quality values, insert lengths from read overlap, the best split at maxEE 2 and the
75th percentile of expected errors in each read there (a stand-in for AmpliTrim's rule). Usage: screen_check.py RUN_1.fastq.gz [RUN_1.fastq.gz ...] (each _2 file is found by name)"""
import gzip,sys,numpy as np
RC=str.maketrans('ACGTN','TGCAN')
def rd(p,n):
    out=[]
    with gzip.open(p,'rt') as f:
        while len(out)<n:
            h=f.readline()
            if not h:break
            s=f.readline().strip();f.readline();q=f.readline().strip();out.append((s,q))
    return out
def screen(r1,r2):
    ins=[];C1=[];C2=[]
    for (a,qa),(b,qb) in zip(r1,r2):
        C1.append(np.concatenate([[0],np.cumsum(10**(-(np.frombuffer(qa.encode(),np.uint8).astype(float)-33)/10))]));C2.append(np.concatenate([[0],np.cumsum(10**(-(np.frombuffer(qb.encode(),np.uint8).astype(float)-33)/10))]))
        brc=b.translate(RC)[::-1]
        for p in (120,160,200,240):
            if len(a)<p+16:continue
            j=brc.find(a[p:p+16])
            if j>=0: ins.append(len(brc)+p-j);break
    l1=int(np.median([len(x[0]) for x in r1]));l2=int(np.median([len(x[0]) for x in r2]))
    T=int(round(np.quantile(ins,.995)))+12;best=None
    for f in range(max(T-l2,50),min(l1,T-50)+1,2):
        r=T-f;e1=np.array([c[f] if len(c)>f else 99 for c in C1]);e2=np.array([c[r] if len(c)>r else 99 for c in C2]);ps=((e1<=2)&(e2<=2)).mean()
        if best is None or ps>best[2]:best=(f,r,ps,e1,e2)
    f,r,ps,e1,e2=best
    return dict(T=T,ins_med=int(np.median(ins)),found=round(len(ins)/len(r1),2),cut=(f,r),pass2=round(ps,3),p75=(round(float(np.quantile(e1,.75)),2),round(float(np.quantile(e2,.75)),2)))
for p1 in sys.argv[1:]:
    r1=rd(p1,1800);r2=rd(p1.replace('_1.fastq','_2.fastq'),1800);print(p1.split('/')[-1],screen(r1,r2))
