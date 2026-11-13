# AmpliTrim report

## Recommended settings

| truncLenF | truncLenR | maxEE | minOverlap |
|---|---|---|---|
| **217** | **222** | 2 | 12 |

In DADA2 (R):

```r
out <- filterAndTrim(fwd, filtF, rev, filtR,
                     truncLen = c(217, 222), maxEE = c(2, 2), truncQ = 2, maxN = 0)
# ... learnErrors(), dada() ...
merged <- mergePairs(dadaF, filtF, dadaR, filtR, minOverlap = 12, maxMismatch = 0)
```

In QIIME 2:

```
qiime dada2 denoise-paired ... --p-trunc-len-f 217 --p-trunc-len-r 222 \
    --p-max-ee-f 2 --p-max-ee-r 2
```

## What to expect

- About **87.6%** of read pairs should pass quality filtering and merge.
- Your longest amplicon is 427 nt. These settings can merge amplicons up to 427 nt, so your whole length range is covered.
- maxEE is 2, DADA2's default: at the recommended cut the 75th percentile of the reads' expected errors is 0.1 forward and 0.3 reverse, both under 2, so the default already covers three quarters of the reads in each direction; 88% of the read pairs pass.

## What maxEE keeps

At the recommended truncation (217 + 222), the share of read pairs that pass DADA2's quality filter, and that then pass filtering and merge, for other maxEE values (forward, reverse):

| maxEE | pairs passing the filter | estimated yield | expected errors per kept read (F / R) | expected errors in the reads added beyond maxEE 2 (F / R) |
|---|---|---|---|---|
| 1 | 82.5% | 82.4% | 0.07 / 0.11 | - |
| **2 (used)** | 87.8% | 87.6% | 0.12 / 0.17 | - |
| 2,3 | 89.3% | 89.1% | 0.13 / 0.21 | 0.69 / 2.44 |
| 2,4 | 90.1% | 89.8% | 0.13 / 0.24 | 0.71 / 2.76 |
| 3 | 90.9% | 90.6% | 0.17 / 0.23 | 1.58 / 1.77 |
| 2,5 | 90.5% | 90.2% | 0.14 / 0.26 | 0.71 / 3.04 |
| 3,5 | 92.4% | 92.0% | 0.18 / 0.29 | 1.42 / 2.44 |
| 5 | 94.9% | 94.2% | 0.28 / 0.32 | 2.28 / 2.18 |

At maxEE 2, **87.8%** of the read pairs pass DADA2's quality filter at these truncation lengths.
DADA2's author calls maxEE = 2 a good general purpose value and says that relaxing it somewhat is also OK. DADA2's error model uses the quality scores, so it tolerates some noisier reads. But pushing through more lower-quality reads may not improve the relative abundances and could make them worse (DADA2 issue #2136, about PacBio reads). The table shows what a looser limit costs: the expected errors in the kept reads.

## Your data

- Reads: 40,000 pairs analysed (up to 285 + 284 nt).
- Amplicons: median 407 nt; 99% are 402-427 nt (all: 26-495), measured from the 91% of pairs that merge at full read length.
- Overlap at the recommended settings: about 28 nt on average.

![summary](summary.png)

## How these settings were chosen

- 40,000 of 120,000 read pairs were analysed. Totals below 439 nt (your longest amplicon plus the minimum overlap of 12) were not tested.
- Totals were tested from 439 nt in steps of 2 nt, stopping once the share of usable pairs stopped improving. For each, a spread of forward/reverse splits among those with the highest filter pass rate were quality-filtered (maxEE 2) and merged with vsearch. Settings within 1 percentage point of the best yield count as tied; the shortest overlap won.

## Limits

- The estimates come from merging raw reads with vsearch, not from DADA2. With long overlaps (well above 50 nt) DADA2's zero-mismatch rule can reject pairs that vsearch accepts, and chimeras or pairs that merge at the wrong offset count as usable here, so the yield can be optimistic. Run DADA2 once with these settings to confirm.
- Only read quality and mergeability are assessed, not taxonomic accuracy.
- The yield is measured on the raw reads, before DADA2 denoises them. In diverse samples (soil, for example) at modest depth DADA2 can keep far fewer reads than this estimate. Use it to compare settings, not as the final retained fraction.
- The reads are assumed to have adapters and primers removed and no quality trimming.

_AmpliTrim 0.2.0_
