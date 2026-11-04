# ITS check

The criteria are in TEST_REGISTER.md, section 19, and were fixed before this ran.

## Verdicts

- **P23** MET: AmpliTrim's share of pairs passing the filter is within 0.2 points of DADA2's, on the same reads: 74.30% against 74.30% (+0.00 points)
- **P24** MET: AmpliTrim's share of forward reads passing alone is within 0.2 points of DADA2's single-end filter, on the same reads: 87.47% against 87.47% (+0.00 points)
- **P25** MET: (exploratory) Of DADA2's loss between the filter and the merged pairs, denoising accounts for more than merging: 14.0% of the input pairs lost to denoising (at least) against 13.4% lost to merging (at most)

## A. The filter, on the same reads (AmpliTrim's own ITS run, and DADA2's filterAndTrim with no truncLen)

Pairs analysed: AmpliTrim 49,720, DADA2 49,720.

| quantity | AmpliTrim | DADA2 | difference (points) |
|---|---|---|---|
| pairs passing the filter | 74.30% | 74.30% | +0.00 |
| forward reads passing alone | 87.47% | 87.47% | +0.00 |

AmpliTrim's rows of 'where the pairs go' for the same run (shares of the pairs analysed):

| step | share |
|---|---|
| too short after the cut at the first base of quality 2 or below | 0.00% |
| contain an N | 0.00% |
| more expected errors than maxEE 2 | 25.70% |
| pass the filter | 74.30% |
| pass the filter but do not merge (vsearch's estimate) | 1.89% |
| pass the filter and merge (vsearch's estimate) | 72.41% |

Pairs that do not merge even at full read length: 15.9%.

## B. Where DADA2 loses the pairs after the filter (night 3, AmpliTrim's own setting, maxEE 2)

From C:\data\runs\night3_2026-10-09, 37 samples, 178,657 input pairs. Shares of the input pairs:

| step | DADA2 |
|---|---|
| pass the filter | 74.2% |
| reads in denoised forward sequences | 61.9% |
| reads in denoised reverse sequences | 60.3% |
| merged | 46.9% |
| after chimera removal | 46.9% |

- Between the filter (74.2%) and the merged pairs (46.9%) DADA2 loses 27.4 points of the input pairs: at least 14.0 points to denoising (a pair needs both reads in a denoised sequence) and at most 13.4 points to merging.
- AmpliTrim's estimate of the pairs that pass the filter but do not merge is 1.9 points (vsearch, on the raw reads: it cannot see denoising).

Next: send this file.
