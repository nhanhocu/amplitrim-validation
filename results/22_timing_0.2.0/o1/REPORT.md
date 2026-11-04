# AmpliTrim report

## Recommended settings

| truncLenF | truncLenR | maxEE | minOverlap |
|---|---|---|---|
| **156** | **169** | 2 | 12 |

In DADA2 (R):

```r
out <- filterAndTrim(fwd, filtF, rev, filtR,
                     truncLen = c(156, 169), maxEE = c(2, 2), truncQ = 2, maxN = 0)
# ... learnErrors(), dada() ...
merged <- mergePairs(dadaF, filtF, dadaR, filtR, minOverlap = 12, maxMismatch = 0)
```

In QIIME 2:

```
qiime dada2 denoise-paired ... --p-trunc-len-f 156 --p-trunc-len-r 169 \
    --p-max-ee-f 2 --p-max-ee-r 2
```

## What to expect

- About **96.4%** of read pairs should pass quality filtering and merge.
- Your longest amplicon is 313 nt. These settings can merge amplicons up to 313 nt, so your whole length range is covered.
- maxEE is 2, DADA2's default: at the recommended cut the 75th percentile of the reads' expected errors is 0.0 forward and 0.0 reverse, both under 2, so the default already covers three quarters of the reads in each direction; 97% of the read pairs pass.

## What maxEE keeps

At the recommended truncation (156 + 169), the share of read pairs that pass DADA2's quality filter, and that then pass filtering and merge, for other maxEE values (forward, reverse):

| maxEE | pairs passing the filter | estimated yield | expected errors per kept read (F / R) | expected errors in the reads added beyond maxEE 2 (F / R) |
|---|---|---|---|---|
| 1 | 94.2% | 94.1% | 0.06 / 0.06 | - |
| **2 (used)** | 96.6% | 96.4% | 0.08 / 0.09 | - |
| 2,3 | 97.1% | 96.8% | 0.09 / 0.10 | 0.80 / 2.44 |
| 2,4 | 97.2% | 97.0% | 0.09 / 0.10 | 0.79 / 2.70 |
| 3 | 97.8% | 97.5% | 0.10 / 0.11 | 1.80 / 1.72 |
| 2,5 | 97.3% | 97.0% | 0.09 / 0.11 | 0.76 / 2.90 |
| 3,5 | 98.1% | 97.7% | 0.11 / 0.12 | 1.64 / 2.16 |
| 5 | 98.9% | 98.3% | 0.14 / 0.13 | 2.44 / 2.10 |

At maxEE 2, **96.6%** of the read pairs pass DADA2's quality filter at these truncation lengths.
DADA2's author calls maxEE = 2 a good general purpose value and says that relaxing it somewhat is also OK. DADA2's error model uses the quality scores, so it tolerates some noisier reads. But pushing through more lower-quality reads may not improve the relative abundances and could make them worse (DADA2 issue #2136, about PacBio reads). The table shows what a looser limit costs: the expected errors in the kept reads.

## Your data

- Reads: 47,528 pairs analysed (up to 280 + 281 nt).
- Amplicons: median 295 nt; 99% are 285-313 nt (all: 181-322), measured from the 90% of pairs that merge at full read length.
- Overlap at the recommended settings: about 29 nt on average.

![summary](summary.png)

## How these settings were chosen

- 47,528 of 570,325 read pairs were analysed. Totals below 325 nt (your longest amplicon plus the minimum overlap of 12) were not tested.
- Totals were tested from 325 nt in steps of 2 nt, stopping once the share of usable pairs stopped improving. For each, a spread of forward/reverse splits among those with the highest filter pass rate were quality-filtered (maxEE 2) and merged with vsearch. Settings within 1 percentage point of the best yield count as tied; the shortest overlap won.

## Limits

- The estimates come from merging raw reads with vsearch, not from DADA2. With long overlaps (well above 50 nt) DADA2's zero-mismatch rule can reject pairs that vsearch accepts, and chimeras or pairs that merge at the wrong offset count as usable here, so the yield can be optimistic. Run DADA2 once with these settings to confirm.
- Only read quality and mergeability are assessed, not taxonomic accuracy.
- The yield is measured on the raw reads, before DADA2 denoises them. In diverse samples (soil, for example) at modest depth DADA2 can keep far fewer reads than this estimate. Use it to compare settings, not as the final retained fraction.
- The reads are assumed to have adapters and primers removed and no quality trimming.

_AmpliTrim 0.2.0_
