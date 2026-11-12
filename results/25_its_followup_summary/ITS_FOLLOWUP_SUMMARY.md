# ITS follow-up: summary

15 criteria (P68 to P82): 8 met, 7 not met, 0 not decided, 0 in no report.

## Outcome table for the register

| | Outcome |
|---|---|
| P68 | MET: On the second ITS study, allowing 2 mismatches merges at least 50% of the pairs that the default refuses for mismatches or indels: 102.0% |
| P69 | NOT MET: On the second ITS study, the share of pairs refused for mismatches or indels is at least 15 points higher in the longest third of the overlaps (from 280 nt) than in the shortest third (up to 204 nt): 70.1% against 70.6% (-0.5 points) |
| P70 | MET: On the second ITS study, at least 20% of the pairs refused for mismatches or indels have an indel: 98.6% |
| P71 | MET: The median overlap of the pairs that enter the merge step is longer on the second ITS study than on the first: 265 nt against 188 nt |
| P72 | NOT MET: Allowing 2 mismatches raises the median number of ASVs per sample by at most 10% on both ITS studies: second ITS study +266.7%, first ITS study +9.5% |
| P73 | NOT MET: On soil V4 at AmpliTrim's cut, at least 50% of the pairs that mergePairs refuses have a forward and a reverse sequence that each occur in an accepted pair of the same sample (the halves are good, the pairing is not): 45.8% |
| P74 | MET: On the single-isolate libraries, allowing 2 mismatches adds at most 1 ASV per sample (median): arfken_its1 +0, arfken_its2 +0 |
| P75 | NOT MET: On the second ITS study, at least 50% of the pairs that mergePairs refuses have a forward and a reverse sequence that each occur in an accepted pair of the same sample: 0.3% |
| P76 | NOT MET: The share of the input pairs that merge at the default is within 5 points between 5,000 and 20,000 pairs per sample, on every label that has both: its2 14.0% to 16.6% (+2.7 points), its 46.9% to 54.1% (+7.2 points), v4 66.8% to 76.5% (+9.7 points) |
| P77 | MET: AmpliTrim's predicted share of pairs that pass the filter is within 1 point of DADA2's on every group: arfken_its1 -0.21, arfken_its2 -0.09, arfken_mix_its1 +0.00, arfken_mix_its2 +0.00 |
| P78 | NOT MET: The estimate of the yield is too high by fewer points on the isolates than on the mixes, on every marker that has both: ITS1 +9.3 against +2.0, ITS2 +0.0 against +0.8 |
| P79 | MET: On the isolates the estimate of the yield is too high by less than 17 points: arfken_its1 +9.3, arfken_its2 +0.0 |
| P80 | MET: On the mixes, allowing 2 mismatches raises the share of merged pairs in spurious sequences by at most 1 point on every marker: its1 -0.00 points (0.01% to 0.01%), its2 +0.48 points (8.50% to 8.98%) |
| P81 | MET: On the mixes, allowing 2 mismatches does not lower the share of the reference sequences that are found, on any marker: its1 71.1% to 80.0%, its2 100.0% to 100.0% |
| P82 | NOT MET: On the mixes, allowing 2 mismatches merges at least 2 points more of the input pairs on at least one marker: its1 +1.9 points, its2 +0.2 points |

## Where each verdict comes from

- P68: `its_followup/ITS_FOLLOWUP_REPORT.md`
- P69: `its_followup/ITS_FOLLOWUP_REPORT.md`
- P70: `its_followup/ITS_FOLLOWUP_REPORT.md`
- P71: `its_followup/ITS_FOLLOWUP_REPORT.md`
- P72: `its_followup/ITS_FOLLOWUP_REPORT.md`
- P73: `its_followup/ITS_FOLLOWUP_REPORT.md`
- P74: `its_followup_arfken/ITS_FOLLOWUP_REPORT.md`
- P75: `its_followup/ITS_FOLLOWUP_REPORT.md`
- P76: `its_depth/ITS_DEPTH_REPORT.md`
- P77: `its_followup_arfken/ITS_ESTIMATES_REPORT.md`
- P78: `its_followup_arfken/ITS_ESTIMATES_REPORT.md`
- P79: `its_followup_arfken/ITS_ESTIMATES_REPORT.md`
- P80: `its_followup_arfken/ITS_TRUTH_REPORT.md`
- P81: `its_followup_arfken/ITS_TRUTH_REPORT.md`
- P82: `its_followup_arfken/ITS_TRUTH_REPORT.md`

Next: send this file.
