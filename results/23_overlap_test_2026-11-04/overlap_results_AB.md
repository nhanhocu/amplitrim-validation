# Minimum-overlap test (register section 27)

| dataset | arm | k | cut F/R | maxEE | pass % | merged % | variants | strains | reads in exact ASVs % | extra ASVs | ASVs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mockA | S | 10 | 273/247 | 2,3 | 71.8 | 69.5 | 36 | 12/14 | 99.78 | 16 | 52 |
| mockA | S | 15 | 273/247 | 2,3 | 71.8 | 69.4 | 35 | 11/14 | 99.77 | 17 | 52 |
| mockA | S | 20 | 273/247 | 2,3 | 71.8 | 68.5 | 34 | 10/14 | 99.76 | 19 | 53 |
| mockA | S | 25 | 273/247 | 2,3 | 71.8 | 49.4 | 20 | 5/14 | 97.98 | 57 | 77 |
| mockA | T | 10 | 273/245 | 2,3 | 72.3 | 70.0 | 36 | 12/14 | 99.77 | 17 | 53 |
| mockA | T | 12 | 273/247 | 2,3 | 71.8 | 69.5 | 36 | 12/14 | 99.78 | 16 | 52 |
| mockA | T | 15 | 273/250 | 2,3 | 70.8 | 68.5 | 36 | 12/14 | 99.79 | 13 | 49 |
| mockA | T | 20 | 273/255 | 2,3 | 69.2 | 66.6 | 36 | 12/14 | 99.80 | 11 | 47 |
| mockA | T | 25 | 273/260 | 2,3 | 67.9 | 65.4 | 36 | 12/14 | 99.81 | 8 | 44 |
| mockB | S | 10 | 274/253 | 4,8 | 72.2 | 70.4 | 6 | 3/3 | 75.24 | 69 | 75 |
| mockB | S | 15 | 274/253 | 4,8 | 72.2 | 67.3 | 3 | 2/3 | 74.35 | 68 | 71 |
| mockB | S | 20 | 274/253 | 4,8 | 72.2 | 67.3 | 3 | 2/3 | 74.40 | 67 | 70 |
| mockB | S | 25 | 274/253 | 4,8 | 72.2 | 67.3 | 3 | 2/3 | 74.40 | 67 | 70 |
| mockB | T | 10 | 274/251 | 4,8 | 72.8 | 71.1 | 6 | 3/3 | 75.07 | 71 | 77 |
| mockB | T | 12 | 274/253 | 4,8 | 72.2 | 70.4 | 6 | 3/3 | 75.24 | 69 | 75 |
| mockB | T | 15 | 274/256 | 4,8 | 71.0 | 68.6 | 7 | 3/3 | 75.11 | 67 | 74 |
| mockB | T | 20 | 274/261 | 4,8 | 69.2 | 66.8 | 7 | 3/3 | 74.89 | 66 | 73 |
| mockB | T | 25 | 274/266 | 4,8 | 67.0 | 63.9 | 6 | 3/3 | 75.45 | 54 | 60 |

Arm T: the cut follows k. Arm S: the cut of k = 12, only minOverlap changes.

## Verdicts
- **P-O1 not judged: only 2 of 4 datasets**: minOverlap 10 on the 12 cut: same merged share (0.1 points), no ASV that 12 lacks (2 of 2 datasets)
- **P-O2 not judged: only 2 of 4 datasets**: k = 12: reads in exact ASVs within 1.0 point of the best k, strains equal the best (2 of 2 datasets)
- **P-O3 NOT MET**: k = 12: no more than 2 unexpected ASVs more than at k = 20 (0 of 2 datasets)
- P-O4 (arm T): merged share at k = 25 at least 1 point below k = 12: 2 of 2 datasets (descriptive)
- P-O4 (arm S): merged share at k = 25 at least 1 point below k = 12: 2 of 2 datasets (descriptive)
