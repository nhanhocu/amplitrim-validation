# Filter agreement: AmpliTrim's estimate against DADA2's filterAndTrim

Folder C:\data\longread\pacbio_kinnex16s\revio_monomer_fastq; forward primer AGRGTTYGATYMTGGCTCAG, reverse primer RGYTACCTTGTTACGACTT; 3 file(s), 150,000 reads (the first 50,000 of each file); tolerance 2 points.

**Gate (L4): MET.** The largest difference is 0.11 points (m84198_231017_000448_s1.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads, maxEE 2); the gate is 2 points for every maxEE in every file.

The estimate is the share of the reads with both primers that are at or under maxEE, counted between the primers (longread_describe.py). DADA2's figure is the share of the reads left after cutadapt removed both primers (insertions and deletions allowed) that filterAndTrim keeps with only maxEE acting.

| sample | maxEE | estimate % | DADA2 % | difference (points) | within |
|---|---|---|---|---|---|
| m84198_231017_000448_s1.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 1 | 78.1 | 78.1 | -0.07 | yes |
| m84198_231017_000448_s1.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 2 | 83.4 | 83.3 | -0.07 | yes |
| m84198_231017_000448_s1.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 3 | 86.3 | 86.2 | -0.07 | yes |
| m84198_231017_000448_s1.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 5 | 89.7 | 89.6 | -0.06 | yes |
| m84198_231017_000448_s1.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 10 | 93.9 | 93.9 | -0.05 | yes |
| m84198_231017_000448_s1.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 1 | 77.1 | 77.0 | -0.10 | yes |
| m84198_231017_000448_s1.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 2 | 82.5 | 82.4 | -0.11 | yes |
| m84198_231017_000448_s1.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 3 | 85.5 | 85.4 | -0.09 | yes |
| m84198_231017_000448_s1.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 5 | 88.9 | 88.8 | -0.09 | yes |
| m84198_231017_000448_s1.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 10 | 93.3 | 93.3 | -0.08 | yes |
| m84198_231017_000448_s1.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 1 | 77.4 | 77.4 | -0.07 | yes |
| m84198_231017_000448_s1.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 2 | 82.6 | 82.5 | -0.05 | yes |
| m84198_231017_000448_s1.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 3 | 85.5 | 85.5 | -0.05 | yes |
| m84198_231017_000448_s1.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 5 | 89.2 | 89.1 | -0.04 | yes |
| m84198_231017_000448_s1.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 10 | 93.6 | 93.6 | -0.04 | yes |

## Reads that survive the primer step (description only, no gate)

| sample | reads | estimate's search % | cutadapt, indels allowed % | cutadapt, no indels, 2 mismatches % | DADA2 removePrimers % |
|---|---|---|---|---|---|
| m84198_231017_000448_s1.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 50,000 | 99.5 | 99.9 | 91.8 | 89.6 |
| m84198_231017_000448_s1.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 50,000 | 99.4 | 99.9 | 90.4 | 88.6 |
| m84198_231017_000448_s1.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 50,000 | 99.6 | 99.9 | 90.9 | 89.4 |

If the gate is not met, look first at the primer table: a gap between the estimate's search and cutadapt means the two do not find the same reads, and a gap in the filter alone means the primer boundaries differ. Nothing else is changed until the cause is known.
