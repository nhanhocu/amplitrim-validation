# AmpliTrim report

## Recommended settings

| truncLenF | truncLenR | maxEE | minOverlap |
|---|---|---|---|
| **257** | **267** | 2,6 | 12 |

In DADA2 (R):

```r
out <- filterAndTrim(fwd, filtF, rev, filtR,
                     truncLen = c(257, 267), maxEE = c(2, 6), truncQ = 2, maxN = 0)
# ... learnErrors(), dada() ...
merged <- mergePairs(dadaF, filtF, dadaR, filtR, minOverlap = 12, maxMismatch = 0)
```

In QIIME 2:

```
qiime dada2 denoise-paired ... --p-trunc-len-f 257 --p-trunc-len-r 267 \
    --p-max-ee-f 2 --p-max-ee-r 6
```

## What to expect

- About **80.6%** of read pairs should pass quality filtering and merge.
- Your longest amplicon is 512 nt. These settings can merge amplicons up to 512 nt, so your whole length range is covered.

## Things to check

- Only 88% of read pairs could be merged at full read length. Some amplicons may be longer than your reads can span (about 580 nt), some reads may be shorter than the rest, or the overlaps may be of poor quality or repetitive. The amplicon lengths above come from the pairs that did merge.

## maxEE: retention against read quality

Each maxEE below was given its own best truncation (the same search as for your setting), so the comparison is not tied to one pair of truncation lengths:

| maxEE | truncLenF | truncLenR | pairs passing the filter | estimated yield | expected errors per kept read (F / R) | expected errors in the reads added beyond maxEE 2 (F / R) |
|---|---|---|---|---|---|---|
| 1 | 276 | 248 | 43.4% | 43.4% | 0.21 / 0.42 | - |
| 2 | 275 | 249 | 63.9% | 63.8% | 0.37 / 0.71 | - |
| 2,3 | 275 | 249 | 71.5% | 71.3% | 0.42 / 0.90 | 0.82 / 2.44 |
| 2,4 | 267 | 257 | 75.7% | 75.6% | 0.39 / 1.19 | 0.76 / 2.80 |
| 3 | 275 | 249 | 75.3% | 75.2% | 0.52 / 0.93 | 1.37 / 2.18 |
| 2,5 | 262 | 262 | 78.8% | 78.5% | 0.39 / 1.42 | 0.73 / 3.08 |
| **2,6 (yours)** | 257 | 267 | 80.9% | 80.6% | 0.38 / 1.67 | 0.70 / 3.33 |
| 3,5 | 268 | 256 | 83.1% | 82.7% | 0.53 / 1.36 | 1.15 / 2.96 |
| 5 | 275 | 249 | 87.7% | 87.1% | 0.77 / 1.28 | 1.85 / 2.80 |

Retention stops improving noticeably at **5,5** (truncLenF 275, truncLenR 249): an estimated 87.1% of pairs, against 80.6% at yours, with 0.77 / 1.28 expected errors per kept read against 0.38 / 1.67. A looser limit beyond that keeps few more reads but admits noisier ones.

DADA2's author has said that maxEE = 2 is a good general-purpose value, that relaxing it somewhat is also fine (the error model uses the quality scores, so it tolerates some noisier reads), and that the number of reads kept is not what matters: relative abundances are, and keeping more lower-quality reads may not improve them and could make them worse. The last column shows what a looser limit costs: the expected errors in the average kept read.

Read the paragraph above as information, not as a recommendation: it looks only at how many pairs are kept, and AmpliTrim does not measure what a looser maxEE does to the accuracy of your results. If you have a mock community, `validation/max_ee_sweep.py` tests it.

## Your data

- Reads: 48,528 pairs analysed (up to 297 + 295 nt).
- Amplicons: median 468 nt; 99% are 431-512 nt (all: 152-536), measured from the 88% of pairs that merge at full read length.
- Overlap at the recommended settings: about 55 nt on average.

![summary](summary.png)

## How these settings were chosen

- 48,528 of 485,272 read pairs were analysed.
- Your longest amplicon is 512 nt, so the settings must keep at least 524 nt in total (512 plus the minimum overlap of 12). Shorter totals are not tested.
- Totals were tested from 524 nt in steps of 2 nt, stopping once the share of usable pairs stopped improving. For each total, a spread of forward/reverse splits among those with the highest filter pass rate were quality-filtered (maxEE 2,6) and merged with vsearch.
- Settings within 1 percentage point of the best yield count as tied; the one with the shortest overlap was chosen.
- Every setting tested is listed in `candidates.csv`.

## Limits

- The estimates come from merging raw reads with vsearch, not from DADA2. With long overlaps (well above 50 nt) DADA2's zero-mismatch rule can reject pairs that vsearch accepts, so the yield can be several points optimistic. Run DADA2 once with these settings to confirm.
- Chimeras, and pairs that merge at the wrong offset, count as usable here, so the yield can be optimistic. This is most likely when amplicons have repetitive overlaps.
- Only read quality and mergeability are assessed, not taxonomic accuracy.
- The yield is measured on the raw reads, before DADA2 denoises them. DADA2 cannot confirm a sequence it sees about once, so in diverse samples (soil, for example) at modest depth the share of reads DADA2 keeps can be far lower than this estimate. Use it to compare settings, not as the final retained fraction.
- The reads are assumed to have adapters and primers removed and no quality trimming.

_AmpliTrim 0.1.0_
