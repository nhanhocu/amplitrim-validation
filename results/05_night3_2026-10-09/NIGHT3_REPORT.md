# Night 3 report (2026-10-09 21:33)

Problems: 0

## Scorecard: each arm against FIGARO's pick (datasets where FIGARO gave a result; real and mock apart)

**mock communities (5 datasets)**

| arm | mockA_high | mcm_v12 | mockB | mcm_v46 | d6300_V3-V4 |
| --- | --- | --- | --- | --- | --- |
| A | trade-off: fewer pairs, cleaner | trade-off: more pairs, noisier | trade-off: fewer pairs, cleaner | trade-off: fewer pairs, cleaner | trade-off: more pairs, noisier |
| G | mixed noise (same pairs) | trade-off: more pairs, noisier | trade-off: fewer pairs, cleaner | mixed noise (fewer pairs) | trade-off: more pairs, noisier |
| F2 | trade-off: fewer pairs, cleaner | worse | trade-off: fewer pairs, cleaner | mixed noise (fewer pairs) | worse |
| R (uses) | mixed noise (same pairs) (G) | trade-off: more pairs, noisier (A) | trade-off: fewer pairs, cleaner (G) | mixed noise (fewer pairs) (G) | trade-off: more pairs, noisier (A) |

**real communities (5 datasets)**

| arm | v1v2 | v4 | wastewater_V3-V4 | spikein_V3-V4 | swabs_V3-V4 |
| --- | --- | --- | --- | --- | --- |
| A | mixed noise (more pairs) | trade-off: more pairs, noisier | trade-off: fewer pairs, cleaner | trade-off: more pairs, noisier | trade-off: more pairs, noisier |
| G | mixed noise (more pairs) | worse | mixed noise (fewer pairs) | trade-off: more pairs, noisier | trade-off: more pairs, noisier |
| F2 | worse | worse | trade-off: fewer pairs, cleaner | trade-off: more pairs, noisier | trade-off: more pairs, noisier |
| R (uses) | mixed noise (more pairs) (A) | trade-off: more pairs, noisier (A) | mixed noise (fewer pairs) (G) | trade-off: more pairs, noisier (A) | trade-off: more pairs, noisier (A) |

## Gain over the default: G and F2 minus A (merged pairs, points)

| dataset | A passes | G minus A | G noise | G accuracy | F2 minus A | F2 maxEE |
| --- | --- | --- | --- | --- | --- | --- |
| mockA_high | 64.7% | +13.4 | noisier | as accurate | -0.4 | 2 |
| v1v2 | 91.2% | +3.7 | mixed | no truth | -12.1 | 2 |
| its | 74.2% | +2.7 | unknown | no truth | - | - |
| v4 | 98.5% | -9.1 | mixed | no truth | -11.4 | 2 |
| mcm_v12 | 96.4% | +1.4 | noisier | no truth | -16.3 | 2 |
| mockB | 20.3% | +29.8 | noisier | more accurate | +25.4 | 2,5 |
| mcm_v46 | 43.1% | +18.8 | mixed | no truth | +17.6 | 2,5 |
| d6300_V3-V4 | 94.6% | +1.5 | noisier | as accurate | -9.3 | 2 |
| d6300_V4-V5 | 63.7% | +11.6 | noisier | as accurate | +0.0 | 2 |
| wastewater_V3-V4 | 53.7% | +7.5 | mixed | no truth | +7.1 | 2,5 |
| spikein_V3-V4 | 87.6% | +2.3 | noisier | no truth | -3.4 | 2 |
| swabs_V3-V4 | 85.0% | +2.0 | noisier | no truth | +0.0 | 2 |

## Datasets

### mockA_high  (mock, 16S, 6 samples; verdicts against FIGARO)

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy | vs A: merged difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 277/243 | 2 | 62.7% | 64.7% | 0.39 / 0.68 | -15.3 | cleaner | trade-off: fewer pairs, cleaner | as accurate | - |
| G | 260/260 | 2,5 | 76.1% | 79.0% | 0.37 / 1.43 | -1.8 | mixed | mixed noise (same pairs) | as accurate | +13.4 |
| F2 | 280/240 | 2 | 62.5% | 64.5% | 0.43 / 0.66 | -15.7 | cleaner | trade-off: fewer pairs, cleaner | less accurate | -0.4 |
| C FIGARO (longest amplicon) | 273/247 | 3,4 | 77.7% | 80.3% | 0.55 / 1.09 | - | - | - | - | - |

F2: median-Q30 cut 268/204, caps 280/280, amplicon needs 520; final cut 280/240; 64.4% pass at (2,2), so maxEE 2.

Accuracy (variants / strains / reads in exact ASVs): A: 36 / 12/14 / 99.7%; G: 37 / 12/14 / 99.8%; F2: 33 / 10/14 / 99.7%; C: 36 / 12/14 / 99.8%

### v1v2  (real, 16S, 33 samples; verdicts against FIGARO)

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy | vs A: merged difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 201/157 | 2 | 84.2% | 91.2% | 0.18 / 0.17 | +3.0 (+2.6 to +3.4) | mixed | mixed noise (more pairs) | no truth | - |
| G | 162/196 | 2,5 | 87.9% | 94.2% | 0.12 / 0.48 | +6.7 (+6.2 to +7.2) | mixed | mixed noise (more pairs) | no truth | +3.7 (+3.3 to +4.1) |
| F2 | 253/213 | 2 | 72.1% | 79.8% | 0.32 / 0.36 | -9.1 (-9.8 to -8.4) | noisier | worse | no truth | -12.1 (-12.7 to -11.4) |
| C FIGARO (longest amplicon) | 225/138 | 2,1 | 81.2% | 88.2% | 0.24 / 0.09 | - | - | - | - | - |

F2: median-Q30 cut 253/213, caps 279/280, amplicon needs 363; final cut 253/213; 79.8% pass at (2,2), so maxEE 2.

### its  (real, ITS, 37 samples; verdicts against A (FIGARO gave no result))

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs A: merged difference | noise | verdict | accuracy | vs A: merged difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 0/0 | 2 | 46.9% | 74.2% | - | - | - | - | - | - |
| G | 0/0 | 2,5 | 49.5% | 85.7% | - | +2.7 (+2.3 to +3.1) | unknown | no result | no truth | +2.7 (+2.3 to +3.1) |

### v4  (real, 16S, 36 samples; verdicts against FIGARO)

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy | vs A: merged difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 124/115 | 2 | 66.8% | 98.5% | 0.09 / 0.09 | +3.5 (+3.1 to +3.9) | noisier | trade-off: more pairs, noisier | no truth | - |
| G | 85/154 | 2,5 | 57.7% | 99.4% | 0.06 / 0.25 | -5.5 (-7.1 to -3.9) | noisier | worse | no truth | -9.1 (-10.9 to -7.1) |
| F2 | 207/185 | 2 | 55.5% | 89.1% | 0.20 / 0.35 | -7.9 (-9.5 to -6.5) | noisier | worse | no truth | -11.4 (-12.8 to -10.1) |
| C FIGARO (longest amplicon) | 120/119 | 1 | 63.3% | 96.5% | 0.07 / 0.08 | - | - | - | - | - |

F2: median-Q30 cut 212/185, caps 207/207, amplicon needs 239; final cut 207/185; 90.5% pass at (2,2), so maxEE 2.

### mcm_v12  (mock, 16S, 6 samples; verdicts against FIGARO)

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy | vs A: merged difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 155/170 | 2 | 95.9% | 96.4% | 0.08 / 0.09 | +2.3 | noisier | trade-off: more pairs, noisier | no truth | - |
| G | 121/204 | 2,5 | 97.3% | 97.7% | 0.06 / 0.19 | +3.7 | noisier | trade-off: more pairs, noisier | no truth | +1.4 |
| F2 | 251/247 | 2 | 79.6% | 80.2% | 0.39 / 0.31 | -14.0 | noisier | worse | no truth | -16.3 |
| C FIGARO (longest amplicon) | 156/169 | 1 | 93.6% | 94.1% | 0.06 / 0.06 | - | - | - | - | - |

F2: median-Q30 cut 251/247, caps 279/279, amplicon needs 325; final cut 251/247; 80.4% pass at (2,2), so maxEE 2.

Accuracy (variants / strains / reads in exact ASVs): A:  /  / -; G:  /  / -; F2:  /  / -; C:  /  / -

### mockB  (mock, 16S, 8 samples; verdicts against FIGARO)

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy | vs A: merged difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 279/248 | 2 | 19.9% | 20.3% | 0.41 / 1.24 | -54.1 | cleaner | trade-off: fewer pairs, cleaner | less accurate | - |
| G | 277/250 | 2,5 | 49.7% | 50.9% | 0.56 / 2.53 | -24.2 | cleaner | trade-off: fewer pairs, cleaner | less accurate | +29.8 |
| F2 | 280/247 | 2,5 | 45.7% | 49.4% | 0.63 / 2.43 | -28.6 | cleaner | trade-off: fewer pairs, cleaner | more accurate | +25.4 |
| C FIGARO (longest amplicon) | 279/248 | 6,9 | 74.3% | 75.9% | 1.30 / 3.63 | - | - | - | - | - |

F2: median-Q30 cut 245/165, caps 280/283, amplicon needs 527; final cut 280/247; 20.1% pass at (2,2), so maxEE 2,5.

Accuracy (variants / strains / reads in exact ASVs): A: 6 / 3/3 / 68.7%; G: 6 / 3/3 / 74.7%; F2: 7 / 3/3 / 82.3%; C: 7 / 3/3 / 78.3%

### mcm_v46  (mock, 16S, 5 samples; verdicts against FIGARO)

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy | vs A: merged difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 273/265 | 2 | 41.6% | 43.1% | 0.63 / 0.63 | -27.0 | cleaner | trade-off: fewer pairs, cleaner | no truth | - |
| G | 259/279 | 2,5 | 60.4% | 62.5% | 0.52 / 1.48 | -8.2 | mixed | mixed noise (fewer pairs) | no truth | +18.8 |
| F2 | 266/272 | 2,5 | 59.2% | 61.3% | 0.55 / 1.42 | -9.4 | mixed | mixed noise (fewer pairs) | no truth | +17.6 |
| C FIGARO (longest amplicon) | 270/268 | 4 | 68.6% | 70.4% | 1.00 / 1.06 | - | - | - | - | - |

F2: median-Q30 cut 230/236, caps 278/281, amplicon needs 538; final cut 266/272; 42.1% pass at (2,2), so maxEE 2,5.

Accuracy (variants / strains / reads in exact ASVs): A:  /  / -; G:  /  / -; F2:  /  / -; C:  /  / -

### d6300_V3-V4  (mock, 16S, 10 samples; verdicts against FIGARO)

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy | vs A: merged difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 224/218 | 2 | 90.6% | 94.6% | 0.29 / 0.26 | +6.1 (+5.7 to +6.5) | noisier | trade-off: more pairs, noisier | as accurate | - |
| G | 224/218 | 2,5 | 92.1% | 96.2% | 0.31 / 0.31 | +7.6 (+7.2 to +8.0) | noisier | trade-off: more pairs, noisier | as accurate | +1.5 (+1.3 to +1.8) |
| F2 | 226/218 | 2 | 81.3% | 85.0% | 0.29 / 0.26 | -3.2 (-20.9 to +5.7) | noisier | worse | as accurate | -9.3 (-27.3 to -0.2) |
| C FIGARO (longest amplicon) | 224/218 | 1 | 84.5% | 88.2% | 0.24 / 0.20 | - | - | - | - | - |

F2: median-Q30 cut 231/228, caps 226/218, amplicon needs 442; final cut 226/218; 85.5% pass at (2,2), so maxEE 2.

Accuracy (variants / strains / reads in exact ASVs): A: 10 / 8/8 / 97.9%; G: 10 / 8/8 / 97.9%; F2: 10 / 8/8 / 97.9%; C: 10 / 8/8 / 97.9%

### d6300_V4-V5  (mock, 16S, 3 samples; verdicts against A (FIGARO gave no result))

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs A: merged difference | noise | verdict | accuracy | vs A: merged difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 282/280 | 2 | 57.2% | 63.7% | 0.09 / 0.57 | - | - | - | - | - |
| G | 282/280 | 2,5 | 68.8% | 76.5% | 0.13 / 1.00 | +11.6 | noisier | trade-off: more pairs, noisier | as accurate | +11.6 |
| F2 | 282/280 | 2 | 57.2% | 63.7% | 0.09 / 0.57 | +0.0 | about the same | matches | as accurate | +0.0 |

F2: median-Q30 cut 286/239, caps 282/280, amplicon needs 562; final cut 282/280; 63.9% pass at (2,2), so maxEE 2.

FIGARO gave no result at: FIGARO (amplicon 550) (not a difference in outcome).

Accuracy (variants / strains / reads in exact ASVs): A: 9 / 8/9 / 98.8%; G: 9 / 8/9 / 98.8%; F2: 9 / 8/9 / 98.8%

### wastewater_V3-V4  (real, 16S, 9 samples; verdicts against FIGARO)

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy | vs A: merged difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 254/186 | 2 | 43.6% | 53.7% | 0.84 / 0.75 | -23.1 | cleaner | trade-off: fewer pairs, cleaner | no truth | - |
| G | 236/206 | 2,5 | 51.1% | 67.8% | 0.69 / 1.98 | -15.7 | mixed | mixed noise (fewer pairs) | no truth | +7.5 |
| F2 | 242/198 | 2,5 | 50.7% | 64.1% | 0.79 / 1.34 | -16.0 | cleaner | trade-off: fewer pairs, cleaner | no truth | +7.1 |
| C FIGARO (longest amplicon) | 247/193 | 5 | 66.7% | 83.1% | 1.38 / 1.48 | - | - | - | - | - |

F2: median-Q30 cut 186/143, caps 282/279, amplicon needs 440; final cut 242/198; 53.2% pass at (2,2), so maxEE 2,5.

### spikein_V3-V4  (real, 16S, 12 samples; verdicts against FIGARO)

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy | vs A: merged difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 222/218 | 2 | 83.6% | 87.6% | 0.41 / 0.36 | +6.3 (+5.3 to +7.4) | noisier | trade-off: more pairs, noisier | no truth | - |
| G | 221/219 | 2,5 | 85.9% | 90.1% | 0.43 / 0.43 | +8.6 (+7.6 to +9.8) | noisier | trade-off: more pairs, noisier | no truth | +2.3 (+2.1 to +2.7) |
| F2 | 232/228 | 2 | 80.1% | 84.8% | 0.43 / 0.40 | +2.9 (+2.3 to +3.5) | noisier | trade-off: more pairs, noisier | no truth | -3.4 (-4.8 to -2.2) |
| C FIGARO (longest amplicon) | 232/207 | 2,1 | 77.3% | 81.6% | 0.40 / 0.26 | - | - | - | - | - |

F2: median-Q30 cut 237/229, caps 232/228, amplicon needs 439; final cut 232/228; 86.9% pass at (2,2), so maxEE 2.

### swabs_V3-V4  (real, 16S, 36 samples; verdicts against FIGARO)

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy | vs A: merged difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 224/218 | 2 | 77.0% | 85.0% | 0.27 / 0.27 | +5.9 (+5.1 to +6.9) | noisier | trade-off: more pairs, noisier | no truth | - |
| G | 224/218 | 2,5 | 79.0% | 87.1% | 0.29 / 0.34 | +7.9 (+6.7 to +9.2) | noisier | trade-off: more pairs, noisier | no truth | +2.0 (+1.7 to +2.4) |
| F2 | 224/218 | 2 | 77.0% | 85.0% | 0.27 / 0.27 | +5.9 (+5.1 to +6.9) | noisier | trade-off: more pairs, noisier | no truth | +0.0 (+0.0 to +0.0) |
| C FIGARO (longest amplicon) | 224/218 | 1 | 71.1% | 78.6% | 0.22 / 0.20 | - | - | - | - | - |

F2: median-Q30 cut 231/228, caps 224/218, amplicon needs 442; final cut 224/218; 85.5% pass at (2,2), so maxEE 2.

Next: send this file, NIGHT3_PROTOCOL.md and night3.log.
