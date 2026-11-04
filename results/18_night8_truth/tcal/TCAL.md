# T-cal: calibration of the expected errors against the true differences

Primers AGRGTTYGATYMTGGCTCAG and RGYTACCTTGTTACGACTT; the first 20,000 reads of each file; a read whose nearest expected variant is more than 50 differences away is unmatched. Minimum reads for a bin to be judged: 300 (T-cal-1 and T-cal-2), 300 for both library types in T-cal-2, 100 per group (T-cal-3).

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

