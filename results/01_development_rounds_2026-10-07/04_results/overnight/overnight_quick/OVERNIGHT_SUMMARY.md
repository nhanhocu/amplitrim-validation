# AmpliTrim overnight validation (QUICK slices), written 2026-10-06 11:18

Margins fixed before the run: {"recovered_variants": 1, "recovered_strains": 1, "identical_points": 0.1, "extra_asvs": 2, "figaro_equivalence_points": 1.0, "stability_truncation_nt": 10, "stability_yield_points": 1.0, "per_sample_rho": 0.8}

## Steps

| step | tier | status | minutes | note |
| --- | --- | --- | --- | --- |
| mock_grid | 1 | ok | 1.1 |  |
| mock_clip250 | 1 | ok | 1.5 |  |
| figaro_mockA | 1 | skipped | 0.0 | no --figaro-script given |
| mock_dilutions | 1 | ok | 2.5 |  |
| mock_miss_trace | 3 | skipped | 0.0 | rapidfuzz is not available |
| mock_pooled | 2 | ok | 0.6 |  |
| stability | 2 | ok | 0.6 |  |
| per_sample_rank | 2 | ok | 1.4 |  |
| its_chimeras | 3 | ok | 0.6 |  |
| figaro_v1v2 | 1 | skipped | 0.0 | no --v1v2 given; no --figaro-script given |
| v1v2_fulldepth | 2 | skipped | 0.0 | no --v1v2 given |

## Verdicts against the pre-set criteria

| step | criterion | outcome | detail |
| --- | --- | --- | --- |
| mock_grid | accuracy: AmpliTrim 257/260 not inferior to the authors' 279/263 at maxEE 2,6 | NOT MET | variants +2, strains +1, reads in identical ASVs -0.33 points, ASVs outside the reference +0 |
| mock_grid | accuracy: AmpliTrim alt 268/249 not inferior to the authors' 279/263 at maxEE 2,6 | NOT MET | variants +2, strains +1, reads in identical ASVs -0.54 points, ASVs outside the reference +1 |
| mock_grid | coverage rule: no variant longer than (total - 12) nt is ever recovered | met | none recovered |
| mock_grid | coverage: E. faecalis (508 nt) recovered once the total allows it | info | 257/260: no, 268/249: no, 279/263: yes |
| mock_grid | coverage: L. reuteri (523 nt) recovered once the total allows it | info | 257/260: no, 268/249: no, 279/263: no |
| mock_clip250 | clip250: FIGARO comparison | info | skipped: no --figaro-script |
| mock_clip250 | clip250: AmpliTrim's recommendation recovers at least as many variants as no truncation (250/250) | met | AmpliTrim 11, 250/250 11 variants |
| mock_dilutions | dilutions 257/260: misses longer than the merge limit | info | 3 of 4 misses; recovered 55/59 (93%) |
| mock_pooled | pooled inference (pseudo-pooled) does not lose variants against per-sample inference | met | variants +1, strains +0, outside the reference +1 |
| stability | stability (mockA_high): recommendation does not depend on the subsample | met | truncF varies by 0 nt, truncR by 0 nt, estimated yield by 0.14 points over 2 runs |
| stability | stability (mockA_all): recommendation does not depend on the subsample | met | truncF varies by 1 nt, truncR by 1 nt, estimated yield by 0.01 points over 2 runs |
| per_sample_rank | per-sample rank agreement (mockA_all) | NOT MET | Spearman +0.54 over 23 samples (margin 0.8) |
| its_chimeras | ITS chimera discrepancy explained by the chimera settings | info | largest removal 0.0% with 'DADA2 R defaults (as used so far)' against 13.9% in the authors' pipeline |

## mock_grid: Mock A, six high-input samples: truncation x maxEE against the expected sequences

```
               setting  maxEE  limit    pass  merged  ASVs  variants  strains  identical  outside
     AmpliTrim 257/260    2,6    505   80.2%   67.0%    26     24/39    10/13     98.17%        2
 AmpliTrim alt 268/249    2,6    505   78.6%   68.9%    27     24/39    10/13     97.97%        3
       authors 279/263    2,6    530   73.0%   60.0%    24     22/39     9/13     98.50%        2
```

## mock_clip250: Mock A clipped to 2x250 (tight overlap, known truth)

```
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail | found identical extra strains
AmpliTrim (maxEE 2,6)           249/249    2,6 |     44.2% yield     82.4/44.2% |      82.4%   41.0%    40.7%    23 |  99.75%     14  0.31% |    11    99.13%    12    4/13
full250                         250/250    2,6 |                     82.1/44.3% |      82.1%   40.8%    40.6%    23 |  99.58%     14  0.51% |    11    98.96%    12    4/13
t240                            240/240    2,6 |                     84.7/37.9% |      84.7%   38.4%    38.2%    10 | 100.00%     10  0.00% |     9    99.70%     1    2/13

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
Across 3 settings, AmpliTrim's estimate minus DADA2: yield against merged share +2.1 points (range -0.5 to +3.4); filter pass +0.0 points (range +0.0 to +0.0). As a fraction of the estimated yield, DADA2's merged share is 0.95 (range 0.92 to 1.01).

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2,6) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  full250: -0.2 points (95% interval -0.2 to -0.1); better in 0 of 6 samples, worse in 6
  t240: -2.6 points (95% interval -3.8 to -1.4); better in 0 of 6 samples, worse in 6
```

## mock_dilutions: Mock A dilution series at several truncations

```
--- 257/260 (merge limit 505 nt): 55 of 59 present variants recovered (93%); 4 misses, 3 of them longer than the limit
    1e9: 35/38 variants, 11/13 strains, merged 78.5%
    1e5: 20/21 variants, 8/9 strains, merged 78.9%
```

## mock_pooled: Mock A with pooled DADA2 inference

```
             inference  merged   ASVs  variants  strains  identical  outside
  per sample (default)   67.0%     26     24/39    10/13     98.17%        2
         pseudo-pooled   72.3%     28     25/39    10/13     96.89%        3
```

## stability: Stability of the recommendation across subsample sizes

```
--- mockA_high
max pairs  every  truncF  truncR    yield   floor  seconds
     5000      1     277     240    65.2%     517        7
    10000      1     277     240    65.4%     517        9
--- mockA_all
max pairs  every  truncF  truncR    yield   floor  seconds
     5000      1     275     242    65.0%     517       10
    10000      1     274     243    65.1%     517       12
```

## per_sample_rank: Per-sample rank agreement of the yield estimate with DADA2

```
--- mockA_all at 253/264, maxEE 2,6: 23 samples; offset (estimate - DADA2) mean +5.9 points, range -0.4 to +18.8; rank correlation +0.54
```

## its_chimeras: ITS: chimera removal under different settings

```
                           chimera removal   merged  non-chimeric   removed    ASVs
         DADA2 R defaults (as used so far)    42.1%         42.1%      0.0%     101
 consensus, minFold 1.0 (q2-dada2 default)    42.1%         42.1%      0.0%     101
                       pooled, minFold 1.0    42.1%         42.1%      0.0%     101
The original authors' pipeline removed 13.9% of merged reads on these samples.
```

## Not testable with the data on hand

- An independent mock community (Zymo D6321, PRJEB67827, with Zymo's own reference sequences): no data on hand.
- V3-V4 2x250 reads (tight overlap on real data) and V4-V5 (PRJNA971391): no data on hand; mock_clip250 is an emulation, not a replacement.
- Other platforms (binned quality scores): no data on hand beyond the exactness checks already made.
- Housekeeping: run the CI workflow, push to GitHub, choose a licence, archive for a DOI, test on Windows and Linux, regenerate Figures 3 and 5 and Table 6 from the saved tables, verify the references.
