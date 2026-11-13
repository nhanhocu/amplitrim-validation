# AmpliTrim report

## Recommended settings

| truncLenF | truncLenR | maxEE | minOverlap |
|---|---|---|---|
| **269** | **171** | 3,2 | 12 |

In DADA2 (R):

```r
out <- filterAndTrim(fwd, filtF, rev, filtR,
                     truncLen = c(269, 171), maxEE = c(3, 2), truncQ = 2, maxN = 0)
# ... learnErrors(), dada() ...
merged <- mergePairs(dadaF, filtF, dadaR, filtR, minOverlap = 12, maxMismatch = 0)
```

In QIIME 2:

```
qiime dada2 denoise-paired ... --p-trunc-len-f 269 --p-trunc-len-r 171 \
    --p-max-ee-f 3 --p-max-ee-r 2
```

## What to expect

- About **68.0%** of read pairs should pass quality filtering and merge.
- Your longest amplicon is 428 nt. These settings can merge amplicons up to 428 nt, so your whole length range is covered.
- maxEE is 3,2, not DADA2's default of 2: at the recommended cut the 75th percentile of the reads' expected errors is 2.3 forward and 2.0 reverse, so each read's limit is set to cover three quarters of the reads in its direction (never below 2). Only 65% of the read pairs pass at maxEE 2 and 69% pass now; the reads this admits are noisier (see the table below). DADA2's author says that relaxing maxEE somewhat is acceptable, because DADA2's error model uses the quality scores. The rule is AmpliTrim's own and has not been tested on independent data (see 'How maxEE is chosen' in the user guide).

## Things to check

- Only 57% of read pairs could be merged at full read length (amplicons longer than about 555 nt, or some reads shorter than the rest); the lengths above come from the pairs that merged.
- Read lengths vary (forward 22-285 nt, reverse 19-282 nt): DADA2 drops reads shorter than truncLen, which loses 2% of pairs here.
- Only 68% of read pairs are expected to pass filtering and merge.

## What maxEE keeps

At the recommended truncation (269 + 171), the share of read pairs that pass DADA2's quality filter, and that then pass filtering and merge, for other maxEE values (forward, reverse):

| maxEE | pairs passing the filter | estimated yield | expected errors per kept read (F / R) | expected errors in the reads added beyond maxEE 2 (F / R) |
|---|---|---|---|---|
| 1 | 50.3% | 50.2% | 0.26 / 0.17 | - |
| 2 | 63.4% | 62.7% | 0.48 / 0.31 | - |
| 2,3 | 64.7% | 63.8% | 0.49 / 0.35 | 1.19 / 2.40 |
| **3,2 (used)** | 69.4% | 68.0% | 0.65 / 0.36 | 2.46 / 0.91 |
| 2,4 | 65.2% | 64.2% | 0.50 / 0.37 | 1.19 / 2.67 |
| 3 | 71.9% | 69.9% | 0.69 / 0.43 | 2.26 / 1.36 |
| 2,5 | 65.4% | 64.4% | 0.50 / 0.38 | 1.20 / 2.83 |
| 3,5 | 73.2% | 70.8% | 0.71 / 0.49 | 2.21 / 1.67 |
| 5 | 81.8% | 77.1% | 1.04 / 0.61 | 2.99 / 1.67 |

At maxEE 3,2, **69.4%** of the read pairs pass DADA2's quality filter at these truncation lengths.
DADA2's author calls maxEE = 2 a good general purpose value and says that relaxing it somewhat is also OK. DADA2's error model uses the quality scores, so it tolerates some noisier reads. But pushing through more lower-quality reads may not improve the relative abundances and could make them worse (DADA2 issue #2136, about PacBio reads). The table shows what a looser limit costs: the expected errors in the kept reads.

## Your data

- Reads: 40,000 pairs analysed (up to 285 + 282 nt).
- Amplicons: median 422 nt; 99% are 128-428 nt (all: 13-495), measured from the 57% of pairs that merge at full read length.
- Overlap at the recommended settings: about 25 nt on average.

![summary](summary.png)

## How these settings were chosen

- 40,000 of 120,000 read pairs were analysed. Totals below 440 nt (your longest amplicon plus the minimum overlap of 12) were not tested.
- Totals were tested from 440 nt in steps of 2 nt, stopping once the share of usable pairs stopped improving. For each, a spread of forward/reverse splits among those with the highest filter pass rate were quality-filtered (maxEE 3,2) and merged with vsearch. Settings within 1 percentage point of the best yield count as tied; the shortest overlap won.

## Limits

- The estimates come from merging raw reads with vsearch, not from DADA2. With long overlaps (well above 50 nt) DADA2's zero-mismatch rule can reject pairs that vsearch accepts, and chimeras or pairs that merge at the wrong offset count as usable here, so the yield can be optimistic. Run DADA2 once with these settings to confirm.
- Only read quality and mergeability are assessed, not taxonomic accuracy.
- The yield is measured on the raw reads, before DADA2 denoises them. In diverse samples (soil, for example) at modest depth DADA2 can keep far fewer reads than this estimate. Use it to compare settings, not as the final retained fraction.
- The reads are assumed to have adapters and primers removed and no quality trimming.

_AmpliTrim 0.2.0_
