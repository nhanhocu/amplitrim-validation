# ITS merge check

The criteria (P26 to P29) are in TEST_REGISTER.md, section 20, and were fixed before this ran.

## Verdicts

- **P26** MET: The default merge reproduces night 3's merged share within 0.3 points: 46.87% against 46.87% (+0.00 points)
- **P27** MET: Denoising accounts for more of the loss between the filter and the merged pairs than merging does, exactly: 15.9% against 11.5% of the input pairs
- **P28** NOT MET: mergePairs with trimOverhang = TRUE merges at least 2 points more of the input pairs than the default: +0.00 points
- **P29** MET: The exact merging loss exceeds AmpliTrim's estimate (1.89 points) by more than 5 points: 11.5 points, +9.6 over

## Where the input pairs go (37 samples, 178,657 input pairs; the exact split, every pair that enters the merge step is counted)

| step | share of the input pairs |
|---|---|
| pass the filter | 74.24% |
| lost in denoising (reads not in a denoised forward and reverse sequence) | 15.87% |
| enter the merge step | 58.37% |
| rejected: overlap shorter than 12 nt | 5.07% |
| rejected: mismatches or indels in the overlap | 6.43% |
| rejected: a clean overlap that is still refused (an overhang) | 0.00% |
| **merged (default)** | **46.87%** |
| merged with `trimOverhang = TRUE` | 46.87% (+0.00 points) |

- Night 3 merged 46.87% on the same reads.
- Between the filter and the merged pairs: 15.9 points to denoising, 11.5 points to merging (rejected pairs).
- AmpliTrim's estimate of 'pass the filter but do not merge' was 1.89 points (vsearch, raw reads).

Next: send this file.
