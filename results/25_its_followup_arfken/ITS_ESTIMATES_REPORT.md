# ITS estimates test

The criteria (P77 to P79) are in TEST_REGISTER.md and were fixed before this ran.

AmpliTrim 0.2.0 (C:\Users\<user>\OneDrive\Documents\GitHub\amplitrim\amplitrim)

## Verdicts

- **P77** MET: AmpliTrim's predicted share of pairs that pass the filter is within 1 point of DADA2's on every group: arfken_its1 -0.21, arfken_its2 -0.09, arfken_mix_its1 +0.00, arfken_mix_its2 +0.00
- **P78** NOT MET: The estimate of the yield is too high by fewer points on the isolates than on the mixes, on every marker that has both: ITS1 +9.3 against +2.0, ITS2 +0.0 against +0.8
- **P79** MET: On the isolates the estimate of the yield is too high by less than 17 points: arfken_its1 +9.3, arfken_its2 +0.0

## Filter (Figure 2 on new data)

| group | AmpliTrim predicts | DADA2 observes | difference (points) |
|---|---|---|---|
| arfken_its1 | 61.99% | 62.20% | -0.21 |
| arfken_its2 | 37.61% | 37.70% | -0.09 |
| arfken_mix_its1 | 74.49% | 74.49% | +0.00 |
| arfken_mix_its2 | 38.06% | 38.06% | +0.00 |

## Yield (Supplementary Figure S2 on new data)

| group | AmpliTrim estimates | DADA2 merged | too high by (points) | pairs analysed by AmpliTrim | samples |
|---|---|---|---|---|---|
| arfken_its1 | 61.92% | 52.60% | +9.3 | 37,076 | 15 |
| arfken_its2 | 37.59% | 37.57% | +0.0 | 36,721 | 15 |
| arfken_mix_its1 | 74.40% | 72.42% | +2.0 | 44,547 | 9 |
| arfken_mix_its2 | 38.05% | 37.28% | +0.8 | 44,269 | 9 |

## Exploratory: AmpliTrim on the whole folders (as a user would), against DADA2 on the thinned reads

| group | filter: AmpliTrim predicts | DADA2 observes | difference (points) | yield: AmpliTrim estimates | DADA2 merged | too high by (points) |
|---|---|---|---|---|---|---|
| arfken_its1 | 67.80% | 62.20% | +5.60 | 67.71% | 52.60% | +15.1 |
| arfken_its2 | 35.91% | 37.70% | -1.79 | 35.90% | 37.57% | -1.7 |
| arfken_mix_its1 | 75.12% | 74.49% | +0.63 | 75.02% | 72.42% | +2.6 |
| arfken_mix_its2 | 38.20% | 38.06% | +0.15 | 38.19% | 37.28% | +0.9 |

Next: send this file.
