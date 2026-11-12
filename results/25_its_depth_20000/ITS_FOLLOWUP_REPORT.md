# ITS follow-up

The criteria (P68 to P75) are in TEST_REGISTER.md and were fixed before this ran.

## Verdicts

- **P68** MET: On the second ITS study, allowing 2 mismatches merges at least 50% of the pairs that the default refuses for mismatches or indels: 102.0%
- **P69** NOT MET: On the second ITS study, the share of pairs refused for mismatches or indels is at least 15 points higher in the longest third of the overlaps (from 282 nt) than in the shortest third (up to 217 nt): 71.5% against 69.8% (+1.7 points)
- **P70** MET: On the second ITS study, at least 20% of the pairs refused for mismatches or indels have an indel: 98.6%
- **P71** MET: The median overlap of the pairs that enter the merge step is longer on the second ITS study than on the first: 268 nt against 188 nt
- **P72** NOT MET: Allowing 2 mismatches raises the median number of ASVs per sample by at most 10% on both ITS studies: second ITS study +227.6%, first ITS study +3.4%
- **P73** MET: On soil V4 at AmpliTrim's cut, at least 50% of the pairs that mergePairs refuses have a forward and a reverse sequence that each occur in an accepted pair of the same sample (the halves are good, the pairing is not): 64.3%
- **P74** not decided: the single-isolate libraries were not run
- **P75** NOT MET: On the second ITS study, at least 50% of the pairs that mergePairs refuses have a forward and a reverse sequence that each occur in an accepted pair of the same sample: 0.3%

## its2 (9 samples, 162,038 input pairs; no truncation)

| step | share of the input pairs |
|---|---|
| pass the filter | 82.82% |
| enter the merge step | 65.48% |
| refused: overlap shorter than 12 nt | 4.28% |
| refused: mismatches or indels in the overlap | 44.58% |
| refused: a clean overlap that is still refused | 0.00% |

| mismatches allowed | merged (share of the input pairs) | of the default's mismatch refusals | of all the default's refused pairs | median ASVs per sample |
|---|---|---|---|---|
| 0 (default) | 16.62% |  |  | 58 |
| 1 | 47.98% | 70.4% | 64.2% | 148 |
| 2 | 62.10% | 102.0% | 93.1% | 190 |
| 5 | 63.85% | 106.0% | 96.7% | 200 |

- Of the pairs refused for any reason, 0.3% have a forward and a reverse sequence that each occur in an accepted pair of the same sample.
- Of the pairs refused for any reason, 7.0% have no overlap at all in the alignment (0 columns).

- Median overlap of the pairs that enter the merge step: 268 nt (shortest third up to 217 nt, longest third from 282 nt).
- Refused for mismatches or indels: 69.8% in the shortest third, 71.5% in the longest.
- Of the pairs refused for mismatches or indels, 98.6% have an indel.

## its (37 samples, 653,775 input pairs; no truncation)

| step | share of the input pairs |
|---|---|
| pass the filter | 74.16% |
| enter the merge step | 66.00% |
| refused: overlap shorter than 12 nt | 3.82% |
| refused: mismatches or indels in the overlap | 8.06% |
| refused: a clean overlap that is still refused | 0.00% |

| mismatches allowed | merged (share of the input pairs) | of the default's mismatch refusals | of all the default's refused pairs | median ASVs per sample |
|---|---|---|---|---|
| 0 (default) | 54.12% |  |  | 148 |
| 1 | 59.68% | 69.0% | 46.8% | 155 |
| 2 | 61.91% | 96.7% | 65.6% | 153 |
| 5 | 63.40% | 115.1% | 78.1% | 156 |

- Of the pairs refused for any reason, 0.9% have a forward and a reverse sequence that each occur in an accepted pair of the same sample.
- Of the pairs refused for any reason, 19.5% have no overlap at all in the alignment (0 columns).

- Median overlap of the pairs that enter the merge step: 188 nt (shortest third up to 179 nt, longest third from 195 nt).
- Refused for mismatches or indels: 13.9% in the shortest third, 22.6% in the longest.
- Of the pairs refused for mismatches or indels, 50.1% have an indel.

## v4 (36 samples, 619,886 input pairs; truncLen 124,115)

| step | share of the input pairs |
|---|---|
| pass the filter | 98.56% |
| enter the merge step | 89.33% |
| refused: overlap shorter than 12 nt | 12.81% |
| refused: mismatches or indels in the overlap | 0.00% |
| refused: a clean overlap that is still refused | 0.00% |

| mismatches allowed | merged (share of the input pairs) | of the default's mismatch refusals | of all the default's refused pairs | median ASVs per sample |
|---|---|---|---|---|
| 0 (default) | 76.52% |  |  | 300.5 |
| 1 | 81.76% |  | 40.9% | 282.5 |
| 2 | 84.77% |  | 64.4% | 271.5 |
| 5 | 86.77% |  | 80.0% | 262 |

- Of the pairs refused for any reason, 64.3% have a forward and a reverse sequence that each occur in an accepted pair of the same sample.
- Of the pairs refused for any reason, 59.7% have no overlap at all in the alignment (0 columns).

- Median overlap of the pairs that enter the merge step: 32 nt (shortest third up to 32 nt, longest third from 32 nt).
- Refused for mismatches or indels: 0.0% in the shortest third, 0.0% in the longest.
- Of the pairs refused for mismatches or indels, none have an indel.

Next: send this file.
