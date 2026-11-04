# Minimum-overlap test (register section 27)

| dataset | arm | k | cut F/R | maxEE | pass % | merged % | variants | strains | reads in exact ASVs % | extra ASVs | ASVs | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| d6300_V3-V4 | S | 10 | 224/218 | 2 | 94.6 | 90.6 | 10 | 8/8 | 97.92 | 1 | 11 |  |
| d6300_V3-V4 | S | 15 | 224/218 | 2 | 94.6 | 0.0 | 0 | 0/8 | 0.00 | 0 | 0 |  |
| d6300_V3-V4 | S | 20 | 224/218 | 2 | 94.6 | 0.0 | 0 | 0/8 | 0.00 | 0 | 0 |  |
| d6300_V3-V4 | S | 25 | 224/218 | 2 | 94.6 | 0.0 | 0 | 0/8 | 0.00 | 0 | 0 |  |
| d6300_V3-V4 | T | 10 | 224/216 | 2 | 94.7 | 90.6 | 10 | 8/8 | 97.93 | 1 | 11 |  |
| d6300_V3-V4 | T | 12 | 224/218 | 2 | 94.6 | 90.6 | 10 | 8/8 | 97.92 | 1 | 11 |  |
| d6300_V3-V4 | T | 15 | 224/221 | 2 | 75.7 | 72.3 | 10 | 8/8 | 97.84 | 1 | 11 |  |
| d6300_V3-V4 | T | 20 | 224/226 | 2 | 28.1 | 26.8 | 10 | 8/8 | 97.86 | 1 | 11 |  |
| d6300_V3-V4 | T | 25 | 224/231 | 2 |  |  |  |  |  |  |  | no result: the cut is longer than the reads (DADA2 removed all reads) |
| d6300_V4-V5 | S | 10 | 282/280 | 2,3 | 70.1 | 63.3 | 9 | 8/9 | 98.79 | 2 | 11 |  |
| d6300_V4-V5 | S | 15 | 282/280 | 2,3 | 70.1 | 62.7 | 9 | 8/9 | 99.92 | 1 | 10 |  |
| d6300_V4-V5 | S | 20 | 282/280 | 2,3 | 70.1 | 62.7 | 9 | 8/9 | 99.92 | 1 | 10 |  |
| d6300_V4-V5 | S | 25 | 282/280 | 2,3 | 70.1 | 62.7 | 9 | 8/9 | 99.92 | 1 | 10 |  |
| d6300_V4-V5 | T | 10 | 282/278 | 2,3 | 77.8 | 70.0 | 9 | 8/9 | 98.88 | 2 | 11 |  |
| d6300_V4-V5 | T | 12 | 282/280 | 2,3 | 70.1 | 63.3 | 9 | 8/9 | 98.79 | 2 | 11 |  |
| d6300_V4-V5 | T | 15 | 282/283 | 2,3 | 0.0 | 0.0 | 0 | 0/9 | 0.00 | 3 | 3 |  |
| d6300_V4-V5 | T | 20 | 282/288 | 2,3 |  |  |  |  |  |  |  | no result: the cut is longer than the reads (DADA2 removed all reads) |
| d6300_V4-V5 | T | 25 | 282/293 | 2,3 |  |  |  |  |  |  |  | no result: the cut is longer than the reads (DADA2 removed all reads) |
| mockA | S | 10 | 273/247 | 2,3 | 71.8 | 69.5 | 36 | 12/14 | 99.78 | 16 | 52 |  |
| mockA | S | 15 | 273/247 | 2,3 | 71.8 | 69.4 | 35 | 11/14 | 99.77 | 17 | 52 |  |
| mockA | S | 20 | 273/247 | 2,3 | 71.8 | 68.5 | 34 | 10/14 | 99.76 | 19 | 53 |  |
| mockA | S | 25 | 273/247 | 2,3 | 71.8 | 49.4 | 20 | 5/14 | 97.98 | 57 | 77 |  |
| mockA | T | 10 | 273/245 | 2,3 | 72.3 | 70.0 | 36 | 12/14 | 99.77 | 17 | 53 |  |
| mockA | T | 12 | 273/247 | 2,3 | 71.8 | 69.5 | 36 | 12/14 | 99.78 | 16 | 52 |  |
| mockA | T | 15 | 273/250 | 2,3 | 70.8 | 68.5 | 36 | 12/14 | 99.79 | 13 | 49 |  |
| mockA | T | 20 | 273/255 | 2,3 | 69.2 | 66.6 | 36 | 12/14 | 99.80 | 11 | 47 |  |
| mockA | T | 25 | 273/260 | 2,3 | 67.9 | 65.4 | 36 | 12/14 | 99.81 | 8 | 44 |  |
| mockB | S | 10 | 274/253 | 4,8 | 72.2 | 70.4 | 6 | 3/3 | 75.24 | 69 | 75 |  |
| mockB | S | 15 | 274/253 | 4,8 | 72.2 | 67.3 | 3 | 2/3 | 74.35 | 68 | 71 |  |
| mockB | S | 20 | 274/253 | 4,8 | 72.2 | 67.3 | 3 | 2/3 | 74.40 | 67 | 70 |  |
| mockB | S | 25 | 274/253 | 4,8 | 72.2 | 67.3 | 3 | 2/3 | 74.40 | 67 | 70 |  |
| mockB | T | 10 | 274/251 | 4,8 | 72.8 | 71.1 | 6 | 3/3 | 75.07 | 71 | 77 |  |
| mockB | T | 12 | 274/253 | 4,8 | 72.2 | 70.4 | 6 | 3/3 | 75.24 | 69 | 75 |  |
| mockB | T | 15 | 274/256 | 4,8 | 71.0 | 68.6 | 7 | 3/3 | 75.11 | 67 | 74 |  |
| mockB | T | 20 | 274/261 | 4,8 | 69.2 | 66.8 | 7 | 3/3 | 74.89 | 66 | 73 |  |
| mockB | T | 25 | 274/266 | 4,8 | 67.0 | 63.9 | 6 | 3/3 | 75.45 | 54 | 60 |  |

Arm T: the cut follows k. Arm S: the cut of k = 12, only minOverlap changes.

## Verdicts
- **P-O1 MET**: minOverlap 10 on the 12 cut: same merged share (0.1 points), no ASV that 12 lacks (4 of 4 datasets)
- **P-O2 MET**: k = 12: reads in exact ASVs within 1.0 point of the best k, strains equal the best (4 of 4 datasets)
- **P-O3 NOT MET**: k = 12: no more than 2 unexpected ASVs more than at k = 20 (1 of 3 datasets)
- P-O4 (arm T): merged share at k = 25 at least 1 point below k = 12: 2 of 2 datasets (descriptive)
- P-O4 (arm S): merged share at k = 25 at least 1 point below k = 12: 3 of 4 datasets (descriptive)

ASV sets: see overlap_results_asv_sets.tsv; two runs with the same fingerprint have exactly the same ASVs.
