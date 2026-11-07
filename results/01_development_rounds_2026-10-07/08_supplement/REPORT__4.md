# AmpliTrim report

## Recommended settings

| truncLenF | truncLenR | maxEE | minOverlap |
|---|---|---|---|
| **220** | **227** | 2 | 12 |

In DADA2 (R):

```r
out <- filterAndTrim(fwd, filtF, rev, filtR,
                     truncLen = c(220, 227), maxEE = c(2, 2), truncQ = 2, maxN = 0)
# ... learnErrors(), dada() ...
merged <- mergePairs(dadaF, filtF, dadaR, filtR, minOverlap = 12, maxMismatch = 0)
```

In QIIME 2:

```
qiime dada2 denoise-paired ... --p-trunc-len-f 220 --p-trunc-len-r 227 \
    --p-max-ee-f 2 --p-max-ee-r 2
```

## What to expect

- About **88.5%** of read pairs should pass quality filtering and merge.
- Your longest amplicon is 433 nt. These settings can merge amplicons up to 435 nt, so your whole length range is covered.

## Things to check

- Only 88% of read pairs could be merged at full read length. Some amplicons may be longer than your reads can span (about 446 nt), some reads may be shorter than the rest, or the overlaps may be of poor quality or repetitive. The amplicon lengths above come from the pairs that did merge.

## Your data

- Reads: 12,000 pairs analysed (231 + 227 nt).
- Amplicons: median 426 nt; 99% are 422-433 nt (all: 421-434), measured from the 88% of pairs that merge at full read length.
- Overlap at the recommended settings: about 20 nt on average.

![summary](summary.png)

## How these settings were chosen

- 12,000 of 12,000 read pairs were analysed.
- Your longest amplicon is 433 nt, so the settings must keep at least 445 nt in total (433 plus the minimum overlap of 12). Shorter totals are not tested.
- Totals were tested from 445 nt in steps of 2 nt, stopping once the share of usable pairs stopped improving. For each total, a spread of forward/reverse splits among those with the highest filter pass rate were quality-filtered (maxEE 2) and merged with vsearch.
- Settings within 1 percentage point of the best yield count as tied; the one with the shortest overlap was chosen.
- Every setting tested is listed in `candidates.csv`.

## Limits

- The estimates come from merging raw reads with vsearch, not from DADA2. With long overlaps (well above 50 nt) DADA2's zero-mismatch rule can reject pairs that vsearch accepts, so the yield can be several points optimistic. Run DADA2 once with these settings to confirm.
- Chimeras, and pairs that merge at the wrong offset, count as usable here, so the yield can be optimistic. This is most likely when amplicons have repetitive overlaps.
- Only read quality and mergeability are assessed, not taxonomic accuracy.
- The reads are assumed to have adapters and primers removed and no quality trimming.

_AmpliTrim 0.1.0_
