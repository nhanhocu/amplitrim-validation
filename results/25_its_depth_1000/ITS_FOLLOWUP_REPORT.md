# ITS follow-up

The criteria (P68 to P75) are in TEST_REGISTER.md and were fixed before this ran.

## Verdicts

- **P68** MET: On the second ITS study, allowing 2 mismatches merges at least 50% of the pairs that the default refuses for mismatches or indels: 99.7%
- **P69** NOT MET: On the second ITS study, the share of pairs refused for mismatches or indels is at least 15 points higher in the longest third of the overlaps (from 280 nt) than in the shortest third (up to 193 nt): 63.5% against 65.3% (-1.7 points)
- **P70** MET: On the second ITS study, at least 20% of the pairs refused for mismatches or indels have an indel: 99.4%
- **P71** MET: The median overlap of the pairs that enter the merge step is longer on the second ITS study than on the first: 256 nt against 188 nt
- **P72** NOT MET: Allowing 2 mismatches raises the median number of ASVs per sample by at most 10% on both ITS studies: second ITS study +400.0%, first ITS study +6.7%
- **P73** NOT MET: On soil V4 at AmpliTrim's cut, at least 50% of the pairs that mergePairs refuses have a forward and a reverse sequence that each occur in an accepted pair of the same sample (the halves are good, the pairing is not): 26.0%
- **P74** not decided: the single-isolate libraries were not run
- **P75** NOT MET: On the second ITS study, at least 50% of the pairs that mergePairs refuses have a forward and a reverse sequence that each occur in an accepted pair of the same sample: 0.5%

## its2 (9 samples, 8,936 input pairs; no truncation)

| step | share of the input pairs |
|---|---|
| pass the filter | 83.11% |
| enter the merge step | 29.61% |
| refused: overlap shorter than 12 nt | 1.45% |
| refused: mismatches or indels in the overlap | 19.36% |
| refused: a clean overlap that is still refused | 0.00% |

| mismatches allowed | merged (share of the input pairs) | of the default's mismatch refusals | of all the default's refused pairs | median ASVs per sample |
|---|---|---|---|---|
| 0 (default) | 8.80% |  |  | 4 |
| 1 | 23.43% | 75.6% | 70.3% | 16 |
| 2 | 28.10% | 99.7% | 92.7% | 20 |
| 5 | 29.21% | 105.4% | 98.1% | 20 |

- Of the pairs refused for any reason, 0.5% have a forward and a reverse sequence that each occur in an accepted pair of the same sample.
- Of the pairs refused for any reason, 6.9% have no overlap at all in the alignment (0 columns).

- Median overlap of the pairs that enter the merge step: 256 nt (shortest third up to 193 nt, longest third from 280 nt).
- Refused for mismatches or indels: 65.3% in the shortest third, 63.5% in the longest.
- Of the pairs refused for mismatches or indels, 99.4% have an indel.

## its (37 samples, 36,790 input pairs; no truncation)

| step | share of the input pairs |
|---|---|
| pass the filter | 74.30% |
| enter the merge step | 45.60% |
| refused: overlap shorter than 12 nt | 4.49% |
| refused: mismatches or indels in the overlap | 4.79% |
| refused: a clean overlap that is still refused | 0.00% |

| mismatches allowed | merged (share of the input pairs) | of the default's mismatch refusals | of all the default's refused pairs | median ASVs per sample |
|---|---|---|---|---|
| 0 (default) | 36.32% |  |  | 30 |
| 1 | 38.70% | 49.6% | 25.6% | 31 |
| 2 | 40.79% | 93.2% | 48.1% | 32 |
| 5 | 42.28% | 124.4% | 64.2% | 34 |

- Of the pairs refused for any reason, 1.1% have a forward and a reverse sequence that each occur in an accepted pair of the same sample.
- Of the pairs refused for any reason, 37.1% have no overlap at all in the alignment (0 columns).

- Median overlap of the pairs that enter the merge step: 188 nt (shortest third up to 181 nt, longest third from 194 nt).
- Refused for mismatches or indels: 14.1% in the shortest third, 18.7% in the longest.
- Of the pairs refused for mismatches or indels, 43.6% have an indel.

## v4 (36 samples, 35,735 input pairs; truncLen 124,115)

| step | share of the input pairs |
|---|---|
| pass the filter | 98.59% |
| enter the merge step | 67.72% |
| refused: overlap shorter than 12 nt | 16.55% |
| refused: mismatches or indels in the overlap | 0.00% |
| refused: a clean overlap that is still refused | 0.00% |

| mismatches allowed | merged (share of the input pairs) | of the default's mismatch refusals | of all the default's refused pairs | median ASVs per sample |
|---|---|---|---|---|
| 0 (default) | 51.17% |  |  | 32 |
| 1 | 56.82% |  | 34.2% | 43 |
| 2 | 61.01% |  | 59.5% | 55 |
| 5 | 63.90% |  | 76.9% | 69.5 |

- Of the pairs refused for any reason, 26.0% have a forward and a reverse sequence that each occur in an accepted pair of the same sample.
- Of the pairs refused for any reason, 58.9% have no overlap at all in the alignment (0 columns).

- Median overlap of the pairs that enter the merge step: 32 nt (shortest third up to 32 nt, longest third from 32 nt).
- Refused for mismatches or indels: 0.0% in the shortest third, 0.0% in the longest.
- Of the pairs refused for mismatches or indels, none have an indel.

Next: send this file.
