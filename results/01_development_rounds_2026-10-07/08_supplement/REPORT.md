# AmpliTrim report

## Recommended settings

| truncLenF | truncLenR | maxEE | minOverlap |
|---|---|---|---|
| **257** | **260** | 2,6 | 12 |

In DADA2 (R):

```r
out <- filterAndTrim(fwd, filtF, rev, filtR,
                     truncLen = c(257, 260), maxEE = c(2, 6), truncQ = 2, maxN = 0)
# ... learnErrors(), dada() ...
merged <- mergePairs(dadaF, filtF, dadaR, filtR, minOverlap = 12, maxMismatch = 0)
```

In QIIME 2:

```
qiime dada2 denoise-paired ... --p-trunc-len-f 257 --p-trunc-len-r 260 \
    --p-max-ee-f 2 --p-max-ee-r 6
```

## What to expect

- About **80.8%** of read pairs should pass quality filtering and merge.
- Your longest amplicon is 505 nt. These settings can merge amplicons up to 505 nt, so your whole length range is covered.

## Things to check

- Only 88% of read pairs could be merged at full read length. Some amplicons may be longer than your reads can span (about 580 nt), some reads may be shorter than the rest, or the overlaps may be of poor quality or repetitive. The amplicon lengths above come from the pairs that did merge.

## Coverage against quality

Your settings can merge amplicons up to 505 nt. The longest amplicons come from taxa with the longest 16S regions, and merging them needs long reads, but quality falls toward the read ends, so covering fewer of them lets the reads be shorter and cleaner. Each row below has its own best truncation:

| share of the longest amplicons left out | longest amplicon covered | total length | truncLenF | truncLenR | pairs passing the filter | estimated yield | expected errors per kept read (F / R) |
|---|---|---|---|---|---|---|---|
| 0.5% | 512 nt | 524 | 257 | 267 | 80.9% | 80.6% | 0.38 / 1.67 |
| **1.0% (yours)** | 505 nt | 517 | 257 | 260 | 81.9% | 80.8% | 0.39 / 1.49 |
| 2.0% | 499 nt | 511 | 245 | 266 | 82.7% | 79.8% | 0.35 / 1.67 |
| 5.0% | 499 nt | 511 | 245 | 266 | 82.7% | 79.8% | 0.35 / 1.67 |
| 10.0% | 499 nt | 511 | 245 | 266 | 82.7% | 79.8% | 0.35 / 1.67 |

Leaving out more of the longest amplicons would barely improve the yield here, so the coverage rule is not what limits it.

## What maxEE keeps

At the recommended truncation (257 + 260), the share of read pairs that pass DADA2's quality filter, and that then pass filtering and merge, for other maxEE values (forward, reverse):

| maxEE | pairs passing the filter | estimated yield | expected errors per kept read (F / R) | FIGARO's score |
|---|---|---|---|---|
| 1 | 37.6% | 37.3% | 0.14 / 0.49 | 37.6 |
| 2 | 60.0% | 59.5% | 0.26 / 0.83 | 58.0 |
| 2,3 | 70.7% | 70.0% | 0.32 / 1.07 | 65.7 |
| 2,4 | 76.6% | 75.8% | 0.35 / 1.26 | 66.6 |
| 3 | 72.8% | 72.1% | 0.38 / 1.09 | 64.8 |
| 2,5 | 79.8% | 78.9% | 0.38 / 1.39 | 62.8 |
| **2,6 (yours)** | 81.9% | 80.8% | 0.39 / 1.49 | 55.9 |
| 3,5 | 83.6% | 82.5% | 0.47 / 1.45 | 63.6 |
| 5 | 86.3% | 85.0% | 0.57 / 1.50 | 54.3 |

At maxEE 2,6, **81.9%** of the read pairs pass DADA2's quality filter at these truncation lengths.
DADA2's author has said that maxEE = 2 is a good general-purpose value, that relaxing it somewhat is also fine (the error model uses the quality scores, so it tolerates some noisier reads), and that the number of reads kept is not what matters: relative abundances are, and keeping more lower-quality reads may not improve them and could make them worse. The last column shows what a looser limit costs: the expected errors in the average kept read.
A low share is not a problem in itself. If too few reads remain to estimate your low-abundance taxa, the DADA2 tutorial describes relaxing maxEE, especially on the reverse read (for example `maxEE = c(2, 5)`), and shortening truncLen to remove low-quality tails while keeping the overlap.

_FIGARO's score is the rule FIGARO uses to rank settings (retention in percent minus (F-1)^2 minus (R-1)^2), applied here to exact pass rates. It is one tool's weighting, not a DADA2 criterion._

## Your data

- Reads: 48,528 pairs analysed (up to 297 + 295 nt).
- Amplicons: median 468 nt; 99% are 431-512 nt (all: 152-536), measured from the 88% of pairs that merge at full read length.
- Overlap at the recommended settings: about 49 nt on average.

![summary](summary.png)

## How these settings were chosen

- 48,528 of 485,272 read pairs were analysed.
- Your longest amplicon is 505 nt, so the settings must keep at least 517 nt in total (505 plus the minimum overlap of 12). Shorter totals are not tested.
- Totals were tested from 517 nt in steps of 2 nt, stopping once the share of usable pairs stopped improving. For each total, a spread of forward/reverse splits among those with the highest filter pass rate were quality-filtered (maxEE 2,6) and merged with vsearch.
- Settings within 1 percentage point of the best yield count as tied; the one with the shortest overlap was chosen.
- Every setting tested is listed in `candidates.csv`.

## Limits

- The estimates come from merging raw reads with vsearch, not from DADA2. With long overlaps (well above 50 nt) DADA2's zero-mismatch rule can reject pairs that vsearch accepts, so the yield can be several points optimistic. Run DADA2 once with these settings to confirm.
- Chimeras, and pairs that merge at the wrong offset, count as usable here, so the yield can be optimistic. This is most likely when amplicons have repetitive overlaps.
- Only read quality and mergeability are assessed, not taxonomic accuracy.
- The yield is measured on the raw reads, before DADA2 denoises them. DADA2 cannot confirm a sequence it sees about once, so in diverse samples (soil, for example) at modest depth the share of reads DADA2 keeps can be far lower than this estimate. Use it to compare settings, not as the final retained fraction.
- The reads are assumed to have adapters and primers removed and no quality trimming.

_AmpliTrim 0.1.0_
