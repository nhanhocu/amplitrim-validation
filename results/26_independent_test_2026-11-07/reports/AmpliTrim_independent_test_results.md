Nhan Thi Ho, Vinmec International Hospital and VinUniversity, Hanoi. 7 November 2026.

The protocol was posted publicly as AmpliTrim issue \#1 before any analysis \[1\]. The analysis was designed, scripted and run with Claude, an AI assistant, and reviewed by the investigator.

# Summary

- **The rule was not put to the test.** On both datasets AmpliTrim kept maxEE at 2, because the expected errors at the chosen cut were well below 2. The benefit of relaxing maxEE (criterion C2) therefore could not be assessed, and this test gives no evidence for or against it.

- **The filter estimate was accurate.** AmpliTrim predicted the share of pairs passing DADA2's filter to within 0.12 points in all six comparisons (C1).

- **The yield estimate was accurate for V3-V4 but not for V1-V2.** It was within 1 point in the UK data and 6 to 9 points too high in the Nigerian data (C3).

- **The recommendation was stable.** Two independent draws of 5,000 pairs per sample gave identical settings in both datasets (C8).

- **Relaxing maxEE to 2,5 would have kept more reads but cost rare ASVs in one dataset.** Genus profiles stayed within sampling noise in both datasets. In the Nigerian data, however, rarefied ASV richness fell by a median of 10.2% (C6, threshold 10%). That supports keeping maxEE at 2 unless the reads need it.

# Data and methods

Two public infant stool datasets were used, neither of them used in AmpliTrim's design or validation \[2\]. CBGS is PRJEB50418, UK infants, 16S V3-V4 \[3\]. NIG is PRJEB31073, Nigerian infants, 16S V1-V2 \[4\]. Both were sequenced on Illumina MiSeq 2 x 300 and keep full quality scores. 24 stool samples per dataset were chosen at random by the fixed rule in the protocol.

CBGS primers were removed with cutadapt, which kept 95.0% to 96.2% of pairs per sample. NIG reads carry no primers. Each sample was split into two disjoint random draws of 5,000 pairs. AmpliTrim 0.2.0 \[5\] chose the settings, and DADA2 1.38.0 \[6\] was run for four arms: R (AmpliTrim's recommendation), D (best truncation at maxEE 2), E (best truncation at maxEE 2,5) and Db (arm D on the second draw, to measure sampling noise). Genera were assigned with the RDP classifier 2.13 at confidence 0.8 \[7\]. CBGS was sequenced on three flow cells, so DADA2 learned error models separately for each.

# Settings chosen by AmpliTrim

| **Arm**                                       | **NIG (V1-V2)**    | **CBGS (V3-V4)**   | **Note**                  |
|-----------------------------------------------|--------------------|--------------------|---------------------------|
| R, recommended                                | 207/231, maxEE 2   | 217/222, maxEE 2   | Identical to D in both    |
| D, maxEE 2                                    | 207/231, maxEE 2   | 217/222, maxEE 2   |                           |
| E, maxEE 2,5                                  | 180/258, maxEE 2,5 | 179/260, maxEE 2,5 | Truncation also changes   |
| Expected errors at cut, 75th percentile (F/R) | 1.52 / 1.17        | 0.11 / 0.25        | Below 2, so no relaxation |

# Results against the frozen criteria

| **Criterion**                                                    | **NIG (V1-V2)**                                                | **CBGS (V3-V4)**                    |
|------------------------------------------------------------------|----------------------------------------------------------------|-------------------------------------|
| C1 filter estimate within 2 points                               | Met. +0.08 (R, D), -0.03 (E)                                   | Met. -0.12 (R, D), 0.00 (E)         |
| C2 relaxed rule merges 2 points more                             | Not applicable, rule kept maxEE 2                              | Not applicable, rule kept maxEE 2   |
| C3 yield estimate within 5 points                                | Not met. +6.1 (R, D), +9.0 (E)                                 | Met. +1.0 (R, D), +0.4 (E)          |
| C4 genus profile, E against D, within noise (median Bray-Curtis) | Met. 0.026 against noise 0.032                                 | Met. 0.003 against noise 0.013      |
| C5 top 10 genera, mean difference at most 1 point                | Met. Largest 0.94 (Bifidobacterium)                            | Met. Largest 0.25 (Bifidobacterium) |
| C6 Shannon at most 0.10, richness at most 10%                    | Not met. Shannon -0.04, richness -10.2% (95% CI -14.3 to -6.3) | Met. Shannon +0.006, richness 0.0%  |
| C7 new ASVs at most 2% of reads, chimeras up at most 2 points    | Met. 1.4%, chimeras -0.18                                      | Met. 0.5%, chimeras -0.22           |
| C8 same setting on a second draw                                 | Met. Identical                                                 | Met. Identical                      |

Comparisons of R against D do not apply, because the two settings were identical. Signed differences are AmpliTrim's estimate minus DADA2, in percentage points of the 120,000 input pairs per dataset.

# What DADA2 kept

| **Dataset and arm** | **Passed filter** | **Merged** | **After chimeras** | **ASVs** |
|---------------------|-------------------|------------|--------------------|----------|
| NIG D               | 75.9%             | 69.7%      | 69.5%              | 364      |
| NIG E               | 86.5%             | 76.5%      | 76.3%              | 327      |
| NIG Db              | 75.7%             | 69.8%      | 69.4%              | 350      |
| CBGS D              | 87.9%             | 86.6%      | 85.7%              | 191      |
| CBGS E              | 91.4%             | 90.2%      | 89.5%              | 202      |
| CBGS Db             | 88.0%             | 86.8%      | 85.9%              | 183      |

Per sample, arm E merged a mean of 6.7 points more pairs than D in NIG (95% CI 5.8 to 7.6) and 3.6 points more in CBGS (3.1 to 4.0).

# Interpretation

The main question, whether relaxing maxEE helps on independent data, remains open. Both datasets have good 2 x 300 reads at the cut AmpliTrim chose, so the rule correctly stayed at 2. To test the relaxation itself, a dataset is needed where the 75th percentile of expected errors at the cut is above 2, for example older MiSeq runs with poor reverse reads.

Arm E shows what a user would get by relaxing maxEE anyway. More reads survive and the genus-level picture does not change. In the Nigerian data, though, each sample had a mean of 3.3 fewer ASVs after rarefaction (27.8 to 24.5). Two draws at the same setting differed by only 0.9%, so this is not sampling noise, and it held across four rarefaction seeds. The 81 ASVs lost held 2.4% of reads in arm D and were spread across many genera. One possible explanation, not tested here, is that noisier reads raise DADA2's estimated error rates so that rare variants are merged into abundant ones. Because arm E also changes the truncation, the two effects cannot be separated. This is a first measurement of the effect that the AmpliTrim validation lists as unmeasured \[2\], and it argues for caution before relaxing.

The yield overshoot in V1-V2 comes from pairs that pass the filter but are lost in denoising and merging (75.9% passing, 69.7% merged). AmpliTrim's own report for this dataset warned that only 41% of pairs merged at full read length and suggested amplicons longer than about 590 nt. The longest merged amplicon was 426 nt, so the wording of that warning may be worth checking for short amplicons.

# Deviations and notes

- Only 54% of CBGS reverse reads matched the primer letter for letter, while cutadapt, which allows a few mismatches as the protocol specifies, found it in at least 95%. The gate was defined on the cutadapt result. Trimmed reads start with ordinary 16S sequence.

- The archive's read count field counts both reads of a pair in CBGS and pairs in NIG. Every selected sample had at least 10,000 pairs, so the selection was not affected.

- The expectation that the rule might relax in NIG was wrong.

- No other changes were made to the protocol.

# Limitations

- These samples have no known composition, so the test measures yield and agreement between settings, not accuracy.

- Two datasets of 24 samples and 5,000 pairs each cannot establish general validity.

- The thresholds for C4 to C7 were set by the investigator without an external standard. The richness result of 10.2% sits just past its 10% threshold.

# Files

Scripts, settings, per-sample tables, DADA2 outputs and AmpliTrim's own reports are in the folder results, next to this report. The protocol is in PROTOCOL.md.

# References

1.  Ho NT. Independent test of AmpliTrim 0.2.0 on infant gut 16S data: protocol. AmpliTrim issue \#1, 7 November 2026. <https://github.com/paytonyau/amplitrim/issues/1>

2.  Yau P. AmpliTrim validation archive. <https://github.com/paytonyau/amplitrim-validation>

3.  European Nucleotide Archive. Study PRJEB50418, fecal and breast milk microbiome of 93 infants. <https://www.ebi.ac.uk/ena/browser/view/PRJEB50418>

4.  European Nucleotide Archive. Study PRJEB31073, gut microbiota of Nigerian children over 12 months. <https://www.ebi.ac.uk/ena/browser/view/PRJEB31073>

5.  Yau P. AmpliTrim, version 0.2.0. <https://github.com/paytonyau/amplitrim>

6.  Callahan BJ, McMurdie PJ, Rosen MJ, Han AW, Johnson AJA, Holmes SP. DADA2: high-resolution sample inference from Illumina amplicon data. Nat Methods. 2016, 13, 581-583.

7.  Wang Q, Garrity GM, Tiedje JM, Cole JR. Naive Bayesian classifier for rapid assignment of rRNA sequences into the new bacterial taxonomy. Appl Environ Microbiol. 2007, 73, 5261-5267.
