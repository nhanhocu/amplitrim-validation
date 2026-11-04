# Night 8: calibration of the expected errors (T-cal) and the truth test, on the Kinnex-16S data of ATCC MSA-1003

Run on 2026-10-15; folder C:\data\runs\18_night8_truth. Gates and predictions: FUTURE.md of the archive (written on 15 October 2026, before the run). Tools: Python 3.12.15; numpy 2.5.3; cutadapt 5.2; R and DADA2 R version 4.6.1 (2026-06-24 ucrt) | DADA2 1.40.0.

## Steps

- pilot: done in 2 min (one DADA2 run on 19,965 reads took 1.8 min; a run of about 100,000 reads would take at least 9 min if the time grew linearly (it grows faster), so the 7 conditions of the truth test on two library types need at least 2.1 h)
- tcal: done in 3 min (T-cal-1 NOT MET; T-cal-2 MET; T-cal-3 MET)
- truth_monomer: done in 109 min (rule gives maxEE 2; T2 NOT MET, T3 NOT MET, T5 MET, T6 MET)
- truth_kinnex: done in 221 min (rule gives maxEE 3; T2 NOT MET, T3 NOT MET, T5 MET, T6 MET)

## T-cal: are the expected errors calibrated?

**Gate (T-cal-1): NOT MET.**

- Monomer, [1, 2) expected errors: differences / expected errors = 2.41 (3,714 reads): OUTSIDE 0.5 to 2.0
- Monomer, [2, 3) expected errors: differences / expected errors = 2.05 (2,139 reads): OUTSIDE 0.5 to 2.0
- Monomer, [3, 5) expected errors: differences / expected errors = 1.83 (2,597 reads): inside 0.5 to 2.0
- Monomer, [5, 10) expected errors: differences / expected errors = 1.55 (3,394 reads): inside 0.5 to 2.0
- Monomer, 10 and over expected errors: differences / expected errors = 1.43 (1,937 reads): inside 0.5 to 2.0
- Kinnex, [1, 2) expected errors: differences / expected errors = 2.03 (7,410 reads): OUTSIDE 0.5 to 2.0
- Kinnex, [2, 3) expected errors: differences / expected errors = 1.75 (3,938 reads): inside 0.5 to 2.0
- Kinnex, [3, 5) expected errors: differences / expected errors = 1.55 (4,945 reads): inside 0.5 to 2.0
- Kinnex, [5, 10) expected errors: differences / expected errors = 1.40 (5,284 reads): inside 0.5 to 2.0
- Kinnex, 10 and over expected errors: differences / expected errors = 1.21 (3,187 reads): inside 0.5 to 2.0

**Gate (T-cal-2): MET.**

- Monomer against Kinnex, [1, 2): ratio 2.41 against 2.03, a factor of 1.18: within 1.5
- Monomer against Kinnex, [2, 3): ratio 2.05 against 1.75, a factor of 1.17: within 1.5
- Monomer against Kinnex, [3, 5): ratio 1.83 against 1.55, a factor of 1.18: within 1.5
- Monomer against Kinnex, [5, 10): ratio 1.55 against 1.40, a factor of 1.11: within 1.5
- Monomer against Kinnex, 10 and over: ratio 1.43 against 1.21, a factor of 1.19: within 1.5

**Gate (T-cal-3): MET.**

- Monomer, [1, 2): rescued 2.38 (506 reads) against the others 2.41 (3,208 reads), a factor of 1.01: within 1.5
- Monomer, [2, 3): rescued 2.00 (287 reads) against the others 2.06 (1,852 reads), a factor of 1.03: within 1.5
- Monomer, [3, 5): rescued 1.87 (414 reads) against the others 1.82 (2,183 reads), a factor of 1.03: within 1.5
- Monomer, [5, 10): rescued 1.64 (626 reads) against the others 1.52 (2,768 reads), a factor of 1.07: within 1.5
- Monomer, 10 and over: rescued 1.43 (455 reads) against the others 1.43 (1,482 reads), a factor of 1.00: within 1.5
- Kinnex, [1, 2): rescued 2.12 (182 reads) against the others 2.03 (7,228 reads), a factor of 1.04: within 1.5
- Kinnex, [2, 3): rescued 1.78 (156 reads) against the others 1.75 (3,782 reads), a factor of 1.02: within 1.5
- Kinnex, [3, 5): rescued 1.57 (329 reads) against the others 1.55 (4,616 reads), a factor of 1.01: within 1.5
- Kinnex, [5, 10): rescued 1.42 (531 reads) against the others 1.40 (4,753 reads), a factor of 1.01: within 1.5
- Kinnex, 10 and over: rescued 1.22 (548 reads) against the others 1.21 (2,639 reads), a factor of 1.02: within 1.5

The floor is the mean number of differences of the matched reads with fewer than 0.05 expected errors: what the quality scores cannot see (PCR errors, chimeras, real divergence).

## Monomer

59,908 reads cut between the primers, 59,467 matched (99.3%), of which 6,649 rescued by the indel-tolerant search; floor 0.612 differences (32,781 reads).

| expected errors | reads | mean expected | mean differences | median | differences / expected | rescued reads | rescued ratio | other reads | other ratio |
|---|---|---|---|---|---|---|---|---|---|
| [0, 0.05) | 32,781 | 0.003 | 0.612 | 0.0 | 198.24 | 3,010 | 184.35 | 29,771 | 199.87 |
| [0.05, 0.25) | 4,992 | 0.129 | 1.092 | 1.0 | 8.48 | 506 | 8.57 | 4,486 | 8.47 |
| [0.25, 1) | 7,913 | 0.542 | 1.756 | 1.0 | 3.24 | 845 | 3.74 | 7,068 | 3.18 |
| [1, 2) | 3,714 | 1.431 | 3.441 | 3.0 | 2.41 | 506 | 2.38 | 3,208 | 2.41 |
| [2, 3) | 2,139 | 2.458 | 5.032 | 4.0 | 2.05 | 287 | 2.00 | 1,852 | 2.06 |
| [3, 5) | 2,597 | 3.917 | 7.162 | 6.0 | 1.83 | 414 | 1.87 | 2,183 | 1.82 |
| [5, 10) | 3,394 | 7.230 | 11.177 | 10.0 | 1.55 | 626 | 1.64 | 2,768 | 1.52 |
| 10 and over | 1,937 | 12.254 | 17.565 | 16.0 | 1.43 | 455 | 1.43 | 1,482 | 1.43 |

## Kinnex

59,971 reads cut between the primers, 59,580 matched (99.3%), of which 2,159 rescued by the indel-tolerant search; floor 0.842 differences (9,747 reads).

| expected errors | reads | mean expected | mean differences | median | differences / expected | rescued reads | rescued ratio | other reads | other ratio |
|---|---|---|---|---|---|---|---|---|---|
| [0, 0.05) | 9,747 | 0.016 | 0.842 | 0.0 | 52.78 | 93 | 44.24 | 9,654 | 52.87 |
| [0.05, 0.25) | 9,191 | 0.133 | 1.079 | 1.0 | 8.09 | 121 | 7.44 | 9,070 | 8.10 |
| [0.25, 1) | 15,878 | 0.553 | 1.651 | 1.0 | 2.99 | 199 | 3.35 | 15,679 | 2.98 |
| [1, 2) | 7,410 | 1.433 | 2.915 | 3.0 | 2.03 | 182 | 2.12 | 7,228 | 2.03 |
| [2, 3) | 3,938 | 2.463 | 4.317 | 4.0 | 1.75 | 156 | 1.78 | 3,782 | 1.75 |
| [3, 5) | 4,945 | 3.906 | 6.072 | 6.0 | 1.55 | 329 | 1.57 | 4,616 | 1.55 |
| [5, 10) | 5,284 | 7.013 | 9.811 | 9.0 | 1.40 | 531 | 1.42 | 4,753 | 1.40 |
| 10 and over | 3,187 | 14.009 | 16.928 | 16.0 | 1.21 | 548 | 1.22 | 2,639 | 1.21 |

## Composition against the expected read shares (pooled over the files of each library type)

**Monomer:** Spearman correlation between the expected and the observed read share over 20 strains: 0.98.

| strain | expected % | observed % | observed / expected |
|---|---|---|---|
| Escherichia_coli_ATCC700926 | 24.036 | 22.056 | 0.92 |
| Staphylococcus_epidermidis_ATCC12228 | 17.168 | 20.734 | 1.21 |
| Streptococcus_mutans_ATCC700610 | 17.168 | 23.711 | 1.38 |
| Cereibacter_sphaeroides_ATCC17029 | 13.735 | 2.564 | 0.19 |
| Porphyromonas_gingivalis_ATCC33277 | 13.735 | 17.623 | 1.28 |
| Clostridium_beijerinckii_ATCC35702 | 4.807 | 2.955 | 0.61 |
| Bacillus_pacificus_ATCC10987 | 4.120 | 5.245 | 1.27 |
| Streptococcus_agalactiae_ATCCBAA-611 | 2.404 | 2.253 | 0.94 |
| Staphylococcus_aureus_ATCCBAA-1556 | 1.717 | 1.179 | 0.69 |
| Pseudomonas_paraeruginosa_ATCC9027 | 0.343 | 0.794 | 2.31 |
| Acinetobacter_baumannii_ATCC17978 | 0.206 | 0.229 | 1.11 |
| Lactobacillus_gasseri_ATCC33323 | 0.206 | 0.195 | 0.95 |
| Neisseria_meningitidis_ATCCBAA-335 | 0.137 | 0.212 | 1.54 |
| Cutibacterium_acnes_ATCC11828 | 0.069 | 0.114 | 1.66 |
| Helicobacter_pylori_ATCC700392 | 0.069 | 0.082 | 1.20 |
| Phocaeicola_vulgatus_ATCC8482 | 0.027 | 0.024 | 0.88 |
| Bifidobacterium_adolescentis_ATCC15703 | 0.019 | 0.007 | 0.35 |
| Enterococcus_faecalis_ATCC47077 | 0.015 | 0.013 | 0.88 |
| Deinococcus_radiodurans_ATCCBAA-816 | 0.011 | 0.008 | 0.74 |
| Schaalia_odontolytica_ATCC17982 | 0.008 | 0.002 | 0.22 |

**Kinnex:** Spearman correlation between the expected and the observed read share over 20 strains: 0.98.

| strain | expected % | observed % | observed / expected |
|---|---|---|---|
| Escherichia_coli_ATCC700926 | 24.036 | 21.192 | 0.88 |
| Staphylococcus_epidermidis_ATCC12228 | 17.168 | 21.324 | 1.24 |
| Streptococcus_mutans_ATCC700610 | 17.168 | 23.847 | 1.39 |
| Cereibacter_sphaeroides_ATCC17029 | 13.735 | 2.732 | 0.20 |
| Porphyromonas_gingivalis_ATCC33277 | 13.735 | 16.803 | 1.22 |
| Clostridium_beijerinckii_ATCC35702 | 4.807 | 3.112 | 0.65 |
| Bacillus_pacificus_ATCC10987 | 4.120 | 5.515 | 1.34 |
| Streptococcus_agalactiae_ATCCBAA-611 | 2.404 | 2.348 | 0.98 |
| Staphylococcus_aureus_ATCCBAA-1556 | 1.717 | 1.316 | 0.77 |
| Pseudomonas_paraeruginosa_ATCC9027 | 0.343 | 0.921 | 2.68 |
| Acinetobacter_baumannii_ATCC17978 | 0.206 | 0.252 | 1.22 |
| Lactobacillus_gasseri_ATCC33323 | 0.206 | 0.176 | 0.86 |
| Neisseria_meningitidis_ATCCBAA-335 | 0.137 | 0.227 | 1.65 |
| Cutibacterium_acnes_ATCC11828 | 0.069 | 0.109 | 1.59 |
| Helicobacter_pylori_ATCC700392 | 0.069 | 0.069 | 1.00 |
| Phocaeicola_vulgatus_ATCC8482 | 0.027 | 0.035 | 1.32 |
| Bifidobacterium_adolescentis_ATCC15703 | 0.019 | 0.005 | 0.26 |
| Enterococcus_faecalis_ATCC47077 | 0.015 | 0.007 | 0.44 |
| Deinococcus_radiodurans_ATCCBAA-816 | 0.011 | 0.005 | 0.44 |
| Schaalia_odontolytica_ATCC17982 | 0.008 | 0.005 | 0.66 |

## Similarity of the compositions

Same barcode pair in two library types (Spearman correlation of the reads per strain):

| barcode pair | library a | library b | Spearman |
|---|---|---|---|
| Fwd_04--Kinnex16S_Rev_22 | Kinnex | Monomer | 0.98 |
| Fwd_07--Kinnex16S_Rev_30 | Kinnex | Monomer | 0.99 |
| Fwd_09--Kinnex16S_Rev_29 | Kinnex | Monomer | 1.00 |

Between the files of one library type (mean Spearman): Kinnex 0.99; Monomer 0.98.


## Truth test: Monomer

## Monomer

101,206 reads between the primers; median length 1473 nt, window 1320 to 1630 nt; the 75th percentile of the expected errors is 0.86, so the package's rule gives **maxEE 2**.

**Gate (T2): NOT MET.** 14 of 15 strains of the three highest tiers have an exact variant (needed: 14); 15 of 19 expected variants of 1% or more recovered exactly (needed: 80%).
**Gate (T3): NOT MET.** 2.93% of the final reads are in 'other' ASVs (at most 2%).
**Gate (T5): MET.** Spearman 0.95 over 17 strains (at least 0.7).
**Gate (T6): MET.** the rule gives maxEE 2, the same condition as the standard.

| condition | maxEE | window | primers | reads kept % | final ASVs | exact | near | other | chimeric ASVs | exact reads % | other reads % | chimeric reads % | variants recovered | top strains | big variants | Spearman | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ee1 | 1 | yes | cutadapt | 76.4 | 49 | 38 | 9 | 2 | 3 | 88.9 | 2.94 | 0.21 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 15.0 |
| ee2 | 2 | yes | cutadapt | 82.6 | 49 | 38 | 9 | 2 | 3 | 88.9 | 2.93 | 0.20 | 38 of 60 | 14 of 15 | 15 of 19 | 0.95 | 12.8 |
| ee3 | 3 | yes | cutadapt | 86.2 | 49 | 38 | 9 | 2 | 3 | 88.8 | 2.94 | 0.20 | 38 of 60 | 14 of 15 | 15 of 19 | 0.95 | 16.4 |
| ee5 | 5 | yes | cutadapt | 90.7 | 49 | 38 | 9 | 2 | 3 | 88.8 | 2.94 | 0.20 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 15.0 |
| ee10 | 10 | yes | cutadapt | 96.7 | 49 | 38 | 9 | 2 | 3 | 88.8 | 2.95 | 0.20 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 22.2 |
| ee2_nowindow | 2 | no | cutadapt | 82.7 | 49 | 38 | 9 | 2 | 3 | 88.9 | 2.93 | 0.20 | 38 of 60 | 14 of 15 | 15 of 19 | 0.95 | 13.1 |
| ee2_dada2primers | 2 | yes | dada2 | 84.1 | 48 | 37 | 9 | 2 | 3 | 88.8 | 2.96 | 0.17 | 37 of 60 | 14 of 15 | 15 of 19 | 0.95 | 13.2 |

The tables of every strain and every ASV are in truth_strains.tsv and truth_asvs_*.tsv. 'Top strains' are those with a genomic share of 0.18% or more; 'big variants' are the expected variants with an expected read share of 1% or more.


## Truth test: Kinnex

## Kinnex

149,931 reads between the primers; median length 1471 nt, window 1320 to 1620 nt; the 75th percentile of the expected errors is 2.66, so the package's rule gives **maxEE 3**.

**Gate (T2): NOT MET.** 14 of 15 strains of the three highest tiers have an exact variant (needed: 14); 15 of 19 expected variants of 1% or more recovered exactly (needed: 80%).
**Gate (T3): NOT MET.** 3.14% of the final reads are in 'other' ASVs (at most 2%).
**Gate (T5): MET.** Spearman 0.96 over 17 strains (at least 0.7).
**Gate (T6): MET.** the rule gives maxEE 3: 38 exact variants against 38 at maxEE 2; 'other' share 3.14% against 3.14% (at most 0.5 points more).

| condition | maxEE | window | primers | reads kept % | final ASVs | exact | near | other | chimeric ASVs | exact reads % | other reads % | chimeric reads % | variants recovered | top strains | big variants | Spearman | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ee1 | 1 | yes | cutadapt | 57.8 | 49 | 38 | 9 | 2 | 6 | 87.9 | 3.11 | 0.04 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 19.3 |
| ee2 | 2 | yes | cutadapt | 70.3 | 49 | 38 | 9 | 2 | 6 | 88.0 | 3.14 | 0.04 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 21.7 |
| ee3 | 3 | yes | cutadapt | 77.0 | 49 | 38 | 9 | 2 | 6 | 88.0 | 3.14 | 0.03 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 24.8 |
| ee5 | 5 | yes | cutadapt | 85.4 | 49 | 38 | 9 | 2 | 8 | 87.9 | 3.14 | 0.04 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 78.2 |
| ee10 | 10 | yes | cutadapt | 94.5 | 49 | 38 | 9 | 2 | 8 | 88.0 | 3.14 | 0.04 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 30.8 |
| ee2_nowindow | 2 | no | cutadapt | 70.3 | 49 | 38 | 9 | 2 | 6 | 88.0 | 3.14 | 0.04 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 21.6 |
| ee2_dada2primers | 2 | yes | dada2 | 72.2 | 49 | 38 | 9 | 2 | 6 | 87.9 | 3.15 | 0.04 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 20.7 |

The tables of every strain and every ASV are in truth_strains.tsv and truth_asvs_*.tsv. 'Top strains' are those with a genomic share of 0.18% or more; 'big variants' are the expected variants with an expected read share of 1% or more.


## The prediction of the rule

Written before the run: the package's percentile rule gives maxEE 2 for Monomer and 3 for Kinnex. It gave: Monomer 2 (as predicted); Kinnex 3 (as predicted).

## Send back

- this file (C:\data\runs\18_night8_truth\NIGHT8_SUMMARY.md)
- C:\data\runs\18_night8_truth\tcal\TCAL.md
- C:\data\runs\18_night8_truth\truth_monomer\TRUTH.md and C:\data\runs\18_night8_truth\truth_kinnex\TRUTH.md
- the two truth_conditions.tsv files, and C:\data\runs\18_night8_truth\tcal\bias.tsv
- C:\data\runs\18_night8_truth\night8.log if a step failed
