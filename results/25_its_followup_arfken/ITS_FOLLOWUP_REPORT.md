# ITS follow-up

The criteria (P68 to P75) are in TEST_REGISTER.md and were fixed before this ran.

## Verdicts

- **P68** not decided: the second ITS study was not run
- **P69** not decided: the second ITS study was not run
- **P70** not decided: the second ITS study was not run
- **P71** not decided: both ITS studies are needed
- **P72** not decided: both ITS studies are needed, each with ASVs at the default
- **P73** not decided: soil V4 was not run
- **P74** MET: On the single-isolate libraries, allowing 2 mismatches adds at most 1 ASV per sample (median): arfken_its1 +0, arfken_its2 +0
- **P75** not decided: the second ITS study was not run

## arfken_its1 (15 samples, 74,151 input pairs; no truncation)

| step | share of the input pairs |
|---|---|
| pass the filter | 62.20% |
| enter the merge step | 62.11% |
| refused: overlap shorter than 12 nt | 0.00% |
| refused: mismatches or indels in the overlap | 9.51% |
| refused: a clean overlap that is still refused | 0.00% |

| mismatches allowed | merged (share of the input pairs) | of the default's mismatch refusals | of all the default's refused pairs | median ASVs per sample |
|---|---|---|---|---|
| 0 (default) | 52.60% |  |  | 2 |
| 1 | 62.03% | 99.2% | 99.2% | 2 |
| 2 | 62.11% | 100.0% | 100.0% | 2 |
| 5 | 62.11% | 100.0% | 100.0% | 2 |

- Of the pairs refused for any reason, 1.8% have a forward and a reverse sequence that each occur in an accepted pair of the same sample.
- Of the pairs refused for any reason, 0.0% have no overlap at all in the alignment (0 columns).

- Median overlap of the pairs that enter the merge step: 199 nt (shortest third up to 199 nt, longest third from 214 nt).
- Refused for mismatches or indels: 2.2% in the shortest third, 15.5% in the longest.
- Of the pairs refused for mismatches or indels, 85.1% have an indel.

## arfken_its2 (15 samples, 73,441 input pairs; no truncation)

| step | share of the input pairs |
|---|---|
| pass the filter | 37.70% |
| enter the merge step | 37.68% |
| refused: overlap shorter than 12 nt | 0.00% |
| refused: mismatches or indels in the overlap | 0.10% |
| refused: a clean overlap that is still refused | 0.00% |

| mismatches allowed | merged (share of the input pairs) | of the default's mismatch refusals | of all the default's refused pairs | median ASVs per sample |
|---|---|---|---|---|
| 0 (default) | 37.57% |  |  | 1 |
| 1 | 37.68% | 100.0% | 100.0% | 1 |
| 2 | 37.68% | 100.0% | 100.0% | 1 |
| 5 | 37.68% | 100.0% | 100.0% | 1 |

- Of the pairs refused for any reason, 1.3% have a forward and a reverse sequence that each occur in an accepted pair of the same sample.
- Of the pairs refused for any reason, 0.0% have no overlap at all in the alignment (0 columns).

- Median overlap of the pairs that enter the merge step: 240 nt (shortest third up to 168 nt, longest third from 262 nt).
- Refused for mismatches or indels: 0.0% in the shortest third, 0.0% in the longest.
- Of the pairs refused for mismatches or indels, 0.0% have an indel.

## arfken_mix_its1 (9 samples, 44,547 input pairs; no truncation)

| step | share of the input pairs |
|---|---|
| pass the filter | 74.49% |
| enter the merge step | 74.34% |
| refused: overlap shorter than 12 nt | 0.00% |
| refused: mismatches or indels in the overlap | 1.92% |
| refused: a clean overlap that is still refused | 0.00% |

| mismatches allowed | merged (share of the input pairs) | of the default's mismatch refusals | of all the default's refused pairs | median ASVs per sample |
|---|---|---|---|---|
| 0 (default) | 72.42% |  |  | 4 |
| 1 | 74.24% | 94.7% | 94.7% | 4 |
| 2 | 74.34% | 100.0% | 100.0% | 6 |
| 5 | 74.34% | 100.0% | 100.0% | 6 |

- Of the pairs refused for any reason, 2.7% have a forward and a reverse sequence that each occur in an accepted pair of the same sample.
- Of the pairs refused for any reason, 0.0% have no overlap at all in the alignment (0 columns).

- Median overlap of the pairs that enter the merge step: 199 nt (shortest third up to 199 nt, longest third from 215 nt).
- Refused for mismatches or indels: 2.0% in the shortest third, 3.0% in the longest.
- Of the pairs refused for mismatches or indels, 0.0% have an indel.

## arfken_mix_its2 (9 samples, 44,269 input pairs; no truncation)

| step | share of the input pairs |
|---|---|
| pass the filter | 38.06% |
| enter the merge step | 37.76% |
| refused: overlap shorter than 12 nt | 0.14% |
| refused: mismatches or indels in the overlap | 0.34% |
| refused: a clean overlap that is still refused | 0.00% |

| mismatches allowed | merged (share of the input pairs) | of the default's mismatch refusals | of all the default's refused pairs | median ASVs per sample |
|---|---|---|---|---|
| 0 (default) | 37.28% |  |  | 10 |
| 1 | 37.40% | 34.2% | 24.3% | 10 |
| 2 | 37.51% | 67.1% | 47.7% | 12 |
| 5 | 37.67% | 113.2% | 80.4% | 12 |

- Of the pairs refused for any reason, 31.3% have a forward and a reverse sequence that each occur in an accepted pair of the same sample.
- Of the pairs refused for any reason, 19.2% have no overlap at all in the alignment (0 columns).

- Median overlap of the pairs that enter the merge step: 240 nt (shortest third up to 240 nt, longest third from 262 nt).
- Refused for mismatches or indels: 0.0% in the shortest third, 2.8% in the longest.
- Of the pairs refused for mismatches or indels, 38.8% have an indel.

Next: send this file.
