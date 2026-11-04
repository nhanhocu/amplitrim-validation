# Filter agreement: AmpliTrim's estimate against DADA2's filterAndTrim

Folder C:\data\runs\17_night7_longread\l4_monomer_input; forward primer AGRGTTYGATYMTGGCTCAG, reverse primer RGYTACCTTGTTACGACTT; 3 file(s), 101,354 reads; tolerance 2 points.

**Gate (L4): MET.** The largest difference is 0.14 points (m64004e_231016_235852.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads, maxEE 2); the gate is 2 points for every maxEE in every file.

The estimate is the share of the reads with both primers that are at or under maxEE, counted between the primers (longread_describe.py). DADA2's figure is the share of the reads left after cutadapt removed both primers (insertions and deletions allowed) that filterAndTrim keeps with only maxEE acting.

| sample | maxEE | estimate % | DADA2 % | difference (points) | within |
|---|---|---|---|---|---|
| m64004e_231016_235852.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 1 | 76.5 | 76.4 | -0.12 | yes |
| m64004e_231016_235852.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 2 | 82.6 | 82.5 | -0.11 | yes |
| m64004e_231016_235852.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 3 | 86.2 | 86.1 | -0.11 | yes |
| m64004e_231016_235852.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 5 | 90.7 | 90.6 | -0.10 | yes |
| m64004e_231016_235852.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 10 | 96.7 | 96.7 | -0.04 | yes |
| m64004e_231016_235852.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 1 | 76.3 | 76.2 | -0.09 | yes |
| m64004e_231016_235852.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 2 | 82.8 | 82.7 | -0.11 | yes |
| m64004e_231016_235852.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 3 | 86.4 | 86.3 | -0.10 | yes |
| m64004e_231016_235852.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 5 | 90.8 | 90.7 | -0.10 | yes |
| m64004e_231016_235852.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 10 | 96.8 | 96.8 | -0.01 | yes |
| m64004e_231016_235852.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 1 | 76.7 | 76.6 | -0.13 | yes |
| m64004e_231016_235852.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 2 | 83.0 | 82.9 | -0.14 | yes |
| m64004e_231016_235852.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 3 | 86.6 | 86.4 | -0.12 | yes |
| m64004e_231016_235852.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 5 | 90.9 | 90.8 | -0.11 | yes |
| m64004e_231016_235852.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 10 | 96.6 | 96.6 | -0.05 | yes |

## Reads that survive the primer step (description only, no gate)

| sample | reads | estimate's search % | cutadapt, indels allowed % | cutadapt, no indels, 2 mismatches % | DADA2 removePrimers % |
|---|---|---|---|---|---|
| m64004e_231016_235852.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads | 44,558 | 99.1 | 99.9 | 89.6 | 84.9 |
| m64004e_231016_235852.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads | 24,730 | 99.0 | 99.8 | 87.6 | 83.7 |
| m64004e_231016_235852.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads | 32,066 | 99.0 | 99.9 | 88.9 | 85.1 |

If the gate is not met, look first at the primer table: a gap between the estimate's search and cutadapt means the two do not find the same reads, and a gap in the filter alone means the primer boundaries differ. Nothing else is changed until the cause is known.
