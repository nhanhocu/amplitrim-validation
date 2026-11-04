# Long-read description of C:\data\longread\pacbio_kinnex16s\sq2_kinnex_fastq

3 files, 902,830 reads; 99.8% have both primers.
The primer at the 5' end of the read is found in 99.9% of the reads and the one at the 3' end in 99.9% (insertions and deletions in a primer count as errors, up to the allowed share).
Reads between the primers: 900,775; median of the file medians 1466 nt; share within 10% of the median 100.0%.
Quality (mean of the error probabilities, as Phred): first 50 bases Q28.5, middle half Q27.9, last 50 bases Q26.5; fewest distinct quality values in a file: 93, lowest maximum: Q93.

Columns: both% reads with both primers; rev% of those, in the reverse orientation; median, mode: length between the primers (mode = commonest 10 nt bin); in10%: share within 10% of the median; >1.5x%: share longer than 1.5 times the median; EE med, EE/kb: expected errors per read and per 1,000 nt (median); <=EEn%: share of reads at or under maxEE n; Qs, Qmax: distinct quality values and the highest; Q 5', Q mid, Q 3': mean quality of the first 50 bases, the middle half and the last 50 bases.

| sample | reads | both% | rev% | median | mode | in10% | >1.5x% | EE med | EE/kb | <=EE2% | <=EE5% | <=EE10% | Qs | Qmax | Q 5' | Q mid | Q 3' |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| m64004e_231003_184443.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 394,216 | 100 | 63 | 1474 | 1470 | 100 | 0.0 | 0.69 | 0.47 | 69 | 85 | 94 | 93 | 93 | 28 | 28 | 26 |
| m64004e_231003_184443.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 221,227 | 100 | 63 | 1466 | 1470 | 100 | 0.0 | 0.74 | 0.51 | 69 | 85 | 94 | 93 | 93 | 29 | 28 | 27 |
| m64004e_231003_184443.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 287,387 | 100 | 63 | 1466 | 1470 | 100 | 0.0 | 0.74 | 0.50 | 69 | 84 | 94 | 93 | 93 | 29 | 28 | 27 |

## What is unusual

- m64004e_231003_184443.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads: 63% of the reads with both primers are in the reverse orientation
- m64004e_231003_184443.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads: 63% of the reads with both primers are in the reverse orientation
- m64004e_231003_184443.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads: 63% of the reads with both primers are in the reverse orientation
