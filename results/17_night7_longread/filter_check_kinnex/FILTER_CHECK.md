# Filter agreement: AmpliTrim's estimate against DADA2's filterAndTrim

Folder C:\data\longread\pacbio_kinnex16s\sq2_kinnex_fastq; forward primer AGRGTTYGATYMTGGCTCAG, reverse primer RGYTACCTTGTTACGACTT; 3 file(s), 150,000 reads (the first 50,000 of each file); tolerance 2 points.

**Gate (L4): MET.** The largest difference is 0.08 points (m64004e_231003_184443.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads, maxEE 3); the gate is 2 points for every maxEE in every file.

The estimate is the share of the reads with both primers that are at or under maxEE, counted between the primers (longread_describe.py). DADA2's figure is the share of the reads left after cutadapt removed both primers (insertions and deletions allowed) that filterAndTrim keeps with only maxEE acting.

| sample | maxEE | estimate % | DADA2 % | difference (points) | within |
|---|---|---|---|---|---|
| m64004e_231003_184443.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 1 | 58.8 | 58.7 | -0.05 | yes |
| m64004e_231003_184443.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 2 | 71.1 | 71.0 | -0.05 | yes |
| m64004e_231003_184443.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 3 | 77.6 | 77.6 | -0.05 | yes |
| m64004e_231003_184443.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 5 | 85.8 | 85.8 | -0.05 | yes |
| m64004e_231003_184443.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 10 | 94.5 | 94.5 | -0.03 | yes |
| m64004e_231003_184443.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 1 | 57.3 | 57.2 | -0.07 | yes |
| m64004e_231003_184443.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 2 | 69.9 | 69.8 | -0.08 | yes |
| m64004e_231003_184443.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 3 | 76.8 | 76.7 | -0.08 | yes |
| m64004e_231003_184443.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 5 | 85.4 | 85.3 | -0.07 | yes |
| m64004e_231003_184443.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 10 | 94.5 | 94.4 | -0.05 | yes |
| m64004e_231003_184443.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 1 | 57.6 | 57.5 | -0.04 | yes |
| m64004e_231003_184443.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 2 | 70.0 | 69.9 | -0.05 | yes |
| m64004e_231003_184443.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 3 | 76.7 | 76.7 | -0.05 | yes |
| m64004e_231003_184443.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 5 | 85.2 | 85.2 | -0.04 | yes |
| m64004e_231003_184443.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 10 | 94.6 | 94.6 | -0.02 | yes |

## Reads that survive the primer step (description only, no gate)

| sample | reads | estimate's search % | cutadapt, indels allowed % | cutadapt, no indels, 2 mismatches % | DADA2 removePrimers % |
|---|---|---|---|---|---|
| m64004e_231003_184443.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 50,000 | 99.8 | 100.0 | 96.3 | 94.8 |
| m64004e_231003_184443.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 50,000 | 99.8 | 100.0 | 96.2 | 95.0 |
| m64004e_231003_184443.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 50,000 | 99.8 | 100.0 | 96.3 | 95.2 |

If the gate is not met, look first at the primer table: a gap between the estimate's search and cutadapt means the two do not find the same reads, and a gap in the filter alone means the primer boundaries differ. Nothing else is changed until the cause is known.
