# Expected amplicons of the mock community, from the genomes

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

## What make_reference.py reported

```
105 sequences read; 105 cut between the primers (AGRGTTYGATYMTGGCTCAG / RGYTACCTTGTTACGACTT, at most 3 mismatches), 0 left out;
60 expected variants of 20 strains:
  Acinetobacter_baumannii_ATCC17978: 6 sequence(s) -> 1 distinct amplicon(s) of 1459 nt   [from NZ_CP053098.1_+_18217, NZ_CP053098.1_+_680529, NZ_CP053098.1_-_206938, ...]
  Bacillus_pacificus_ATCC10987: 12 sequence(s) -> 6 distinct amplicon(s) of 1473, 1474, 1474, 1473, 1473, 1473 nt   [from NC_003909.8_+_145500, NC_003909.8_+_279605, NC_003909.8_+_29088, ...]
  Bifidobacterium_adolescentis_ATCC15703: 5 sequence(s) -> 3 distinct amplicon(s) of 1452, 1449, 1454 nt   [from NC_008618.1_-_178185, NC_008618.1_-_27128, NC_008618.1_-_473195, ...]
  Cereibacter_sphaeroides_ATCC17029: 4 sequence(s) -> 1 distinct amplicon(s) of 1389 nt   [from NC_009049.1_+_87771, NC_009050.1_+_575902, NC_009050.1_+_611548, ...]
  Clostridium_beijerinckii_ATCC35702: 14 sequence(s) -> 14 distinct amplicon(s) of 1434, 1434, 1434, 1434, 1434, 1434, 1434, 1434, 1434, 1434, 1434, 1434, 1434, 1434 nt   [from NZ_CP006777.1_+_142452, NZ_CP006777.1_+_2031249, NZ_CP006777.1_+_2254709, ...]
  Cutibacterium_acnes_ATCC11828: 2 sequence(s) -> 1 distinct amplicon(s) of 1447 nt   [from NC_017550.1_+_1599937, NC_017550.1_-_2258456]
  Deinococcus_radiodurans_ATCCBAA-816: 3 sequence(s) -> 2 distinct amplicon(s) of 1424, 1424 nt   [from NZ_CP038663.1_+_84839, NZ_CP038663.1_-_179229, NZ_CP038663.1_-_359976]
  Enterococcus_faecalis_ATCC47077: 4 sequence(s) -> 2 distinct amplicon(s) of 1483, 1481 nt   [from NC_017316.1_+_213428, NC_017316.1_+_818921, NC_017316.1_-_424261, ...]
  Escherichia_coli_ATCC700926: 7 sequence(s) -> 6 distinct amplicon(s) of 1464, 1464, 1464, 1464, 1464, 1464 nt   [from NC_000913.3_+_223777, NC_000913.3_+_3941814, NC_000913.3_+_4035537, ...]
  Helicobacter_pylori_ATCC700392: 2 sequence(s) -> 2 distinct amplicon(s) of 1424, 1425 nt   [from NC_018939.1_-_155243, NC_018939.1_-_458802]
  Lactobacillus_gasseri_ATCC33323: 6 sequence(s) -> 1 distinct amplicon(s) of 1495 nt   [from NC_008530.1_+_477580, NC_008530.1_-_100599, NC_008530.1_-_106114, ...]
  Neisseria_meningitidis_ATCCBAA-335: 4 sequence(s) -> 1 distinct amplicon(s) of 1463 nt   [from NC_003112.2_+_307728, NC_003112.2_+_60978, NC_003112.2_-_134916, ...]
  Phocaeicola_vulgatus_ATCC8482: 7 sequence(s) -> 6 distinct amplicon(s) of 1450, 1450, 1450, 1450, 1450, 1450 nt   [from NC_009614.1_+_2095451, NC_009614.1_+_2183543, NC_009614.1_+_2587730, ...]
  Porphyromonas_gingivalis_ATCC33277: 4 sequence(s) -> 1 distinct amplicon(s) of 1454 nt   [from NC_010729.1_+_229317, NC_010729.1_+_2295559, NC_010729.1_+_477281, ...]
  Pseudomonas_paraeruginosa_ATCC9027: 1 sequence(s) -> 1 distinct amplicon(s) of 1458 nt   [from NZ_NIQD01000024.1_+_420]
  Schaalia_odontolytica_ATCC17982: 2 sequence(s) -> 1 distinct amplicon(s) of 1463 nt   [from NZ_DS264586.1_+_1312171, NZ_DS264586.1_-_617745]
  Staphylococcus_aureus_ATCCBAA-1556: 5 sequence(s) -> 3 distinct amplicon(s) of 1474, 1474, 1474 nt   [from NC_007793.1_+_512897, NC_007793.1_+_556528, NC_007793.1_-_575202, ...]
  Staphylococcus_epidermidis_ATCC12228: 5 sequence(s) -> 5 distinct amplicon(s) of 1473, 1473, 1473, 1473, 1473 nt   [from NC_004461.1_-_117161, NC_004461.1_-_161798, NC_004461.1_-_686133, ...]
  Streptococcus_agalactiae_ATCCBAA-611: 7 sequence(s) -> 1 distinct amplicon(s) of 1471 nt   [from NC_004116.1_+_16410, NC_004116.1_+_165247, NC_004116.1_+_22241, ...]
  Streptococcus_mutans_ATCC700610: 5 sequence(s) -> 2 distinct amplicon(s) of 1479, 1479 nt   [from NC_004350.2_+_16876, NC_004350.2_+_185748, NC_004350.2_-_154588, ...]
```
