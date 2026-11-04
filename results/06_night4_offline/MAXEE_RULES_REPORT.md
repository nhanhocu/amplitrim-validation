# Night 4 (offline): a simple maxEE rule against FIGARO's

The criteria are in TEST_REGISTER.md, section 16, and were fixed before this ran.

## Verdicts

- **P13** NOT MET: The mean rule (unfloored) is within 1 of FIGARO's maxEE on each read, at FIGARO's cut, on at least 8 of the 10 datasets: 7 of 10 run
- **P14** NOT MET: On the 4 poor datasets the floored mean rule at AmpliTrim's cut is within 1 of FIGARO's pick on each read on at least 3: 1 of 4 run
- **P15** MET: On the 6 clean datasets the floored mean rule at AmpliTrim's cut gives (2,2) on at least 5: 6 of 6 run
- **P16** MET: The median rule matches FIGARO on no more datasets than the mean rule: median 6, mean 7 (of 10 run)

## Exploratory (not pre-registered; added after a first, partial run, and not part of the criteria)

FIGARO's maxEE is `int(x) + 1`, so its curve value x at the cut lay in [pick - 1, pick). If x were k times a statistic of the reads at FIGARO's cut, which k would reproduce every pick (every read of every dataset run)? A k fitted here is fitted on the datasets that test it, so it would be post hoc and adds a parameter.

| statistic of the reads at FIGARO's cut | k reproducing every pick | reads reproduced at k = 1 |
|---|---|---|
| mean | none (the windows do not overlap: 1.89 and above, below 1.73) | 10 of 20 |
| median | none (the windows do not overlap: 14.38 and above, below 2.26) | 10 of 20 |
| p75 | none (the windows do not overlap: 2.12 and above, below 1.25) | 10 of 20 |
| p90 | none (the windows do not overlap: 0.85 and above, below 0.68) | 11 of 20 |

## Datasets

### mockA_high  (poor: FIGARO chose maxEE 3,4)

Check on the reads: at FIGARO's cut 273/247 and maxEE 3,4, AmpliTrim's filter passes 80.2% of the pairs and DADA2 passed 80.3% in night 3

| at | read-pair statistic | forward / reverse | mean rule | mean rule, floored | median rule | median rule, floored | FIGARO |
|---|---|---|---|---|---|---|---|
| FIGARO's cut 273/247 | mean expected errors | 1.30 / 1.95 | 2,2 | 2,2 | 1,2 | 2,2 | 3,4 |
| | median expected errors | 0.42 / 1.08 | | | | | |
| AmpliTrim's cut 277/243 | mean expected errors | 1.39 / 1.85 | 2,2 | 2,2 | 1,1 | 2,2 | 3,4 |
| | median expected errors | 0.48 / 1.00 | | | | | |

FIGARO's pick means its curve value was in [2, 3) forward and [3, 4) reverse. Expected errors of the reads at its cut (forward / reverse): mean 1.30 / 1.95; median 0.42 / 1.08; p75 1.50 / 2.55; p90 3.73 / 4.91.

At AmpliTrim's cut (277/243), what each maxEE keeps (exact quality table):

| maxEE | pairs passing | expected errors per kept read (F / R) |
|---|---|---|
| default (2,2): 2,2 | 64.6% | 0.39 / 0.68 |
| mean rule, floored: 2,2 | 64.6% | 0.39 / 0.68 |
| FIGARO's pick: 3,4 | 80.1% | 0.59 / 1.04 |

### v1v2  (clean: FIGARO chose maxEE 2,1)

Check on the reads: at FIGARO's cut 225/138 and maxEE 2,1, AmpliTrim's filter passes 88.2% of the pairs and DADA2 passed 88.2% in night 3

| at | read-pair statistic | forward / reverse | mean rule | mean rule, floored | median rule | median rule, floored | FIGARO |
|---|---|---|---|---|---|---|---|
| FIGARO's cut 225/138 | mean expected errors | 0.70 / 0.24 | 1,1 | 2,2 | 1,1 | 2,2 | 2,1 |
| | median expected errors | 0.07 / 0.03 | | | | | |
| AmpliTrim's cut 201/157 | mean expected errors | 0.49 / 0.37 | 1,1 | 2,2 | 1,1 | 2,2 | 2,1 |
| | median expected errors | 0.04 / 0.05 | | | | | |

FIGARO's pick means its curve value was in [1, 2) forward and [0, 1) reverse. Expected errors of the reads at its cut (forward / reverse): mean 0.70 / 0.24; median 0.07 / 0.03; p75 0.47 / 0.14; p90 2.00 / 0.61.

At AmpliTrim's cut (201/157), what each maxEE keeps (exact quality table):

| maxEE | pairs passing | expected errors per kept read (F / R) |
|---|---|---|
| default (2,2): 2,2 | 91.1% | 0.18 / 0.17 |
| mean rule, floored: 2,2 | 91.1% | 0.18 / 0.17 |
| FIGARO's pick: 2,1 | 88.1% | 0.16 / 0.13 |

### v4  (clean: FIGARO chose maxEE 1,1)

Check on the reads: at FIGARO's cut 120/119 and maxEE 1,1, AmpliTrim's filter passes 96.4% of the pairs and DADA2 passed 96.5% in night 3

| at | read-pair statistic | forward / reverse | mean rule | mean rule, floored | median rule | median rule, floored | FIGARO |
|---|---|---|---|---|---|---|---|
| FIGARO's cut 120/119 | mean expected errors | 0.11 / 0.14 | 1,1 | 2,2 | 1,1 | 2,2 | 1,1 |
| | median expected errors | 0.02 / 0.03 | | | | | |
| AmpliTrim's cut 124/115 | mean expected errors | 0.12 / 0.13 | 1,1 | 2,2 | 1,1 | 2,2 | 1,1 |
| | median expected errors | 0.02 / 0.02 | | | | | |

FIGARO's pick means its curve value was in [0, 1) forward and [0, 1) reverse. Expected errors of the reads at its cut (forward / reverse): mean 0.11 / 0.14; median 0.02 / 0.03; p75 0.04 / 0.11; p90 0.21 / 0.27.

At AmpliTrim's cut (124/115), what each maxEE keeps (exact quality table):

| maxEE | pairs passing | expected errors per kept read (F / R) |
|---|---|---|
| default (2,2): 2,2 | 98.6% | 0.09 / 0.09 |
| mean rule, floored: 2,2 | 98.6% | 0.09 / 0.09 |
| FIGARO's pick: 1,1 | 96.5% | 0.07 / 0.08 |

### mcm_v12  (clean: FIGARO chose maxEE 1,1)

Check on the reads: at FIGARO's cut 156/169 and maxEE 1,1, AmpliTrim's filter passes 94.4% of the pairs and DADA2 passed 94.1% in night 3

| at | read-pair statistic | forward / reverse | mean rule | mean rule, floored | median rule | median rule, floored | FIGARO |
|---|---|---|---|---|---|---|---|
| FIGARO's cut 156/169 | mean expected errors | 0.20 / 0.18 | 1,1 | 2,2 | 1,1 | 2,2 | 1,1 |
| | median expected errors | 0.03 / 0.03 | | | | | |
| AmpliTrim's cut 155/170 | mean expected errors | 0.20 / 0.18 | 1,1 | 2,2 | 1,1 | 2,2 | 1,1 |
| | median expected errors | 0.03 / 0.03 | | | | | |

FIGARO's pick means its curve value was in [0, 1) forward and [0, 1) reverse. Expected errors of the reads at its cut (forward / reverse): mean 0.20 / 0.18; median 0.03 / 0.03; p75 0.04 / 0.04; p90 0.22 / 0.24.

At AmpliTrim's cut (155/170), what each maxEE keeps (exact quality table):

| maxEE | pairs passing | expected errors per kept read (F / R) |
|---|---|---|
| default (2,2): 2,2 | 96.7% | 0.08 / 0.09 |
| mean rule, floored: 2,2 | 96.7% | 0.08 / 0.09 |
| FIGARO's pick: 1,1 | 94.3% | 0.06 / 0.06 |

### mockB  (poor: FIGARO chose maxEE 6,9)

Check on the reads: at FIGARO's cut 279/248 and maxEE 6,9, AmpliTrim's filter passes 76.6% of the pairs and DADA2 passed 75.9% in night 3

| at | read-pair statistic | forward / reverse | mean rule | mean rule, floored | median rule | median rule, floored | FIGARO |
|---|---|---|---|---|---|---|---|
| FIGARO's cut 279/248 | mean expected errors | 2.65 / 5.17 | 3,6 | 3,6 | 2,4 | 2,4 | 6,9 |
| | median expected errors | 1.23 / 3.99 | | | | | |
| AmpliTrim's cut 279/248 | mean expected errors | 2.65 / 5.17 | 3,6 | 3,6 | 2,4 | 2,4 | 6,9 |
| | median expected errors | 1.23 / 3.99 | | | | | |

FIGARO's pick means its curve value was in [5, 6) forward and [8, 9) reverse. Expected errors of the reads at its cut (forward / reverse): mean 2.65 / 5.17; median 1.23 / 3.99; p75 3.54 / 7.21; p90 7.55 / 11.44.

At AmpliTrim's cut (279/248), what each maxEE keeps (exact quality table):

| maxEE | pairs passing | expected errors per kept read (F / R) |
|---|---|---|
| default (2,2): 2,2 | 19.6% | 0.41 / 1.24 |
| mean rule, floored: 3,6 | 59.2% | 0.79 / 2.81 |
| FIGARO's pick: 6,9 | 76.6% | 1.30 / 3.63 |

### mcm_v46  (poor: FIGARO chose maxEE 4,4)

Check on the reads: at FIGARO's cut 270/268 and maxEE 4,4, AmpliTrim's filter passes 70.3% of the pairs and DADA2 passed 70.4% in night 3

| at | read-pair statistic | forward / reverse | mean rule | mean rule, floored | median rule | median rule, floored | FIGARO |
|---|---|---|---|---|---|---|---|
| FIGARO's cut 270/268 | mean expected errors | 2.13 / 2.15 | 3,3 | 3,3 | 2,2 | 2,2 | 4,4 |
| | median expected errors | 1.00 / 1.08 | | | | | |
| AmpliTrim's cut 273/265 | mean expected errors | 2.24 / 2.00 | 3,3 | 3,3 | 2,1 | 2,2 | 4,4 |
| | median expected errors | 1.09 / 0.94 | | | | | |

FIGARO's pick means its curve value was in [3, 4) forward and [3, 4) reverse. Expected errors of the reads at its cut (forward / reverse): mean 2.13 / 2.15; median 1.00 / 1.08; p75 2.82 / 2.87; p90 5.85 / 5.78.

At AmpliTrim's cut (273/265), what each maxEE keeps (exact quality table):

| maxEE | pairs passing | expected errors per kept read (F / R) |
|---|---|---|
| default (2,2): 2,2 | 43.3% | 0.63 / 0.63 |
| mean rule, floored: 3,3 | 59.7% | 0.84 / 0.85 |
| FIGARO's pick: 4,4 | 70.5% | 1.03 / 1.02 |

### d6300_V3-V4  (clean: FIGARO chose maxEE 1,1)

Check on the reads: at FIGARO's cut 224/218 and maxEE 1,1, AmpliTrim's filter passes 88.1% of the pairs and DADA2 passed 88.2% in night 3

| at | read-pair statistic | forward / reverse | mean rule | mean rule, floored | median rule | median rule, floored | FIGARO |
|---|---|---|---|---|---|---|---|
| FIGARO's cut 224/218 | mean expected errors | 0.42 / 0.41 | 1,1 | 2,2 | 1,1 | 2,2 | 1,1 |
| | median expected errors | 0.22 / 0.15 | | | | | |
| AmpliTrim's cut 224/218 | mean expected errors | 0.42 / 0.41 | 1,1 | 2,2 | 1,1 | 2,2 | 1,1 |
| | median expected errors | 0.22 / 0.15 | | | | | |

FIGARO's pick means its curve value was in [0, 1) forward and [0, 1) reverse. Expected errors of the reads at its cut (forward / reverse): mean 0.42 / 0.41; median 0.22 / 0.15; p75 0.39 / 0.37; p90 0.87 / 0.90.

At AmpliTrim's cut (224/218), what each maxEE keeps (exact quality table):

| maxEE | pairs passing | expected errors per kept read (F / R) |
|---|---|---|
| default (2,2): 2,2 | 94.6% | 0.29 / 0.26 |
| mean rule, floored: 2,2 | 94.6% | 0.29 / 0.26 |
| FIGARO's pick: 1,1 | 88.1% | 0.24 / 0.20 |

### wastewater_V3-V4  (poor: FIGARO chose maxEE 5,5)

Check on the reads: at FIGARO's cut 247/193 and maxEE 5,5, AmpliTrim's filter passes 84.7% of the pairs and DADA2 passed 83.1% in night 3

| at | read-pair statistic | forward / reverse | mean rule | mean rule, floored | median rule | median rule, floored | FIGARO |
|---|---|---|---|---|---|---|---|
| FIGARO's cut 247/193 | mean expected errors | 2.24 / 2.13 | 3,3 | 3,3 | 2,2 | 2,2 | 5,5 |
| | median expected errors | 1.29 / 1.45 | | | | | |
| AmpliTrim's cut 254/186 | mean expected errors | 2.50 / 1.77 | 3,2 | 3,2 | 2,2 | 2,2 | 5,5 |
| | median expected errors | 1.52 / 1.07 | | | | | |

FIGARO's pick means its curve value was in [4, 5) forward and [4, 5) reverse. Expected errors of the reads at its cut (forward / reverse): mean 2.24 / 2.13; median 1.29 / 1.45; p75 2.92 / 2.56; p90 5.43 / 4.71.

At AmpliTrim's cut (254/186), what each maxEE keeps (exact quality table):

| maxEE | pairs passing | expected errors per kept read (F / R) |
|---|---|---|
| default (2,2): 2,2 | 55.4% | 0.84 / 0.75 |
| mean rule, floored: 3,2 | 64.8% | 1.07 / 0.80 |
| FIGARO's pick: 5,5 | 84.1% | 1.55 / 1.16 |

### spikein_V3-V4  (clean: FIGARO chose maxEE 2,1)

Check on the reads: at FIGARO's cut 232/207 and maxEE 2,1, AmpliTrim's filter passes 83.4% of the pairs and DADA2 passed 81.6% in night 3

| at | read-pair statistic | forward / reverse | mean rule | mean rule, floored | median rule | median rule, floored | FIGARO |
|---|---|---|---|---|---|---|---|
| FIGARO's cut 232/207 | mean expected errors | 0.72 / 0.58 | 1,1 | 2,2 | 1,1 | 2,2 | 2,1 |
| | median expected errors | 0.38 / 0.23 | | | | | |
| AmpliTrim's cut 222/218 | mean expected errors | 0.68 / 0.64 | 1,1 | 2,2 | 1,1 | 2,2 | 2,1 |
| | median expected errors | 0.32 / 0.29 | | | | | |

FIGARO's pick means its curve value was in [1, 2) forward and [0, 1) reverse. Expected errors of the reads at its cut (forward / reverse): mean 0.72 / 0.58; median 0.38 / 0.23; p75 0.71 / 0.53; p90 1.71 / 1.38.

At AmpliTrim's cut (222/218), what each maxEE keeps (exact quality table):

| maxEE | pairs passing | expected errors per kept read (F / R) |
|---|---|---|
| default (2,2): 2,2 | 89.3% | 0.41 / 0.36 |
| mean rule, floored: 2,2 | 89.3% | 0.41 / 0.36 |
| FIGARO's pick: 2,1 | 83.5% | 0.37 / 0.29 |

### swabs_V3-V4  (clean: FIGARO chose maxEE 1,1)

Check on the reads: at FIGARO's cut 224/218 and maxEE 1,1, AmpliTrim's filter passes 79.3% of the pairs and DADA2 passed 78.6% in night 3

| at | read-pair statistic | forward / reverse | mean rule | mean rule, floored | median rule | median rule, floored | FIGARO |
|---|---|---|---|---|---|---|---|
| FIGARO's cut 224/218 | mean expected errors | 0.44 / 0.49 | 1,1 | 2,2 | 1,1 | 2,2 | 1,1 |
| | median expected errors | 0.21 / 0.15 | | | | | |
| AmpliTrim's cut 224/218 | mean expected errors | 0.44 / 0.49 | 1,1 | 2,2 | 1,1 | 2,2 | 1,1 |
| | median expected errors | 0.21 / 0.15 | | | | | |

FIGARO's pick means its curve value was in [0, 1) forward and [0, 1) reverse. Expected errors of the reads at its cut (forward / reverse): mean 0.44 / 0.49; median 0.21 / 0.15; p75 0.38 / 0.39; p90 0.90 / 1.17.

At AmpliTrim's cut (224/218), what each maxEE keeps (exact quality table):

| maxEE | pairs passing | expected errors per kept read (F / R) |
|---|---|---|
| default (2,2): 2,2 | 85.5% | 0.27 / 0.27 |
| mean rule, floored: 2,2 | 85.5% | 0.27 / 0.27 |
| FIGARO's pick: 1,1 | 79.3% | 0.22 / 0.20 |
