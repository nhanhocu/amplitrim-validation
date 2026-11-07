# AmpliTrim overnight validation (full), written 2026-10-07 02:05

Margins fixed before the run: {"recovered_variants": 1, "recovered_strains": 1, "identical_points": 0.1, "extra_asvs": 2, "figaro_equivalence_points": 1.0, "stability_truncation_nt": 10, "stability_yield_points": 1.0, "per_sample_rho": 0.8, "landscape_regret_points": 1.0}

## Steps

| step | tier | status | minutes | note |
| --- | --- | --- | --- | --- |
| mock_grid | 1 | ok | 28.2 |  |
| asv_classify | 1 | ok | 0.1 |  |
| mock_clip250 | 1 | ok | 8.1 |  |
| figaro_mockA | 1 | ok | 5.1 |  |
| mock_dilutions | 1 | ok | 20.2 |  |
| coverage_levels | 1 | ok | 46.9 |  |
| landscape | 1 | ok | 51.0 |  |
| mock_miss_trace | 3 | ok | 3.0 |  |
| mock_pooled | 2 | ok | 8.9 |  |
| stability | 2 | ok | 24.8 |  |
| per_sample_rank | 2 | ok | 16.4 |  |
| its_chimeras | 3 | ok | 99.2 |  |
| figaro_v1v2 | 1 | ok | 11.4 |  |
| v1v2_fulldepth | 2 | ok | 37.6 |  |
| battery | 1 | ok | 29.9 |  |
| extra_datasets | 1 | ok | 21.6 |  |

## Verdicts against the pre-set criteria

| step | criterion | outcome | detail |
| --- | --- | --- | --- |
| mock_grid | accuracy: AmpliTrim 257/260 not inferior to the authors' 279/263 at maxEE 2,6 | NOT MET | variants -2, strains -2, reads in identical ASVs -0.08 points, ASVs outside the reference +8 |
| mock_grid | accuracy: AmpliTrim alt 268/249 not inferior to the authors' 279/263 at maxEE 2,6 | NOT MET | variants -2, strains -2, reads in identical ASVs -0.09 points, ASVs outside the reference +13 |
| mock_grid | accuracy: AmpliTrim 257/260 not inferior to the authors' 279/263 at maxEE 3,5 | NOT MET | variants -2, strains -2, reads in identical ASVs -0.08 points, ASVs outside the reference +8 |
| mock_grid | accuracy: AmpliTrim alt 268/249 not inferior to the authors' 279/263 at maxEE 3,5 | NOT MET | variants -2, strains -2, reads in identical ASVs -0.02 points, ASVs outside the reference +12 |
| mock_grid | coverage rule: no variant longer than (total - 12) nt is ever recovered | met | none recovered |
| mock_grid | coverage: E. faecalis (508 nt) recovered once the total allows it | info | 257/260: no, 268/249: no, 279/263: yes, 257/267: yes, 265/270: yes |
| mock_grid | coverage: L. reuteri (523 nt) recovered once the total allows it | info | 257/260: no, 268/249: no, 279/263: yes, 257/267: no, 265/270: yes |
| asv_classify | ASVs outside the reference: where AmpliTrim's 257/260 has more than the authors' 279/263 | info | +7 in all; listed elsewhere +1, chimera +4, error variant +1, unlisted variant +1, unexplained +1 |
| mock_clip250 | clip250: FIGARO comparison | info | skipped: no --figaro-script |
| mock_clip250 | clip250: AmpliTrim's recommendation recovers at least as many variants as no truncation (250/250) | met | AmpliTrim 15, 250/250 15 variants |
| figaro_mockA | mockA: AmpliTrim equals FIGARO at FIGARO's maxEE (3,4) | met | -0.2 points (95% interval -0.8 to +0.6); margin +/-1.0 |
| mock_dilutions | dilutions 257/260: misses longer than the merge limit | info | 11 of 13 misses; recovered 185/198 (93%) |
| mock_dilutions | dilutions 265/270: misses longer than the merge limit | info | 0 of 3 misses; recovered 193/198 (97%) |
| mock_dilutions | dilutions 279/263: misses longer than the merge limit | info | 0 of 4 misses; recovered 194/198 (98%) |
| coverage_levels | coverage levels: mockA_high | info | mockA_high: covering the longest 0.1% instead of 1% changes the truncation from 257/260 to 257/263 and the merged share by -0.2 points; variants +1, strains +1, ASVs outside the reference -4; the 1% setting leaves 3 ASVs (0.25% of reads) beyond its limit |
| coverage_levels | coverage levels: v1v2 | info | v1v2: covering the longest 0.1% instead of 1% changes the truncation from 196/159 to 195/168 and the merged share by -0.4 points; the 1% setting leaves 5 ASVs (0.58% of reads) beyond its limit |
| coverage_levels | coverage levels: v4 | info | v4: covering the longest 0.1% instead of 1% changes the truncation from 120/118 to 129/115 and the merged share by +2.6 points; the 1% setting leaves 30 ASVs (0.64% of reads) beyond its limit |
| coverage_levels | coverage levels: mcm_v12 | info | mcm_v12: covering the longest 0.1% instead of 1% changes the truncation from 160/165 to 160/165 and the merged share by +0.0 points; the 1% setting leaves 0 ASVs (0.00% of reads) beyond its limit |
| landscape | landscape (mockA_high): AmpliTrim's recommendation is near the best setting that covers the amplicons | met | 0.3 points below the best of 25 DADA2 runs (margin 1.0) |
| landscape | landscape (v1v2): AmpliTrim's recommendation is near the best setting that covers the amplicons | met | 0.1 points below the best of 9 DADA2 runs (margin 1.0) |
| landscape | landscape (v4): AmpliTrim's recommendation is near the best setting that covers the amplicons | NOT MET | 6.8 points below the best of 9 DADA2 runs (margin 1.0) |
| landscape | landscape (mcm_v12): AmpliTrim's recommendation is near the best setting that covers the amplicons | met | 0.1 points below the best of 9 DADA2 runs (margin 1.0) |
| mock_miss_trace | misses traced | info | 5 missed variants traced; read counts before filtering are listed above |
| mock_pooled | pooled inference (pseudo-pooled) does not lose variants against per-sample inference | met | variants +0, strains +0, outside the reference +0 |
| mock_pooled | pooled inference (fully pooled) does not lose variants against per-sample inference | met | variants +0, strains +0, outside the reference +13 |
| stability | stability (mockA_high): recommendation does not depend on the subsample | met | truncF varies by 0 nt, truncR by 0 nt, estimated yield by 0.54 points over 6 runs |
| stability | stability (mockA_all): recommendation does not depend on the subsample | met | truncF varies by 1 nt, truncR by 1 nt, estimated yield by 0.21 points over 6 runs |
| stability | stability (v1v2): recommendation does not depend on the subsample | met | truncF varies by 1 nt, truncR by 1 nt, estimated yield by 0.19 points over 6 runs |
| stability | stability (v4): recommendation does not depend on the subsample | met | truncF varies by 3 nt, truncR by 3 nt, estimated yield by 0.19 points over 6 runs |
| stability | stability (mcm_v12): recommendation does not depend on the subsample | met | truncF varies by 3 nt, truncR by 3 nt, estimated yield by 0.29 points over 6 runs |
| per_sample_rank | per-sample rank agreement (mockA_all) | NOT MET | Spearman +0.60 over 23 samples (margin 0.8) |
| per_sample_rank | per-sample rank agreement (v1v2) | NOT MET | Spearman +0.63 over 33 samples (margin 0.8) |
| per_sample_rank | per-sample rank agreement (v4) | NOT MET | Spearman +0.70 over 36 samples (margin 0.8) |
| per_sample_rank | per-sample rank (mcm_v12) | info | only 6 samples in common; at least 10 are needed |
| its_chimeras | ITS chimera discrepancy explained by the chimera settings | info | largest removal 1.5% with 'pooled, minFold 1.0' against 13.9% in the authors' pipeline |
| figaro_v1v2 | v1v2: AmpliTrim equals FIGARO at FIGARO's maxEE (2,1) | met | +0.1 points (95% interval -0.4 to +0.6); margin +/-1.0 |
| v1v2_fulldepth | v1v2_full: AmpliTrim equals FIGARO at FIGARO's maxEE (2,1) | NOT MET | +0.9 points (95% interval +0.5 to +1.4); margin +/-1.0 |
| v1v2_fulldepth | calibration at full depth: merged / estimated yield (V1-V2, 8 samples) | info | mean 0.97, range 0.96 to 0.97 over 5 settings (V1-V2 at 5,000 pairs: 0.92; ITS: 0.65 thinned, 0.88 full) |
| battery | battery_mockA_high: AmpliTrim equals FIGARO at FIGARO's maxEE (3,4) | met | -0.2 points (95% interval -0.8 to +0.6); margin +/-1.0 |
| battery | battery_v1v2: AmpliTrim equals FIGARO at FIGARO's maxEE (2,1) | met | +0.1 points (95% interval -0.4 to +0.6); margin +/-1.0 |
| extra_datasets | battery_v4: AmpliTrim equals FIGARO at FIGARO's maxEE (1) | NOT MET | +2.0 points (95% interval +1.6 to +2.4); margin +/-1.0 |
| extra_datasets | battery_mcm_v12: AmpliTrim equals FIGARO at FIGARO's maxEE (1) | met | -0.0 points (95% interval -0.0 to +0.0); margin +/-1.0 |

## mock_grid: Mock A, six high-input samples: truncation x maxEE against the expected sequences

```
               setting  maxEE  limit    pass  merged  ASVs  variants  strains  identical  outside
     AmpliTrim 257/260    2,6    505   81.6%   78.4%    50     35/39    11/13     99.73%       15
     AmpliTrim 257/260    3,5    505   82.9%   79.7%    50     35/39    11/13     99.73%       15
 AmpliTrim alt 268/249    2,6    505   80.4%   77.6%    55     35/39    11/13     99.72%       20
 AmpliTrim alt 268/249    3,5    505   83.7%   80.8%    54     35/39    11/13     99.79%       19
       authors 279/263    2,6    530   75.0%   72.3%    44     37/39    13/13     99.81%        7
       authors 279/263    3,5    530   78.5%   75.8%    44     37/39    13/13     99.81%        7
    longer 524 257/267    2,6    512   80.6%   77.7%    49     36/39    12/13     99.70%       13
    longer 524 257/267    3,5    512   81.1%   78.2%    47     35/39    12/13     99.75%       12
    longer 535 265/270    2,6    523   79.0%   76.2%    48     36/39    13/13     99.74%       12
    longer 535 265/270    3,5    523   79.7%   76.9%    48     36/39    13/13     99.74%       12
```

## asv_classify: What the ASVs outside the expected sequences are

```
ASVs per class (share of all ASV reads in brackets); outside = every class except expected and listed elsewhere
               setting  outside   listed elsewhere        contaminant            chimera      error variant   unlisted variant        unexplained
     257/260 maxEE 2,6       14          1 (0.06%)          5 (0.14%)          5 (0.01%)          1 (0.01%)          1 (0.02%)          2 (0.03%)
     257/260 maxEE 3,5       14          1 (0.05%)          5 (0.14%)          5 (0.01%)          1 (0.01%)          1 (0.02%)          2 (0.03%)
     257/267 maxEE 2,6       12          1 (0.05%)          5 (0.14%)          3 (0.02%)          1 (0.03%)          1 (0.02%)          2 (0.03%)
     257/267 maxEE 3,5       12          0 (0.00%)          5 (0.14%)          3 (0.02%)          1 (0.03%)          1 (0.02%)          2 (0.03%)
     265/270 maxEE 2,6       12          0 (0.00%)          5 (0.14%)          2 (0.02%)          2 (0.04%)          1 (0.02%)          2 (0.03%)
     265/270 maxEE 3,5       12          0 (0.00%)          5 (0.14%)          2 (0.02%)          2 (0.04%)          1 (0.02%)          2 (0.03%)
     268/249 maxEE 2,6       19          1 (0.06%)          5 (0.14%)          9 (0.03%)          0 (0.00%)          0 (0.00%)          5 (0.05%)
     268/249 maxEE 3,5       19          0 (0.00%)          5 (0.13%)          9 (0.03%)          0 (0.00%)          0 (0.00%)          5 (0.05%)
     279/263 maxEE 2,6        7          0 (0.00%)          5 (0.15%)          1 (0.00%)          0 (0.00%)          0 (0.00%)          1 (0.03%)
     279/263 maxEE 3,5        7          0 (0.00%)          5 (0.15%)          1 (0.00%)          0 (0.00%)          0 (0.00%)          1 (0.03%)
```

## mock_clip250: Mock A clipped to 2x250 (tight overlap, known truth)

```
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail | found identical extra strains
AmpliTrim (maxEE 2,6)           249/249    2,6 |     45.3% yield     82.4/44.3% |      83.8%   44.4%    42.4%    83 |  97.08%     24  1.66% |    15    96.56%    68    4/13
full250                         250/250    2,6 |                     82.1/44.4% |      83.5%   44.4%    42.4%    89 |  96.81%     25  1.74% |    15    96.29%    74    4/13
t240                            240/240    2,6 |                     84.6/38.1% |      85.8%   40.0%    39.1%    41 |  98.96%     17  0.78% |    11    97.72%    30    2/13

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
Across 3 settings, AmpliTrim's estimate minus DADA2: yield against merged share -0.7 points (range -1.9 to +0.0); filter pass -1.3 points (range -1.4 to -1.2). As a fraction of the estimated yield, DADA2's merged share is 1.02 (range 1.00 to 1.05).

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2,6) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  full250: -0.0 points (95% interval -0.1 to +0.0); better in 2 of 6 samples, worse in 4
  t240: -4.0 points (95% interval -5.6 to -2.5); better in 0 of 6 samples, worse in 6
```

## figaro_mockA: AmpliTrim against FIGARO on mock A (six high-input samples)

```
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail | found identical extra strains
AmpliTrim (maxEE 2)             277/240      2 |     64.2% yield     63.4/63.2% |      64.5%   61.8%    59.9%    35 |  85.89%     31  0.18% |    31    99.74%     4   10/13
AmpliTrim (maxEE 2,6)           255/262    2,6 |     79.5% yield     79.1/78.5% |      80.2%   74.6%    72.6%    35 |  87.46%     29  0.21% |    29    99.75%     6   10/13
AmpliTrim (maxEE 3,5)           270/247    3,5 |     82.0% yield     81.9/81.3% |      82.7%   78.9%    76.7%    36 |  85.85%     31  0.18% |    31    99.78%     5   10/13
FIGARO (amplicon 505)           273/244    3,4 |  79.6% retained     79.4/78.9% |      79.9%   76.4%    74.1%    35 |  85.91%     31  0.18% |    31    99.77%     4   10/13
AmpliTrim (FIGARO's maxEE 3,4)  269/248    3,4 |     79.4% yield     79.5/79.0% |      79.9%   76.1%    74.0%    34 |  86.12%     30  0.19% |    30    99.77%     4   10/13
authors                         279/263    2,6 |                     71.3/71.2% |      73.1%   68.0%    66.5%    33 |  87.89%     30  0.10% |    30    99.86%     3   11/13

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 505) was run on the 87% of the sampled pairs whose reads are 280 and 283 nt long (it needs reads of one length).
Across 6 settings, AmpliTrim's estimate minus DADA2: yield against merged share +2.7 points (range +1.3 to +3.9); filter pass -0.9 points (range -1.8 to -0.4). Rank correlation of the estimated yield with DADA2's merged share: +0.94. As a fraction of the estimated yield, DADA2's merged share is 0.96 (range 0.95 to 0.98).
The strict estimate (no mismatch allowed in the overlap) minus DADA2's merged share: -28.5 points (range -35.6 to -18.4); rank correlation +0.89.
FIGARO's predicted retention minus DADA2's pass rate: -0.4 points (FIGARO (amplicon 505)). It predicts the filter only, so it is not expected to match the merged share.

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 2,6): +12.8 points (95% interval +11.4 to +14.2); better in 6 of 6 samples, worse in 0
  AmpliTrim (maxEE 3,5): +17.1 points (95% interval +15.6 to +18.5); better in 6 of 6 samples, worse in 0
  FIGARO (amplicon 505): +14.6 points (95% interval +13.2 to +16.1); better in 6 of 6 samples, worse in 0
  AmpliTrim (FIGARO's maxEE 3,4): +14.5 points (95% interval +12.7 to +16.5); better in 6 of 6 samples, worse in 0
  authors: +6.0 points (95% interval +2.7 to +8.6); better in 5 of 6 samples, worse in 1

Paired per-sample differences against FIGARO (amplicon 505):
  AmpliTrim (maxEE 2): -14.6 points (95% interval -16.1 to -13.2); better in 0 of 6 samples, worse in 6
  AmpliTrim (maxEE 2,6): -1.9 points (95% interval -3.9 to -0.6); better in 0 of 6 samples, worse in 6
  AmpliTrim (maxEE 3,5): +2.5 points (95% interval +2.0 to +3.1); better in 6 of 6 samples, worse in 0
  AmpliTrim (FIGARO's maxEE 3,4): -0.2 points (95% interval -0.8 to +0.6); better in 1 of 6 samples, worse in 5
  authors: -8.6 points (95% interval -12.8 to -6.2); better in 0 of 6 samples, worse in 6
```

## mock_dilutions: Mock A dilution series at several truncations

```
--- 257/260 (merge limit 505 nt): 185 of 198 present variants recovered (93%); 13 misses, 11 of them longer than the limit
    1e9: 35/38 variants, 11/13 strains, merged 78.5%
    1e8: 34/37 variants, 11/13 strains, merged 78.0%
    1e7: 36/39 variants, 11/13 strains, merged 81.9%
    1e6: 35/37 variants, 12/13 strains, merged 81.4%
    1e5: 20/21 variants, 8/9 strains, merged 78.9%
    1e4: 10/10 variants, 7/7 strains, merged 78.9%
    1e3: 11/12 variants, 9/10 strains, merged 81.2%
    1e2: 4/4 variants, 3/3 strains, merged 79.6%
--- 265/270 (merge limit 523 nt): 193 of 198 present variants recovered (97%); 3 misses, 0 of them longer than the limit
    1e9: 36/38 variants, 13/13 strains, merged 76.5%
    1e8: 36/37 variants, 13/13 strains, merged 75.8%
    1e7: 38/39 variants, 13/13 strains, merged 79.7%
    1e6: 36/37 variants, 13/13 strains, merged 79.0%
    1e5: 21/21 variants, 9/9 strains, merged 77.0%
    1e4: 10/10 variants, 7/7 strains, merged 76.3%
    1e3: 12/12 variants, 10/10 strains, merged 79.2%
    1e2: 4/4 variants, 3/3 strains, merged 79.2%
--- 279/263 (merge limit 530 nt): 194 of 198 present variants recovered (98%); 4 misses, 0 of them longer than the limit
    1e9: 36/38 variants, 13/13 strains, merged 73.0%
    1e8: 37/37 variants, 13/13 strains, merged 71.0%
    1e7: 39/39 variants, 13/13 strains, merged 76.3%
    1e6: 36/37 variants, 13/13 strains, merged 73.6%
    1e5: 21/21 variants, 9/9 strains, merged 67.5%
    1e4: 10/10 variants, 7/7 strains, merged 63.9%
    1e3: 12/12 variants, 10/10 strains, merged 70.1%
    1e2: 3/4 variants, 2/3 strains, merged 68.6%
```

## coverage_levels: What leaving out 1%, 0.5%, 0.2%, 0.1% and 0% of the longest amplicons costs and buys

```
--- mockA_high (maxEE 2,6)
 level  truncation  limit  left out  estimate   merged  variants  strains  outside     ASVs beyond the limit
  1.0%     257/260    505     0.31%     80.7%    78.4%     35/39    11/13       15        3 (0.25% of reads)
  0.5%     257/260    505     0.31%     80.7%    78.4%     35/39    11/13       15        3 (0.25% of reads)
  0.2%     257/263    508     0.06%     80.7%    78.2%     36/39    12/13       11        2 (0.02% of reads)
  0.1%     257/263    508     0.06%     80.7%    78.2%     36/39    12/13       11        2 (0.02% of reads)
  0.0%     268/280    536     0.00%     76.3%    73.2%     36/39    13/13       11        0 (0.00% of reads)

--- v1v2 (maxEE 2)
 level  truncation  limit  left out  estimate   merged     ASVs beyond the limit
  1.0%     196/159    343     0.79%     90.3%    83.9%        5 (0.58% of reads)
  0.5%     190/168    346     0.22%     90.7%    83.7%        3 (0.15% of reads)
  0.2%     195/168    351     0.08%     90.6%    83.5%        2 (0.04% of reads)
  0.1%     195/168    351     0.08%     90.6%    83.5%        2 (0.04% of reads)
  0.0%     279/280    547     0.00%     35.4%    29.4%        0 (0.00% of reads)

--- v4 (maxEE 2)
 level  truncation  limit  left out  estimate   merged     ASVs beyond the limit
  1.0%     120/118    226     0.61%     98.0%    64.3%       30 (0.64% of reads)
  0.5%     124/115    227     0.17%     98.5%    66.8%        6 (0.22% of reads)
  0.2%     124/115    227     0.17%     98.5%    66.8%        6 (0.22% of reads)
  0.1%     129/115    232     0.01%     98.6%    66.9%        1 (0.01% of reads)
  0.0%     133/120    241     0.00%     98.5%    64.9%        0 (0.00% of reads)

--- mcm_v12 (maxEE 2)
 level  truncation  limit  left out  estimate   merged     ASVs beyond the limit
  1.0%     160/165    313     0.01%     96.4%    95.9%        0 (0.00% of reads)
  0.5%     160/165    313     0.01%     96.4%    95.9%        0 (0.00% of reads)
  0.2%     160/165    313     0.01%     96.4%    95.9%        0 (0.00% of reads)
  0.1%     160/165    313     0.01%     96.4%    95.9%        0 (0.00% of reads)
  0.0%     205/222    415     0.00%     92.7%    92.0%        0 (0.00% of reads)

```

## landscape: Is the recommendation near the best of a DADA2 grid around it?

```
--- mockA_high (maxEE 2,6); AmpliTrim recommends 257/260 (coverage floor 517); share of pairs merged; * = AmpliTrim, . = total below the floor
  trF\trR     240     250     260     270     280
       237   24.9.   40.3.   42.2.   53.8.   74.6 
       247   39.4.   43.0.   54.0.   76.2    73.0 
       257   42.3.   54.8.   76.0*   74.9    71.7 
       267   54.0.   76.3    74.3    73.1    70.4 
       277   73.9    73.2    71.2    70.2    67.7 
  best of the grid: 267/250 at 76.3%; best among settings that meet the floor: 267/250 at 76.3%; AmpliTrim 76.0%, so 0.3 points below the best that covers the amplicons
  recovered: AmpliTrim 30/39 variants, 10/13 strains; the best feasible setting 31/39, 10/13

--- v1v2 (maxEE 2); AmpliTrim recommends 196/159 (coverage floor 355); share of pairs merged; * = AmpliTrim, . = total below the floor
  trF\trR     149     159     169
       186   60.9.   72.0.   82.7 
       196   71.8.   82.6*   82.1 
       206   82.6    82.1    81.3 
  best of the grid: 186/169 at 82.7%; best among settings that meet the floor: 186/169 at 82.7%; AmpliTrim 82.6%, so 0.1 points below the best that covers the amplicons

--- v4 (maxEE 2); AmpliTrim recommends 120/118 (coverage floor 238); share of pairs merged; * = AmpliTrim, . = total below the floor
  trF\trR     108     118     128
       110    3.6.   58.9.   56.3 
       120   66.1.   59.6*   56.9 
       130   66.4    60.2    57.1 
  best of the grid: 130/108 at 66.4%; best among settings that meet the floor: 130/108 at 66.4%; AmpliTrim 59.6%, so 6.8 points below the best that covers the amplicons

--- mcm_v12 (maxEE 2); AmpliTrim recommends 160/165 (coverage floor 325); share of pairs merged; * = AmpliTrim, . = total below the floor
  trF\trR     155     165     175
       150   25.3.   94.1.   95.9 
       160   94.0.   95.9*   95.7 
       170   95.7    95.6    95.5 
  best of the grid: 150/175 at 95.9%; best among settings that meet the floor: 150/175 at 95.9%; AmpliTrim 95.9%, so 0.1 points below the best that covers the amplicons

```

## mock_miss_trace: Where the unexplained mock A misses are lost

```
--- 10^9 cells (3 samples): 3 present variant(s) not recovered exactly
    Enterococcus faecalis (508 nt): reads identical to it before filtering: 42; within 1 edit: 95; within 2 edits: 115; nearest ASV: 51 edits, 1 reads
    Staphylococcus epidermidis (497 nt): reads identical to it before filtering: 9; within 1 edit: 43; within 2 edits: 58; nearest ASV: 1 edits, 107 reads
    Lactobacillus reuteri (523 nt): reads identical to it before filtering: 2; within 1 edit: 2; within 2 edits: 2; nearest ASV: 107 edits, 832 reads
--- 10^6 cells (3 samples): 2 present variant(s) not recovered exactly
    Escherichia coli (490 nt): reads identical to it before filtering: 242; within 1 edit: 359; within 2 edits: 933; nearest ASV: 2 edits, 1085 reads
    Enterococcus faecalis (508 nt): reads identical to it before filtering: 16; within 1 edit: 28; within 2 edits: 42; nearest ASV: 73 edits, 2326 reads
```

## mock_pooled: Mock A with pooled DADA2 inference

```
             inference  merged   ASVs  variants  strains  identical  outside
  per sample (default)   78.4%     50     35/39    11/13     99.73%       15
         pseudo-pooled   78.5%     50     35/39    11/13     99.73%       15
          fully pooled   79.0%     63     35/39    11/13     98.62%       28
```

## stability: Stability of the recommendation across subsample sizes

```
--- mockA_high
max pairs  every  truncF  truncR    yield   floor  seconds
    20000      1     277     240    65.1%     517       13
    20000      2     277     240    65.1%     517       13
    50000      1     277     240    65.4%     517       30
    50000      2     277     240    65.4%     517       30
   100000      1     277     240    65.7%     517       45
   100000      2     277     240    65.7%     517       44
--- mockA_all
max pairs  every  truncF  truncR    yield   floor  seconds
    20000      1     274     243    65.6%     517       18
    20000      2     274     243    65.6%     517       18
    50000      1     275     242    65.8%     517       36
    50000      2     275     242    65.8%     517       37
   100000      1     275     242    65.7%     517       71
   100000      2     275     242    65.7%     517       68
--- v1v2
max pairs  every  truncF  truncR    yield   floor  seconds
    20000      1     197     158    90.3%     355       28
    20000      2     197     158    90.3%     355       28
    50000      1     196     159    90.3%     355       45
    50000      2     196     159    90.3%     355       48
   100000      1     196     159    90.5%     355       72
   100000      2     196     159    90.5%     355       74
--- v4
max pairs  every  truncF  truncR    yield   floor  seconds
    20000      1     123     115    97.8%     238       37
    20000      2     123     115    97.8%     238       38
    50000      1     120     118    98.0%     238       52
    50000      2     120     118    98.0%     238       52
   100000      1     123     115    97.9%     238       79
   100000      2     123     115    97.9%     238       76
--- mcm_v12
max pairs  every  truncF  truncR    yield   floor  seconds
    20000      1     158     167    96.7%     325       50
    20000      2     158     167    96.7%     325       57
    50000      1     160     165    96.4%     325       73
    50000      2     160     165    96.4%     325       75
   100000      1     157     168    96.5%     325       91
   100000      2     157     168    96.5%     325       89
```

## per_sample_rank: Per-sample rank agreement of the yield estimate with DADA2

```
--- mockA_all at 257/260, maxEE 2,6: 23 samples; offset (estimate - DADA2) mean +2.6 points, range -0.0 to +10.3; rank correlation +0.60
--- v1v2 at 196/159, maxEE 2: 33 samples; offset (estimate - DADA2) mean +6.5 points, range +1.4 to +14.2; rank correlation +0.63
--- v4 at 123/115, maxEE 2: 36 samples; offset (estimate - DADA2) mean +31.5 points, range +8.1 to +48.2; rank correlation +0.70
```

## its_chimeras: ITS: chimera removal under different settings

```
                           chimera removal   merged  non-chimeric   removed    ASVs
         DADA2 R defaults (as used so far)    63.3%         63.2%      0.2%    5456
 consensus, minFold 1.0 (q2-dada2 default)    63.3%         63.0%      0.6%    5449
                       pooled, minFold 1.0    63.3%         62.4%      1.5%    5340
The original authors' pipeline removed 13.9% of merged reads on these samples.
```

## figaro_v1v2: AmpliTrim against FIGARO on the V1-V2 study

```
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail
AmpliTrim (maxEE 2)             198/157      2 |     90.5% yield     91.5/90.6% |      91.5%   84.2%    82.0%   808 |  32.32%    178 15.40%
FIGARO (amplicon 343)           225/130    2,1 |  88.1% retained     88.5/87.9% |      88.5%   82.2%    80.0%   857 |  32.05%    180 15.87%
AmpliTrim (FIGARO's maxEE 2,1)  211/144    2,1 |     88.3% yield     89.2/88.4% |      89.1%   82.3%    80.3%   806 |  32.14%    179 15.65%
more_overlap                    230/200      2 |                     84.9/84.8% |      84.8%   77.1%    76.2%   775 |  32.27%    179 15.05%

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 343) was run on the 47% of the sampled pairs whose reads are 281 and 281 nt long (it needs reads of one length).
Across 4 settings, AmpliTrim's estimate minus DADA2: yield against merged share +6.5 points (range +5.7 to +7.7); filter pass +0.0 points (range +0.0 to +0.1). Rank correlation of the estimated yield with DADA2's merged share: +1.00. As a fraction of the estimated yield, DADA2's merged share is 0.93 (range 0.91 to 0.94).
The strict estimate (no mismatch allowed in the overlap) minus DADA2's merged share: -6.0 points (range -12.0 to -3.4); rank correlation +1.00.
FIGARO's predicted retention minus DADA2's pass rate: -0.4 points (FIGARO (amplicon 343)). It predicts the filter only, so it is not expected to match the merged share.

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  FIGARO (amplicon 343): -2.0 points (95% interval -2.5 to -1.5); better in 5 of 33 samples, worse in 27
  AmpliTrim (FIGARO's maxEE 2,1): -1.9 points (95% interval -2.2 to -1.6); better in 0 of 33 samples, worse in 33
  more_overlap: -7.1 points (95% interval -7.7 to -6.5); better in 0 of 33 samples, worse in 33

Paired per-sample differences against FIGARO (amplicon 343):
  AmpliTrim (maxEE 2): +2.0 points (95% interval +1.5 to +2.5); better in 27 of 33 samples, worse in 5
  AmpliTrim (FIGARO's maxEE 2,1): +0.1 points (95% interval -0.4 to +0.6); better in 19 of 33 samples, worse in 14
  more_overlap: -5.1 points (95% interval -5.8 to -4.4); better in 0 of 33 samples, worse in 33
```

## v1v2_fulldepth: V1-V2 at full depth (8 samples): calibration of the yield estimate

```
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail
AmpliTrim (maxEE 2)             195/160      2 |     90.8% yield     91.3/90.6% |      91.6%   87.7%    77.9%   960 |  41.27%    150 14.56%
AmpliTrim (maxEE 3)             185/170      3 |     93.5% yield     94.3/93.3% |      94.4%   90.5%    80.3%   974 |  41.25%    150 14.62%
FIGARO (amplicon 343)           227/128    2,1 |  88.2% retained     88.1/87.5% |      88.5%   84.9%    75.9%   951 |  40.98%    150 14.63%
AmpliTrim (FIGARO's maxEE 2,1)  211/144    2,1 |     88.6% yield     89.2/88.6% |      89.5%   85.8%    76.1%   951 |  41.20%    154 14.32%
more_overlap                    230/200      2 |                     84.9/84.8% |      85.1%   81.3%    74.3%   900 |  40.32%    151 14.53%

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 343) was run on the 50% of the sampled pairs whose reads are 281 and 281 nt long (it needs reads of one length).
Across 5 settings, AmpliTrim's estimate minus DADA2: yield against merged share +2.9 points (range +2.6 to +3.5); filter pass -0.3 points (range -0.4 to -0.1). Rank correlation of the estimated yield with DADA2's merged share: +1.00. As a fraction of the estimated yield, DADA2's merged share is 0.97 (range 0.96 to 0.97).
The strict estimate (no mismatch allowed in the overlap) minus DADA2's merged share: -10.5 points (range -16.5 to -7.2); rank correlation +0.70.
FIGARO's predicted retention minus DADA2's pass rate: -0.3 points (FIGARO (amplicon 343)). It predicts the filter only, so it is not expected to match the merged share.

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 3): +2.8 points (95% interval +2.5 to +3.0); better in 8 of 8 samples, worse in 0
  FIGARO (amplicon 343): -2.7 points (95% interval -3.4 to -2.1); better in 0 of 8 samples, worse in 8
  AmpliTrim (FIGARO's maxEE 2,1): -1.8 points (95% interval -2.2 to -1.4); better in 0 of 8 samples, worse in 8
  more_overlap: -6.6 points (95% interval -7.3 to -6.0); better in 0 of 8 samples, worse in 8

Paired per-sample differences against FIGARO (amplicon 343):
  AmpliTrim (maxEE 2): +2.7 points (95% interval +2.1 to +3.4); better in 8 of 8 samples, worse in 0
  AmpliTrim (maxEE 3): +5.5 points (95% interval +4.8 to +6.1); better in 8 of 8 samples, worse in 0
  AmpliTrim (FIGARO's maxEE 2,1): +0.9 points (95% interval +0.5 to +1.4); better in 7 of 8 samples, worse in 1
  more_overlap: -3.8 points (95% interval -5.1 to -2.8); better in 0 of 8 samples, worse in 8
```

## battery: The standard battery on each dataset (the test-stage table)

```
--- mockA_high (V1-V3, 16S, 6 samples)
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail | found identical extra strains
AmpliTrim (maxEE 2,6)           255/262    2,6 |     79.5% yield     79.1/78.5% |      80.2%   74.6%    72.6%    35 |  87.46%     29  0.21% |    29    99.75%     6   10/13
AmpliTrim (maxEE 1)             277/240      1 |     44.4% yield     42.9/42.8% |      44.5%   42.6%    41.3%    31 |  86.73%     29  0.12% |    28    99.70%     3   10/13
AmpliTrim (maxEE 5)             273/244      5 |     86.8% yield     88.1/86.9% |      88.0%   84.2%    81.7%    36 |  85.93%     31  0.19% |    32    99.81%     4   11/13
FIGARO (amplicon 505)           273/244    3,4 |  79.6% retained     79.4/78.9% |      79.9%   76.4%    74.1%    35 |  85.91%     31  0.18% |    31    99.77%     4   10/13
AmpliTrim (FIGARO's maxEE 3,4)  269/248    3,4 |     79.4% yield     79.5/79.0% |      79.9%   76.1%    74.0%    34 |  86.12%     30  0.19% |    30    99.77%     4   10/13
full                               none    2,6 |                                |      70.8%   64.2%    63.2%    31 |  87.30%     31  0.00% |    29    97.70%     2   10/13

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 505) was run on the 87% of the sampled pairs whose reads are 280 and 283 nt long (it needs reads of one length).
Across 5 settings, AmpliTrim's estimate minus DADA2: yield against merged share +2.4 points (range +0.3 to +3.9); filter pass -0.7 points (range -1.6 to +0.1). Rank correlation of the estimated yield with DADA2's merged share: +0.90. As a fraction of the estimated yield, DADA2's merged share is 0.97 (range 0.95 to 0.99).
The strict estimate (no mismatch allowed in the overlap) minus DADA2's merged share: -25.8 points (range -34.5 to -7.9); rank correlation +1.00.
FIGARO's predicted retention minus DADA2's pass rate: -0.4 points (FIGARO (amplicon 505)). It predicts the filter only, so it is not expected to match the merged share.

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2,6) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 1): -32.1 points (95% interval -34.2 to -30.0); better in 0 of 6 samples, worse in 6
  AmpliTrim (maxEE 5): +9.8 points (95% interval +7.4 to +13.9); better in 6 of 6 samples, worse in 0
  FIGARO (amplicon 505): +1.9 points (95% interval +0.6 to +3.9); better in 6 of 6 samples, worse in 0
  AmpliTrim (FIGARO's maxEE 3,4): +1.7 points (95% interval -0.1 to +4.4); better in 4 of 6 samples, worse in 2
  full: -10.5 points (95% interval -12.1 to -9.1); better in 0 of 6 samples, worse in 6

Paired per-sample differences against FIGARO (amplicon 505):
  AmpliTrim (maxEE 2,6): -1.9 points (95% interval -3.9 to -0.6); better in 0 of 6 samples, worse in 6
  AmpliTrim (maxEE 1): -34.0 points (95% interval -37.0 to -31.4); better in 0 of 6 samples, worse in 6
  AmpliTrim (maxEE 5): +8.0 points (95% interval +6.5 to +10.1); better in 6 of 6 samples, worse in 0
  AmpliTrim (FIGARO's maxEE 3,4): -0.2 points (95% interval -0.8 to +0.6); better in 1 of 6 samples, worse in 5
  full: -12.4 points (95% interval -15.9 to -10.0); better in 0 of 6 samples, worse in 6

--- v1v2 (V1-V2, 16S, 33 samples)
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail
AmpliTrim (maxEE 2)             198/157      2 |     90.5% yield     91.5/90.6% |      91.5%   84.2%    82.0%   808 |  32.32%    178 15.40%
AmpliTrim (maxEE 1)             197/158      1 |     85.0% yield     85.6/85.0% |      85.6%   78.6%    76.7%   805 |  32.33%    179 15.35%
AmpliTrim (maxEE 5)             184/171      5 |     95.5% yield     97.6/95.5% |      97.6%   89.3%    87.2%   817 |  32.23%    177 15.54%
FIGARO (amplicon 343)           225/130    2,1 |  88.1% retained     88.5/87.9% |      88.5%   82.2%    80.0%   857 |  32.05%    180 15.87%
AmpliTrim (FIGARO's maxEE 2,1)  211/144    2,1 |     88.3% yield     89.2/88.4% |      89.1%   82.3%    80.3%   806 |  32.14%    179 15.65%
full                               none      2 |                                |      35.4%   29.3%    29.1%   475 |  38.28%    167 10.50%

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 343) was run on the 47% of the sampled pairs whose reads are 281 and 281 nt long (it needs reads of one length).
Across 5 settings, AmpliTrim's estimate minus DADA2: yield against merged share +6.2 points (range +5.7 to +6.4); filter pass +0.0 points (range +0.0 to +0.1). Rank correlation of the estimated yield with DADA2's merged share: +1.00. As a fraction of the estimated yield, DADA2's merged share is 0.93 (range 0.93 to 0.94).
The strict estimate (no mismatch allowed in the overlap) minus DADA2's merged share: -4.8 points (range -10.4 to -1.5); rank correlation +0.90.
FIGARO's predicted retention minus DADA2's pass rate: -0.4 points (FIGARO (amplicon 343)). It predicts the filter only, so it is not expected to match the merged share.

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 1): -5.5 points (95% interval -5.8 to -5.3); better in 0 of 33 samples, worse in 33
  AmpliTrim (maxEE 5): +5.1 points (95% interval +4.6 to +5.5); better in 33 of 33 samples, worse in 0
  FIGARO (amplicon 343): -2.0 points (95% interval -2.5 to -1.5); better in 5 of 33 samples, worse in 27
  AmpliTrim (FIGARO's maxEE 2,1): -1.9 points (95% interval -2.2 to -1.6); better in 0 of 33 samples, worse in 33
  full: -55.0 points (95% interval -56.4 to -53.6); better in 0 of 33 samples, worse in 33

Paired per-sample differences against FIGARO (amplicon 343):
  AmpliTrim (maxEE 2): +2.0 points (95% interval +1.5 to +2.5); better in 27 of 33 samples, worse in 5
  AmpliTrim (maxEE 1): -3.5 points (95% interval -4.1 to -3.0); better in 0 of 33 samples, worse in 33
  AmpliTrim (maxEE 5): +7.1 points (95% interval +6.7 to +7.5); better in 33 of 33 samples, worse in 0
  AmpliTrim (FIGARO's maxEE 2,1): +0.1 points (95% interval -0.4 to +0.6); better in 19 of 33 samples, worse in 14
  full: -53.0 points (95% interval -54.5 to -51.5); better in 0 of 33 samples, worse in 33

--- its (ITS1, ITS, 37 samples)
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail
AmpliTrim (maxEE 1)                none      1 |     54.6% yield     56.0/54.6% |      55.9%   39.5%    39.5%  1419 |  34.82%    157 22.24%
AmpliTrim (maxEE 2)                none      2 |     72.2% yield     74.3/72.2% |      74.2%   46.9%    46.9%  1474 |  33.32%    165 22.44%
AmpliTrim (maxEE 5)                none      5 |     83.8% yield     95.4/83.8% |      95.4%   53.4%    53.4%  1484 |  31.69%    165 22.84%
trunc200                        200/200      2 |                     42.0/37.1% |      42.0%   23.3%    23.3%  1242 |  38.48%    166 24.30%

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
Across 4 settings, AmpliTrim's estimate minus DADA2: yield against merged share +21.1 points (range +13.7 to +30.4); filter pass +0.0 points (range -0.1 to +0.1). Rank correlation of the estimated yield with DADA2's merged share: +1.00. As a fraction of the estimated yield, DADA2's merged share is 0.66 (range 0.63 to 0.72).

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 1) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 2): +7.4 points (95% interval +7.0 to +7.8); better in 37 of 37 samples, worse in 0
  AmpliTrim (maxEE 5): +13.9 points (95% interval +12.9 to +15.0); better in 37 of 37 samples, worse in 0
  trunc200: -16.1 points (95% interval -17.9 to -14.3); better in 0 of 37 samples, worse in 37

```

## extra_datasets: New datasets: the standard battery (their coverage levels are in coverage_levels)

```
--- v4 (V4, 16S, 36 samples)
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail
AmpliTrim (maxEE 2)             124/114      2 |     97.9% yield     98.6/97.8% |      98.5%   67.2%    65.0%  2396 |  38.15%    141 36.21%
AmpliTrim (maxEE 1)             123/115      1 |     96.0% yield     96.5/95.8% |      96.5%   64.9%    62.9%  2256 |  38.71%    142 35.28%
AmpliTrim (maxEE 5)             125/113      5 |     98.7% yield     99.8/98.7% |      99.8%   69.1%    66.4%  2541 |  37.67%    143 36.50%
FIGARO (amplicon 226)           119/119      1 |  98.4% retained     96.5/95.8% |      96.5%   62.9%    61.7%  2095 |  39.49%    149 33.50%
full                               none      2 |                                |      86.4%   54.2%    54.1%  1550 |  42.03%    146 29.36%

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 226) was run on the 86% of the sampled pairs whose reads are 207 and 207 nt long (it needs reads of one length).
Across 4 settings, AmpliTrim's estimate minus DADA2: yield against merged share +31.0 points (range +29.5 to +32.9); filter pass -0.0 points (range -0.0 to +0.0). Rank correlation of the estimated yield with DADA2's merged share: +1.00. As a fraction of the estimated yield, DADA2's merged share is 0.68 (range 0.66 to 0.70).
The strict estimate (no mismatch allowed in the overlap) minus DADA2's merged share: +24.7 points (range +23.4 to +26.8); rank correlation +1.00.
FIGARO's predicted retention minus DADA2's pass rate: +1.9 points (FIGARO (amplicon 226)). It predicts the filter only, so it is not expected to match the merged share.

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 1): -2.3 points (95% interval -2.6 to -2.0); better in 0 of 36 samples, worse in 36
  AmpliTrim (maxEE 5): +1.9 points (95% interval +1.7 to +2.2); better in 36 of 36 samples, worse in 0
  FIGARO (amplicon 226): -4.3 points (95% interval -4.9 to -3.7); better in 0 of 36 samples, worse in 36
  full: -13.0 points (95% interval -13.9 to -12.2); better in 0 of 36 samples, worse in 36

Paired per-sample differences against FIGARO (amplicon 226):
  AmpliTrim (maxEE 2): +4.3 points (95% interval +3.7 to +4.9); better in 36 of 36 samples, worse in 0
  AmpliTrim (maxEE 1): +2.0 points (95% interval +1.6 to +2.4); better in 35 of 36 samples, worse in 1
  AmpliTrim (maxEE 5): +6.2 points (95% interval +5.6 to +6.8); better in 36 of 36 samples, worse in 0
  full: -8.7 points (95% interval -9.5 to -8.0); better in 0 of 36 samples, worse in 36

--- mcm_v12 (V1-V2, 16S, 6 samples)
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail
AmpliTrim (maxEE 2)             155/170      2 |     96.3% yield     96.3/96.1% |      96.4%   95.9%    95.7%    29 |  95.17%     26  0.24%
AmpliTrim (maxEE 1)             155/170      1 |     94.0% yield     94.0/94.0% |      94.1%   93.6%    93.4%    29 |  95.16%     26  0.24%
AmpliTrim (maxEE 5)             132/193      5 |     98.3% yield     98.8/98.3% |      98.9%   98.3%    97.9%    29 |  95.18%     26  0.24%
FIGARO (amplicon 313)           156/169      1 |  94.2% retained     94.0/94.0% |      94.1%   93.6%    93.4%    29 |  95.16%     26  0.24%
full                               none      2 |                                |      50.0%   26.0%    26.0%    17 |  99.78%     16  0.09%

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 313) was run on the 57% of the sampled pairs whose reads are 280 and 280 nt long (it needs reads of one length).
Across 4 settings, AmpliTrim's estimate minus DADA2: yield against merged share +0.3 points (range -0.1 to +0.4); filter pass -0.1 points (range -0.1 to -0.0). Rank correlation of the estimated yield with DADA2's merged share: +1.00. As a fraction of the estimated yield, DADA2's merged share is 1.00 (range 1.00 to 1.00).
The strict estimate (no mismatch allowed in the overlap) minus DADA2's merged share: -2.9 points (range -5.0 to -1.8); rank correlation +0.80.
FIGARO's predicted retention minus DADA2's pass rate: +0.2 points (FIGARO (amplicon 313)). It predicts the filter only, so it is not expected to match the merged share.

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 1): -2.3 points (95% interval -2.5 to -2.2); better in 0 of 6 samples, worse in 6
  AmpliTrim (maxEE 5): +2.4 points (95% interval +2.3 to +2.5); better in 6 of 6 samples, worse in 0
  FIGARO (amplicon 313): -2.3 points (95% interval -2.5 to -2.2); better in 0 of 6 samples, worse in 6
  full: -69.9 points (95% interval -73.6 to -66.4); better in 0 of 6 samples, worse in 6

Paired per-sample differences against FIGARO (amplicon 313):
  AmpliTrim (maxEE 2): +2.3 points (95% interval +2.2 to +2.5); better in 6 of 6 samples, worse in 0
  AmpliTrim (maxEE 1): -0.0 points (95% interval -0.0 to +0.0); better in 1 of 6 samples, worse in 5
  AmpliTrim (maxEE 5): +4.7 points (95% interval +4.5 to +4.9); better in 6 of 6 samples, worse in 0
  full: -67.6 points (95% interval -71.3 to -64.0); better in 0 of 6 samples, worse in 6

```

## Not testable with the data on hand

- An independent mock community (Zymo D6321, PRJEB67827, with Zymo's own reference sequences): no data on hand (python validation\check_build.py --download mockB).
- V3-V4 2x250 reads (tight overlap on real data) and V4-V5 (PRJNA971391): no data on hand (check_build.py --download v3v4 / v4v5); mock_clip250 is an emulation, not a replacement.
- Other platforms (binned quality scores): no data on hand beyond the exactness checks already made.
- Housekeeping: run the CI workflow, push to GitHub, choose a licence, archive for a DOI, test on Windows and Linux, regenerate Figures 3 and 5 and Table 6 from the saved tables, verify the references.
