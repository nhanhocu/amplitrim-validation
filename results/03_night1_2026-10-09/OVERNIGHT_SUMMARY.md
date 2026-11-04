# AmpliTrim overnight validation (full), written 2026-10-09 07:59

Margins fixed before the run: {"recovered_variants": 1, "recovered_strains": 1, "identical_points": 0.1, "extra_asvs": 2, "figaro_equivalence_points": 1.0, "stability_truncation_nt": 10, "stability_yield_points": 1.0, "per_sample_rho": 0.8, "landscape_regret_points": 1.0}

## Steps

| step | tier | status | minutes | note |
| --- | --- | --- | --- | --- |
| battery | 1 | ok | 35.6 |  |
| extra_datasets | 1 | ok | 177.0 |  |

## Verdicts against the pre-set criteria

| step | criterion | outcome | detail |
| --- | --- | --- | --- |
| battery | battery_mockA_high: AmpliTrim equals FIGARO at FIGARO's maxEE (3,4) | met | -0.0 points (95% interval -0.3 to +0.3); margin +/-1.0 |
| battery | battery_v1v2: AmpliTrim equals FIGARO at FIGARO's maxEE (2,1) | met | +0.4 points (95% interval -0.1 to +0.8); margin +/-1.0 |
| extra_datasets | battery_v4: AmpliTrim equals FIGARO at FIGARO's maxEE (1) | met | +0.0 points (95% interval +0.0 to +0.0); margin +/-1.0 |
| extra_datasets | battery_mcm_v12: AmpliTrim equals FIGARO at FIGARO's maxEE (1) | met | -0.0 points (95% interval -0.0 to +0.0); margin +/-1.0 |
| extra_datasets | battery_mockB: AmpliTrim equals FIGARO at FIGARO's maxEE (6,9) | NOT MET | +2.6 points (95% interval +0.3 to +5.2); margin +/-1.0 |
| extra_datasets | battery_mcm_v46: paired comparison with FIGARO | info | no paired per-sample comparison was printed (it needs at least 6 samples) |
| extra_datasets | battery_d6300_V3-V4: AmpliTrim equals FIGARO at FIGARO's maxEE (1) | met | +0.0 points (95% interval +0.0 to +0.0); margin +/-1.0 |
| extra_datasets | battery_d6300_V4-V5: FIGARO ran | NOT MET | no FIGARO row in the comparison table (FIGARO may have refused these reads) |
| extra_datasets | battery_wastewater_V3-V4: AmpliTrim equals FIGARO at FIGARO's maxEE (5) | NOT MET | -1.0 points (95% interval -1.4 to -0.7); margin +/-1.0 |
| extra_datasets | battery_spikein_V3-V4: AmpliTrim equals FIGARO at FIGARO's maxEE (2,1) | NOT MET | +1.3 points (95% interval +0.4 to +2.5); margin +/-1.0 |
| extra_datasets | battery_swabs_V3-V4: AmpliTrim equals FIGARO at FIGARO's maxEE (1) | met | +0.0 points (95% interval +0.0 to +0.0); margin +/-1.0 |

## battery: The standard battery on each dataset (the test-stage table)

```
--- mockA_high (V1-V3, 16S, 6 samples)
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail | found identical extra strains
AmpliTrim (maxEE 2,6)           258/262    2,6 |     79.5% yield     78.6/78.3% |      79.8%   74.2%    72.3%    36 |  87.27%     30  0.23% |    30    99.73%     6   11/13
AmpliTrim (maxEE 1)             280/240      1 |     43.3% yield     41.6/41.6% |      43.3%   41.3%    40.0%    29 |  87.49%     28  0.04% |    27    99.77%     2    9/13
AmpliTrim (maxEE 5)             273/247      5 |     86.9% yield     87.6/86.9% |      87.5%   83.6%    81.3%    37 |  85.78%     32  0.19% |    33    99.81%     4   12/13
FIGARO (amplicon 508)           273/247    3,4 |  78.9% retained     78.9/78.7% |      79.4%   75.8%    73.7%    36 |  85.77%     32  0.19% |    32    99.77%     4   11/13
AmpliTrim (FIGARO's maxEE 3,4)  272/248    3,4 |     79.2% yield     79.0/78.8% |      79.4%   75.8%    73.7%    35 |  85.95%     31  0.19% |    31    99.77%     4   11/13
full                               none    2,6 |                                |      70.8%   64.2%    63.2%    31 |  87.30%     31  0.00% |    29    97.70%     2   10/13

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 508) was run on the 87% of the sampled pairs whose reads are 280 and 283 nt long (it needs reads of one length).
Across 5 settings, AmpliTrim's estimate minus DADA2: yield against merged share +2.7 points (range +0.3 to +4.2); filter pass -0.8 points (range -1.7 to +0.1). Rank correlation of the estimated yield with DADA2's merged share: +0.90. As a fraction of the estimated yield, DADA2's merged share is 0.97 (range 0.95 to 0.99).
The strict estimate (no mismatch allowed in the overlap) minus DADA2's merged share: -26.9 points (range -36.4 to -8.4); rank correlation +1.00.
FIGARO's predicted retention minus DADA2's pass rate: -0.4 points (FIGARO (amplicon 508)). It predicts the filter only, so it is not expected to match the merged share.

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2,6) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 1): -33.0 points (95% interval -35.1 to -30.7); better in 0 of 6 samples, worse in 6
  AmpliTrim (maxEE 5): +9.8 points (95% interval +6.9 to +14.4); better in 6 of 6 samples, worse in 0
  FIGARO (amplicon 508): +1.8 points (95% interval +0.2 to +4.4); better in 5 of 6 samples, worse in 1
  AmpliTrim (FIGARO's maxEE 3,4): +1.8 points (95% interval -0.0 to +4.7); better in 5 of 6 samples, worse in 1
  full: -10.0 points (95% interval -11.4 to -8.7); better in 0 of 6 samples, worse in 6

Paired per-sample differences against FIGARO (amplicon 508):
  AmpliTrim (maxEE 2,6): -1.8 points (95% interval -4.4 to -0.2); better in 1 of 6 samples, worse in 5
  AmpliTrim (maxEE 1): -34.8 points (95% interval -38.4 to -31.9); better in 0 of 6 samples, worse in 6
  AmpliTrim (maxEE 5): +7.9 points (95% interval +6.5 to +10.1); better in 6 of 6 samples, worse in 0
  AmpliTrim (FIGARO's maxEE 3,4): -0.0 points (95% interval -0.3 to +0.3); better in 2 of 6 samples, worse in 4
  full: -11.8 points (95% interval -15.6 to -9.4); better in 0 of 6 samples, worse in 6

--- v1v2 (V1-V2, 16S, 33 samples)
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail
AmpliTrim (maxEE 2)             201/157      2 |     90.9% yield     91.3/91.0% |      91.2%   84.2%    82.1%   808 |  32.21%    179 15.50%
AmpliTrim (maxEE 1)             198/160      1 |     85.1% yield     85.3/85.1% |      85.2%   78.5%    76.6%   807 |  32.22%    180 15.44%
AmpliTrim (maxEE 5)             186/172      5 |     96.1% yield     97.5/96.1% |      97.5%   89.5%    87.4%   819 |  32.12%    178 15.56%
FIGARO (amplicon 346)           225/133    2,1 |  88.0% retained     88.4/88.2% |      88.4%   82.0%    80.0%   845 |  32.01%    182 15.85%
AmpliTrim (FIGARO's maxEE 2,1)  211/147    2,1 |     88.6% yield     88.8/88.6% |      88.8%   82.3%    80.3%   804 |  32.01%    180 15.69%
full                               none      2 |                                |      35.4%   29.3%    29.1%   475 |  38.28%    167 10.50%

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 346) was run on the 47% of the sampled pairs whose reads are 281 and 281 nt long (it needs reads of one length).
Across 5 settings, AmpliTrim's estimate minus DADA2: yield against merged share +6.5 points (range +6.3 to +6.8); filter pass +0.0 points (range +0.0 to +0.1). Rank correlation of the estimated yield with DADA2's merged share: +1.00. As a fraction of the estimated yield, DADA2's merged share is 0.93 (range 0.92 to 0.93).
The strict estimate (no mismatch allowed in the overlap) minus DADA2's merged share: -5.1 points (range -10.9 to -1.7); rank correlation +0.70.
FIGARO's predicted retention minus DADA2's pass rate: -0.4 points (FIGARO (amplicon 346)). It predicts the filter only, so it is not expected to match the merged share.

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 1): -5.7 points (95% interval -6.1 to -5.4); better in 0 of 33 samples, worse in 33
  AmpliTrim (maxEE 5): +5.3 points (95% interval +4.8 to +5.8); better in 33 of 33 samples, worse in 0
  FIGARO (amplicon 346): -2.2 points (95% interval -2.7 to -1.8); better in 4 of 33 samples, worse in 29
  AmpliTrim (FIGARO's maxEE 2,1): -1.9 points (95% interval -2.1 to -1.6); better in 0 of 33 samples, worse in 33
  full: -55.0 points (95% interval -56.4 to -53.6); better in 0 of 33 samples, worse in 33

Paired per-sample differences against FIGARO (amplicon 346):
  AmpliTrim (maxEE 2): +2.2 points (95% interval +1.8 to +2.7); better in 29 of 33 samples, worse in 4
  AmpliTrim (maxEE 1): -3.5 points (95% interval -4.0 to -3.0); better in 0 of 33 samples, worse in 33
  AmpliTrim (maxEE 5): +7.5 points (95% interval +7.1 to +8.0); better in 33 of 33 samples, worse in 0
  AmpliTrim (FIGARO's maxEE 2,1): +0.4 points (95% interval -0.1 to +0.8); better in 22 of 33 samples, worse in 11
  full: -52.8 points (95% interval -54.2 to -51.3); better in 0 of 33 samples, worse in 33

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
AmpliTrim (maxEE 2)             124/115      2 |     98.3% yield     98.6/98.3% |      98.5%   66.8%    64.6%  2237 |  38.37%    142 35.67%
AmpliTrim (maxEE 1)             120/119      1 |     96.4% yield     96.4/96.2% |      96.5%   63.3%    61.9%  2094 |  39.38%    145 34.13%
AmpliTrim (maxEE 5)             125/114      5 |     99.2% yield     99.8/99.1% |      99.8%   68.2%    65.7%  2372 |  38.11%    141 36.27%
FIGARO (amplicon 227)           120/119      1 |  98.4% retained     96.4/96.2% |      96.5%   63.3%    61.9%  2094 |  39.38%    145 34.13%
full                               none      2 |                                |      86.4%   54.2%    54.1%  1550 |  42.03%    146 29.36%

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 227) was run on the 86% of the sampled pairs whose reads are 207 and 207 nt long (it needs reads of one length).
Across 4 settings, AmpliTrim's estimate minus DADA2: yield against merged share +32.1 points (range +31.0 to +32.9); filter pass -0.0 points (range -0.0 to +0.0). Rank correlation of the estimated yield with DADA2's merged share: +1.00. As a fraction of the estimated yield, DADA2's merged share is 0.67 (range 0.66 to 0.69).
The strict estimate (no mismatch allowed in the overlap) minus DADA2's merged share: +25.0 points (range +23.0 to +26.6); rank correlation +1.00.
FIGARO's predicted retention minus DADA2's pass rate: +1.9 points (FIGARO (amplicon 227)). It predicts the filter only, so it is not expected to match the merged share.

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 1): -3.5 points (95% interval -4.0 to -3.1); better in 0 of 36 samples, worse in 36
  AmpliTrim (maxEE 5): +1.3 points (95% interval +1.1 to +1.5); better in 35 of 36 samples, worse in 1
  FIGARO (amplicon 227): -3.5 points (95% interval -4.0 to -3.1); better in 0 of 36 samples, worse in 36
  full: -12.7 points (95% interval -13.5 to -11.8); better in 0 of 36 samples, worse in 36

Paired per-sample differences against FIGARO (amplicon 227):
  AmpliTrim (maxEE 2): +3.5 points (95% interval +3.1 to +4.0); better in 36 of 36 samples, worse in 0
  AmpliTrim (maxEE 1): +0.0 points (95% interval +0.0 to +0.0); better in 0 of 36 samples, worse in 0
  AmpliTrim (maxEE 5): +4.9 points (95% interval +4.4 to +5.4); better in 36 of 36 samples, worse in 0
  full: -9.1 points (95% interval -9.8 to -8.4); better in 0 of 36 samples, worse in 36

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

--- mockB (V1-V3, 16S, 8 samples)
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail | found identical extra strains
AmpliTrim (maxEE 2)             279/248      2 |     20.2% yield     20.3/20.2% |      20.3%   19.9%    19.8%    72 |  87.90%     58  0.81% |     6    68.70%    66     3/3
AmpliTrim (maxEE 1)             280/247      1 |      6.5% yield       6.7/6.7% |       6.5%    5.7%     5.7%    36 |  93.02%     36  0.00% |     6    68.32%    30     3/3
AmpliTrim (maxEE 5)             277/250      5 |     56.1% yield     57.7/56.5% |      57.2%   55.8%    55.8%    74 |  89.86%     53  1.20% |     6    73.59%    68     3/3
FIGARO (amplicon 515)           279/248    6,9 |  78.8% retained     75.5/67.5% |      75.9%   74.3%    74.2%    76 |  91.20%     52  1.23% |     7    78.28%    69     3/3
AmpliTrim (FIGARO's maxEE 6,9)  274/253    6,9 |     70.3% yield     78.7/70.2% |      78.7%   76.7%    76.7%    74 |  90.05%     54  1.02% |     6    75.26%    68     3/3
full                               none      2 |                                |       2.9%    2.0%     2.0%    21 |  95.22%     21  0.00% |     4    54.35%    17     3/3

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 515) was run on the 90% of the sampled pairs whose reads are 280 and 283 nt long (it needs reads of one length).
Across 5 settings, AmpliTrim's estimate minus DADA2: yield against merged share -2.2 points (range -6.7 to +1.1); filter pass +0.1 points (range -0.4 to +0.5). Rank correlation of the estimated yield with DADA2's merged share: +1.00. As a fraction of the estimated yield, DADA2's merged share is 1.00 (range 0.84 to 1.10).
The strict estimate (no mismatch allowed in the overlap) minus DADA2's merged share: -35.1 points (range -63.3 to -1.1); rank correlation +0.70.
FIGARO's predicted retention minus DADA2's pass rate: +2.9 points (FIGARO (amplicon 515)). It predicts the filter only, so it is not expected to match the merged share.

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 1): -14.3 points (95% interval -15.6 to -12.8); better in 0 of 8 samples, worse in 8
  AmpliTrim (maxEE 5): +36.0 points (95% interval +34.9 to +37.2); better in 8 of 8 samples, worse in 0
  FIGARO (amplicon 515): +54.1 points (95% interval +50.3 to +58.0); better in 8 of 8 samples, worse in 0
  AmpliTrim (FIGARO's maxEE 6,9): +56.7 points (95% interval +55.1 to +58.7); better in 8 of 8 samples, worse in 0
  full: -18.0 points (95% interval -19.6 to -15.9); better in 0 of 8 samples, worse in 8

Paired per-sample differences against FIGARO (amplicon 515):
  AmpliTrim (maxEE 2): -54.1 points (95% interval -58.0 to -50.3); better in 0 of 8 samples, worse in 8
  AmpliTrim (maxEE 1): -68.4 points (95% interval -71.1 to -65.5); better in 0 of 8 samples, worse in 8
  AmpliTrim (maxEE 5): -18.1 points (95% interval -21.4 to -14.6); better in 0 of 8 samples, worse in 8
  AmpliTrim (FIGARO's maxEE 6,9): +2.6 points (95% interval +0.3 to +5.2); better in 5 of 8 samples, worse in 3
  full: -72.1 points (95% interval -74.7 to -69.3); better in 0 of 8 samples, worse in 8

--- mcm_v46 (V4-V6, 16S, 5 samples)
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail
AmpliTrim (maxEE 2)             273/265      2 |     42.1% yield     42.9/41.9% |      43.1%   41.6%    37.1%    26 |  98.02%     20  0.34%
AmpliTrim (maxEE 1)             258/280      1 |     19.5% yield     19.3/19.1% |      19.6%   18.7%    17.2%    22 |  98.69%     20  0.12%
AmpliTrim (maxEE 5)             269/273      5 |     73.2% yield     76.7/73.2% |      76.7%   74.6%    65.4%    28 |  97.19%     21  0.33%
FIGARO (amplicon 526)           270/268      4 |  71.3% retained     70.3/64.9% |      70.4%   68.6%    60.2%    26 |  97.33%     21  0.25%
AmpliTrim (FIGARO's maxEE 4)    271/267      4 |     65.1% yield     70.4/65.1% |      70.5%   68.8%    60.4%    28 |  97.26%     21  0.35%
full                               none      2 |                                |      31.8%   20.8%    19.7%    27 |  98.41%     22  0.18%

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 526) was run on the 98% of the sampled pairs whose reads are 278 and 281 nt long (it needs reads of one length).
Across 5 settings, AmpliTrim's estimate minus DADA2: yield against merged share -1.6 points (range -3.8 to +0.4); filter pass -0.2 points (range -0.3 to -0.0). Rank correlation of the estimated yield with DADA2's merged share: +1.00. As a fraction of the estimated yield, DADA2's merged share is 1.02 (range 0.98 to 1.06).
The strict estimate (no mismatch allowed in the overlap) minus DADA2's merged share: -17.7 points (range -32.6 to -1.4); rank correlation +0.70.
FIGARO's predicted retention minus DADA2's pass rate: +0.9 points (FIGARO (amplicon 526)). It predicts the filter only, so it is not expected to match the merged share.

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 1): only 5 samples, too few for an interval
  AmpliTrim (maxEE 5): only 5 samples, too few for an interval
  FIGARO (amplicon 526): only 5 samples, too few for an interval
  AmpliTrim (FIGARO's maxEE 4): only 5 samples, too few for an interval
  full: only 5 samples, too few for an interval

Paired per-sample differences against FIGARO (amplicon 526):

--- d6300_V3-V4 (?, 16S, 10 samples)
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail | found identical extra strains
AmpliTrim (maxEE 2)             224/218      2 |     93.6% yield     94.7/93.6% |      94.6%   90.6%    86.5%    11 | 100.00%     11  0.00% |    10    97.92%     1     8/8
AmpliTrim (maxEE 1)             224/218      1 |     87.7% yield     88.3/87.7% |      88.2%   84.5%    80.8%    11 | 100.00%     11  0.00% |    10    97.88%     1     8/8
AmpliTrim (maxEE 5)             224/218      5 |     96.8% yield     99.0/96.9% |      98.8%   94.5%    90.2%    11 | 100.00%     11  0.00% |    10    97.95%     1     8/8
FIGARO (amplicon 430)           224/218      1 |  88.8% retained     88.3/87.7% |      88.2%   84.5%    80.8%    11 | 100.00%     11  0.00% |    10    97.88%     1     8/8
full                           0/0         2 | DADA2 could not run: DADA2 failed: Error: Input sequences must all be longer than the kmer-size (5).
Execution halted

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 430) was run on the 8% of the sampled pairs whose reads are 227 and 227 nt long (it needs reads of one length).
Across 4 settings, AmpliTrim's estimate minus DADA2: yield against merged share +2.9 points (range +2.3 to +3.2); filter pass +0.1 points (range +0.1 to +0.1). Rank correlation of the estimated yield with DADA2's merged share: +1.00. As a fraction of the estimated yield, DADA2's merged share is 0.97 (range 0.96 to 0.98).
The strict estimate (no mismatch allowed in the overlap) minus DADA2's merged share: +0.2 points (range -1.8 to +1.2); rank correlation +1.00.
FIGARO's predicted retention minus DADA2's pass rate: +0.6 points (FIGARO (amplicon 430)). It predicts the filter only, so it is not expected to match the merged share.

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 1): -6.1 points (95% interval -6.5 to -5.7); better in 0 of 10 samples, worse in 10
  AmpliTrim (maxEE 5): +4.0 points (95% interval +3.5 to +4.6); better in 10 of 10 samples, worse in 0
  FIGARO (amplicon 430): -6.1 points (95% interval -6.5 to -5.7); better in 0 of 10 samples, worse in 10

Paired per-sample differences against FIGARO (amplicon 430):
  AmpliTrim (maxEE 2): +6.1 points (95% interval +5.7 to +6.5); better in 10 of 10 samples, worse in 0
  AmpliTrim (maxEE 1): +0.0 points (95% interval +0.0 to +0.0); better in 0 of 10 samples, worse in 0
  AmpliTrim (maxEE 5): +10.0 points (95% interval +9.3 to +10.8); better in 10 of 10 samples, worse in 0

--- d6300_V4-V5 (?, 16S, 3 samples)
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail | found identical extra strains
AmpliTrim (maxEE 2)             282/280      2 |     63.6% yield     63.7/63.6% |      63.7%   57.2%    47.5%    11 | 100.00%     10  0.08% |     9    98.75%     2     8/9
AmpliTrim (maxEE 1)             282/280      1 |     51.0% yield     51.1/51.0% |      51.0%   45.5%    38.1%    10 | 100.00%     10  0.00% |     9    98.85%     1     8/9
AmpliTrim (maxEE 5)             282/280      5 |     77.1% yield     77.7/77.5% |      77.4%   69.5%    57.7%    11 | 100.00%     10  0.07% |     9    98.82%     2     8/9
full                               none      2 |                                |      71.7%   63.9%    53.9%    11 | 100.00%     10  0.07% |     9    98.90%     2     8/9

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 550): FIGARO failed (exit 1).
e>
    main()
  File "C:\figaro\figaro-master\figaro\figaro.py", line 380, in main
    trimParameterPrediction.performAnalysisLite(
  File "C:\figaro\figaro-master\figaro\trimParameterPrediction.py", line 780, in performAnalysisLite
    resultTable = runTrimParameterTestLite(
                  ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\figaro\figaro-master\figaro\trimParameterPrediction.py", line 552, in runTrimParameterTestLite
    forwardExpectedErrors = forwardExpectedErrorMatrix[
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
IndexError: index -1 is out of bounds for axis 0 with size 0

Across 3 settings, AmpliTrim's estimate minus DADA2: yield against merged share +6.7 points (range +5.6 to +8.0); filter pass +0.2 points (range -0.0 to +0.4). As a fraction of the estimated yield, DADA2's merged share is 0.90 (range 0.89 to 0.90).

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 1): only 3 samples, too few for an interval
  AmpliTrim (maxEE 5): only 3 samples, too few for an interval
  full: only 3 samples, too few for an interval

--- wastewater_V3-V4 (?, 16S, 9 samples)
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail
AmpliTrim (maxEE 2)             254/186      2 |     48.8% yield     53.9/49.0% |      53.7%   43.6%    35.2%   124 |  69.65%     74  2.91%
AmpliTrim (maxEE 1)             254/186      1 |     25.9% yield     27.1/26.2% |      26.7%   20.9%    17.7%   103 |  69.54%     70  1.86%
AmpliTrim (maxEE 5)             247/199      5 |     72.9% yield     82.4/72.9% |      82.2%   65.7%    52.6%   111 |  70.45%     73  2.14%
FIGARO (amplicon 428)           247/193      5 |  79.7% retained     83.3/64.6% |      83.1%   66.7%    53.3%   118 |  70.02%     72  2.40%
full                               none      2 |                                |       0.3%    0.2%     0.2%     8 | 100.00%      8  0.00%

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 428) was run on the 61% of the sampled pairs whose reads are 284 and 280 nt long (it needs reads of one length).
Across 4 settings, AmpliTrim's estimate minus DADA2: yield against merged share +3.9 points (range -2.1 to +7.2); filter pass +0.2 points (range +0.2 to +0.4). Rank correlation of the estimated yield with DADA2's merged share: +0.80. As a fraction of the estimated yield, DADA2's merged share is 0.91 (range 0.80 to 1.03).
The strict estimate (no mismatch allowed in the overlap) minus DADA2's merged share: -26.4 points (range -44.8 to -3.1); rank correlation +0.40.
FIGARO's predicted retention minus DADA2's pass rate: -3.3 points (FIGARO (amplicon 428)). It predicts the filter only, so it is not expected to match the merged share.

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 1): -22.7 points (95% interval -24.8 to -20.8); better in 0 of 9 samples, worse in 9
  AmpliTrim (maxEE 5): +22.1 points (95% interval +20.3 to +23.9); better in 9 of 9 samples, worse in 0
  FIGARO (amplicon 428): +23.1 points (95% interval +21.3 to +25.0); better in 9 of 9 samples, worse in 0
  full: -43.4 points (95% interval -45.0 to -41.6); better in 0 of 9 samples, worse in 9

Paired per-sample differences against FIGARO (amplicon 428):
  AmpliTrim (maxEE 2): -23.1 points (95% interval -25.0 to -21.3); better in 0 of 9 samples, worse in 9
  AmpliTrim (maxEE 1): -45.9 points (95% interval -49.6 to -42.3); better in 0 of 9 samples, worse in 9
  AmpliTrim (maxEE 5): -1.0 points (95% interval -1.4 to -0.7); better in 0 of 9 samples, worse in 9
  full: -66.6 points (95% interval -69.5 to -63.3); better in 0 of 9 samples, worse in 9

--- spikein_V3-V4 (?, 16S, 12 samples)
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail
AmpliTrim (maxEE 2)             222/218      2 |     87.3% yield     87.0/86.4% |      87.6%   83.6%    83.3%   253 |  59.01%     98  3.47%
AmpliTrim (maxEE 1)             230/210      1 |     77.5% yield     76.9/76.7% |      77.4%   73.5%    73.3%   218 |  59.85%     96  3.07%
AmpliTrim (maxEE 5)             231/209      5 |     94.7% yield     95.8/94.1% |      96.2%   90.5%    90.3%   225 |  59.07%     93  3.54%
FIGARO (amplicon 428)           232/208    2,1 |  84.9% retained     81.1/80.9% |      81.5%   77.2%    77.1%   218 |  60.31%     97  3.08%
AmpliTrim (FIGARO's maxEE 2,1)  230/210    2,1 |     82.8% yield     82.2/82.0% |      82.8%   78.6%    78.4%   225 |  59.20%     98  3.15%
full                               none      2 |                                |      86.8%   81.7%    81.6%   207 |  59.74%     96  2.98%

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 428) was run on the 25% of the sampled pairs whose reads are 233 and 228 nt long (it needs reads of one length).
Across 5 settings, AmpliTrim's estimate minus DADA2: yield against merged share +3.4 points (range +2.9 to +3.7); filter pass -0.5 points (range -0.6 to -0.3). Rank correlation of the estimated yield with DADA2's merged share: +1.00. As a fraction of the estimated yield, DADA2's merged share is 0.96 (range 0.95 to 0.97).
The strict estimate (no mismatch allowed in the overlap) minus DADA2's merged share: -2.3 points (range -5.5 to -0.1); rank correlation +1.00.
FIGARO's predicted retention minus DADA2's pass rate: +3.4 points (FIGARO (amplicon 428)). It predicts the filter only, so it is not expected to match the merged share.

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 1): -10.1 points (95% interval -10.7 to -9.5); better in 0 of 12 samples, worse in 12
  AmpliTrim (maxEE 5): +6.9 points (95% interval +6.4 to +7.3); better in 12 of 12 samples, worse in 0
  FIGARO (amplicon 428): -6.3 points (95% interval -7.5 to -5.3); better in 0 of 12 samples, worse in 12
  AmpliTrim (FIGARO's maxEE 2,1): -5.0 points (95% interval -5.4 to -4.6); better in 0 of 12 samples, worse in 12
  full: -1.8 points (95% interval -2.2 to -1.4); better in 0 of 12 samples, worse in 12

Paired per-sample differences against FIGARO (amplicon 428):
  AmpliTrim (maxEE 2): +6.3 points (95% interval +5.3 to +7.5); better in 12 of 12 samples, worse in 0
  AmpliTrim (maxEE 1): -3.8 points (95% interval -4.6 to -2.9); better in 0 of 12 samples, worse in 12
  AmpliTrim (maxEE 5): +13.2 points (95% interval +12.2 to +14.4); better in 12 of 12 samples, worse in 0
  AmpliTrim (FIGARO's maxEE 2,1): +1.3 points (95% interval +0.4 to +2.5); better in 10 of 12 samples, worse in 2
  full: +4.5 points (95% interval +3.6 to +5.5); better in 12 of 12 samples, worse in 0

--- swabs_V3-V4 (?, 16S, 36 samples)
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail
AmpliTrim (maxEE 2)             224/218      2 |     84.3% yield     84.9/84.2% |      85.0%   77.0%    72.9%  1589 |  36.83%    155 19.68%
AmpliTrim (maxEE 1)             224/218      1 |     78.2% yield     78.6/78.2% |      78.6%   71.1%    67.3%  1548 |  37.05%    149 20.15%
AmpliTrim (maxEE 5)             224/218      5 |     88.4% yield     89.9/88.3% |      90.0%   81.6%    77.1%  1598 |  36.68%    155 19.67%
FIGARO (amplicon 430)           224/218      1 |  86.3% retained     78.6/78.2% |      78.6%   71.1%    67.3%  1548 |  37.05%    149 20.15%
full                           0/0         2 | DADA2 could not run: DADA2 failed: Error: Input sequences must all be longer than the kmer-size (5).
Execution halted

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
FIGARO (amplicon 430) was run on the 9% of the sampled pairs whose reads are 229 and 222 nt long (it needs reads of one length).
Across 4 settings, AmpliTrim's estimate minus DADA2: yield against merged share +7.0 points (range +6.7 to +7.2); filter pass -0.1 points (range -0.1 to -0.0). Rank correlation of the estimated yield with DADA2's merged share: +1.00. As a fraction of the estimated yield, DADA2's merged share is 0.91 (range 0.91 to 0.92).
The strict estimate (no mismatch allowed in the overlap) minus DADA2's merged share: +1.7 points (range -1.2 to +3.2); rank correlation +1.00.
FIGARO's predicted retention minus DADA2's pass rate: +7.7 points (FIGARO (amplicon 430)). It predicts the filter only, so it is not expected to match the merged share.

Per-sample difference in the share of pairs DADA2 merged, against AmpliTrim (maxEE 2) (the first method unless --baseline says otherwise); mean, bootstrap 95% interval over samples:
  AmpliTrim (maxEE 1): -5.9 points (95% interval -6.8 to -5.1); better in 0 of 36 samples, worse in 34
  AmpliTrim (maxEE 5): +4.6 points (95% interval +3.9 to +5.3); better in 34 of 36 samples, worse in 0
  FIGARO (amplicon 430): -5.9 points (95% interval -6.8 to -5.1); better in 0 of 36 samples, worse in 34

Paired per-sample differences against FIGARO (amplicon 430):
  AmpliTrim (maxEE 2): +5.9 points (95% interval +5.1 to +6.8); better in 34 of 36 samples, worse in 0
  AmpliTrim (maxEE 1): +0.0 points (95% interval +0.0 to +0.0); better in 0 of 36 samples, worse in 0
  AmpliTrim (maxEE 5): +10.6 points (95% interval +9.0 to +12.1); better in 34 of 36 samples, worse in 0

```

## Not testable with the data on hand

- An independent mock community (Zymo D6321, PRJEB67827, with Zymo's own reference sequences): no data on hand (python validation\check_build.py --download mockB).
- V3-V4 2x250 reads (tight overlap on real data) and V4-V5 (PRJNA971391): no data on hand (check_build.py --download v3v4 / v4v5); mock_clip250 is an emulation, not a replacement.
- Other platforms (binned quality scores): no data on hand beyond the exactness checks already made.
- Housekeeping: run the CI workflow, push to GitHub, choose a licence, archive for a DOI, test on Windows and Linux, regenerate Figures 3 and 5 and Table 6 from the saved tables, verify the references.
