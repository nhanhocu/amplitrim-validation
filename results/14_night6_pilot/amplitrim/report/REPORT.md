# AmpliTrim report

## Recommended settings

| truncLenF | truncLenR | maxEE | minOverlap |
|---|---|---|---|
| **277** | **165** | 2 | 12 |

In DADA2 (R):

```r
out <- filterAndTrim(fwd, filtF, rev, filtR,
                     truncLen = c(277, 165), maxEE = c(2, 2), truncQ = 2, maxN = 0)
# ... learnErrors(), dada() ...
merged <- mergePairs(dadaF, filtF, dadaR, filtR, minOverlap = 12, maxMismatch = 0)
```

In QIIME 2:

```
qiime dada2 denoise-paired ... --p-trunc-len-f 277 --p-trunc-len-r 165 \
    --p-max-ee-f 2 --p-max-ee-r 2
```

## What to expect

- About **73.1%** of read pairs should pass quality filtering and merge.
- Your longest amplicon is 428 nt. These settings can merge amplicons up to 430 nt, so your whole length range is covered.
- maxEE is 2, DADA2's default: at the recommended cut the 75th percentile of the reads' expected errors is 0.3 forward and 0.2 reverse, both under 2, so the default already covers three quarters of the reads in each direction; 84% of the read pairs pass.

## Things to check

- Quality scores take only 2 distinct values, so the per-base quality that DADA2 relies on is missing. In a test, DADA2 could not learn an error model from such data. This is consistent with a simplified-quality file such as the SRA 'lite' format; use the original FASTQ files instead.
- Only 50% of read pairs could be merged at full read length. Some amplicons may be longer than your reads can span (about 557 nt), some reads may be shorter than the rest, or the overlaps may be of poor quality or repetitive. The amplicon lengths above come from the pairs that did merge.

## What maxEE keeps

At the recommended truncation (277 + 165), the share of read pairs that pass DADA2's quality filter, and that then pass filtering and merge, for other maxEE values (forward, reverse):

| maxEE | pairs passing the filter | estimated yield | expected errors per kept read (F / R) | expected errors in the reads added beyond maxEE 2 (F / R) |
|---|---|---|---|---|
| 1 | 84.4% | 73.1% | 0.28 / 0.17 | - |
| **2 (used)** | 84.4% | 73.1% | 0.28 / 0.17 | - |
| 2,3 | 84.4% | 73.1% | 0.28 / 0.17 | - |
| 2,4 | 84.4% | 73.1% | 0.28 / 0.17 | - |
| 3 | 84.4% | 73.1% | 0.28 / 0.17 | - |
| 2,5 | 84.4% | 73.1% | 0.28 / 0.17 | - |
| 3,5 | 84.4% | 73.1% | 0.28 / 0.17 | - |
| 5 | 84.4% | 73.1% | 0.28 / 0.17 | - |

At maxEE 2, **84.4%** of the read pairs pass DADA2's quality filter at these truncation lengths.
DADA2's author calls maxEE = 2 a good general purpose value and says that relaxing it somewhat is also OK. DADA2's error model uses the quality scores, so it tolerates some noisier reads. But pushing through more lower-quality reads may not improve the relative abundances and could make them worse (DADA2 issue #2136, about PacBio reads). The table shows what a looser limit costs: the expected errors in the kept reads.
A low share is not a problem in itself: DADA2's author says that the number of reads is not the aim, and that keeping about 40% after filtering is fine (DADA2 issue #2136, about PacBio reads).

## Your data

- Reads: 9,632 pairs analysed (up to 288 + 281 nt).
- Amplicons: median 422 nt; 99% are 401-428 nt (all: 62-429), measured from the 50% of pairs that merge at full read length.
- Overlap at the recommended settings: about 27 nt on average.

![summary](summary.png)

## How these settings were chosen

- 9,632 of 9,632 read pairs were analysed. Totals below 440 nt (your longest amplicon plus the minimum overlap of 12) were not tested.
- Totals were tested from 440 nt in steps of 2 nt, stopping once the share of usable pairs stopped improving. For each, a spread of forward/reverse splits among those with the highest filter pass rate were quality-filtered (maxEE 2) and merged with vsearch. Settings within 1 percentage point of the best yield count as tied; the shortest overlap won.

## Limits

- The estimates come from merging raw reads with vsearch, not from DADA2. With long overlaps (well above 50 nt) DADA2's zero-mismatch rule can reject pairs that vsearch accepts, and chimeras or pairs that merge at the wrong offset count as usable here, so the yield can be optimistic. Run DADA2 once with these settings to confirm.
- Only read quality and mergeability are assessed, not taxonomic accuracy.
- The yield is measured on the raw reads, before DADA2 denoises them. In diverse samples (soil, for example) at modest depth DADA2 can keep far fewer reads than this estimate. Use it to compare settings, not as the final retained fraction.
- The reads are assumed to have adapters and primers removed and no quality trimming.

_AmpliTrim 0.1.0_
