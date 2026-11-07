# ITS merge check

The criteria (P26 to P29) are in TEST_REGISTER.md, section 20, and were fixed before this ran.

## Verdicts

- **P26** not decided: The default merge reproduces night 3's merged share within 0.3 points: 13.96% against night 3 not found
- **P27** NOT MET: Denoising accounts for more of the loss between the filter and the merged pairs than merging does, exactly: 30.1% against 38.8% of the input pairs
- **P28** NOT MET: mergePairs with trimOverhang = TRUE merges at least 2 points more of the input pairs than the default: +0.00 points
- **P29** MET: The exact merging loss exceeds AmpliTrim's estimate (1.89 points) by more than 5 points: 38.8 points, +36.9 over

## Where the input pairs go (9 samples, 43,405 input pairs; the exact split, every pair that enters the merge step is counted)

| step | share of the input pairs |
|---|---|
| pass the filter | 82.86% |
| lost in denoising (reads not in a denoised forward and reverse sequence) | 30.09% |
| enter the merge step | 52.77% |
| rejected: overlap shorter than 12 nt | 3.81% |
| rejected: mismatches or indels in the overlap | 35.00% |
| rejected: a clean overlap that is still refused (an overhang) | 0.00% |
| **merged (default)** | **13.96%** |
| merged with `trimOverhang = TRUE` | 13.96% (+0.00 points) |

- Night 3's track was not found, so P26 is not decided.
- Between the filter and the merged pairs: 30.1 points to denoising, 38.8 points to merging (rejected pairs).
- AmpliTrim's estimate of 'pass the filter but do not merge' was 1.89 points (vsearch, raw reads).

Next: send this file.
