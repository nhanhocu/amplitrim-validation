# ITS depth series

The criterion (P76) is in TEST_REGISTER.md and was fixed before this ran.

## Verdict

- **P76** NOT MET: The share of the input pairs that merge at the default is within 5 points between 5,000 and 20,000 pairs per sample, on every label that has both: its2 14.0% to 16.6% (+2.7 points), its 46.9% to 54.1% (+7.2 points), v4 66.8% to 76.5% (+9.7 points)

## its2

| pairs per sample | samples | pass the filter | enter the merge step | refused: short | refused: mismatches or indels | merged at the default | of the refused, merged at 5 mismatches |
|---|---|---|---|---|---|---|---|
| 1,000 | 9 | 83.11% | 29.61% | 1.45% | 19.36% | 8.80% | 98.1% |
| 5,000 | 9 | 82.86% | 52.77% | 3.81% | 35.00% | 13.96% | 96.8% |
| 20,000 | 9 | 82.82% | 65.48% | 4.28% | 44.58% | 16.62% | 96.7% |

## its

| pairs per sample | samples | pass the filter | enter the merge step | refused: short | refused: mismatches or indels | merged at the default | of the refused, merged at 5 mismatches |
|---|---|---|---|---|---|---|---|
| 1,000 | 37 | 74.30% | 45.60% | 4.49% | 4.79% | 36.32% | 64.2% |
| 5,000 | 37 | 74.24% | 58.37% | 5.07% | 6.43% | 46.87% | 73.2% |
| 20,000 | 37 | 74.16% | 66.00% | 3.82% | 8.06% | 54.12% | 78.1% |

## v4

| pairs per sample | samples | pass the filter | enter the merge step | refused: short | refused: mismatches or indels | merged at the default | of the refused, merged at 5 mismatches |
|---|---|---|---|---|---|---|---|
| 1,000 | 36 | 98.59% | 67.72% | 16.55% | 0.00% | 51.17% | 76.9% |
| 5,000 | 36 | 98.53% | 82.35% | 15.51% | 0.00% | 66.84% | 81.8% |
| 20,000 | 36 | 98.56% | 89.33% | 12.81% | 0.00% | 76.52% | 80.0% |

Next: send this file.
