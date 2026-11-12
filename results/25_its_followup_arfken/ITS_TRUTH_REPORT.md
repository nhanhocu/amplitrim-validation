# ITS truth test

The criteria (P80 to P82) are in TEST_REGISTER.md and were fixed before this ran.

## Verdicts

- **P80** MET: On the mixes, allowing 2 mismatches raises the share of merged pairs in spurious sequences by at most 1 point on every marker: its1 -0.00 points (0.01% to 0.01%), its2 +0.48 points (8.50% to 8.98%)
- **P81** MET: On the mixes, allowing 2 mismatches does not lower the share of the reference sequences that are found, on any marker: its1 71.1% to 80.0%, its2 100.0% to 100.0%
- **P82** NOT MET: On the mixes, allowing 2 mismatches merges at least 2 points more of the input pairs on at least one marker: its1 +1.9 points, its2 +0.2 points

## ITS1 mixes

Reference sequences per isolate: C 1, K 4, M 5, P 2, T 1. Mix samples: 9.

| mismatches allowed | merged (share of the input pairs) | merged pairs in spurious sequences | reference sequences found |
|---|---|---|---|
| 0 (default) | 72.42% | 0.01% | 71.11% |
| 1 | 74.24% | 0.01% | 71.11% |
| 2 | 74.34% | 0.01% | 80.00% |
| 5 | 74.34% | 0.01% | 80.00% |

## ITS2 mixes

Reference sequences per isolate: C 1, K 2, M 1, P 4, T 1. Mix samples: 9.

| mismatches allowed | merged (share of the input pairs) | merged pairs in spurious sequences | reference sequences found |
|---|---|---|---|
| 0 (default) | 37.28% | 8.50% | 100.00% |
| 1 | 37.40% | 8.80% | 100.00% |
| 2 | 37.51% | 8.98% | 100.00% |
| 5 | 37.67% | 9.37% | 100.00% |

Next: send this file.
