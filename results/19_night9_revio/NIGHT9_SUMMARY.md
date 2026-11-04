# Night 9: the Revio hold-out (quality scores, T-cal and the truth test on Revio Monomer reads of ATCC MSA-1003)

Run on 2026-10-15; folder C:\data\runs\19_night9_revio. Design, predictions and gates: FUTURE.md of the archive (written on 15 October 2026, before the data were downloaded). Tools: Python 3.12.15; numpy 2.5.3; cutadapt 5.2; R and DADA2 R version 4.6.1 (2026-06-24 ucrt) | DADA2 1.40.0.

## Steps

- quality: done in 1 min (Revio: highest Q 40, 7 distinct values, binned; SequelII: highest Q 93, 93 distinct values, not binned)
- tcal: done in 2 min (T-cal-1 NOT MET; T-cal-2 NOT MET; T-cal-3 NOT MET)
- truth: done in 36 min (error model binned:3,10,17,22,27,35,40; the rule gives maxEE 2; T2 MET, T3 MET, T5 MET, T6 MET)

## Quality scores

| library | file | highest | distinct values | values |
|---|---|---|---|---|
| Revio | m84198_231017_000448_s1.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads.fastq.gz | 40 | 7 | 3 10 17 22 27 35 40 |
| Revio | m84198_231017_000448_s1.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads.fastq.gz | 40 | 7 | 3 10 17 22 27 35 40 |
| Revio | m84198_231017_000448_s1.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads.fastq.gz | 40 | 7 | 3 10 17 22 27 35 40 |
| SequelII | m64004e_231016_235852.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads.fastq.gz | 93 | 92 | (many) |
| SequelII | m64004e_231016_235852.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads.fastq.gz | 93 | 93 | (many) |
| SequelII | m64004e_231016_235852.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads.fastq.gz | 93 | 93 | (many) |

## T-cal: Revio against Sequel II (reference: the refined set). T-cal-1 below is the gate T-cal-R1 and T-cal-2 is T-cal-R2

**Gate (T-cal-1): NOT MET.**

- Revio, [1, 2) expected errors: differences / expected errors = 1.36 (3,169 reads): inside 0.5 to 2.0
- Revio, [2, 3) expected errors: differences / expected errors = 1.15 (1,764 reads): inside 0.5 to 2.0
- Revio, [3, 5) expected errors: differences / expected errors = 0.84 (2,123 reads): inside 0.5 to 2.0
- Revio, [5, 10) expected errors: differences / expected errors = 0.55 (2,690 reads): inside 0.5 to 2.0
- Revio, 10 and over expected errors: differences / expected errors = 0.31 (3,688 reads): OUTSIDE 0.5 to 2.0
- SequelII, [1, 2) expected errors: differences / expected errors = 2.25 (3,714 reads): OUTSIDE 0.5 to 2.0
- SequelII, [2, 3) expected errors: differences / expected errors = 1.94 (2,139 reads): inside 0.5 to 2.0
- SequelII, [3, 5) expected errors: differences / expected errors = 1.77 (2,597 reads): inside 0.5 to 2.0
- SequelII, [5, 10) expected errors: differences / expected errors = 1.51 (3,394 reads): inside 0.5 to 2.0
- SequelII, 10 and over expected errors: differences / expected errors = 1.42 (1,937 reads): inside 0.5 to 2.0

**Gate (T-cal-2): NOT MET.**

- Revio against SequelII, [1, 2): ratio 1.36 against 2.25, a factor of 1.66: BEYOND 1.5
- Revio against SequelII, [2, 3): ratio 1.15 against 1.94, a factor of 1.68: BEYOND 1.5
- Revio against SequelII, [3, 5): ratio 0.84 against 1.77, a factor of 2.11: BEYOND 1.5
- Revio against SequelII, [5, 10): ratio 0.55 against 1.51, a factor of 2.74: BEYOND 1.5
- Revio against SequelII, 10 and over: ratio 0.31 against 1.42, a factor of 4.55: BEYOND 1.5

**Gate (T-cal-3): NOT MET.**

- Revio, [1, 2): rescued 1.74 (269 reads) against the others 1.32 (2,900 reads), a factor of 1.32: within 1.5
- Revio, [2, 3): rescued 1.87 (176 reads) against the others 1.07 (1,588 reads), a factor of 1.74: BEYOND 1.5
- Revio, [3, 5): rescued 1.33 (223 reads) against the others 0.78 (1,900 reads), a factor of 1.72: BEYOND 1.5
- Revio, [5, 10): rescued 0.92 (315 reads) against the others 0.50 (2,375 reads), a factor of 1.82: BEYOND 1.5
- Revio, 10 and over: rescued 0.29 (484 reads) against the others 0.31 (3,204 reads), a factor of 1.07: within 1.5
- SequelII, [1, 2): rescued 2.21 (506 reads) against the others 2.25 (3,208 reads), a factor of 1.02: within 1.5
- SequelII, [2, 3): rescued 1.88 (287 reads) against the others 1.95 (1,852 reads), a factor of 1.04: within 1.5
- SequelII, [3, 5): rescued 1.80 (414 reads) against the others 1.76 (2,183 reads), a factor of 1.02: within 1.5
- SequelII, [5, 10): rescued 1.61 (626 reads) against the others 1.49 (2,768 reads), a factor of 1.08: within 1.5
- SequelII, 10 and over: rescued 1.42 (455 reads) against the others 1.42 (1,482 reads), a factor of 1.00: within 1.5

The floor is the mean number of differences of the matched reads with fewer than 0.05 expected errors: what the quality scores cannot see (PCR errors, chimeras, real divergence).

## Revio

59,961 reads cut between the primers, 59,773 matched (99.7%), of which 6,498 rescued by the indel-tolerant search; floor - differences (0 reads).

| expected errors | reads | mean expected | mean differences | median | differences / expected | rescued reads | rescued ratio | other reads | other ratio |
|---|---|---|---|---|---|---|---|---|---|
| [0, 0.05) | 0 | - | - | - | - | 0 | - | 0 | - |
| [0.05, 0.25) | 39,337 | 0.152 | 0.441 | 0.0 | 2.90 | 4,296 | 3.11 | 35,041 | 2.87 |
| [0.25, 1) | 7,002 | 0.542 | 1.082 | 1.0 | 2.00 | 735 | 1.90 | 6,267 | 2.01 |
| [1, 2) | 3,169 | 1.445 | 1.961 | 1.0 | 1.36 | 269 | 1.74 | 2,900 | 1.32 |
| [2, 3) | 1,764 | 2.472 | 2.850 | 2.0 | 1.15 | 176 | 1.87 | 1,588 | 1.07 |
| [3, 5) | 2,123 | 3.921 | 3.281 | 2.0 | 0.84 | 223 | 1.33 | 1,900 | 0.78 |
| [5, 10) | 2,690 | 7.176 | 3.964 | 3.0 | 0.55 | 315 | 0.92 | 2,375 | 0.50 |
| 10 and over | 3,688 | 20.283 | 6.316 | 5.0 | 0.31 | 484 | 0.29 | 3,204 | 0.31 |

## SequelII

59,908 reads cut between the primers, 59,468 matched (99.3%), of which 6,649 rescued by the indel-tolerant search; floor 0.378 differences (32,781 reads).

| expected errors | reads | mean expected | mean differences | median | differences / expected | rescued reads | rescued ratio | other reads | other ratio |
|---|---|---|---|---|---|---|---|---|---|
| [0, 0.05) | 32,781 | 0.003 | 0.378 | 0.0 | 122.36 | 3,010 | 124.06 | 29,771 | 122.16 |
| [0.05, 0.25) | 4,993 | 0.129 | 0.859 | 1.0 | 6.67 | 506 | 6.92 | 4,487 | 6.64 |
| [0.25, 1) | 7,913 | 0.542 | 1.520 | 1.0 | 2.80 | 845 | 3.30 | 7,068 | 2.74 |
| [1, 2) | 3,714 | 1.431 | 3.215 | 3.0 | 2.25 | 506 | 2.21 | 3,208 | 2.25 |
| [2, 3) | 2,139 | 2.458 | 4.770 | 4.0 | 1.94 | 287 | 1.88 | 1,852 | 1.95 |
| [3, 5) | 2,597 | 3.917 | 6.923 | 6.0 | 1.77 | 414 | 1.80 | 2,183 | 1.76 |
| [5, 10) | 3,394 | 7.230 | 10.931 | 10.0 | 1.51 | 626 | 1.61 | 2,768 | 1.49 |
| 10 and over | 1,937 | 12.254 | 17.368 | 16.0 | 1.42 | 455 | 1.42 | 1,482 | 1.42 |

## Composition against the expected read shares (pooled over the files of each library type)

**Revio:** Spearman correlation between the expected and the observed read share over 20 strains: 0.66.

| strain | expected % | observed % | observed / expected |
|---|---|---|---|
| Escherichia_coli_ATCC700926 | 24.036 | 0.261 | 0.01 |
| Staphylococcus_epidermidis_ATCC12228 | 17.168 | 0.361 | 0.02 |
| Streptococcus_mutans_ATCC700610 | 17.168 | 43.817 | 2.55 |
| Cereibacter_sphaeroides_ATCC17029 | 13.735 | 6.362 | 0.46 |
| Porphyromonas_gingivalis_ATCC33277 | 13.735 | 17.580 | 1.28 |
| Clostridium_beijerinckii_ATCC35702 | 4.807 | 4.942 | 1.03 |
| Bacillus_pacificus_ATCC10987 | 4.120 | 15.144 | 3.68 |
| Streptococcus_agalactiae_ATCCBAA-611 | 2.404 | 6.133 | 2.55 |
| Staphylococcus_aureus_ATCCBAA-1556 | 1.717 | 0.012 | 0.01 |
| Pseudomonas_paraeruginosa_ATCC9027 | 0.343 | 3.915 | 11.40 |
| Acinetobacter_baumannii_ATCC17978 | 0.206 | 0.525 | 2.55 |
| Lactobacillus_gasseri_ATCC33323 | 0.206 | 0.487 | 2.36 |
| Neisseria_meningitidis_ATCCBAA-335 | 0.137 | 0.000 | 0.00 |
| Cutibacterium_acnes_ATCC11828 | 0.069 | 0.325 | 4.72 |
| Helicobacter_pylori_ATCC700392 | 0.069 | 0.002 | 0.02 |
| Phocaeicola_vulgatus_ATCC8482 | 0.027 | 0.049 | 1.82 |
| Bifidobacterium_adolescentis_ATCC15703 | 0.019 | 0.007 | 0.35 |
| Enterococcus_faecalis_ATCC47077 | 0.015 | 0.050 | 3.28 |
| Deinococcus_radiodurans_ATCCBAA-816 | 0.011 | 0.013 | 1.17 |
| Schaalia_odontolytica_ATCC17982 | 0.008 | 0.015 | 1.98 |

**SequelII:** Spearman correlation between the expected and the observed read share over 20 strains: 0.98.

| strain | expected % | observed % | observed / expected |
|---|---|---|---|
| Escherichia_coli_ATCC700926 | 24.036 | 22.056 | 0.92 |
| Staphylococcus_epidermidis_ATCC12228 | 17.168 | 20.734 | 1.21 |
| Streptococcus_mutans_ATCC700610 | 17.168 | 23.710 | 1.38 |
| Cereibacter_sphaeroides_ATCC17029 | 13.735 | 2.564 | 0.19 |
| Porphyromonas_gingivalis_ATCC33277 | 13.735 | 17.623 | 1.28 |
| Clostridium_beijerinckii_ATCC35702 | 4.807 | 2.955 | 0.61 |
| Bacillus_pacificus_ATCC10987 | 4.120 | 5.247 | 1.27 |
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

## Similarity of the compositions

Same barcode pair in two library types (Spearman correlation of the reads per strain):

| barcode pair | library a | library b | Spearman |
|---|---|---|---|
| Fwd_04--Kinnex16S_Rev_22 | Revio | SequelII | 0.70 |
| Fwd_07--Kinnex16S_Rev_30 | Revio | SequelII | 0.72 |
| Fwd_09--Kinnex16S_Rev_29 | Revio | SequelII | 0.62 |

Between the files of one library type (mean Spearman): Revio 0.90; SequelII 0.98.


## Truth test: Revio

## Revio

149,901 reads between the primers; median length 1473 nt, window 1320 to 1630 nt; the 75th percentile of the expected errors is 0.75, so the package's rule gives **maxEE 2**.

Quality scores: highest 40, 7 distinct values (3, 10, 17, 22, 27, 35, 40); error model: **binned:3,10,17,22,27,35,40**.

**Gate (T2): MET.** 15 of 15 strains of the three highest tiers have an exact or an added ASV (needed: 14); 49 of 49 sequences of the replication set recovered (needed: 90%).
**Gate (T3): MET.** 0.00% of the final reads are in ASVs that are neither exact nor added (at most 2%).
**Gate (T5): MET.** Spearman 0.96 over 17 strains (at least 0.7).
**Gate (T6): MET.** the rule gives maxEE 2, the same condition as the standard.

| condition | maxEE | window | primers | error model | reads kept % | final ASVs | exact | added | near | other | chimeric ASVs | exact reads % | unexplained reads % | chimeric reads % | reference variants recovered | top strains | replicated | Spearman | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ee2 | 2 | yes | cutadapt | binned:3,10,17,22,27,35,40 | 82.9 | 53 | 43 | 10 | 0 | 0 | 8 | 94.1 | 0.00 | 0.17 | 53 of 69 | 15 of 15 | 49 of 49 | 0.96 | 10.2 |
| ee2_dada2primers | 2 | yes | dada2 | binned:3,10,17,22,27,35,40 | 83.5 | 57 | 42 | 10 | 1 | 4 | 5 | 94.2 | 0.06 | 0.15 | 52 of 69 | 15 of 15 | 49 of 49 | 0.96 | 13.1 |
| ee2_naive | 2 | yes | cutadapt | PacBioErrfun | 82.9 | 53 | 43 | 10 | 0 | 0 | 8 | 94.1 | 0.00 | 0.17 | 53 of 69 | 15 of 15 | 49 of 49 | 0.96 | 11.7 |

Scored against the original variants (no gate):

| condition | variants recovered | 'other' reads % | top strains | big variants |
|---|---|---|---|---|
| ee2 | 42 of 60 | 1.19 | 14 of 15 | 15 of 19 |
| ee2_dada2primers | 41 of 60 | 1.22 | 14 of 15 | 15 of 19 |
| ee2_naive | 42 of 60 | 1.19 | 14 of 15 | 15 of 19 |

The tables of every strain and every ASV are in truth_strains.tsv and truth_asvs_*.tsv. 'Top strains' are those with a genomic share of 0.18% or more; 'unexplained' reads are those in ASVs that are neither exact nor added; 'replicated' counts the sequences of the replication set that were recovered.


## The predictions (written before the data were seen)

1. The Revio reads are binned (highest Q at most 40 and at most 12 distinct values): highest Q 40, 7 distinct values: as predicted.
2. The binned model recovers at least as many of the replication set as the naive condition: 49 against 49: as predicted.
3. At least 90% of the replication set is found again: 49 of 49 (100.0%): as predicted.

## Send back

- this file (C:\data\runs\19_night9_revio\NIGHT9_SUMMARY.md)
- C:\data\runs\19_night9_revio\quality.tsv
- C:\data\runs\19_night9_revio\tcal\TCAL.md
- C:\data\runs\19_night9_revio\truth\TRUTH.md, its truth_conditions.tsv and truth_strains.tsv
- C:\data\runs\19_night9_revio\night9.log if a step failed
