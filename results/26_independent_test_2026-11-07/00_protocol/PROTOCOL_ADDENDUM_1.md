# Addendum 1: testing the maxEE relaxation on datasets with poorer reads

Written on 7 November 2026, before any read file of these datasets was downloaded beyond the small slices used for screening (described below). AmpliTrim and DADA2 have not been run on them.

Investigator: Nhan Thi Ho. Analysis assisted by Claude, which wrote this addendum, the screening code and the scripts. The investigator is responsible for all analyses and contents.

## Why

In the first test (issue #1), AmpliTrim kept maxEE at 2 on both infant datasets, so criterion C2 could not be assessed. This addendum looks for human gut 16S datasets where the rule should relax, and tests it there. Everything in the original protocol applies unless changed below.

## How the datasets were found

1. ENA was searched for read runs of human gut metagenome (taxon 408170), Illumina MiSeq, amplicon, paired. That returned 422,383 runs in 2,302 studies.
2. Eligible studies had at least 30 runs with 10,000 or more reads, a typical 2 x 250 or 2 x 300 read length (480 to 602 bases per spot), and were not used in AmpliTrim's validation or in issue #1. That left 1,387 studies.
3. The studies were sorted by accession and shuffled with a mulberry32 generator, seed 20261107. They were screened in that order, one run each, using the first 250 kB of each read file.
4. For each run, the screen measured the number of distinct quality values, estimated insert lengths from read overlap, set the total cut to the 99.5th percentile insert plus 12, found the split with the most pairs passing maxEE 2, and took the 75th percentile of expected errors in each read there. This mimics AmpliTrim's rule. On the two datasets of issue #1 it gave lower values than AmpliTrim's own measure (0.9 against 1.5 in NIG), so it is conservative.
5. The first two studies in that order with at least 20 distinct quality values, 16S rRNA gene amplicons and a screen value of 2 or more in either read were selected. One earlier hit (PRJNA703732, rank 29) was a fungal ITS study and was excluded, since AmpliTrim's rule does not apply to ITS.

The full screening log is in `screening_log.tsv`. Two studies were screened in parallel after the stop and are listed but played no part in the choice.

## Datasets

| Label | Accession | Population | Region and primers | Screen at maxEE 2 (pass, p75 F/R) | Eligible runs |
|---|---|---|---|---|---|
| KFS | PRJDB8879 | Korean adults, fermented soybean paste trial, stool | V3-V4, 341F / 805R | 60.3%, 2.83 / 2.17 | 96 |
| HDP | PRJNA714241 | Hemodialysis patients, stool | V3-V4, 341F / 805R | 64.2%, 2.93 / 1.87 | 39 |

Both are MiSeq 2 x 300 with primers in the reads.

## Sample selection

As in the original protocol, with seed 20261107: MiSeq paired runs with an archive read count of at least 10,000, sorted by run accession, shuffled, first 24 taken. The runs are listed in `manifest2.tsv`.

## Changes to read preparation

- **Partial files.** The full files are about 0.8 GB (KFS) and 2.6 GB (HDP) for 24 samples, too large for the available connection. Only the first 4,000,000 bytes of each compressed file are downloaded. Incomplete trailing records are dropped, and pairs are kept only where forward and reverse read names match. These reads come from the start of each run, which is usually the first tile or tiles of the flow cell, and may differ in quality from the run as a whole. The screen used the same part of the files. MD5 sums cannot be checked on partial files, so the byte count is checked instead.
- **Primers.** Remove 341F (`CCTACGGGNGGCWGCAG`) and 805R (`GACTACHVGGGTATCTAATCC`) with cutadapt 5.2, anchored at the 5' end, error rate 0.1, discarding pairs without both. If fewer than 90% of pairs are kept in a dataset, stop and report.
- **Minimum reads.** A sample needs at least 10,000 pairs after primer removal (two draws of 5,000). Samples below that are reported and dropped. If fewer than 16 samples remain in a dataset, stop and report.

## New gate

- **G1.** The rule must relax in arm R on draw a (recommended maxEE above 2 in at least one read). If it does not, the dataset is reported and C2 and the R against D comparisons do not apply.

## Arms and criteria

Arms R, D, E and Db and criteria C1 to C8 are unchanged. In these datasets R and D should differ, so the comparisons of R against D apply.

- **Primary:** C2 (DADA2 merges at least 2 points more pairs in R than in D) and C4 for R against D (median genus Bray-Curtis no larger than D against Db).
- **H1, new and directional:** in the first test, maxEE 2,5 lowered rarefied ASV richness by 10.2% in NIG. Hypothesis: arm R gives lower rarefied ASV richness than arm D. Supported if the median paired difference is below 0 and its bootstrap 95% interval excludes 0. This is reported alongside C6, which keeps its original thresholds.

## Expectations, written before running

- G1 met in both datasets.
- C1 met in both.
- C2 met in both. Only 60% to 64% of pairs passed maxEE 2 in the screen, so relaxing should keep clearly more.
- C3 uncertain.
- H1 supported in at least one dataset.
- No direction predicted for C4.

## How results will be read

As in the original protocol. All results are reported, including any criterion not met. These samples have no known composition, so the test measures yield and agreement between settings, not accuracy.
