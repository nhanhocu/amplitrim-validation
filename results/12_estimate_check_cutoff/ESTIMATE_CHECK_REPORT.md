# Estimate check

The criteria (P36 to P38) are in TEST_REGISTER.md, section 23, and were fixed before this ran.

## Verdicts

- **P36** NOT MET: The strict estimate is closer to DADA2's merged share than the tolerant one, as the mean over the datasets of the mean absolute difference: 12.5 against 6.5 points (5 of 12 datasets closer)
- **P37** NOT MET: The strict estimate ranks the settings at least as well as the tolerant one (within 0.05), mean rank correlation over the 10 datasets with at least 4 settings: +0.76 against +0.92
- **P38** NOT MET: An intermediate cut-off is closer to DADA2's merge step than both 0 and 10 differences, by at least 2 points: the closest is 10 (6.6 points away on average) against 27.6 at 0 and 6.6 at 10

## A. The two estimates against DADA2 (98 settings on 12 datasets; points of the input pairs)

| dataset | settings | tolerant minus DADA2 | strict minus DADA2 | closer | rank correlation, tolerant | rank correlation, strict |
|---|---|---|---|---|---|---|
| d6300_V3-V4 | 4 | +3.1 | +0.1 | strict | +1.00 | +1.00 |
| d6300_V4-V5 | 9 | +6.4 | -6.1 | tolerant | +1.00 | +1.00 |
| its | 1 | +13.7 | +2.4 | strict | - | - |
| mcm_v12 | 7 | +0.3 | -4.3 | tolerant | +1.00 | +0.86 |
| mcm_v46 | 8 | -2.0 | -17.6 | tolerant | +0.98 | +0.74 |
| mockA_high | 8 | +0.8 | -23.1 | tolerant | +1.00 | +0.74 |
| mockB | 12 | -2.2 | -37.8 | tolerant | +0.99 | +0.41 |
| spikein_V3-V4 | 5 | +3.3 | -4.7 | tolerant | +1.00 | +0.70 |
| swabs_V3-V4 | 3 | +7.1 | +1.7 | strict | - | - |
| v1v2 | 8 | +6.1 | -5.5 | strict | +1.00 | +0.93 |
| v4 | 8 | +26.5 | +17.7 | strict | +0.26 | +0.83 |
| wastewater_V3-V4 | 11 | +3.9 | -26.9 | tolerant | +0.94 | +0.43 |

## B. The number of differences vsearch may allow, against DADA2's merging

| setting | 0 | 1 | 2 | 3 | 4 | 5 | 7 | 10 | DADA2 merge step | denoising loss (at least) |
|---|---|---|---|---|---|---|---|---|---|---|
| d6300_V3-V4: AmpliTrim (FIGARO's maxEE 1) | 97.1% | 99.3% | 99.3% | 99.3% | 99.3% | 99.3% | 99.3% | 99.3% | 96.6% | 0.9% |
| d6300_V3-V4: AmpliTrim (maxEE 2) | 95.7% | 98.9% | 98.9% | 98.9% | 98.9% | 98.9% | 98.9% | 98.9% | 96.7% | 1.0% |
| d6300_V3-V4: AmpliTrim (maxEE 2,5) | 95.0% | 98.5% | 98.5% | 98.5% | 98.5% | 98.5% | 98.5% | 98.5% | 96.6% | 1.0% |
| d6300_V4-V5: AmpliTrim (FIGARO's maxEE 1) | 91.6% | 99.1% | 99.8% | 99.9% | 99.9% | 100.0% | 100.0% | 100.0% | 91.6% | 2.6% |
| d6300_V4-V5: AmpliTrim (maxEE 1,3) | 78.0% | 92.5% | 97.3% | 99.0% | 99.6% | 99.8% | 99.9% | 99.9% | 92.2% | 2.2% |
| d6300_V4-V5: AmpliTrim (maxEE 2) | 82.7% | 95.8% | 98.8% | 99.6% | 99.8% | 99.9% | 99.9% | 99.9% | 92.3% | 2.7% |
| d6300_V4-V5: AmpliTrim (maxEE 2, leave out 5.0%) | 96.3% | 97.7% | 97.7% | 97.7% | 97.7% | 97.7% | 97.7% | 97.7% | 98.5% | 1.8% |
| d6300_V4-V5: AmpliTrim (maxEE 2,3) | 77.1% | 91.8% | 96.7% | 98.7% | 99.4% | 99.7% | 99.8% | 99.9% | 92.3% | 2.2% |
| d6300_V4-V5: AmpliTrim (maxEE 2,4) | 73.5% | 88.4% | 94.3% | 97.2% | 98.6% | 99.3% | 99.7% | 99.9% | 91.7% | 2.1% |
| d6300_V4-V5: AmpliTrim (maxEE 2,5) | 71.3% | 86.0% | 92.2% | 95.5% | 97.4% | 98.5% | 99.4% | 99.8% | 91.7% | 2.1% |
| d6300_V4-V5: AmpliTrim (maxEE 5) | 70.5% | 85.0% | 91.2% | 94.7% | 96.7% | 97.9% | 99.0% | 99.6% | 91.7% | 2.1% |
| its: AmpliTrim (maxEE 2) | 59.2% | 74.9% | 82.8% | 88.1% | 91.7% | 94.1% | 96.5% | 97.5% | 77.7% | 18.8% |
| its: AmpliTrim (maxEE 2,5) | 51.2% | 65.0% | 72.4% | 77.7% | 81.7% | 84.9% | 89.3% | 92.8% | 72.9% | 20.6% |
| its: AmpliTrim (maxEE 3) | 51.9% | 66.0% | 73.7% | 79.4% | 83.8% | 87.2% | 91.8% | 95.1% | 74.1% | 19.4% |
| mcm_v12: AmpliTrim (FIGARO's maxEE 1) | 97.4% | 99.7% | 99.9% | 99.9% | 99.9% | 99.9% | 99.9% | 99.9% | 99.6% | 0.2% |
| mcm_v12: AmpliTrim (maxEE 2) | 96.1% | 99.1% | 99.6% | 99.8% | 99.8% | 99.8% | 99.8% | 99.8% | 99.6% | 0.1% |
| mcm_v12: AmpliTrim (maxEE 2, leave out 5.0%) | 95.2% | 97.1% | 97.3% | 97.4% | 97.4% | 97.4% | 97.4% | 97.4% | 97.3% | 0.1% |
| mcm_v12: AmpliTrim (maxEE 2,5) | 94.5% | 98.2% | 99.0% | 99.4% | 99.6% | 99.7% | 99.7% | 99.7% | 99.8% | 0.1% |
| mcm_v46: AmpliTrim (maxEE 2) | 79.2% | 95.9% | 97.5% | 97.5% | 97.5% | 97.5% | 97.5% | 97.5% | 99.5% | 3.0% |
| mcm_v46: AmpliTrim (maxEE 2,5) | 65.2% | 86.8% | 91.4% | 91.4% | 91.4% | 91.4% | 91.4% | 91.4% | 99.5% | 2.8% |
| mcm_v46: AmpliTrim (maxEE 3) | 71.0% | 91.8% | 95.2% | 95.2% | 95.2% | 95.2% | 95.2% | 95.2% | 99.5% | 2.2% |
| mcm_v46: AmpliTrim (maxEE 4) | 65.1% | 87.7% | 92.4% | 92.4% | 92.4% | 92.4% | 92.4% | 92.4% | 99.5% | 2.0% |
| mcm_v46: AmpliTrim (maxEE 5) | 54.2% | 79.8% | 91.4% | 95.1% | 95.2% | 95.3% | 95.3% | 95.3% | 99.5% | 2.3% |
| mockA_high: AmpliTrim (FIGARO's maxEE 3,4) | 60.9% | 83.4% | 92.6% | 96.8% | 98.6% | 99.3% | 99.7% | 99.8% | 97.3% | 0.5% |
| mockA_high: AmpliTrim (maxEE 2) | 69.0% | 91.0% | 97.5% | 99.4% | 99.8% | 99.9% | 99.9% | 99.9% | 97.5% | 0.6% |
| mockA_high: AmpliTrim (maxEE 2,3) | 66.4% | 88.4% | 96.0% | 98.6% | 99.5% | 99.7% | 99.9% | 99.9% | 97.3% | 0.5% |
| mockA_high: AmpliTrim (maxEE 2,5) | 59.1% | 82.0% | 91.6% | 96.1% | 98.1% | 99.0% | 99.6% | 99.7% | 96.8% | 0.5% |
| mockA_high: AmpliTrim (maxEE 3) | 63.7% | 86.2% | 94.7% | 97.9% | 99.2% | 99.6% | 99.8% | 99.8% | 97.3% | 0.5% |
| mockA_high: AmpliTrim (maxEE 3,5) | 56.7% | 79.6% | 90.0% | 94.9% | 97.4% | 98.6% | 99.4% | 99.6% | 97.2% | 0.5% |
| mockB: AmpliTrim (FIGARO's maxEE 6,9) | 15.5% | 31.2% | 43.9% | 54.3% | 62.8% | 69.9% | 80.2% | 89.4% | 98.6% | 1.2% |
| mockB: AmpliTrim (maxEE 2) | 49.6% | 82.5% | 95.0% | 98.5% | 99.4% | 99.6% | 99.6% | 99.6% | 98.8% | 1.1% |
| mockB: AmpliTrim (maxEE 2,5) | 24.4% | 48.3% | 66.1% | 78.5% | 87.0% | 92.5% | 97.3% | 98.8% | 98.8% | 1.1% |
| mockB: AmpliTrim (maxEE 3,5) | 23.1% | 46.0% | 63.4% | 76.1% | 84.9% | 91.0% | 96.6% | 98.6% | 98.7% | 1.1% |
| mockB: AmpliTrim (maxEE 4,5) | 22.5% | 45.0% | 62.2% | 74.9% | 83.9% | 90.3% | 96.2% | 98.5% | 98.6% | 1.2% |
| mockB: AmpliTrim (maxEE 4,6) | 20.0% | 40.1% | 55.8% | 67.8% | 77.1% | 84.2% | 92.5% | 97.1% | 98.6% | 1.1% |
| mockB: AmpliTrim (maxEE 5) | 22.2% | 44.4% | 61.4% | 74.1% | 83.2% | 89.6% | 95.8% | 98.3% | 98.6% | 1.1% |
| mockB: AmpliTrim (maxEE 5,9) | 15.7% | 31.7% | 44.6% | 55.1% | 63.7% | 70.8% | 81.1% | 90.1% | 98.6% | 1.2% |
| spikein_V3-V4: AmpliTrim (FIGARO's maxEE 2,1) | 94.6% | 99.5% | 99.8% | 99.8% | 99.8% | 99.8% | 99.8% | 99.8% | 97.5% | 2.6% |
| spikein_V3-V4: AmpliTrim (maxEE 2) | 92.0% | 98.9% | 99.4% | 99.4% | 99.4% | 99.4% | 99.4% | 99.4% | 98.1% | 2.7% |
| spikein_V3-V4: AmpliTrim (maxEE 2,5) | 90.7% | 98.1% | 98.7% | 98.9% | 98.9% | 99.0% | 99.0% | 99.0% | 98.0% | 2.7% |
| swabs_V3-V4: AmpliTrim (FIGARO's maxEE 1) | 94.7% | 99.2% | 99.5% | 99.5% | 99.5% | 99.5% | 99.5% | 99.5% | 93.6% | 3.4% |
| swabs_V3-V4: AmpliTrim (maxEE 2,5) | 91.5% | 97.8% | 98.5% | 98.8% | 98.8% | 98.9% | 98.9% | 98.9% | 93.8% | 3.3% |
| v1v2: AmpliTrim (FIGARO's maxEE 2,1) | 88.1% | 96.9% | 98.9% | 99.4% | 99.6% | 99.7% | 99.7% | 99.7% | 95.4% | 2.9% |
| v1v2: AmpliTrim (maxEE 1) | 89.9% | 98.3% | 99.4% | 99.7% | 99.7% | 99.7% | 99.7% | 99.7% | 94.6% | 2.7% |
| v1v2: AmpliTrim (maxEE 2) | 86.0% | 95.7% | 98.2% | 99.1% | 99.4% | 99.5% | 99.6% | 99.6% | 94.7% | 2.6% |
| v1v2: AmpliTrim (maxEE 2, leave out 5.0%) | 86.1% | 95.3% | 97.6% | 98.4% | 98.7% | 98.8% | 98.9% | 98.9% | 94.4% | 2.6% |
| v1v2: AmpliTrim (maxEE 2,5) | 83.1% | 92.9% | 96.1% | 97.7% | 98.4% | 98.9% | 99.3% | 99.4% | 95.3% | 2.1% |
| v4: AmpliTrim (FIGARO's maxEE 1) | 92.9% | 98.9% | 99.7% | 99.8% | 99.8% | 99.8% | 99.8% | 99.8% | 76.0% | 13.7% |
| v4: AmpliTrim (maxEE 2) | 91.8% | 98.2% | 99.3% | 99.6% | 99.7% | 99.7% | 99.8% | 99.8% | 78.2% | 13.3% |
| v4: AmpliTrim (maxEE 2, leave out 1.0%) | 91.7% | 97.8% | 98.9% | 99.1% | 99.2% | 99.3% | 99.3% | 99.3% | 78.7% | 13.3% |
| v4: AmpliTrim (maxEE 2, leave out 5.0%) | 95.0% | 97.1% | 97.1% | 97.1% | 97.1% | 97.1% | 97.1% | 97.1% | 85.0% | 13.9% |
| v4: AmpliTrim (maxEE 2,5) | 86.4% | 96.0% | 98.1% | 98.9% | 99.2% | 99.4% | 99.5% | 99.5% | 65.3% | 11.1% |
| wastewater_V3-V4: AmpliTrim (FIGARO's maxEE 4) | 26.9% | 51.9% | 69.4% | 80.2% | 84.5% | 87.5% | 90.9% | 92.3% | 83.5% | 4.2% |
| wastewater_V3-V4: AmpliTrim (FIGARO's maxEE 5) | 25.1% | 48.6% | 65.5% | 76.3% | 80.5% | 83.7% | 87.7% | 89.8% | 83.5% | 4.2% |
| wastewater_V3-V4: AmpliTrim (maxEE 2) | 49.3% | 78.4% | 86.3% | 89.9% | 91.5% | 92.1% | 92.4% | 92.4% | 84.5% | 3.9% |
| wastewater_V3-V4: AmpliTrim (maxEE 2, leave out 5.0%) | 42.0% | 72.9% | 87.4% | 92.0% | 94.1% | 94.9% | 95.3% | 95.4% | 83.4% | 4.3% |
| wastewater_V3-V4: AmpliTrim (maxEE 2,5) | 24.8% | 50.0% | 64.8% | 71.4% | 76.0% | 78.9% | 82.3% | 83.3% | 78.6% | 4.1% |
| wastewater_V3-V4: AmpliTrim (maxEE 3) | 35.0% | 62.9% | 75.7% | 81.6% | 85.3% | 87.6% | 89.4% | 89.7% | 83.6% | 4.1% |
| wastewater_V3-V4: AmpliTrim (maxEE 4,3) | 33.6% | 61.2% | 77.9% | 83.6% | 87.3% | 89.4% | 91.4% | 91.9% | 84.1% | 5.0% |

| allowed differences | 0 | 1 | 2 | 3 | 4 | 5 | 7 | 10 |
|---|---|---|---|---|---|---|---|---|
| vsearch minus DADA2, mean (points) | -25.0 | -10.2 | -3.8 | -0.5 | +1.5 | +2.9 | +4.3 | +5.1 |
| vsearch minus DADA2, mean absolute (points) | 27.6 | 15.0 | 10.1 | 8.4 | 7.6 | 7.2 | 6.9 | 6.6 |

Next: send this file.
