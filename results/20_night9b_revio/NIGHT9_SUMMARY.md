# Night 9: the Revio hold-out (quality scores, T-cal and the truth test on Revio Monomer reads of ATCC MSA-1003)

Run on 2026-10-16; folder C:\data\runs\20_night9b_revio. Design, predictions and gates: FUTURE.md of the archive (written on 15 October 2026, before the data were downloaded). Tools: Python 3.12.15; numpy 2.5.3; cutadapt 5.2; R and DADA2 R version 4.6.1 (2026-06-24 ucrt) | DADA2 1.40.0.

## Steps

- quality: done in 1 min (Revio: highest Q 40, 7 distinct values, binned; SequelII: highest Q 93, 93 distinct values, not binned)
- order: done in 1 min (Revio: 3 of 3 files NOT RANDOM; SequelII: 0 of 3 files NOT RANDOM)
- tcal: done in 2 min (T-cal-1 NOT MET; T-cal-2 NOT MET; T-cal-3 NOT MET)
- truth: done in 37 min (error model binned:3,10,17,22,27,35,40; the rule gives maxEE 2; T2 MET, T3 MET, T5 MET, T6 MET)

## Quality scores

| library | file | highest | distinct values | values |
|---|---|---|---|---|
| Revio | m84198_231017_000448_s1.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads.fastq.gz | 40 | 7 | 3 10 17 22 27 35 40 |
| Revio | m84198_231017_000448_s1.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads.fastq.gz | 40 | 7 | 3 10 17 22 27 35 40 |
| Revio | m84198_231017_000448_s1.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads.fastq.gz | 40 | 7 | 3 10 17 22 27 35 40 |
| SequelII | m64004e_231016_235852.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads.fastq.gz | 93 | 92 | (many) |
| SequelII | m64004e_231016_235852.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads.fastq.gz | 93 | 93 | (many) |
| SequelII | m64004e_231016_235852.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads.fastq.gz | 93 | 93 | (many) |

## Order of the reads (is a file in random order?)

## m84198_231017_000448_s1.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads

127,547 reads; 10 blocks of 12,754 reads; the first 400 reads of each block.
Chi-square 13394 on 63 degrees of freedom (z 1187.6); V 0.698 against 0.048 for random order; **NOT RANDOM**.

Share of the reads of each block (%) for the six most abundant strains, and the mean expected errors:

| block | reads | Streptococcus mutans 700 | Staphylococcus epidermid | Porphyromonas gingivalis | Pseudomonas paraeruginos | Escherichia coli 700926 | Bacillus pacificus 10987 | mean expected errors |
|---|---|---|---|---|---|---|---|---|
| 1 | 398 | 5.5 | 1.5 | 1.5 | 88.4 | 1.0 | 0.8 | 2.86 |
| 2 | 400 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.91 |
| 3 | 400 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.81 |
| 4 | 400 | 99.8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 4.02 |
| 5 | 399 | 0.0 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | 3.24 |
| 6 | 399 | 63.9 | 8.0 | 8.8 | 0.0 | 0.0 | 0.5 | 1.96 |
| 7 | 399 | 4.0 | 70.2 | 0.0 | 0.0 | 0.0 | 20.1 | 1.68 |
| 8 | 400 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.75 |
| 9 | 398 | 1.8 | 74.4 | 0.0 | 0.0 | 0.0 | 13.8 | 1.61 |
| 10 | 392 | 0.3 | 29.8 | 0.0 | 0.0 | 68.6 | 0.0 | 4.93 |

## m84198_231017_000448_s1.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads

70,986 reads; 10 blocks of 7,098 reads; the first 400 reads of each block.
Chi-square 14178 on 72 degrees of freedom (z 1175.5); V 0.672 against 0.048 for random order; **NOT RANDOM**.

Share of the reads of each block (%) for the six most abundant strains, and the mean expected errors:

| block | reads | Porphyromonas gingivalis | Staphylococcus epidermid | Escherichia coli 700926 | Streptococcus mutans 700 | Pseudomonas paraeruginos | Clostridium beijerinckii | mean expected errors |
|---|---|---|---|---|---|---|---|---|
| 1 | 396 | 7.3 | 5.3 | 6.3 | 4.0 | 68.4 | 1.0 | 3.68 |
| 2 | 398 | 0.0 | 0.0 | 0.0 | 100.0 | 0.0 | 0.0 | 1.11 |
| 3 | 400 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 2.03 |
| 4 | 398 | 0.0 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | 2.78 |
| 5 | 398 | 23.9 | 32.2 | 0.0 | 21.9 | 0.0 | 4.3 | 2.08 |
| 6 | 400 | 58.8 | 0.0 | 0.0 | 0.0 | 0.0 | 23.0 | 2.80 |
| 7 | 399 | 87.2 | 4.5 | 0.0 | 0.0 | 0.0 | 1.3 | 3.72 |
| 8 | 400 | 0.0 | 93.0 | 0.0 | 0.0 | 0.0 | 0.0 | 2.87 |
| 9 | 400 | 0.0 | 94.2 | 0.0 | 0.0 | 0.0 | 0.0 | 1.13 |
| 10 | 400 | 0.0 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | 1.28 |

## m84198_231017_000448_s1.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads

93,404 reads; 10 blocks of 9,340 reads; the first 400 reads of each block.
Chi-square 15739 on 81 degrees of freedom (z 1230.2); V 0.663 against 0.048 for random order; **NOT RANDOM**.

Share of the reads of each block (%) for the six most abundant strains, and the mean expected errors:

| block | reads | Staphylococcus epidermid | Escherichia coli 700926 | Streptococcus mutans 700 | Porphyromonas gingivalis | Pseudomonas paraeruginos | Cereibacter sphaeroides  | mean expected errors |
|---|---|---|---|---|---|---|---|---|
| 1 | 398 | 0.8 | 0.8 | 0.5 | 1.5 | 95.2 | 0.0 | 2.86 |
| 2 | 400 | 0.0 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.80 |
| 3 | 400 | 0.0 | 0.0 | 0.0 | 100.0 | 0.0 | 0.0 | 1.89 |
| 4 | 400 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 3.52 |
| 5 | 400 | 20.5 | 0.0 | 63.2 | 3.2 | 0.0 | 0.2 | 2.35 |
| 6 | 399 | 21.6 | 0.0 | 9.8 | 13.0 | 0.0 | 25.6 | 1.59 |
| 7 | 398 | 43.2 | 0.3 | 0.8 | 33.7 | 0.0 | 0.0 | 2.55 |
| 8 | 399 | 94.2 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 2.52 |
| 9 | 400 | 94.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.46 |
| 10 | 398 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.07 |

## m64004e_231016_235852.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads

44,558 reads; 10 blocks of 4,455 reads; the first 400 reads of each block.
Chi-square 55 on 63 degrees of freedom (z -0.7); V 0.045 against 0.048 for random order; **consistent with random order**.

Share of the reads of each block (%) for the six most abundant strains, and the mean expected errors:

| block | reads | Streptococcus mutans 700 | Escherichia coli 700926 | Staphylococcus epidermid | Porphyromonas gingivalis | Bacillus pacificus 10987 | Clostridium beijerinckii | mean expected errors |
|---|---|---|---|---|---|---|---|---|
| 1 | 393 | 48.9 | 12.7 | 13.7 | 14.0 | 3.1 | 1.5 | 1.33 |
| 2 | 394 | 44.9 | 16.2 | 13.5 | 11.9 | 4.1 | 2.3 | 1.39 |
| 3 | 395 | 49.9 | 13.9 | 15.2 | 9.1 | 3.3 | 2.0 | 1.22 |
| 4 | 395 | 45.6 | 16.5 | 14.4 | 12.2 | 2.5 | 3.3 | 1.36 |
| 5 | 395 | 45.3 | 15.4 | 13.2 | 12.2 | 4.6 | 2.0 | 1.19 |
| 6 | 396 | 44.9 | 15.2 | 13.1 | 14.4 | 5.3 | 1.8 | 1.22 |
| 7 | 393 | 45.8 | 18.1 | 15.8 | 10.9 | 3.3 | 2.5 | 1.21 |
| 8 | 393 | 49.6 | 15.8 | 12.7 | 9.9 | 3.8 | 2.5 | 1.50 |
| 9 | 391 | 45.0 | 18.2 | 12.5 | 11.8 | 4.9 | 1.5 | 1.47 |
| 10 | 395 | 44.1 | 17.7 | 15.4 | 11.6 | 3.3 | 1.8 | 1.09 |

## m64004e_231016_235852.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads

24,730 reads; 10 blocks of 2,473 reads; the first 400 reads of each block.
Chi-square 81 on 72 degrees of freedom (z 0.8); V 0.051 against 0.048 for random order; **consistent with random order**.

Share of the reads of each block (%) for the six most abundant strains, and the mean expected errors:

| block | reads | Escherichia coli 700926 | Staphylococcus epidermid | Porphyromonas gingivalis | Streptococcus mutans 700 | Bacillus pacificus 10987 | Clostridium beijerinckii | mean expected errors |
|---|---|---|---|---|---|---|---|---|
| 1 | 398 | 24.1 | 22.6 | 18.6 | 13.1 | 3.3 | 4.8 | 1.46 |
| 2 | 395 | 24.1 | 24.6 | 20.8 | 12.2 | 9.1 | 3.5 | 1.32 |
| 3 | 396 | 27.8 | 24.2 | 18.2 | 13.6 | 5.6 | 2.5 | 1.28 |
| 4 | 400 | 25.8 | 23.2 | 19.0 | 15.2 | 5.0 | 3.5 | 0.97 |
| 5 | 396 | 24.7 | 21.7 | 22.0 | 11.4 | 6.6 | 4.5 | 1.39 |
| 6 | 397 | 25.2 | 21.4 | 21.4 | 13.1 | 5.8 | 4.3 | 1.16 |
| 7 | 397 | 28.0 | 24.2 | 16.6 | 12.3 | 5.0 | 4.5 | 1.39 |
| 8 | 396 | 25.5 | 24.2 | 20.5 | 12.1 | 6.1 | 4.0 | 1.25 |
| 9 | 397 | 24.2 | 26.4 | 22.2 | 11.8 | 5.3 | 1.8 | 1.15 |
| 10 | 395 | 22.8 | 20.3 | 20.8 | 12.9 | 6.6 | 5.3 | 1.23 |

## m64004e_231016_235852.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads

32,066 reads; 10 blocks of 3,206 reads; the first 400 reads of each block.
Chi-square 77 on 72 degrees of freedom (z 0.4); V 0.050 against 0.048 for random order; **consistent with random order**.

Share of the reads of each block (%) for the six most abundant strains, and the mean expected errors:

| block | reads | Escherichia coli 700926 | Staphylococcus epidermid | Porphyromonas gingivalis | Streptococcus mutans 700 | Bacillus pacificus 10987 | Clostridium beijerinckii | mean expected errors |
|---|---|---|---|---|---|---|---|---|
| 1 | 397 | 24.9 | 28.2 | 17.9 | 9.8 | 6.0 | 4.0 | 1.25 |
| 2 | 399 | 25.8 | 25.8 | 18.8 | 13.5 | 4.5 | 4.0 | 1.47 |
| 3 | 397 | 19.9 | 23.4 | 23.7 | 12.8 | 6.5 | 2.3 | 1.21 |
| 4 | 395 | 23.8 | 20.5 | 25.1 | 11.1 | 5.3 | 4.1 | 1.47 |
| 5 | 400 | 27.2 | 21.0 | 21.0 | 13.2 | 4.8 | 5.0 | 1.32 |
| 6 | 397 | 27.7 | 24.2 | 17.4 | 12.1 | 7.6 | 2.8 | 1.18 |
| 7 | 399 | 23.8 | 21.3 | 19.0 | 13.8 | 8.8 | 4.0 | 1.21 |
| 8 | 400 | 25.8 | 23.8 | 21.8 | 13.2 | 5.2 | 3.2 | 1.67 |
| 9 | 400 | 26.8 | 21.5 | 18.0 | 16.8 | 5.2 | 2.5 | 1.06 |
| 10 | 396 | 24.0 | 24.5 | 18.2 | 12.1 | 6.3 | 4.5 | 1.10 |


## T-cal: Revio against Sequel II (reference: the refined set). T-cal-1 below is the gate T-cal-R1 and T-cal-2 is T-cal-R2

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


## Truth test: Revio

## Revio

149,897 reads between the primers; median length 1472 nt, window 1320 to 1620 nt; the 75th percentile of the expected errors is 0.77, so the package's rule gives **maxEE 2**.

Quality scores: highest 40, 7 distinct values (3, 10, 17, 22, 27, 35, 40); error model: **binned:3,10,17,22,27,35,40**.

**Gate (T2): MET.** 15 of 15 strains of the three highest tiers have an exact or an added ASV (needed: 14); 49 of 49 sequences of the replication set recovered (needed: 90%).
**Gate (T3): MET.** 0.00% of the final reads are in ASVs that are neither exact nor added (at most 2%).
**Gate (T5): MET.** Spearman 0.97 over 17 strains (at least 0.7).
**Gate (T6): MET.** the rule gives maxEE 2, the same condition as the standard.

| condition | maxEE | window | primers | error model | reads kept % | final ASVs | exact | added | near | other | chimeric ASVs | exact reads % | unexplained reads % | chimeric reads % | reference variants recovered | top strains | replicated | Spearman | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ee2 | 2 | yes | cutadapt | binned:3,10,17,22,27,35,40 | 82.7 | 51 | 41 | 10 | 0 | 0 | 7 | 88.3 | 0.00 | 0.11 | 51 of 69 | 15 of 15 | 49 of 49 | 0.97 | 12.4 |
| ee2_dada2primers | 2 | yes | dada2 | binned:3,10,17,22,27,35,40 | 83.4 | 51 | 41 | 10 | 0 | 0 | 7 | 88.3 | 0.00 | 0.11 | 51 of 69 | 15 of 15 | 49 of 49 | 0.97 | 11.5 |
| ee2_naive | 2 | yes | cutadapt | PacBioErrfun | 82.7 | 51 | 41 | 10 | 0 | 0 | 7 | 88.3 | 0.00 | 0.11 | 51 of 69 | 15 of 15 | 49 of 49 | 0.97 | 11.1 |

Scored against the original variants (no gate):

| condition | variants recovered | 'other' reads % | top strains | big variants |
|---|---|---|---|---|
| ee2 | 40 of 60 | 3.03 | 14 of 15 | 15 of 19 |
| ee2_dada2primers | 40 of 60 | 3.01 | 14 of 15 | 15 of 19 |
| ee2_naive | 40 of 60 | 3.03 | 14 of 15 | 15 of 19 |

The tables of every strain and every ASV are in truth_strains.tsv and truth_asvs_*.tsv. 'Top strains' are those with a genomic share of 0.18% or more; 'unexplained' reads are those in ASVs that are neither exact nor added; 'replicated' counts the sequences of the replication set that were recovered.


## The predictions (written before the data were seen)

1. The Revio reads are binned (highest Q at most 40 and at most 12 distinct values): highest Q 40, 7 distinct values: as predicted.
2. The binned model recovers at least as many of the replication set as the naive condition: 49 against 49: as predicted.
3. At least 90% of the replication set is found again: 49 of 49 (100.0%): as predicted.
4. The order check flags the Revio files and not the Sequel II files: Revio 3 of 3 NOT RANDOM, Sequel II 0 of 3: as predicted.
5. T-cal and the truth test see the same composition in each Revio file (Spearman at least 0.9): Fwd_04--Kinnex16S_Rev_22 0.99, Fwd_07--Kinnex16S_Rev_30 1.00, Fwd_09--Kinnex16S_Rev_29 0.99: as predicted.

## Send back

- this file (C:\data\runs\20_night9b_revio\NIGHT9_SUMMARY.md)
- C:\data\runs\20_night9b_revio\quality.tsv
- C:\data\runs\20_night9b_revio\tcal\TCAL.md
- C:\data\runs\20_night9b_revio\truth\TRUTH.md, its truth_conditions.tsv and truth_strains.tsv
- C:\data\runs\20_night9b_revio\night9.log if a step failed
