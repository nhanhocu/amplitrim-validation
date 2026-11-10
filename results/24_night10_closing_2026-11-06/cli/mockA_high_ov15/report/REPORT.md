# AmpliTrim report

## Recommended settings

| truncLenF | truncLenR | maxEE | minOverlap |
|---|---|---|---|
| **275** | **248** | 2,3 | 15 |

In DADA2 (R):

```r
out <- filterAndTrim(fwd, filtF, rev, filtR,
                     truncLen = c(275, 248), maxEE = c(2, 3), truncQ = 2, maxN = 0)
# ... learnErrors(), dada() ...
merged <- mergePairs(dadaF, filtF, dadaR, filtR, minOverlap = 15, maxMismatch = 0)
```

In QIIME 2:

```
qiime dada2 denoise-paired ... --p-trunc-len-f 275 --p-trunc-len-r 248 \
    --p-max-ee-f 2 --p-max-ee-r 3
```

## What to expect

- About **70.9%** of read pairs should pass quality filtering and merge.
- Your longest amplicon is 508 nt. These settings can merge amplicons up to 508 nt, so your whole length range is covered.
- maxEE is 2,3, not DADA2's default of 2: at the recommended cut the 75th percentile of the reads' expected errors is 1.6 forward and 2.5 reverse, so each read's limit is set to cover three quarters of the reads in its direction (never below 2). Only 64% of the read pairs pass at maxEE 2 and 71% pass now; the reads this admits are noisier (see the table below). DADA2's author says that relaxing maxEE somewhat is acceptable, because DADA2's error model uses the quality scores. The rule is AmpliTrim's own and has not been tested on independent data (see 'How maxEE is chosen' in the user guide).

## Things to check

- Only 89% of read pairs could be merged at full read length (amplicons longer than about 579 nt, or some reads shorter than the rest); the lengths above come from the pairs that merged.
- Quality filtering removes 29% of read pairs at these settings.

## What maxEE keeps

At the recommended truncation (275 + 248), the share of read pairs that pass DADA2's quality filter, and that then pass filtering and merge, for other maxEE values (forward, reverse):

| maxEE | pairs passing the filter | estimated yield | expected errors per kept read (F / R) | expected errors in the reads added beyond maxEE 2 (F / R) |
|---|---|---|---|---|
| 1 | 42.5% | 42.5% | 0.21 / 0.44 | - |
| 2 | 63.1% | 63.1% | 0.37 / 0.72 | - |
| **2,3 (used)** | 71.0% | 70.9% | 0.42 / 0.91 | 0.82 / 2.44 |
| 2,4 | 74.8% | 74.7% | 0.44 / 1.04 | 0.86 / 2.77 |
| 3 | 74.8% | 74.7% | 0.52 / 0.95 | 1.35 / 2.19 |
| 2,5 | 76.9% | 76.7% | 0.46 / 1.13 | 0.89 / 3.02 |
| 3,5 | 82.5% | 82.3% | 0.60 / 1.22 | 1.34 / 2.84 |
| 5 | 87.4% | 87.0% | 0.78 / 1.30 | 1.85 / 2.81 |

At maxEE 2,3, **71.0%** of the read pairs pass DADA2's quality filter at these truncation lengths.
DADA2's author calls maxEE = 2 a good general purpose value and says that relaxing it somewhat is also OK. DADA2's error model uses the quality scores, so it tolerates some noisier reads. But pushing through more lower-quality reads may not improve the relative abundances and could make them worse (DADA2 issue #2136, about PacBio reads). The table shows what a looser limit costs: the expected errors in the kept reads.

## Your data

- Reads: 47,380 pairs analysed (up to 297 + 297 nt).
- Amplicons: median 484 nt; 99% are 460-505 nt (all: 378-536), measured from the 89% of pairs that merge at full read length.
- Overlap at the recommended settings: about 44 nt on average.

## How these settings were chosen

- 47,380 of 142,140 read pairs were analysed. Totals below 523 nt (your longest amplicon plus the minimum overlap of 15) were not tested.
- Totals were tested from 523 nt in steps of 2 nt, stopping once the share of usable pairs stopped improving. For each, a spread of forward/reverse splits among those with the highest filter pass rate were quality-filtered (maxEE 2,3) and merged with vsearch. Settings within 1 percentage point of the best yield count as tied; the shortest overlap won.

## Limits

- The estimates come from merging raw reads with vsearch, not from DADA2. With long overlaps (well above 50 nt) DADA2's zero-mismatch rule can reject pairs that vsearch accepts, and chimeras or pairs that merge at the wrong offset count as usable here, so the yield can be optimistic. Run DADA2 once with these settings to confirm.
- Only read quality and mergeability are assessed, not taxonomic accuracy.
- The yield is measured on the raw reads, before DADA2 denoises them. In diverse samples (soil, for example) at modest depth DADA2 can keep far fewer reads than this estimate. Use it to compare settings, not as the final retained fraction.
- The reads are assumed to have adapters and primers removed and no quality trimming.

_AmpliTrim 0.2.0_
