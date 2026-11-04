# Is the order of the reads random?

Each file is split into blocks of consecutive reads; the first reads of each block are cut between the primers and given the strain of their nearest expected variant. A chi-square test of homogeneity on the strains with at least 1% of the sample asks whether the strains are spread evenly over the blocks; V is Cramér's V, and 'V for random order' is what a table of that size gives by chance. NOT RANDOM: the statistic is more than 4 standard deviations above its expected value and V is more than 2 times that of random order.

## m64004e_231003_184443.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads

394,216 reads; 10 blocks of 39,421 reads; the first 400 reads of each block.
Chi-square 72 on 63 degrees of freedom (z 0.8); V 0.051 against 0.048 for random order; **consistent with random order**.

Share of the reads of each block (%) for the six most abundant strains, and the mean expected errors:

| block | reads | Streptococcus mutans 700 | Staphylococcus epidermid | Escherichia coli 700926 | Porphyromonas gingivalis | Bacillus pacificus 10987 | Clostridium beijerinckii | mean expected errors |
|---|---|---|---|---|---|---|---|---|
| 1 | 394 | 43.4 | 15.0 | 16.2 | 12.4 | 4.3 | 3.6 | 2.30 |
| 2 | 396 | 42.9 | 13.6 | 19.9 | 10.9 | 2.3 | 3.0 | 2.25 |
| 3 | 396 | 44.4 | 16.7 | 14.6 | 12.1 | 4.5 | 1.5 | 2.41 |
| 4 | 395 | 44.6 | 16.2 | 14.9 | 12.2 | 3.5 | 3.3 | 2.16 |
| 5 | 397 | 45.1 | 14.6 | 16.6 | 15.1 | 2.3 | 1.3 | 2.55 |
| 6 | 397 | 50.6 | 12.3 | 14.4 | 13.1 | 2.8 | 0.8 | 2.35 |
| 7 | 395 | 47.8 | 18.2 | 13.2 | 9.1 | 3.8 | 3.3 | 2.63 |
| 8 | 395 | 46.6 | 13.7 | 14.4 | 11.9 | 4.3 | 2.3 | 2.54 |
| 9 | 397 | 46.3 | 17.4 | 11.6 | 11.6 | 4.8 | 2.8 | 2.44 |
| 10 | 398 | 40.5 | 17.6 | 17.6 | 13.3 | 3.8 | 2.8 | 2.45 |

## m64004e_231003_184443.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads

221,227 reads; 10 blocks of 22,122 reads; the first 400 reads of each block.
Chi-square 111 on 81 degrees of freedom (z 2.3); V 0.056 against 0.048 for random order; **consistent with random order**.

Share of the reads of each block (%) for the six most abundant strains, and the mean expected errors:

| block | reads | Escherichia coli 700926 | Staphylococcus epidermid | Porphyromonas gingivalis | Streptococcus mutans 700 | Bacillus pacificus 10987 | Clostridium beijerinckii | mean expected errors |
|---|---|---|---|---|---|---|---|---|
| 1 | 400 | 24.8 | 24.2 | 19.8 | 10.0 | 8.5 | 4.0 | 2.67 |
| 2 | 396 | 26.5 | 28.5 | 14.9 | 14.6 | 5.1 | 3.8 | 2.47 |
| 3 | 394 | 24.6 | 22.8 | 19.5 | 12.9 | 5.8 | 2.5 | 2.52 |
| 4 | 397 | 23.9 | 24.2 | 17.9 | 13.4 | 7.8 | 2.5 | 2.83 |
| 5 | 396 | 26.3 | 23.5 | 20.2 | 13.4 | 6.6 | 4.0 | 2.21 |
| 6 | 398 | 22.6 | 24.1 | 16.8 | 13.8 | 5.8 | 3.8 | 2.86 |
| 7 | 398 | 27.6 | 25.4 | 13.8 | 12.3 | 5.8 | 3.8 | 2.50 |
| 8 | 397 | 23.9 | 24.2 | 22.7 | 14.4 | 5.5 | 3.5 | 2.75 |
| 9 | 400 | 24.2 | 20.0 | 17.5 | 15.2 | 8.2 | 5.5 | 2.17 |
| 10 | 398 | 28.9 | 29.1 | 15.1 | 11.6 | 4.3 | 2.8 | 2.10 |

## m64004e_231003_184443.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads

287,387 reads; 10 blocks of 28,738 reads; the first 400 reads of each block.
Chi-square 62 on 81 degrees of freedom (z -1.5); V 0.042 against 0.048 for random order; **consistent with random order**.

Share of the reads of each block (%) for the six most abundant strains, and the mean expected errors:

| block | reads | Escherichia coli 700926 | Staphylococcus epidermid | Porphyromonas gingivalis | Streptococcus mutans 700 | Bacillus pacificus 10987 | Clostridium beijerinckii | mean expected errors |
|---|---|---|---|---|---|---|---|---|
| 1 | 397 | 25.2 | 23.2 | 19.9 | 10.1 | 8.3 | 2.8 | 2.32 |
| 2 | 396 | 26.5 | 23.5 | 19.4 | 11.6 | 5.6 | 3.8 | 2.09 |
| 3 | 398 | 24.9 | 23.4 | 17.1 | 14.8 | 6.8 | 4.3 | 2.49 |
| 4 | 397 | 25.2 | 23.4 | 18.4 | 11.3 | 6.8 | 5.3 | 2.36 |
| 5 | 397 | 24.9 | 24.7 | 19.6 | 11.8 | 5.5 | 4.0 | 1.98 |
| 6 | 399 | 25.6 | 24.6 | 20.6 | 13.0 | 3.8 | 4.0 | 2.14 |
| 7 | 396 | 24.0 | 26.3 | 21.0 | 11.6 | 5.1 | 4.0 | 2.40 |
| 8 | 399 | 25.8 | 25.1 | 19.0 | 11.5 | 6.5 | 4.3 | 2.15 |
| 9 | 399 | 22.1 | 25.8 | 18.8 | 12.5 | 5.5 | 3.8 | 2.30 |
| 10 | 399 | 24.1 | 27.8 | 15.3 | 9.8 | 7.5 | 4.8 | 2.15 |

