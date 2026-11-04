# Night 4b report (2026-10-10 10:21)

Problems: 0

## Predictions

- **P19** NOT MET: H minus G, merged points: mockA_high -6.7, mockB +5.3, mcm_v46 -2.6, d6300_V4-V5 -5.4, wastewater_V3-V4 +6.8
- **P20** NOT MET: H against G, accuracy: mockA_high as accurate, mockB less accurate, d6300_V4-V5 as accurate
- **P21** MET: H minus G, merged points: mockB +5.3, wastewater_V3-V4 +6.8
- **P22** MET: H80 minus H (the cost of the cap), merged points: mockB +20.2

## The rule's maxEE and the gain over rule R's setting (merged pairs, points)

| dataset | rule's maxEE (H / H80) | H minus G | H minus A | H accuracy vs G | merged ok | accuracy ok |
| --- | --- | --- | --- | --- | --- | --- |
| mockA_high | 2,3 / 3 | -6.7 | +6.7 | as accurate | NO | yes |
| mockB | 4,5 / 5,9 | +5.3 | +35.2 | less accurate | yes | NO |
| mcm_v46 | 3 / 4 | -2.6 | +16.2 | no truth | NO | - |
| d6300_V4-V5 | 2,3 / 2,4 | -5.4 | +6.1 | as accurate | NO | yes |
| wastewater_V3-V4 | 4,3 / 4,3 | +6.8 | +14.3 | no truth | yes | - |

## Not run

- v1v2: the rule gives (2,2) at AmpliTrim's cut 195/168 for both rules: identical to A by construction, nothing to run
- its: ITS: nothing is truncated, so there is no cut to compute the rule at; not part of this test
- v4: the rule gives (2,2) at AmpliTrim's cut 124/115 for both rules: identical to A by construction, nothing to run
- mcm_v12: the rule gives (2,2) at AmpliTrim's cut 160/165 for both rules: identical to A by construction, nothing to run
- d6300_V3-V4: the rule gives (2,2) at AmpliTrim's cut 224/218 for both rules: identical to A by construction, nothing to run
- spikein_V3-V4: the rule gives (2,2) at AmpliTrim's cut 229/210 for both rules: identical to A by construction, nothing to run
- swabs_V3-V4: the rule gives (2,2) at AmpliTrim's cut 224/218 for both rules: identical to A by construction, nothing to run

## Datasets

### mockA_high  (mock, 16S, 6 samples; verdicts against FIGARO)

The rule at AmpliTrim's cut 277/243: mean expected errors 1.39 / 1.85; 75th percentile 1.63 / 2.40; 80th percentile 2.14 / 2.92; maxEE 2,3 for H (q = 0.75, cap 5) and 3 for H80 (q = 0.8, no cap).

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | verdict | vs G: merged difference | accuracy vs G |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 277/243 | 2 | 62.7% | 64.7% | 0.39 / 0.68 | -15.3 | trade-off: fewer pairs, cleaner | - | - |
| G | 260/260 | 2,5 | 76.1% | 79.0% | 0.37 / 1.43 | -1.8 | mixed noise (same pairs) | - | - |
| H | 273/247 | 2,3 | 69.5% | 71.8% | 0.40 / 0.91 | -8.6 | trade-off: fewer pairs, cleaner | -6.7 | as accurate |
| H80 | 275/245 | 3 | 73.3% | 75.7% | 0.53 / 0.92 | -4.2 | trade-off: fewer pairs, cleaner | -2.4 | as accurate |
| C FIGARO (longest amplicon) | 273/247 | 3,4 | 77.7% | 80.3% | 0.55 / 1.09 | - | - | - | - |

Adoption check for H: merged pairs at least G's within the margin: **NO**; accuracy not below G's: yes.

What the cap costs (H80 minus H, merged pairs): +4.3 points.

Accuracy (variants / strains / reads in exact ASVs): A: 36 / 12/14 / 99.7%; G: 37 / 12/14 / 99.8%; H: 36 / 12/14 / 99.8%; H80: 36 / 12/14 / 99.8%; C: 36 / 12/14 / 99.8%

### mockB  (mock, 16S, 8 samples; verdicts against FIGARO)

The rule at AmpliTrim's cut 280/247: mean expected errors 2.73 / 5.10; 75th percentile 3.65 / 7.12; 80th percentile 4.55 / 8.19; maxEE 4,5 for H (q = 0.75, cap 5) and 5,9 for H80 (q = 0.8, no cap).

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | verdict | vs G: merged difference | accuracy vs G |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 279/248 | 2 | 19.9% | 20.3% | 0.41 / 1.24 | -54.1 | trade-off: fewer pairs, cleaner | - | - |
| G | 277/250 | 2,5 | 49.7% | 50.9% | 0.56 / 2.53 | -24.2 | trade-off: fewer pairs, cleaner | - | - |
| H | 277/250 | 4,5 | 55.0% | 56.4% | 0.76 / 2.61 | -18.9 | trade-off: fewer pairs, cleaner | +5.3 | less accurate |
| H80 | 274/253 | 5,9 | 75.3% | 77.3% | 1.06 / 3.82 | +1.2 | mixed noise (same pairs) | +25.5 | more accurate |
| C FIGARO (longest amplicon) | 279/248 | 6,9 | 74.3% | 75.9% | 1.30 / 3.63 | - | - | - | - |

Adoption check for H: merged pairs at least G's within the margin: yes; accuracy not below G's: **NO**.

What the cap costs (H80 minus H, merged pairs): +20.2 points.

Accuracy (variants / strains / reads in exact ASVs): A: 6 / 3/3 / 68.7%; G: 6 / 3/3 / 74.7%; H: 6 / 3/3 / 73.8%; H80: 6 / 3/3 / 75.5%; C: 7 / 3/3 / 78.3%

### mcm_v46  (mock, 16S, 5 samples; verdicts against FIGARO)

The rule at AmpliTrim's cut 273/265: mean expected errors 2.24 / 2.00; 75th percentile 3.00 / 2.63; 80th percentile 3.71 / 3.25; maxEE 3 for H (q = 0.75, cap 5) and 4 for H80 (q = 0.8, no cap).

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | verdict | vs G: merged difference | accuracy vs G |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 273/265 | 2 | 41.6% | 43.1% | 0.63 / 0.63 | -27.0 | trade-off: fewer pairs, cleaner | - | - |
| G | 259/279 | 2,5 | 60.4% | 62.5% | 0.52 / 1.48 | -8.2 | mixed noise (fewer pairs) | - | - |
| H | 271/267 | 3 | 57.9% | 59.5% | 0.83 / 0.86 | -10.7 | trade-off: fewer pairs, cleaner | -2.6 | no truth |
| H80 | 271/267 | 4 | 68.8% | 70.5% | 1.01 / 1.04 | +0.3 | matches | +8.4 | no truth |
| C FIGARO (longest amplicon) | 270/268 | 4 | 68.6% | 70.4% | 1.00 / 1.06 | - | - | - | - |

Adoption check for H: merged pairs at least G's within the margin: **NO**; accuracy not below G's: no truth.

What the cap costs (H80 minus H, merged pairs): +11.0 points.

Accuracy (variants / strains / reads in exact ASVs): A:  /  / -; G:  /  / -; H:  /  / -; H80:  /  / -; C:  /  / -

### d6300_V4-V5  (mock, 16S, 3 samples; verdicts against A (FIGARO gave no result))

The rule at AmpliTrim's cut 282/280: mean expected errors 0.41 / 2.24; 75th percentile 0.19 / 2.43; 80th percentile 0.31 / 3.25; maxEE 2,3 for H (q = 0.75, cap 5) and 2,4 for H80 (q = 0.8, no cap).

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs A: merged difference | verdict | vs G: merged difference | accuracy vs G |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 282/280 | 2 | 57.2% | 63.7% | 0.09 / 0.57 | - | - | - | - |
| G | 282/280 | 2,5 | 68.8% | 76.5% | 0.13 / 1.00 | +11.6 | trade-off: more pairs, noisier | - | - |
| H | 282/280 | 2,3 | 63.3% | 70.1% | 0.10 / 0.74 | +6.1 | trade-off: more pairs, noisier | -5.4 | as accurate |
| H80 | 282/280 | 2,4 | 66.4% | 74.0% | 0.12 / 0.89 | +9.3 | trade-off: more pairs, noisier | -2.3 | as accurate |

Adoption check for H: merged pairs at least G's within the margin: **NO**; accuracy not below G's: yes.

What the cap costs (H80 minus H, merged pairs): +3.1 points.

FIGARO gave no result at: FIGARO (amplicon 550) (not a difference in outcome).

Accuracy (variants / strains / reads in exact ASVs): A: 9 / 8/9 / 98.8%; G: 9 / 8/9 / 98.8%; H: 9 / 8/9 / 98.8%; H80: 9 / 8/9 / 98.8%

### wastewater_V3-V4  (real, 16S, 9 samples; verdicts against FIGARO)

The rule at AmpliTrim's cut 254/186: mean expected errors 2.50 / 1.77; 75th percentile 3.30 / 2.09; 80th percentile 3.92 / 2.52; maxEE 4,3 for H (q = 0.75, cap 5) and 4,3 for H80 (q = 0.8, no cap).

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | verdict | vs G: merged difference | accuracy vs G |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 254/186 | 2 | 43.6% | 53.7% | 0.84 / 0.75 | -23.1 | trade-off: fewer pairs, cleaner | - | - |
| G | 236/206 | 2,5 | 51.1% | 67.8% | 0.69 / 1.98 | -15.7 | mixed noise (fewer pairs) | - | - |
| H | 261/183 | 4,3 | 57.9% | 72.5% | 1.49 / 0.84 | -8.8 | mixed noise (fewer pairs) | +6.8 | no truth |
| H80 | 261/183 | 4,3 | 57.9% | 72.5% | 1.49 / 0.84 | -8.8 | mixed noise (fewer pairs) | +6.8 | no truth |
| C FIGARO (longest amplicon) | 247/193 | 5 | 66.7% | 83.1% | 1.38 / 1.48 | - | - | - | - |

Adoption check for H: merged pairs at least G's within the margin: yes; accuracy not below G's: no truth.

What the cap costs (H80 minus H, merged pairs): +0.0 points.

Next: send this file, NIGHT4_PROTOCOL.md and night4.log.
