# Independent test of AmpliTrim 0.2.0 on infant gut 16S data: protocol

Written on 6 November 2026, before any read file was downloaded. The 96 read files were then downloaded and checked against their MD5 sums on 6 November (finished 18:10 Vietnam time). They have not been opened or analysed, and AmpliTrim and DADA2 have not been run on them. Posted publicly on 7 November 2026, before any analysis.

Investigator: Nhan Thi Ho. Analysis assisted by Claude. The investigator is responsible for all analyses, contents.

## Question

Does AmpliTrim's maxEE rule hold on independent human gut data, and does the choice of setting change the community profile a user would report?

The AmpliTrim validation states that the rule has not been tested on independent data and that the effect of noisier reads on abundances in rich real communities was not measured. The one independent attempt so far (PRJNA933120) could not decide this, because the deposited Illumina reads had only two quality values.

## Datasets

Neither dataset was used in the design or validation of AmpliTrim, and neither has an AmpliTrim result yet.

| Label | Accession | Population | Region | Platform | Runs in archive |
|---|---|---|---|---|---|
| CBGS | PRJEB50418 | UK infants, Cambridge Baby Growth and Breastfeeding Study, stool | V3-V4 | MiSeq 2 x 300 | 380 (317 gut, 63 breast milk) |
| NIG | PRJEB31073 | Nigerian infants, stool | V1-V2 | MiSeq 2 x 300 | 169 |

## What was seen before freezing

For each dataset, the first 1,600 to 3,700 reads of one forward and one reverse file were inspected in the browser for read length, the number of distinct quality values (32 to 33 in all four files) and the first bases of the reads. Archive metadata was read for sample type and read counts. Nothing else was looked at.

## Sample selection (fixed rule)

1. Keep gut samples only (CBGS: sample title "human gut microbiome").
2. Keep runs with an archive read count of at least 10,000.
3. Sort by run accession, shuffle with a Fisher-Yates shuffle driven by a mulberry32 generator with seed 20261106, and take the first 24.

The chosen runs and their MD5 sums are in `manifest.tsv`. Any run with fewer than 5,000 pairs after primer removal is reported and dropped.

## Read preparation

- **Primers, CBGS.** Reads appear to start with 341F (`CCTACGGGNGGCWGCAG`) and with a reverse primer lacking its first three bases (`TACNVGGGTATCTAATCC`). Remove both with cutadapt 5.2, anchored at the 5' end, error rate 0.1, discarding pairs without both. If fewer than 90% of pairs carry both, stop and report before going further.
- **Primers, NIG.** Reads appear to start after the primers (custom sequencing primers). Count reads starting with 27F or the 338R primer. If at most 1% do, no trimming. If more do, trim as above and record it.
- **Thinning.** For each sample, draw two disjoint random sets of pairs with a fixed seed: draw a (5,000 pairs) and draw b (up to 5,000 of the remaining pairs).
- **Quality check.** At least 20 distinct quality values must be present in every file, otherwise the sample is reported and dropped.

## Arms

All arms use AmpliTrim 0.2.0 from PyPI with vsearch 2.32.0 and DADA2 1.38.0 in R, with `truncQ = 2`, `maxN = 0`, `minOverlap = 12`, `maxMismatch = 0`, per-sample inference and consensus chimera removal. Error models are learned per sequencing run if a dataset has more than one flow cell.

| Arm | Reads | Setting |
|---|---|---|
| R | draw a | AmpliTrim's released recommendation, truncation and maxEE |
| D | draw a | AmpliTrim's best truncation at maxEE 2 |
| E | draw a | AmpliTrim's best truncation at maxEE 2,5 |
| Db | draw b | The same truncation and maxEE as arm D. Used only to measure sampling noise |

AmpliTrim is also run on draw b with default settings, for the stability check. Genera are assigned with the RDP classifier 2.13 and its built-in training set at confidence 0.8, unclassified reads kept as their own group.

## Criteria, set before running

Margins C1 and C2 are the ones in the AmpliTrim register (P46 and P47). The others are set here.

| ID | Check | Met if |
|---|---|---|
| C1 | Filter estimate against DADA2, in arms R, D and E | AmpliTrim's estimated share passing is within 2 points of DADA2's |
| C2 | Benefit of the rule, only if the rule relaxes maxEE above 2 | DADA2 merges at least 2 points more of the pairs in R than in D. If the rule stays at 2, this does not apply and gives no evidence about the rule |
| C3 | Yield estimate against DADA2, in arms R, D and E | AmpliTrim's estimated yield is within 5 points of DADA2's merged share |
| C4 (primary) | Genus profile, R against D and E against D | Median per-sample Bray-Curtis dissimilarity is no larger than the median for D against Db (sampling noise) |
| C5 | Abundant genera, same comparisons | Mean absolute difference in relative abundance is at most 1 percentage point for each of the 10 most abundant genera |
| C6 | Diversity, same comparisons | Median paired difference in ASV-level Shannon index is at most 0.10 in size, and in ASV richness rarefied to a common depth is at most 10% |
| C7 | New ASVs, same comparisons | ASVs absent from D hold at most 2% of the reads of the relaxed arm, and the share of merged reads removed as chimeras rises by at most 2 points |
| C8 | Stability, draw a against draw b | Total truncation differs by at most 10 nt and the maxEE is the same |

Per-sample differences are reported with a bootstrap 95% interval over samples (10,000 resamples, seed 1). If R and D are the same setting, the comparisons of R against D are not applicable and E against D is still reported.

## Expectations, written before running

- C1 met on both datasets. The AmpliTrim estimate was within 0.8 points on its 12 earlier datasets.
- C3 is uncertain. The yield estimate has overshot by more than 20 points on diverse real samples.
- The reverse reads of both datasets fall to about Q10 to Q13 by base 300, so the rule may relax maxEE at least in NIG. No direction is predicted for C4.

## How results will be read

- All results are reported whichever way they go, including any criterion not met and any change from this protocol.
- There is no known truth in these samples, so this test measures yield and agreement between settings, not accuracy. Agreement does not show that a setting is correct.
- Two datasets are two independent observations. They cannot show that the rule is valid in general.
- Results do not lead to any change in the released package without a separate decision by its author.
