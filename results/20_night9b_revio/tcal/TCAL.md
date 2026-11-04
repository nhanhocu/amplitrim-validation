# T-cal: calibration of the expected errors against the true differences

Primers AGRGTTYGATYMTGGCTCAG and RGYTACCTTGTTACGACTT; the first 20,000 reads of each file; a read whose nearest expected variant is more than 50 differences away is unmatched. Minimum reads for a bin to be judged: 300 (T-cal-1 and T-cal-2), 300 for both library types in T-cal-2, 100 per group (T-cal-3).

**Gate (T-cal-1): NOT MET.**

- Revio, [1, 2) expected errors: differences / expected errors = 1.28 (3,105 reads): inside 0.5 to 2.0
- Revio, [2, 3) expected errors: differences / expected errors = 1.06 (1,733 reads): inside 0.5 to 2.0
- Revio, [3, 5) expected errors: differences / expected errors = 0.75 (2,077 reads): inside 0.5 to 2.0
- Revio, [5, 10) expected errors: differences / expected errors = 0.48 (2,560 reads): OUTSIDE 0.5 to 2.0
- Revio, 10 and over expected errors: differences / expected errors = 0.31 (3,830 reads): OUTSIDE 0.5 to 2.0
- SequelII, [1, 2) expected errors: differences / expected errors = 2.19 (3,804 reads): OUTSIDE 0.5 to 2.0
- SequelII, [2, 3) expected errors: differences / expected errors = 1.95 (2,089 reads): inside 0.5 to 2.0
- SequelII, [3, 5) expected errors: differences / expected errors = 1.78 (2,565 reads): inside 0.5 to 2.0
- SequelII, [5, 10) expected errors: differences / expected errors = 1.53 (3,492 reads): inside 0.5 to 2.0
- SequelII, 10 and over expected errors: differences / expected errors = 1.42 (1,936 reads): inside 0.5 to 2.0

**Gate (T-cal-2): NOT MET.**

- Revio against SequelII, [1, 2): ratio 1.28 against 2.19, a factor of 1.71: BEYOND 1.5
- Revio against SequelII, [2, 3): ratio 1.06 against 1.95, a factor of 1.84: BEYOND 1.5
- Revio against SequelII, [3, 5): ratio 0.75 against 1.78, a factor of 2.37: BEYOND 1.5
- Revio against SequelII, [5, 10): ratio 0.48 against 1.53, a factor of 3.18: BEYOND 1.5
- Revio against SequelII, 10 and over: ratio 0.31 against 1.42, a factor of 4.52: BEYOND 1.5

**Gate (T-cal-3): NOT MET.**

- Revio, [1, 2): rescued 2.05 (255 reads) against the others 1.21 (2,850 reads), a factor of 1.69: BEYOND 1.5
- Revio, [2, 3): rescued 2.20 (161 reads) against the others 0.94 (1,572 reads), a factor of 2.35: BEYOND 1.5
- Revio, [3, 5): rescued 1.29 (196 reads) against the others 0.69 (1,881 reads), a factor of 1.86: BEYOND 1.5
- Revio, [5, 10): rescued 0.66 (254 reads) against the others 0.46 (2,306 reads), a factor of 1.42: within 1.5
- Revio, 10 and over: rescued 0.32 (513 reads) against the others 0.31 (3,317 reads), a factor of 1.03: within 1.5
- SequelII, [1, 2): rescued 2.23 (497 reads) against the others 2.19 (3,307 reads), a factor of 1.02: within 1.5
- SequelII, [2, 3): rescued 1.81 (266 reads) against the others 1.97 (1,823 reads), a factor of 1.09: within 1.5
- SequelII, [3, 5): rescued 1.80 (409 reads) against the others 1.77 (2,156 reads), a factor of 1.02: within 1.5
- SequelII, [5, 10): rescued 1.61 (657 reads) against the others 1.51 (2,835 reads), a factor of 1.06: within 1.5
- SequelII, 10 and over: rescued 1.43 (462 reads) against the others 1.41 (1,474 reads), a factor of 1.01: within 1.5

The floor is the mean number of differences of the matched reads with fewer than 0.05 expected errors: what the quality scores cannot see (PCR errors, chimeras, real divergence).

## Revio

59,958 reads cut between the primers, 59,790 matched (99.7%), of which 5,291 rescued by the indel-tolerant search; floor - differences (0 reads).

| expected errors | reads | mean expected | mean differences | median | differences / expected | rescued reads | rescued ratio | other reads | other ratio |
|---|---|---|---|---|---|---|---|---|---|
| [0, 0.05) | 0 | - | - | - | - | 0 | - | 0 | - |
| [0.05, 0.25) | 39,160 | 0.152 | 0.414 | 0.0 | 2.72 | 3,283 | 3.07 | 35,877 | 2.69 |
| [0.25, 1) | 7,325 | 0.538 | 1.106 | 1.0 | 2.05 | 629 | 2.40 | 6,696 | 2.02 |
| [1, 2) | 3,105 | 1.442 | 1.847 | 1.0 | 1.28 | 255 | 2.05 | 2,850 | 1.21 |
| [2, 3) | 1,733 | 2.471 | 2.608 | 1.0 | 1.06 | 161 | 2.20 | 1,572 | 0.94 |
| [3, 5) | 2,077 | 3.926 | 2.938 | 2.0 | 0.75 | 196 | 1.29 | 1,881 | 0.69 |
| [5, 10) | 2,560 | 7.143 | 3.441 | 3.0 | 0.48 | 254 | 0.66 | 2,306 | 0.46 |
| 10 and over | 3,830 | 20.377 | 6.386 | 5.0 | 0.31 | 513 | 0.32 | 3,317 | 0.31 |

## SequelII

59,907 reads cut between the primers, 59,468 matched (99.3%), of which 6,635 rescued by the indel-tolerant search; floor 0.367 differences (32,659 reads).

| expected errors | reads | mean expected | mean differences | median | differences / expected | rescued reads | rescued ratio | other reads | other ratio |
|---|---|---|---|---|---|---|---|---|---|
| [0, 0.05) | 32,659 | 0.003 | 0.367 | 0.0 | 120.38 | 2,977 | 114.81 | 29,682 | 121.04 |
| [0.05, 0.25) | 4,970 | 0.129 | 0.854 | 1.0 | 6.60 | 504 | 6.84 | 4,466 | 6.57 |
| [0.25, 1) | 7,953 | 0.541 | 1.538 | 1.0 | 2.84 | 863 | 3.18 | 7,090 | 2.80 |
| [1, 2) | 3,804 | 1.431 | 3.140 | 3.0 | 2.19 | 497 | 2.23 | 3,307 | 2.19 |
| [2, 3) | 2,089 | 2.467 | 4.801 | 4.0 | 1.95 | 266 | 1.81 | 1,823 | 1.97 |
| [3, 5) | 2,565 | 3.918 | 6.962 | 6.0 | 1.78 | 409 | 1.80 | 2,156 | 1.77 |
| [5, 10) | 3,492 | 7.188 | 11.008 | 10.0 | 1.53 | 657 | 1.61 | 2,835 | 1.51 |
| 10 and over | 1,936 | 12.214 | 17.293 | 16.0 | 1.42 | 462 | 1.43 | 1,474 | 1.41 |

## Composition against the expected read shares (pooled over the files of each library type)

**Revio:** Spearman correlation between the expected and the observed read share over 20 strains: 0.98.

| strain | expected % | observed % | observed / expected |
|---|---|---|---|
| Escherichia_coli_ATCC700926 | 24.036 | 22.250 | 0.93 |
| Staphylococcus_epidermidis_ATCC12228 | 17.168 | 21.107 | 1.23 |
| Streptococcus_mutans_ATCC700610 | 17.168 | 24.042 | 1.40 |
| Cereibacter_sphaeroides_ATCC17029 | 13.735 | 2.266 | 0.17 |
| Porphyromonas_gingivalis_ATCC33277 | 13.735 | 17.018 | 1.24 |
| Clostridium_beijerinckii_ATCC35702 | 4.807 | 2.689 | 0.56 |
| Bacillus_pacificus_ATCC10987 | 4.120 | 5.421 | 1.32 |
| Streptococcus_agalactiae_ATCCBAA-611 | 2.404 | 2.305 | 0.96 |
| Staphylococcus_aureus_ATCCBAA-1556 | 1.717 | 1.234 | 0.72 |
| Pseudomonas_paraeruginosa_ATCC9027 | 0.343 | 0.841 | 2.45 |
| Acinetobacter_baumannii_ATCC17978 | 0.206 | 0.184 | 0.89 |
| Lactobacillus_gasseri_ATCC33323 | 0.206 | 0.201 | 0.97 |
| Neisseria_meningitidis_ATCCBAA-335 | 0.137 | 0.214 | 1.56 |
| Cutibacterium_acnes_ATCC11828 | 0.069 | 0.094 | 1.36 |
| Helicobacter_pylori_ATCC700392 | 0.069 | 0.079 | 1.14 |
| Phocaeicola_vulgatus_ATCC8482 | 0.027 | 0.027 | 1.00 |
| Bifidobacterium_adolescentis_ATCC15703 | 0.019 | 0.007 | 0.35 |
| Enterococcus_faecalis_ATCC47077 | 0.015 | 0.013 | 0.87 |
| Deinococcus_radiodurans_ATCCBAA-816 | 0.011 | 0.005 | 0.44 |
| Schaalia_odontolytica_ATCC17982 | 0.008 | 0.003 | 0.44 |

**SequelII:** Spearman correlation between the expected and the observed read share over 20 strains: 0.98.

| strain | expected % | observed % | observed / expected |
|---|---|---|---|
| Escherichia_coli_ATCC700926 | 24.036 | 22.128 | 0.92 |
| Staphylococcus_epidermidis_ATCC12228 | 17.168 | 20.675 | 1.20 |
| Streptococcus_mutans_ATCC700610 | 17.168 | 23.746 | 1.38 |
| Cereibacter_sphaeroides_ATCC17029 | 13.735 | 2.543 | 0.19 |
| Porphyromonas_gingivalis_ATCC33277 | 13.735 | 17.705 | 1.29 |
| Clostridium_beijerinckii_ATCC35702 | 4.807 | 2.983 | 0.62 |
| Bacillus_pacificus_ATCC10987 | 4.120 | 5.146 | 1.25 |
| Streptococcus_agalactiae_ATCCBAA-611 | 2.404 | 2.240 | 0.93 |
| Staphylococcus_aureus_ATCCBAA-1556 | 1.717 | 1.138 | 0.66 |
| Pseudomonas_paraeruginosa_ATCC9027 | 0.343 | 0.802 | 2.34 |
| Acinetobacter_baumannii_ATCC17978 | 0.206 | 0.225 | 1.09 |
| Lactobacillus_gasseri_ATCC33323 | 0.206 | 0.188 | 0.91 |
| Neisseria_meningitidis_ATCCBAA-335 | 0.137 | 0.212 | 1.54 |
| Cutibacterium_acnes_ATCC11828 | 0.069 | 0.114 | 1.66 |
| Helicobacter_pylori_ATCC700392 | 0.069 | 0.087 | 1.27 |
| Phocaeicola_vulgatus_ATCC8482 | 0.027 | 0.030 | 1.13 |
| Bifidobacterium_adolescentis_ATCC15703 | 0.019 | 0.005 | 0.26 |
| Enterococcus_faecalis_ATCC47077 | 0.015 | 0.020 | 1.32 |
| Deinococcus_radiodurans_ATCCBAA-816 | 0.011 | 0.012 | 1.03 |
| Schaalia_odontolytica_ATCC17982 | 0.008 | 0.000 | 0.00 |

## Similarity of the compositions

Same barcode pair in two library types (Spearman correlation of the reads per strain):

| barcode pair | library a | library b | Spearman |
|---|---|---|---|
| Fwd_04--Kinnex16S_Rev_22 | Revio | SequelII | 0.98 |
| Fwd_07--Kinnex16S_Rev_30 | Revio | SequelII | 0.99 |
| Fwd_09--Kinnex16S_Rev_29 | Revio | SequelII | 0.99 |

Between the files of one library type (mean Spearman): Revio 0.98; SequelII 0.99.

