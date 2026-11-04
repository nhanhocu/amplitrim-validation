# Night 7: long-read checks on the PacBio Kinnex-16S data of ATCC MSA-1003

Run on 2026-10-15; folder C:\data\runs\17_night7_longread. Gates and predictions: FUTURE.md of the archive (written before the run). Tools: Python 3.12.15; numpy 2.5.3; cutadapt 5.2; R and DADA2 R version 4.6.1 (2026-06-24 ucrt) | DADA2 1.40.0.

## Steps

- genomes: done in 1 min (20 genomes in C:\data\longread\pacbio_kinnex16s\ref\genomes (20 downloaded, 0 already there))
- amplicons: done in 1 min (20 of 20 genomes give an amplicon, 60 expected variants; 2 thing(s) to check in C:\data\runs\17_night7_longread\genome_amplicons\EXPECTED_AMPLICONS.md)
- filter_monomer: done in 7 min (gate L4 MET (largest difference 0.14 points))
- filter_kinnex: done in 11 min (gate L4 MET (largest difference 0.08 points))

## L4, filter agreement: Monomer files (Sequel II, three barcode pairs)

**Gate (L4): MET.** The largest difference is 0.14 points (m64004e_231016_235852.Kinnex16S_Fwd_09--Kinnex16S_Rev_29.hifi_reads, maxEE 2); the gate is 2 points for every maxEE in every file.

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

## L4, filter agreement: Kinnex files (Sequel II, three barcode pairs, the first reads of each)

**Gate (L4): MET.** The largest difference is 0.08 points (m64004e_231003_184443.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads, maxEE 3); the gate is 2 points for every maxEE in every file.

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

## Expected amplicons of the 20 strains

Primers AGRGTTYGATYMTGGCTCAG and RGYTACCTTGTTACGACTT, at most 3 mismatches each, between 1,000 and 2,000 nt between the primers; 20 genome(s), 20 with at least one amplicon, 60 expected variants from 105 copies of the gene.

The expected read share is the strain's share of genomic DNA times its number of copies of the gene, as a share of the total over all strains; the last column is that share of 30,000 reads.

| strain | tier | genome (sequences) | copies | variants | length (nt) | primer mismatches (5', 3') | genomic share % | expected read share % | reads per 30,000 |
|---|---|---|---|---|---|---|---|---|---|
| Escherichia_coli_ATCC700926 | A (designation to confirm) | 4,641,652 (1) | 7 | 6 | 1464 | 0, 0 | 18 | 24.036 | 7210.7 |
| Staphylococcus_epidermidis_ATCC12228 | A | 2,564,615 (7) | 5 | 5 | 1473 | 0, 0 | 18 | 17.168 | 5150.5 |
| Streptococcus_mutans_ATCC700610 | A (designation to confirm) | 2,032,925 (1) | 5 | 2 | 1479 | 0, 0 | 18 | 17.168 | 5150.5 |
| Cereibacter_sphaeroides_ATCC17029 | A | 4,489,380 (3) | 4 | 1 | 1389 | 0, 0 | 18 | 13.735 | 4120.4 |
| Porphyromonas_gingivalis_ATCC33277 | A | 2,354,886 (1) | 4 | 1 | 1454 | 0, 0 | 18 | 13.735 | 4120.4 |
| Clostridium_beijerinckii_ATCC35702 | A | 5,999,050 (1) | 14 | 14 | 1434 | 0, 0 | 1.8 | 4.807 | 1442.1 |
| Bacillus_pacificus_ATCC10987 | A | 5,432,652 (2) | 12 | 6 | 1473-1474 | 0, 0 | 1.8 | 4.120 | 1236.1 |
| Streptococcus_agalactiae_ATCCBAA-611 | A (designation to confirm) | 2,160,267 (1) | 7 | 1 | 1471 | 0, 0 | 1.8 | 2.404 | 721.1 |
| Staphylococcus_aureus_ATCCBAA-1556 | A | 2,917,469 (4) | 5 | 3 | 1474 | 0, 0 | 1.8 | 1.717 | 515.1 |
| Pseudomonas_paraeruginosa_ATCC9027 | A (draft) | 6,350,027 (56) | 1 | 1 | 1458 | 0, 0 | 1.8 | 0.343 | 103.0 |
| Acinetobacter_baumannii_ATCC17978 | A | 4,030,054 (3) | 6 | 1 | 1459 | 0, 0 | 0.18 | 0.206 | 61.8 |
| Lactobacillus_gasseri_ATCC33323 | A | 1,894,360 (1) | 6 | 1 | 1495 | 0, 0 | 0.18 | 0.206 | 61.8 |
| Neisseria_meningitidis_ATCCBAA-335 | A (designation to confirm) | 2,272,360 (1) | 4 | 1 | 1463 | 0, 0 | 0.18 | 0.137 | 41.2 |
| Cutibacterium_acnes_ATCC11828 | A | 2,488,626 (1) | 2 | 1 | 1447 | 0, 0 | 0.18 | 0.069 | 20.6 |
| Helicobacter_pylori_ATCC700392 | A (designation to confirm) | 1,667,892 (1) | 2 | 2 | 1424-1425 | 0, 0 | 0.18 | 0.069 | 20.6 |
| Phocaeicola_vulgatus_ATCC8482 | A | 5,163,189 (1) | 7 | 6 | 1450 | 1, 0 | 0.02 | 0.027 | 8.0 |
| Bifidobacterium_adolescentis_ATCC15703 | A | 2,089,645 (1) | 5 | 3 | 1449-1454 | 0, 0 | 0.02 | 0.019 | 5.7 |
| Enterococcus_faecalis_ATCC47077 | A (designation to confirm) | 2,739,625 (1) | 4 | 2 | 1481-1483 | 0, 0 | 0.02 | 0.015 | 4.6 |
| Deinococcus_radiodurans_ATCCBAA-816 | B | 3,279,598 (4) | 3 | 2 | 1424 | 0, 0 | 0.02 | 0.011 | 3.4 |
| Schaalia_odontolytica_ATCC17982 | A (draft) | 2,393,958 (2) | 2 | 1 | 1463 | 0, 0 | 0.02 | 0.008 | 2.3 |

## To check

- Pseudomonas_paraeruginosa_ATCC9027: a draft genome; copies of the rRNA operon may be collapsed, so its copy number and its expected read share are uncertain
- Schaalia_odontolytica_ATCC17982: a draft genome; copies of the rRNA operon may be collapsed, so its copy number and its expected read share are uncertain


## Send back

- this file (C:\data\runs\17_night7_longread\NIGHT7_SUMMARY.md)
- C:\data\runs\17_night7_longread\filter_check_monomer\FILTER_CHECK.md and C:\data\runs\17_night7_longread\filter_check_kinnex\FILTER_CHECK.md
- C:\data\runs\17_night7_longread\genome_amplicons\EXPECTED_AMPLICONS.md
- C:\data\runs\17_night7_longread\night7.log if a step failed
