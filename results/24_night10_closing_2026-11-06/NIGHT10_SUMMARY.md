# Night 10: the closing run

Written 2026-11-07 12:16. Package: not checked in this start (see the log).
Pilot: no.

## Steps

| Step | Status | Detail |
| --- | --- | --- |
| version | done | ok |
| accept | done | mockB, v4, its: C:\data\runs\night10_closing_2026-11-06\accept\RELEASE_CHECK_REPORT.md |
| cli__negative | done | ok: exit 3 and a message, no traceback |
| cli_d6300_V3-V4 | done |  |
| cli_d6300_V4-V5 | done |  |
| cli_its | done |  |
| cli_mcm_v12 | done |  |
| cli_mcm_v46 | done |  |
| cli_miseqsop_mock | done |  |
| cli_mockA_high | done |  |
| cli_mockB | done |  |
| cli_spikein_V3-V4 | done |  |
| cli_swabs_V3-V4 | done |  |
| cli_v1v2 | done |  |
| cli_v4 | done |  |
| cli_wastewater_V3-V4 | done |  |
| tail | done | C:\data\runs\night10_closing_2026-11-06\tail\tail_summary.md |
| coverage_d6300_V3-V4 | done |  |
| coverage_d6300_V4-V5 | done |  |
| coverage_mcm_v12 | done |  |
| coverage_mcm_v46 | done |  |
| coverage_miseqsop_mock | done |  |
| coverage_mockA_high | done |  |
| coverage_mockB | done |  |
| coverage_spikein_V3-V4 | done |  |
| coverage_swabs_V3-V4 | done |  |
| coverage_v1v2 | done |  |
| coverage_v4 | done |  |
| coverage_wastewater_V3-V4 | done |  |
| battery | skipped | give the new 16S datasets with --new NAME ... (names registered in amplitrim_paths.json) |
| its | done | C:\data\runs\night10_closing_2026-11-06\its_new\compare_methods.txt |
| overlap | done | C:\data\runs\night10_closing_2026-11-06\overlap\overlap_results.md |
| grid | done | C:\data\runs\night10_closing_2026-11-06\grid |

## The command line on every dataset (Supplementary Table S4: run time and memory; the repeat and --min-overlap checks)

| Dataset | Exit | Seconds | Peak MB | Pairs analysed | Cut F/R | maxEE | minOverlap | Warnings | Checks |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| d6300_V3-V4 | 0 | 29.2 | 227 | 48758 | 224/218 | 2 | 12 | 0 | - |
| d6300_V4-V5 | 0 | 55.4 | 339 | 49114 | 282/280 | 2,3 | 12 | 2 | - |
| its | 0 | 53.1 | 186 | 49720 | 0/0 | 2 | 12 | 2 | - |
| mcm_v12 | 0 | 70.1 | 232 | 49713 | 160/165 | 2 | 12 | 0 | - |
| mcm_v46 | 0 | 141.4 | 336 | 49302 | 273/265 | 4,3 | 12 | 2 | - |
| miseqsop_mock | 0 | 4.6 | 52 | 4779 | 132/134 | 2 | 12 | 0 | - |
| mockA_high | 0 | 61.4 | 352 | 47380 | 273/247 | 2,3 | 12 | 2 | repeat: same; min_overlap_15: ok; cut_15: 275/248; min_overlap_20: ok; cut_20: 277/251 |
| mockB | 0 | 45.0 | 326 | 43922 | 274/253 | 4,8 | 12 | 3 | - |
| spikein_V3-V4 | 0 | 68.3 | 220 | 49885 | 229/210 | 2 | 12 | 0 | - |
| swabs_V3-V4 | 0 | 53.9 | 223 | 49505 | 224/218 | 2 | 12 | 1 | - |
| v1v2 | 0 | 48.0 | 209 | 49235 | 195/168 | 2 | 12 | 1 | repeat: same; min_overlap_15: ok; cut_15: 196/170; min_overlap_20: ok; cut_20: 203/168 |
| v4 | 0 | 59.6 | 168 | 49720 | 124/115 | 2 | 12 | 0 | - |
| wastewater_V3-V4 | 0 | 118.2 | 345 | 49440 | 260/182 | 4,3 | 12 | 2 | - |

## The coverage setting (share of the longest amplicons left out), maxEE 2: DADA2's merged share, and AmpliTrim's own estimate for the same row

| Dataset | Share left out | Cut F/R | Filter pass | AmpliTrim's estimate | DADA2 merged | Estimate minus merged (points) | Strains | Reads in exact ASVs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| d6300_V3-V4 | 0.2% (default) | 224/218 | 94.6% | 93.6% | 90.6% | +3.0 | 8/8 | 97.9% |
| d6300_V3-V4 | 0% | 225/218 | 85.2% | 84.9% | 81.5% | +3.4 | 8/8 | 97.9% |
| d6300_V3-V4 | 1% | 224/218 | 94.6% | 93.6% | 90.6% | +3.0 | 8/8 | 97.9% |
| d6300_V3-V4 | 5% | 224/218 | 94.6% | 93.6% | 90.6% | +3.0 | 8/8 | 97.9% |
| d6300_V4-V5 | 0.2% (default) | 282/280 | 63.7% | 63.6% | 57.2% | +6.4 | 8/9 | 98.8% |
| d6300_V4-V5 | 0% | 282/281 | 1.1% | 1.0% | 0.8% | +0.3 | 4/9 | 31.6% |
| d6300_V4-V5 | 1% | 268/118 | 92.9% | 90.7% | 89.8% | +1.0 | 8/9 | 99.9% |
| d6300_V4-V5 | 5% | 268/118 | 92.9% | 90.7% | 89.8% | +1.0 | 8/9 | 99.9% |
| mcm_v12 | 0.2% (default) | 155/170 | 96.4% | 96.3% | 95.9% | +0.4 | - | - |
| mcm_v12 | 0% | 160/168 | 96.4% | 96.2% | 95.8% | +0.4 | - | - |
| mcm_v12 | 1% | 155/170 | 96.4% | 96.3% | 95.9% | +0.4 | - | - |
| mcm_v12 | 5% | 144/170 | 96.6% | 94.2% | 93.8% | +0.3 | - | - |
| mcm_v46 | 0.2% (default) | 273/265 | 43.1% | 42.1% | 41.6% | +0.4 | - | - |
| mcm_v46 | 0% | 274/265 | 42.6% | 42.0% | 40.5% | +1.5 | - | - |
| mcm_v46 | 1% | 273/265 | 43.1% | 42.1% | 41.6% | +0.4 | - | - |
| mcm_v46 | 5% | 273/265 | 43.1% | 42.1% | 41.6% | +0.4 | - | - |
| miseqsop_mock | 0.2% (default) | 132/134 | 98.2% | 96.4% | 97.1% | -0.8 | 19/21 | 100.0% |
| miseqsop_mock | 0% | 132/134 | 98.2% | 96.4% | 97.1% | -0.8 | 19/21 | 100.0% |
| miseqsop_mock | 1% | 132/134 | 98.2% | 96.4% | 97.1% | -0.8 | 19/21 | 100.0% |
| miseqsop_mock | 5% | 132/134 | 98.2% | 96.4% | 97.1% | -0.8 | 19/21 | 100.0% |
| mockA_high | 0.2% (default) | 277/243 | 64.7% | 64.5% | 62.7% | +1.8 | 12/14 | 99.7% |
| mockA_high | 0% | 280/268 | 51.3% | 51.2% | 49.3% | +1.9 | 11/14 | 99.8% |
| mockA_high | 1% | 277/240 | 65.8% | 65.4% | 63.9% | +1.5 | 11/14 | 99.7% |
| mockA_high | 5% | 276/235 | 67.5% | 65.8% | 64.8% | +1.0 | 10/14 | 99.7% |
| mockB | 0.2% (default) | 279/248 | 20.3% | 20.2% | 19.9% | +0.4 | 3/3 | 68.7% |
| mockB | 0% | 280/254 | 15.8% | 15.8% | 13.9% | +1.9 | 3/3 | 73.0% |
| mockB | 1% | 279/248 | 20.3% | 20.2% | 19.9% | +0.4 | 3/3 | 68.7% |
| mockB | 5% | 279/248 | 20.3% | 20.2% | 19.9% | +0.4 | 3/3 | 68.7% |
| spikein_V3-V4 | 0.2% (default) | 222/218 | 87.6% | 87.3% | 83.6% | +3.7 | - | - |
| spikein_V3-V4 | 0% | 234/229 | 12.9% | 13.2% | 11.3% | +1.8 | - | - |
| spikein_V3-V4 | 1% | 216/223 | 87.6% | 86.7% | 83.6% | +3.2 | - | - |
| spikein_V3-V4 | 5% | 216/223 | 87.6% | 86.7% | 83.6% | +3.2 | - | - |
| swabs_V3-V4 | 0.2% (default) | 224/218 | 85.0% | 84.3% | 77.0% | +7.3 | - | - |
| swabs_V3-V4 | 0% | 225/218 | 82.9% | 82.5% | 75.1% | +7.4 | - | - |
| swabs_V3-V4 | 1% | 224/218 | 85.0% | 84.3% | 77.0% | +7.3 | - | - |
| swabs_V3-V4 | 5% | 224/218 | 85.0% | 84.3% | 77.0% | +7.3 | - | - |
| v1v2 | 0.2% (default) | 201/157 | 91.2% | 90.9% | 84.2% | +6.7 | - | - |
| v1v2 | 0% | 279/261 | 51.8% | 51.8% | 45.5% | +6.3 | - | - |
| v1v2 | 1% | 198/157 | 91.5% | 90.5% | 84.2% | +6.4 | - | - |
| v1v2 | 5% | 198/157 | 91.5% | 90.5% | 84.2% | +6.4 | - | - |
| v4 | 0.2% (default) | 124/115 | 98.5% | 98.3% | 66.8% | +31.5 | - | - |
| v4 | 0% | 141/124 | 98.2% | 98.2% | 64.0% | +34.3 | - | - |
| v4 | 1% | 124/114 | 98.5% | 97.9% | 67.2% | +30.7 | - | - |
| v4 | 5% | 115/105 | 98.8% | 96.2% | 72.3% | +23.9 | - | - |
| wastewater_V3-V4 | 0.2% (default) | 254/186 | 53.7% | 48.8% | 43.6% | +5.2 | - | - |
| wastewater_V3-V4 | 0% | 254/186 | 53.7% | 48.8% | 43.6% | +5.2 | - | - |
| wastewater_V3-V4 | 1% | 254/186 | 53.7% | 48.8% | 43.6% | +5.2 | - | - |
| wastewater_V3-V4 | 5% | 256/187 | 51.9% | 49.0% | 41.4% | +7.6 | - | - |

## The longest amplicons

# The longest amplicons of ready

15000 pairs (at most 5000 per sample) gave 13675 merged sequences; lengths: median 374, longest 550.
Classified: the 103 sequences longer than 374 nt (the longest 1.0%), against a control of 103 sequences within 5 nt of the median.

| Group | Best hit in SILVA | n | share | median identity (%) |
| --- | --- | --- | --- | --- |
| long | Eukaryota | 101 | 98.1% | 99.8 |
| long | Bacteria | 2 | 1.9% | 99.8 |
| control | Bacteria | 103 | 100.0% | 100.0 |

How far to trust the hits (identity is that of the best hit of each query to SILVA; the merged reads are not quality filtered):

| Group | queries | hit lines | queries with a hit | identity at least 97% | identity at least 90% | most frequent best hits (last two fields of the SILVA label) |
| --- | --- | --- | --- | --- | --- | --- |
| long | 103 | 206 | 103 | 94% | 98% | Saccharomyces / Hordeum vulgare subsp. vulgare (domesticated barley) (85); Saccharomyces / Clostridium sp. D53t1_180928_C8 (11); Limosilactobacillus / Limosilactobacillus fermentum (1); Cryptococcus / Klebsiella pneumoniae (1); Salmonella / Salmonella sp. KF (1); Saccharomyces / Saccharomyces cerevisiae (1) |
| control | 103 | 206 | 103 | 95% | 100% | Bacillus / Bacillus subtilis (18); Escherichia-Shigella / Escherichia coli (14); Enterococcus / Enterococcus faecalis (11); Limosilactobacillus / Limosilactobacillus fermentum (11); Salmonella / Salmonella enterica subsp. enterica serovar Indiana (6); Staphylococcus / Staphylococcus aureus (4) |

Read it as: if the long group is mostly Eukaryota while the control is Bacteria, the long amplicons are 18S of eukaryotes amplified by the same primers; if both are Bacteria,
they are long 16S. A long group with mostly 'no hit' and a control with hits says the long sequences are not in SILVA (or are not rRNA); if the control has no hits either,
the search does not work on this dataset (check the SILVA file and the identity threshold).


## A second ITS dataset

```
method                            trunc  maxEE |  own prediction AmpliTrim est. | DADA2 pass  merged  no chim  ASVs |  top 15 >=0.1%   tail
AmpliTrim (maxEE 2)                none      2 |     82.1% yield     82.9/82.1% |      82.9%   14.0%    14.0%   180 |  54.23%    135  2.46%

own prediction: AmpliTrim's estimated yield (pairs passing the filter and merging), or FIGARO's predicted retention (the filter only).
AmpliTrim est.: AmpliTrim's engine applied to that method's setting, as filter pass / yield, so every row is judged by one estimator.
```

## The minimum overlap on a hold-out mock

# Minimum-overlap test (register section 27)

| dataset | arm | k | cut F/R | maxEE | pass % | merged % | variants | strains | reads in exact ASVs % | extra ASVs | ASVs | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| miseqsop_mock | S | 10 | 132/134 | 2 | 98.2 | 97.1 | 20 | 19/21 | 100.00 | 0 | 20 |  |
| miseqsop_mock | S | 15 | 132/134 | 2 | 98.2 | 0.0 | 0 | 0/21 | 0.00 | 0 | 0 |  |
| miseqsop_mock | S | 20 | 132/134 | 2 | 98.2 | 0.0 | 0 | 0/21 | 0.00 | 0 | 0 |  |
| miseqsop_mock | S | 25 | 132/134 | 2 | 98.2 | 0.0 | 0 | 0/21 | 0.00 | 0 | 0 |  |
| miseqsop_mock | T | 10 | 132/132 | 2 | 98.2 | 97.2 | 20 | 19/21 | 100.00 | 0 | 20 |  |
| miseqsop_mock | T | 12 | 132/134 | 2 | 98.2 | 97.1 | 20 | 19/21 | 100.00 | 0 | 20 |  |
| miseqsop_mock | T | 15 | 132/137 | 2 | 98.1 | 97.0 | 20 | 19/21 | 100.00 | 0 | 20 |  |
| miseqsop_mock | T | 20 | 132/142 | 2 | 98.0 | 96.6 | 20 | 19/21 | 100.00 | 0 | 20 |  |
| miseqsop_mock | T | 25 | 132/147 | 2 | 97.9 | 96.6 | 20 | 19/21 | 100.00 | 0 | 20 |  |

Arm T: the cut follows k. Arm S: the cut of k = 12, only minOverlap changes.

## Verdicts
- **P-O1 not judged: only 1 of 4 datasets**: minOverlap 10 on the 12 cut: same merged share (0.1 points), no ASV that 12 lacks (1 of 1 datasets)
- **P-O2 not judged: only 1 of 4 datasets**: k = 12: reads in exact ASVs within 1.0 point of the best k, strains equal the best (1 of 1 datasets)
- **P-O3 not judged: only 1 of 4 datasets**: k = 12: no more than 2 unexpected ASVs more than at k = 20 (1 of 1 datasets)
- P-O4 (arm T): merged share at k = 25 at least 1 point below k = 12: 0 of 1 datasets (descriptive)
- P-O4 (arm S): merged share at k = 25 at least 1 point below k = 12: 1 of 1 datasets (descriptive)

ASV sets: see overlap_results_asv_sets.tsv; two runs with the same fingerprint have exactly the same ASVs.


## The release check on the installed package

# Release check

The criterion (P30) is in TEST_REGISTER.md, section 21, and was fixed before this ran.

## Verdict

- **P30** not decided (not all 12 datasets were run, or a tested result was not found): the released package recommends exactly the settings that were run through DADA2 on every dataset: 2 of 3 the same, 1 different.

| dataset | tested | what was tested | released package | the same |
|---|---|---|---|---|
| its | night 3, arm A | 0/0, maxEE 2 | 0/0, maxEE 2 | yes |
| v4 | night 3, arm A | 124/115, maxEE 2 | 124/115, maxEE 2 | yes |
| mockB | night 4b, arm H | 277/250, maxEE 4,5 | 274/253, maxEE 4,8 | **NO** |

Where the settings differ, the DADA2 results of the nights are not claimed for the released package: DADA2 has to be run at the released settings.

Next: send this file.


## Where the other scripts wrote

- battery (night4.py): its own folder and NIGHT4_REPORT.md, printed in C:\data\runs\night10_closing_2026-11-06\night10.log
- grid (overnight.py --only landscape): C:\data\runs\night10_closing_2026-11-06\grid (OVERNIGHT_SUMMARY.md)

The criteria are in TEST_REGISTER.md, section 29; the verdicts are written there as section 30, after this file has been read, not here.
