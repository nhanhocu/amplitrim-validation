# ITS follow-up

The criteria (P68 to P75) are in TEST_REGISTER.md and were fixed before this ran.

## Verdicts

- **P68** MET: On the second ITS study, allowing 2 mismatches merges at least 50% of the pairs that the default refuses for mismatches or indels: 102.0%
- **P69** NOT MET: On the second ITS study, the share of pairs refused for mismatches or indels is at least 15 points higher in the longest third of the overlaps (from 280 nt) than in the shortest third (up to 204 nt): 70.1% against 70.6% (-0.5 points)
- **P70** MET: On the second ITS study, at least 20% of the pairs refused for mismatches or indels have an indel: 98.6%
- **P71** MET: The median overlap of the pairs that enter the merge step is longer on the second ITS study than on the first: 265 nt against 188 nt
- **P72** NOT MET: Allowing 2 mismatches raises the median number of ASVs per sample by at most 10% on both ITS studies: second ITS study +266.7%, first ITS study +9.5%
- **P73** NOT MET: On soil V4 at AmpliTrim's cut, at least 50% of the pairs that mergePairs refuses have a forward and a reverse sequence that each occur in an accepted pair of the same sample (the halves are good, the pairing is not): 45.8%
- **P74** not decided: the single-isolate libraries were not run
- **P75** NOT MET: On the second ITS study, at least 50% of the pairs that mergePairs refuses have a forward and a reverse sequence that each occur in an accepted pair of the same sample: 0.3%

## its2 (9 samples, 43,405 input pairs; no truncation)

| step | share of the input pairs |
|---|---|
| pass the filter | 82.86% |
| enter the merge step | 52.77% |
| refused: overlap shorter than 12 nt | 3.81% |
| refused: mismatches or indels in the overlap | 35.00% |
| refused: a clean overlap that is still refused | 0.00% |

| mismatches allowed | merged (share of the input pairs) | of the default's mismatch refusals | of all the default's refused pairs | median ASVs per sample |
|---|---|---|---|---|
| 0 (default) | 13.96% |  |  | 24 |
| 1 | 39.15% | 72.0% | 64.9% | 64 |
| 2 | 49.66% | 102.0% | 92.0% | 88 |
| 5 | 51.53% | 107.3% | 96.8% | 97 |

- Of the pairs refused for any reason, 0.3% have a forward and a reverse sequence that each occur in an accepted pair of the same sample.
- Of the pairs refused for any reason, 8.7% have no overlap at all in the alignment (0 columns).

- Median overlap of the pairs that enter the merge step: 265 nt (shortest third up to 204 nt, longest third from 280 nt).
- Refused for mismatches or indels: 70.6% in the shortest third, 70.1% in the longest.
- Of the pairs refused for mismatches or indels, 98.6% have an indel.

## its (37 samples, 178,657 input pairs; no truncation)

| step | share of the input pairs |
|---|---|
| pass the filter | 74.24% |
| enter the merge step | 58.37% |
| refused: overlap shorter than 12 nt | 5.07% |
| refused: mismatches or indels in the overlap | 6.43% |
| refused: a clean overlap that is still refused | 0.00% |

| mismatches allowed | merged (share of the input pairs) | of the default's mismatch refusals | of all the default's refused pairs | median ASVs per sample |
|---|---|---|---|---|
| 0 (default) | 46.87% |  |  | 105 |
| 1 | 51.16% | 66.7% | 37.3% | 114 |
| 2 | 53.04% | 96.0% | 53.7% | 115 |
| 5 | 55.29% | 130.9% | 73.2% | 117 |

- Of the pairs refused for any reason, 0.8% have a forward and a reverse sequence that each occur in an accepted pair of the same sample.
- Of the pairs refused for any reason, 32.7% have no overlap at all in the alignment (0 columns).

- Median overlap of the pairs that enter the merge step: 188 nt (shortest third up to 181 nt, longest third from 195 nt).
- Refused for mismatches or indels: 11.4% in the shortest third, 22.3% in the longest.
- Of the pairs refused for mismatches or indels, 49.0% have an indel.

## v4 (36 samples, 173,367 input pairs; truncLen 124,115)

| step | share of the input pairs |
|---|---|
| pass the filter | 98.53% |
| enter the merge step | 82.35% |
| refused: overlap shorter than 12 nt | 15.51% |
| refused: mismatches or indels in the overlap | 0.00% |
| refused: a clean overlap that is still refused | 0.00% |

| mismatches allowed | merged (share of the input pairs) | of the default's mismatch refusals | of all the default's refused pairs | median ASVs per sample |
|---|---|---|---|---|
| 0 (default) | 66.84% |  |  | 174.5 |
| 1 | 73.07% |  | 40.2% | 198.5 |
| 2 | 76.83% |  | 64.4% | 211.5 |
| 5 | 79.54% |  | 81.8% | 221.5 |

- Of the pairs refused for any reason, 45.8% have a forward and a reverse sequence that each occur in an accepted pair of the same sample.
- Of the pairs refused for any reason, 59.7% have no overlap at all in the alignment (0 columns).

- Median overlap of the pairs that enter the merge step: 32 nt (shortest third up to 32 nt, longest third from 32 nt).
- Refused for mismatches or indels: 0.0% in the shortest third, 0.0% in the longest.
- Of the pairs refused for mismatches or indels, none have an indel.

Next: send this file.
