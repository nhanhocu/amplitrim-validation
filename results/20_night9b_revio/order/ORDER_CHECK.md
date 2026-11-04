# Is the order of the reads random?

Each file is split into blocks of consecutive reads; the first reads of each block are cut between the primers and given the strain of their nearest expected variant. A chi-square test of homogeneity on the strains with at least 1% of the sample asks whether the strains are spread evenly over the blocks; V is Cramér's V, and 'V for random order' is what a table of that size gives by chance. NOT RANDOM: the statistic is more than 4 standard deviations above its expected value and V is more than 2 times that of random order.

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

