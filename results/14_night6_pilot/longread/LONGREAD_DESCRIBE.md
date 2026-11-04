# Long-read description of C:\data\runs\night6_pilot\raw_pacbio

2 files, 31,995 reads; 85.5% have both primers.
Reads between the primers: 27,365; median of the file medians 1454 nt; share within 10% of the median 99.5%.
Quality (mean of the error probabilities, as Phred): first 50 bases Q31.3, middle half Q31.2, last 50 bases Q29.1; fewest distinct quality values in a file: 93, lowest maximum: Q93.

Columns: both% reads with both primers; rev% of those, in the reverse orientation; median, mode: length between the primers (mode = commonest 10 nt bin); in10%: share within 10% of the median; >1.5x%: share longer than 1.5 times the median; EE med, EE/kb: expected errors per read and per 1,000 nt (median); <=EEn%: share of reads at or under maxEE n; Qs, Qmax: distinct quality values and the highest; Q 5', Q mid, Q 3': mean quality of the first 50 bases, the middle half and the last 50 bases.

| sample | reads | both% | rev% | median | mode | in10% | >1.5x% | EE med | EE/kb | <=EE2% | <=EE5% | <=EE10% | Qs | Qmax | Q 5' | Q mid | Q 3' |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SRR23380944 | 18,587 | 88 | 55 | 1456 | 1450 | 100 | 0.0 | 0.00 | 0.00 | 86 | 93 | 98 | 93 | 93 | 32 | 32 | 31 |
| SRR23381018 | 13,408 | 82 | 54 | 1453 | 1450 | 99 | 0.3 | 0.16 | 0.11 | 76 | 89 | 96 | 93 | 93 | 30 | 30 | 27 |

## What is unusual

- SRR23380944: only 88% of the reads have both primers
- SRR23380944: 55% of the reads with both primers are in the reverse orientation
- SRR23381018: only 82% of the reads have both primers
- SRR23381018: 54% of the reads with both primers are in the reverse orientation
