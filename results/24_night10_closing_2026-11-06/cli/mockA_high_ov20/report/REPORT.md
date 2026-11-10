# AmpliTrim report

## Recommended settings

| truncLenF | truncLenR | maxEE | minOverlap |
|---|---|---|---|
| **277** | **251** | 2,3 | 20 |

In DADA2 (R):

```r
out <- filterAndTrim(fwd, filtF, rev, filtR,
                     truncLen = c(277, 251), maxEE = c(2, 3), truncQ = 2, maxN = 0)
# ... learnErrors(), dada() ...
merged <- mergePairs(dadaF, filtF, dadaR, filtR, minOverlap = 20, maxMismatch = 0)
```

In QIIME 2:

```
qiime dada2 denoise-paired ... --p-trunc-len-f 277 --p-trunc-len-r 251 \
    --p-max-ee-f 2 --p-max-ee-r 3
```

## What to expect

- About **69.3%** of read pairs should pass quality filtering and merge.
- Your longest amplicon is 508 nt. These settings can merge amplicons up to 508 nt, so your whole length range is covered.
- maxEE is 2,3, not DADA2's default of 2: at the recommended cut the 75th percentile of the reads' expected errors is 1.8 forward and 2.6 reverse, so each read's limit is set to cover three quarters of the reads in its direction (never below 2). Only 62% of the read pairs pass at maxEE 2 and 69% pass now; the reads this admits are noisier (see the table below). DADA2's author says that relaxing maxEE somewhat is acceptable, because DADA2's error model uses the quality scores. The rule is AmpliTrim's own and has not been tested on independent data (see 'How maxEE is chosen' in the user guide).

## Things to check

- Only 89% of read pairs could be merged at full read length (amplicons longer than about 574 nt, or some reads shorter than the rest); the lengths above come from the pairs that merged.
- Only 69% of read pairs are expected to pass filtering and merge.

## What maxEE keeps

At the recommended truncation (277 + 251), the share of read pairs that pass DADA2's quality filter, and that then pass filtering and merge, for other maxEE values (forward, reverse):

| maxEE | pairs passing the filter | estimated yield | expected errors per kept read (F / R) | expected errors in the reads added beyond maxEE 2 (F / R) |
|---|---|---|---|---|
| 1 | 39.4% | 39.3% | 0.21 / 0.46 | - |
| 2 | 60.8% | 60.8% | 0.37 / 0.77 | - |
| **2,3 (used)** | 69.4% | 69.3% | 0.42 / 0.97 | 0.81 / 2.44 |
| 2,4 | 73.6% | 73.6% | 0.45 / 1.11 | 0.86 / 2.77 |
| 3 | 73.0% | 72.9% | 0.52 / 1.01 | 1.29 / 2.22 |
| 2,5 | 75.9% | 75.7% | 0.47 / 1.21 | 0.88 / 3.02 |
| 3,5 | 81.5% | 81.3% | 0.61 / 1.30 | 1.31 / 2.87 |
| 5 | 86.5% | 86.1% | 0.79 / 1.38 | 1.80 / 2.85 |

At maxEE 2,3, **69.4%** of the read pairs pass DADA2's quality filter at these truncation lengths.
DADA2's author calls maxEE = 2 a good general purpose value and says that relaxing it somewhat is also OK. DADA2's error model uses the quality scores, so it tolerates some noisier reads. But pushing through more lower-quality reads may not improve the relative abundances and could make them worse (DADA2 issue #2136, about PacBio reads). The table shows what a looser limit costs: the expected errors in the kept reads.

## Your data

- Reads: 47,380 pairs analysed (up to 297 + 297 nt).
- Amplicons: median 484 nt; 99% are 460-505 nt (all: 378-536), measured from the 89% of pairs that merge at full read length.
- Overlap at the recommended settings: about 49 nt on average.

## How these settings were chosen

- 47,380 of 142,140 read pairs were analysed. Totals below 528 nt (your longest amplicon plus the minimum overlap of 20) were not tested.
- Totals were tested from 528 nt in steps of 2 nt, stopping once the share of usable pairs stopped improving. For each, a spread of forward/reverse splits among those with the highest filter pass rate were quality-filtered (maxEE 2,3) and merged with vsearch. Settings within 1 percentage point of the best yield count as tied; the shortest overlap won.

## Limits

- The estimates come from merging raw reads with vsearch, not from DADA2. With long overlaps (well above 50 nt) DADA2's zero-mismatch rule can reject pairs that vsearch accepts, and chimeras or pairs that merge at the wrong offset count as usable here, so the yield can be optimistic. Run DADA2 once with these settings to confirm.
- Only read quality and mergeability are assessed, not taxonomic accuracy.
- The yield is measured on the raw reads, before DADA2 denoises them. In diverse samples (soil, for example) at modest depth DADA2 can keep far fewer reads than this estimate. Use it to compare settings, not as the final retained fraction.
- The reads are assumed to have adapters and primers removed and no quality trimming.

_AmpliTrim 0.2.0_
