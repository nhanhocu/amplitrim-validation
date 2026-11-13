# AmpliTrim report

## Recommended settings

| truncLenF | truncLenR | maxEE | minOverlap |
|---|---|---|---|
| **207** | **231** | 2 | 12 |

In DADA2 (R):

```r
out <- filterAndTrim(fwd, filtF, rev, filtR,
                     truncLen = c(207, 231), maxEE = c(2, 2), truncQ = 2, maxN = 0)
# ... learnErrors(), dada() ...
merged <- mergePairs(dadaF, filtF, dadaR, filtR, minOverlap = 12, maxMismatch = 0)
```

In QIIME 2:

```
qiime dada2 denoise-paired ... --p-trunc-len-f 207 --p-trunc-len-r 231 \
    --p-max-ee-f 2 --p-max-ee-r 2
```

## What to expect

- About **75.8%** of read pairs should pass quality filtering and merge.
- Your longest amplicon is 426 nt. These settings can merge amplicons up to 426 nt, so your whole length range is covered.
- maxEE is 2, DADA2's default: at the recommended cut the 75th percentile of the reads' expected errors is 1.5 forward and 1.2 reverse, both under 2, so the default already covers three quarters of the reads in each direction; 76% of the read pairs pass.

## Things to check

- Only 41% of read pairs could be merged at full read length (amplicons longer than about 590 nt, or some reads shorter than the rest); the lengths above come from the pairs that merged.
- Quality filtering removes 24% of read pairs at these settings.

## What maxEE keeps

At the recommended truncation (207 + 231), the share of read pairs that pass DADA2's quality filter, and that then pass filtering and merge, for other maxEE values (forward, reverse):

| maxEE | pairs passing the filter | estimated yield | expected errors per kept read (F / R) | expected errors in the reads added beyond maxEE 2 (F / R) |
|---|---|---|---|---|
| 1 | 50.1% | 50.1% | 0.37 / 0.40 | - |
| **2 (used)** | 76.0% | 75.8% | 0.61 / 0.59 | - |
| 2,3 | 79.1% | 78.9% | 0.62 / 0.66 | 0.89 / 2.39 |
| 2,4 | 80.2% | 79.8% | 0.62 / 0.70 | 0.89 / 2.65 |
| 3 | 86.8% | 86.3% | 0.78 / 0.69 | 1.99 / 1.41 |
| 2,5 | 80.7% | 80.3% | 0.62 / 0.73 | 0.89 / 2.85 |
| 3,5 | 89.0% | 87.9% | 0.79 / 0.77 | 1.87 / 1.81 |
| 5 | 95.2% | 92.1% | 0.99 / 0.82 | 2.50 / 1.69 |

At maxEE 2, **76.0%** of the read pairs pass DADA2's quality filter at these truncation lengths.
DADA2's author calls maxEE = 2 a good general purpose value and says that relaxing it somewhat is also OK. DADA2's error model uses the quality scores, so it tolerates some noisier reads. But pushing through more lower-quality reads may not improve the relative abundances and could make them worse (DADA2 issue #2136, about PacBio reads). The table shows what a looser limit costs: the expected errors in the kept reads.
A low share is not a problem in itself: DADA2's author says that the number of reads is not the aim, and that keeping about 40% after filtering is fine (DADA2 issue #2136, about PacBio reads).

## Your data

- Reads: 40,000 pairs analysed (301 + 301 nt).
- Amplicons: median 308 nt; 99% are 203-405 nt (all: 34-560), measured from the 41% of pairs that merge at full read length.
- 2% of amplicons are shorter than the reads. If primers or adapters have not been removed, those reads run past the amplicon into them; remove them first.
- Overlap at the recommended settings: about 124 nt on average.

![summary](summary.png)

## How these settings were chosen

- 40,000 of 120,000 read pairs were analysed. Totals below 438 nt (your longest amplicon plus the minimum overlap of 12) were not tested.
- Totals were tested from 438 nt in steps of 2 nt, stopping once the share of usable pairs stopped improving. For each, a spread of forward/reverse splits among those with the highest filter pass rate were quality-filtered (maxEE 2) and merged with vsearch. Settings within 1 percentage point of the best yield count as tied; the shortest overlap won.

## Limits

- The estimates come from merging raw reads with vsearch, not from DADA2. With long overlaps (well above 50 nt) DADA2's zero-mismatch rule can reject pairs that vsearch accepts, and chimeras or pairs that merge at the wrong offset count as usable here, so the yield can be optimistic. Run DADA2 once with these settings to confirm.
- Only read quality and mergeability are assessed, not taxonomic accuracy.
- The yield is measured on the raw reads, before DADA2 denoises them. In diverse samples (soil, for example) at modest depth DADA2 can keep far fewer reads than this estimate. Use it to compare settings, not as the final retained fraction.
- The reads are assumed to have adapters and primers removed and no quality trimming.

_AmpliTrim 0.2.0_
