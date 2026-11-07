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
