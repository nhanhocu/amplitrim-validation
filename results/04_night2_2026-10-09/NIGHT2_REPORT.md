# Night 2 report (2026-10-09 15:50)

Problems: 0

## Scorecard: each AmpliTrim arm against FIGARO's pick (datasets where FIGARO gave a result; real and mock apart)

**mock communities (5 datasets)**

| arm | mockA_high | mcm_v12 | mockB | mcm_v46 | d6300_V3-V4 |
| --- | --- | --- | --- | --- | --- |
| A | trade-off: fewer pairs, cleaner | trade-off: more pairs, noisier | trade-off: fewer pairs, cleaner | trade-off: fewer pairs, cleaner | trade-off: more pairs, noisier |
| B | trade-off: fewer pairs, cleaner | trade-off: more pairs, noisier | trade-off: fewer pairs, cleaner | trade-off: fewer pairs, cleaner | trade-off: more pairs, noisier |
| B2 | trade-off: more pairs, noisier | trade-off: more pairs, noisier | trade-off: fewer pairs, cleaner | trade-off: more pairs, noisier | trade-off: more pairs, noisier |
| B4 | trade-off: fewer pairs, cleaner | matches | trade-off: fewer pairs, cleaner | trade-off: fewer pairs, cleaner | matches |
| D | matches | matches | mixed noise (more pairs) | matches | matches |
| E | no result | no result | no result | no result | no result |
| F | trade-off: fewer pairs, cleaner | worse | trade-off: fewer pairs, cleaner | trade-off: fewer pairs, cleaner | - |

**real communities (5 datasets)**

| arm | v1v2 | v4 | wastewater_V3-V4 | spikein_V3-V4 | swabs_V3-V4 |
| --- | --- | --- | --- | --- | --- |
| A | mixed noise (more pairs) | trade-off: more pairs, noisier | trade-off: fewer pairs, cleaner | trade-off: more pairs, noisier | trade-off: more pairs, noisier |
| B | mixed noise (more pairs) | trade-off: more pairs, noisier | trade-off: fewer pairs, cleaner | trade-off: more pairs, noisier | trade-off: more pairs, noisier |
| B2 | mixed noise (more pairs) | trade-off: more pairs, noisier | worse | trade-off: more pairs, noisier | trade-off: more pairs, noisier |
| B4 | mixed noise (fewer pairs) | matches | trade-off: fewer pairs, cleaner | trade-off: more pairs, noisier | matches |
| D | better | matches | worse | matches | matches |
| E | no result | no result | no result | no result | no result |
| F | worse | worse | trade-off: fewer pairs, cleaner | - | - |

## Datasets

### mockA_high  (mock, 16S, 6 samples; verdicts against FIGARO)

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 277/243 | 2 | 62.7% | 64.7% | 0.39 / 0.68 | -15.3 | cleaner | trade-off: fewer pairs, cleaner | as accurate |
| B | 277/243 | 2 | 62.7% | 64.7% | 0.39 / 0.68 | -15.3 | cleaner | trade-off: fewer pairs, cleaner | as accurate |
| B2 | 271/249 | 3,5 | 80.5% | 83.2% | 0.56 / 1.26 | +2.7 | noisier | trade-off: more pairs, noisier | as accurate |
| B4 | 273/247 | 2,3 | 69.5% | 71.8% | 0.40 / 0.91 | -8.6 | cleaner | trade-off: fewer pairs, cleaner | as accurate |
| C FIGARO (longest amplicon) | 273/247 | 3,4 | 77.7% | 80.3% | 0.55 / 1.09 | - | - | - | - |
| D | 273/247 | 3,4 | 77.7% | 80.3% | 0.55 / 1.09 | +0.0 | about the same | matches | as accurate |
| E | 0/0 | 2 | 39.4% | 41.3% | - | -38.0 | unknown | no result | less accurate |
| F | 268/204 | 2 | 21.8% | 76.3% | 0.40 / 0.42 | -56.0 | cleaner | trade-off: fewer pairs, cleaner | less accurate |

Accuracy (variants / strains / reads in exact ASVs): A: 36 / 12/14 / 99.7%; B: 36 / 12/14 / 99.7%; B2: 36 / 12/14 / 99.8%; B4: 36 / 12/14 / 99.8%; C: 36 / 12/14 / 99.8%; D: 36 / 12/14 / 99.8%; E: 33 / 11/14 / 99.8%; F: 8 / 1/14 / 98.3%

### v1v2  (real, 16S, 33 samples; verdicts against FIGARO)

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 201/157 | 2 | 84.2% | 91.2% | 0.18 / 0.17 | +3.0 (+2.6 to +3.4) | mixed | mixed noise (more pairs) | no truth |
| B | 201/157 | 2 | 84.2% | 91.2% | 0.18 / 0.17 | +3.0 (+2.6 to +3.4) | mixed | mixed noise (more pairs) | no truth |
| B2 | 201/157 | 2 | 84.2% | 91.2% | 0.18 / 0.17 | +3.0 (+2.6 to +3.4) | mixed | mixed noise (more pairs) | no truth |
| B4 | 198/160 | 1 | 78.5% | 85.2% | 0.11 / 0.12 | -2.7 (-3.2 to -2.3) | mixed | mixed noise (fewer pairs) | no truth |
| C FIGARO (longest amplicon) | 225/138 | 2,1 | 81.2% | 88.2% | 0.24 / 0.09 | - | - | - | - |
| C FIGARO (typical amplicon) | 225/102 | 2,1 | 43.3% | 89.1% | 0.25 / 0.04 | -38.0 (-43.1 to -32.1) | cleaner | trade-off: fewer pairs, cleaner | no truth |
| D | 211/147 | 2,1 | 82.3% | 88.8% | 0.19 / 0.11 | +1.1 (+0.7 to +1.5) | cleaner | better | no truth |
| E | 0/0 | 2 | 29.3% | 35.4% | - | -52.0 (-53.3 to -50.7) | unknown | no result | no truth |
| F | 253/213 | 2 | 72.1% | 79.8% | 0.32 / 0.36 | -9.1 (-9.8 to -8.4) | noisier | worse | no truth |

### its  (real, ITS, 37 samples; verdicts against A (FIGARO gave no result))

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs A: merged difference | noise | verdict | accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 0/0 | 2 | 46.9% | 74.2% | - | - | - | - | - |
| B | 0/0 | 2 | 46.9% | 74.2% | - | +0.0 (+0.0 to +0.0) | unknown | no result | no truth |
| B2 | 0/0 | 3 | 50.5% | 84.7% | - | +3.7 (+3.3 to +4.1) | unknown | no result | no truth |
| E | 200/200 | 2 | 23.3% | 42.0% | 0.29 / 0.45 | -23.5 (-25.3 to -21.9) | unknown | no result | no truth |

FIGARO gave no result at: FIGARO (amplicon 451) (not a difference in outcome).

### v4  (real, 16S, 36 samples; verdicts against FIGARO)

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 124/115 | 2 | 66.8% | 98.5% | 0.09 / 0.09 | +3.5 (+3.1 to +3.9) | noisier | trade-off: more pairs, noisier | no truth |
| B | 124/115 | 2 | 66.8% | 98.5% | 0.09 / 0.09 | +3.5 (+3.1 to +3.9) | noisier | trade-off: more pairs, noisier | no truth |
| B2 | 124/115 | 2 | 66.8% | 98.5% | 0.09 / 0.09 | +3.5 (+3.1 to +3.9) | noisier | trade-off: more pairs, noisier | no truth |
| B4 | 120/119 | 1 | 63.3% | 96.5% | 0.07 / 0.08 | +0.0 (+0.0 to +0.0) | about the same | matches | no truth |
| C FIGARO (longest amplicon) | 120/119 | 1 | 63.3% | 96.5% | 0.07 / 0.08 | - | - | - | - |
| C FIGARO (typical amplicon) | 118/101 | 1 | 72.1% | 97.0% | 0.07 / 0.06 | +8.7 (+7.6 to +9.8) | about the same | better | no truth |
| D | 120/119 | 1 | 63.3% | 96.5% | 0.07 / 0.08 | +0.0 (+0.0 to +0.0) | about the same | matches | no truth |
| E | 0/0 | 2 | 54.2% | 86.4% | - | -9.1 (-9.8 to -8.4) | unknown | no result | no truth |
| F | 212/185 | 2 | 0.8% | 1.6% | 0.25 / 0.56 | -62.7 (-67.1 to -58.6) | noisier | worse | no truth |

### mcm_v12  (mock, 16S, 6 samples; verdicts against FIGARO)

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 155/170 | 2 | 95.9% | 96.4% | 0.08 / 0.09 | +2.3 | noisier | trade-off: more pairs, noisier | no truth |
| B | 155/170 | 2 | 95.9% | 96.4% | 0.08 / 0.09 | +2.3 | noisier | trade-off: more pairs, noisier | no truth |
| B2 | 155/170 | 2 | 95.9% | 96.4% | 0.08 / 0.09 | +2.3 | noisier | trade-off: more pairs, noisier | no truth |
| B4 | 155/170 | 1 | 93.6% | 94.1% | 0.06 / 0.06 | -0.0 | about the same | matches | no truth |
| C FIGARO (longest amplicon) | 156/169 | 1 | 93.6% | 94.1% | 0.06 / 0.06 | - | - | - | - |
| C FIGARO (typical amplicon) | 147/160 | 1 | 54.4% | 94.5% | 0.05 / 0.06 | -39.2 | about the same | worse | no truth |
| D | 155/170 | 1 | 93.6% | 94.1% | 0.06 / 0.06 | -0.0 | about the same | matches | no truth |
| E | 0/0 | 2 | 26.0% | 50.0% | - | -67.6 | unknown | no result | no truth |
| F | 251/247 | 2 | 79.6% | 80.2% | 0.39 / 0.31 | -14.0 | noisier | worse | no truth |

Accuracy (variants / strains / reads in exact ASVs): A:  /  / -; B:  /  / -; B2:  /  / -; B4:  /  / -; C:  /  / -; C_typical:  /  / -; D:  /  / -; E:  /  / -; F:  /  / -

### mockB  (mock, 16S, 8 samples; verdicts against FIGARO)

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 279/248 | 2 | 19.9% | 20.3% | 0.41 / 1.24 | -54.1 | cleaner | trade-off: fewer pairs, cleaner | less accurate |
| B | 277/250 | 3,5 | 53.4% | 54.7% | 0.69 / 2.59 | -20.6 | cleaner | trade-off: fewer pairs, cleaner | less accurate |
| B2 | 277/250 | 5 | 55.8% | 57.2% | 0.82 / 2.62 | -18.1 | cleaner | trade-off: fewer pairs, cleaner | less accurate |
| B4 | 277/250 | 4,6 | 61.8% | 63.3% | 0.86 / 2.93 | -12.2 | cleaner | trade-off: fewer pairs, cleaner | less accurate |
| C FIGARO (longest amplicon) | 279/248 | 6,9 | 74.3% | 75.9% | 1.30 / 3.63 | - | - | - | - |
| C FIGARO (typical amplicon) | 272/199 | 5 | 45.7% | 80.6% | 1.07 / 1.16 | -30.2 | cleaner | trade-off: fewer pairs, cleaner | mixed |
| D | 274/253 | 6,9 | 76.7% | 78.7% | 1.14 / 3.86 | +2.6 | mixed | mixed noise (more pairs) | less accurate |
| E | 0/0 | 2 | 2.0% | 2.9% | - | -72.1 | unknown | no result | less accurate |
| F | 245/165 | 2 | 0.0% | 73.9% | 0.35 / 0.37 | -74.1 | cleaner | trade-off: fewer pairs, cleaner | less accurate |

Accuracy (variants / strains / reads in exact ASVs): A: 6 / 3/3 / 68.7%; B: 6 / 3/3 / 74.2%; B2: 6 / 3/3 / 73.6%; B4: 6 / 3/3 / 74.9%; C: 7 / 3/3 / 78.3%; C_typical: 2 / 1/3 / 90.5%; D: 6 / 3/3 / 75.3%; E: 4 / 3/3 / 54.3%; F: 0 / 0/3 / 0.0%

### mcm_v46  (mock, 16S, 5 samples; verdicts against FIGARO)

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 273/265 | 2 | 41.6% | 43.1% | 0.63 / 0.63 | -27.0 | cleaner | trade-off: fewer pairs, cleaner | no truth |
| B | 271/267 | 3 | 57.9% | 59.5% | 0.83 / 0.86 | -10.7 | cleaner | trade-off: fewer pairs, cleaner | no truth |
| B2 | 269/273 | 5 | 74.6% | 76.7% | 1.15 / 1.30 | +6.0 | noisier | trade-off: more pairs, noisier | no truth |
| B4 | 271/267 | 3 | 57.9% | 59.5% | 0.83 / 0.86 | -10.7 | cleaner | trade-off: fewer pairs, cleaner | no truth |
| C FIGARO (longest amplicon) | 270/268 | 4 | 68.6% | 70.4% | 1.00 / 1.06 | - | - | - | - |
| D | 271/267 | 4 | 68.8% | 70.5% | 1.01 / 1.04 | +0.3 | about the same | matches | no truth |
| E | 0/0 | 2 | 20.8% | 31.8% | - | -47.8 | unknown | no result | no truth |
| F | 230/236 | 2 | 0.0% | 74.8% | 0.35 / 0.41 | -68.6 | cleaner | trade-off: fewer pairs, cleaner | no truth |

Accuracy (variants / strains / reads in exact ASVs): A:  /  / -; B:  /  / -; B2:  /  / -; B4:  /  / -; C:  /  / -; D:  /  / -; E:  /  / -; F:  /  / -

### d6300_V3-V4  (mock, 16S, 10 samples; verdicts against FIGARO)

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 224/218 | 2 | 90.6% | 94.6% | 0.29 / 0.26 | +6.1 (+5.7 to +6.5) | noisier | trade-off: more pairs, noisier | as accurate |
| B | 224/218 | 2 | 90.6% | 94.6% | 0.29 / 0.26 | +6.1 (+5.7 to +6.5) | noisier | trade-off: more pairs, noisier | as accurate |
| B2 | 224/218 | 2 | 90.6% | 94.6% | 0.29 / 0.26 | +6.1 (+5.7 to +6.5) | noisier | trade-off: more pairs, noisier | as accurate |
| B4 | 224/218 | 1 | 84.5% | 88.2% | 0.24 / 0.20 | +0.0 (+0.0 to +0.0) | about the same | matches | as accurate |
| C FIGARO (longest amplicon) | 224/218 | 1 | 84.5% | 88.2% | 0.24 / 0.20 | - | - | - | - |
| D | 224/218 | 1 | 84.5% | 88.2% | 0.24 / 0.20 | +0.0 (+0.0 to +0.0) | about the same | matches | as accurate |
| E | 0/0 | 2 | 90.4% | 94.5% | - | +5.9 (+5.5 to +6.5) | unknown | no result | as accurate |

Accuracy (variants / strains / reads in exact ASVs): A: 10 / 8/8 / 97.9%; B: 10 / 8/8 / 97.9%; B2: 10 / 8/8 / 97.9%; B4: 10 / 8/8 / 97.9%; C: 10 / 8/8 / 97.9%; D: 10 / 8/8 / 97.9%; E: 10 / 8/8 / 97.9%

### d6300_V4-V5  (mock, 16S, 3 samples; verdicts against A (FIGARO gave no result))

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs A: merged difference | noise | verdict | accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 282/280 | 2 | 57.2% | 63.7% | 0.09 / 0.57 | - | - | - | - |
| B | 282/280 | 2 | 57.2% | 63.7% | 0.09 / 0.57 | +0.0 | about the same | matches | as accurate |
| B2 | 282/280 | 5 | 69.5% | 77.4% | 0.16 / 1.02 | +12.3 | noisier | trade-off: more pairs, noisier | as accurate |
| B4 | 282/280 | 1,3 | 62.4% | 69.2% | 0.09 / 0.73 | +5.3 | noisier | trade-off: more pairs, noisier | more accurate |
| C FIGARO (typical amplicon) | 249/137 | 1 | 80.3% | 87.9% | 0.09 / 0.07 | +23.1 | cleaner | better | more accurate |
| E | 0/0 | 2 | 63.9% | 71.7% | - | +6.7 | unknown | no result | more accurate |

FIGARO gave no result at: FIGARO (amplicon 550) (not a difference in outcome).

Accuracy (variants / strains / reads in exact ASVs): A: 9 / 8/9 / 98.8%; B: 9 / 8/9 / 98.8%; B2: 9 / 8/9 / 98.8%; B4: 9 / 8/9 / 98.9%; C_typical: 9 / 8/9 / 100.0%; E: 9 / 8/9 / 98.9%

### wastewater_V3-V4  (real, 16S, 9 samples; verdicts against FIGARO)

Fewer than 10 samples: point estimates only, no interval.

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 254/186 | 2 | 43.6% | 53.7% | 0.84 / 0.75 | -23.1 | cleaner | trade-off: fewer pairs, cleaner | no truth |
| B | 254/186 | 2 | 43.6% | 53.7% | 0.84 / 0.75 | -23.1 | cleaner | trade-off: fewer pairs, cleaner | no truth |
| B2 | 247/199 | 5 | 65.7% | 82.2% | 1.36 / 1.66 | -1.0 | noisier | worse | no truth |
| B4 | 247/195 | 3 | 54.8% | 68.3% | 1.00 / 1.22 | -12.0 | cleaner | trade-off: fewer pairs, cleaner | no truth |
| C FIGARO (longest amplicon) | 247/193 | 5 | 66.7% | 83.1% | 1.38 / 1.48 | - | - | - | - |
| C FIGARO (typical amplicon) | 234/180 | 4 | 25.5% | 82.7% | 1.01 / 0.95 | -41.4 | cleaner | trade-off: fewer pairs, cleaner | no truth |
| D | 247/199 | 5 | 65.7% | 82.2% | 1.36 / 1.66 | -1.0 | noisier | worse | no truth |
| E | 0/0 | 2 | 0.2% | 0.3% | - | -66.6 | unknown | no result | no truth |
| F | 186/143 | 2 | 0.2% | 81.7% | 0.28 / 0.27 | -66.5 | cleaner | trade-off: fewer pairs, cleaner | no truth |

### spikein_V3-V4  (real, 16S, 12 samples; verdicts against FIGARO)

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 222/218 | 2 | 83.6% | 87.6% | 0.41 / 0.36 | +6.3 (+5.3 to +7.4) | noisier | trade-off: more pairs, noisier | no truth |
| B | 222/218 | 2 | 83.6% | 87.6% | 0.41 / 0.36 | +6.3 (+5.3 to +7.4) | noisier | trade-off: more pairs, noisier | no truth |
| B2 | 222/218 | 2 | 83.6% | 87.6% | 0.41 / 0.36 | +6.3 (+5.3 to +7.4) | noisier | trade-off: more pairs, noisier | no truth |
| B4 | 222/218 | 2 | 83.6% | 87.6% | 0.41 / 0.36 | +6.3 (+5.3 to +7.4) | noisier | trade-off: more pairs, noisier | no truth |
| C FIGARO (longest amplicon) | 232/207 | 2,1 | 77.3% | 81.6% | 0.40 / 0.26 | - | - | - | - |
| D | 230/210 | 2,1 | 78.6% | 82.8% | 0.39 / 0.27 | +1.3 (+0.4 to +2.4) | about the same | matches | no truth |
| E | 0/0 | 2 | 81.7% | 86.7% | - | +4.4 (+3.6 to +5.4) | unknown | no result | no truth |

### swabs_V3-V4  (real, 16S, 36 samples; verdicts against FIGARO)

| arm | cut F/R | maxEE | merged | passing the filter | errors per kept read F / R | vs C: merged difference | noise | verdict | accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 224/218 | 2 | 77.0% | 85.0% | 0.27 / 0.27 | +5.9 (+5.1 to +6.9) | noisier | trade-off: more pairs, noisier | no truth |
| B | 224/218 | 2 | 77.0% | 85.0% | 0.27 / 0.27 | +5.9 (+5.1 to +6.9) | noisier | trade-off: more pairs, noisier | no truth |
| B2 | 224/218 | 2 | 77.0% | 85.0% | 0.27 / 0.27 | +5.9 (+5.1 to +6.9) | noisier | trade-off: more pairs, noisier | no truth |
| B4 | 224/218 | 1 | 71.1% | 78.6% | 0.22 / 0.20 | +0.0 (+0.0 to +0.0) | about the same | matches | no truth |
| C FIGARO (longest amplicon) | 224/218 | 1 | 71.1% | 78.6% | 0.22 / 0.20 | - | - | - | - |
| D | 224/218 | 1 | 71.1% | 78.6% | 0.22 / 0.20 | +0.0 (+0.0 to +0.0) | about the same | matches | no truth |
| E | 0/0 | 2 | 81.4% | 92.4% | - | +10.4 (+5.9 to +16.1) | unknown | no result | no truth |

## The coverage setting (share of the longest amplicons AmpliTrim may leave unmergeable)

**v1v2**: longest amplicon 351, typical 315

| setting | cut F/R | passing the filter | merged |
| --- | --- | --- | --- |
| AmpliTrim (maxEE 2) (default 0.2%) | 201/157 | 91.2% | 84.2% |
| AmpliTrim (maxEE 2, leave out 1.0%) | 198/157 | 91.5% | 84.2% |
| AmpliTrim (maxEE 2, leave out 5.0%) | 198/157 | 91.5% | 84.2% |

**v4**: longest amplicon 227, typical 207

| setting | cut F/R | passing the filter | merged |
| --- | --- | --- | --- |
| AmpliTrim (maxEE 2) (default 0.2%) | 124/115 | 98.5% | 66.8% |
| AmpliTrim (maxEE 2, leave out 1.0%) | 124/114 | 98.5% | 67.2% |
| AmpliTrim (maxEE 2, leave out 5.0%) | 115/105 | 98.8% | 72.3% |

**mcm_v12**: longest amplicon 313, typical 295

| setting | cut F/R | passing the filter | merged |
| --- | --- | --- | --- |
| AmpliTrim (maxEE 2) (default 0.2%) | 155/170 | 96.4% | 95.9% |
| AmpliTrim (maxEE 2, leave out 1.0%) | 155/170 | 96.4% | 95.9% |
| AmpliTrim (maxEE 2, leave out 5.0%) | 144/170 | 96.6% | 93.8% |

**mockB**: longest amplicon 515, typical 459

| setting | cut F/R | passing the filter | merged |
| --- | --- | --- | --- |
| AmpliTrim (maxEE 2) (default 0.2%) | 279/248 | 20.3% | 19.9% |
| AmpliTrim (maxEE 2, leave out 1.0%) | 279/248 | 20.3% | 19.9% |
| AmpliTrim (maxEE 2, leave out 5.0%) | 279/248 | 20.3% | 19.9% |

**d6300_V4-V5**: longest amplicon 550, typical 374

| setting | cut F/R | passing the filter | merged |
| --- | --- | --- | --- |
| AmpliTrim (maxEE 2) (default 0.2%) | 282/280 | 63.7% | 57.2% |
| AmpliTrim (maxEE 2, leave out 1.0%) | 268/118 | 92.9% | 89.8% |
| AmpliTrim (maxEE 2, leave out 5.0%) | 268/118 | 92.9% | 89.8% |

**wastewater_V3-V4**: longest amplicon 428, typical 402

| setting | cut F/R | passing the filter | merged |
| --- | --- | --- | --- |
| AmpliTrim (maxEE 2) (default 0.2%) | 254/186 | 53.7% | 43.6% |
| AmpliTrim (maxEE 2, leave out 1.0%) | 254/186 | 53.7% | 43.6% |
| AmpliTrim (maxEE 2, leave out 5.0%) | 256/187 | 51.9% | 41.4% |

## Stability of the picks across three disjoint sets of samples

| dataset | tool | picks (cut F/R; maxEE) | holds |
| --- | --- | --- | --- |
| mockA_high | - | 6 samples (9 are needed) | - |
| v1v2 | AmpliTrim | 197/161; 2 ; 188/167; 2 ; 201/162; 2 | no |
| v1v2 | AmpliTrim B | 197/161; 2 ; 188/167; 2 ; 201/162; 2 | no |
| v1v2 | FIGARO | 222/141; 2,1 ; 227/136; 2,1 ; 227/136; 2,1 | yes |
| v4 | AmpliTrim | 124/115; 2 ; 124/115; 2 ; 113/126; 2 | no |
| v4 | AmpliTrim B | 124/115; 2 ; 124/115; 2 ; 113/126; 2 | no |
| v4 | FIGARO | 118/121; 1 ; 124/115; 1 ; 123/116; 1 | yes |
| mcm_v12 | - | 6 samples (9 are needed) | - |
| mockB | - | 8 samples (9 are needed) | - |
| mcm_v46 | - | 5 samples (9 are needed) | - |
| d6300_V3-V4 | AmpliTrim | 226/216; 2 ; 225/217; 2 ; 224/218; 2 | yes |
| d6300_V3-V4 | AmpliTrim B | 226/216; 2 ; 225/217; 2 ; 224/218; 2 | yes |
| d6300_V3-V4 | FIGARO | 221/221; 1 ; error ; 217/225; 1,3 | no |
| d6300_V4-V5 | - | 3 samples (9 are needed) | - |
| wastewater_V3-V4 | AmpliTrim | 254/186; 2 ; 254/186; 2 ; 254/186; 2 | yes |
| wastewater_V3-V4 | AmpliTrim B | 254/186; 2 ; 254/186; 2 ; 254/186; 2 | yes |
| wastewater_V3-V4 | FIGARO | 257/183; 5,4 ; 256/184; 5,4 ; 240/200; 4,5 | no |
| spikein_V3-V4 | AmpliTrim | 222/218; 2 ; 231/208; 2 ; 229/210; 2 | yes |
| spikein_V3-V4 | AmpliTrim B | 222/218; 2 ; 231/208; 2 ; 229/210; 2 | yes |
| spikein_V3-V4 | FIGARO | 222/217; 1 ; 210/229; 1,2 ; 233/206; 2,1 | no |
| swabs_V3-V4 | AmpliTrim | 224/218; 2 ; 224/218; 2 ; 224/218; 2 | yes |
| swabs_V3-V4 | AmpliTrim B | 224/218; 2 ; 224/218; 2 ; 224/218; 2 | yes |
| swabs_V3-V4 | FIGARO | 220/222; 1 ; 224/218; 1 ; 228/214; 1 | yes |

Next: send this file, NIGHT2_PROTOCOL.md and night2.log.
