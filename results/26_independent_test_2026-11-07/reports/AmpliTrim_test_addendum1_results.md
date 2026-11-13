Nhan Thi Ho, Vinmec International Hospital and VinUniversity, Hanoi. 7 November 2026.

The addendum was posted publicly on AmpliTrim issue \#1 before the reads were opened \[1\]. The analysis was designed, scripted and run with Claude, an AI assistant, and reviewed by the investigator.

# Summary

- **The rule relaxed, so this time it was tested.** AmpliTrim raised maxEE to 3,3 in KFS and 3,2 in HDP (gate G1 met).

- **Relaxing kept more reads, as intended.** DADA2 merged 10.9 points more pairs than at maxEE 2 in KFS (95% CI 10.2 to 11.4, all 24 samples up) and 3.1 points more in HDP (2.5 to 3.6, 22 of 24 up). Both meet the 2-point margin of criterion C2, the primary test.

- **It did not change the community picture.** Genus profiles moved less than sampling noise (C4), no top-10 genus moved by more than 0.8 points (C5), diversity was unchanged (C6), and new ASVs held under 2% of reads (C7).

- **The expected loss of rare ASVs did not appear.** Hypothesis H1, that the rule's setting lowers ASV richness, was not supported. Richness rose by 3.4% in KFS and did not change in HDP. The larger setting maxEE 2,5 did lower richness again (by 10.7% and 7.7%), as it had in the Nigerian data.

- **The yield estimate failed badly in HDP.** It was 18 to 20 points too high, because DADA2 lost many pairs at merging. It was within 5 points in KFS.

- **The filter estimate and the stability check held again.** C1 was within 0.25 points in all six comparisons, and a second draw gave the same maxEE in both datasets (C8).

# Data and methods

Datasets were found by a seeded random screen of 1,387 eligible ENA studies, described in the addendum \[1\]. KFS is PRJDB8879, Korean adults in a fermented soybean paste trial \[2\]. HDP is PRJNA714241, hemodialysis patients \[3\]. Both are stool, 16S V3-V4 with primers 341F and 805R, MiSeq 2 x 300. The first 4,000,000 bytes of each read file were used, giving 17,491 to 23,081 complete pairs per sample. Cutadapt kept 95.7% to 97.2% of pairs per sample in KFS and 94.8% to 97.2% in HDP. All 24 samples per dataset passed every preparation gate.

Arms, software and criteria were as in the original protocol and its first report \[1\]. DADA2 learned error models for each of the four KFS flow cells. HDP's read headers carry no flow cell, so one model was learned for all its samples.

# Settings chosen by AmpliTrim

| **Arm**                                                   | **KFS**            | **HDP**            |
|-----------------------------------------------------------|--------------------|--------------------|
| R, recommended                                            | 248/192, maxEE 3,3 | 261/179, maxEE 3,2 |
| D, maxEE 2                                                | 247/193, maxEE 2   | 251/189, maxEE 2   |
| E, maxEE 2,5                                              | 220/220, maxEE 2,5 | 220/220, maxEE 2,5 |
| Expected errors at the maxEE 2 cut, 75th percentile (F/R) | 2.75 / 2.18        | 2.42 / 1.92        |
| Pairs passing at maxEE 2, AmpliTrim's estimate            | 60.4%              | 64.3%              |

# Results against the frozen criteria

| **Criterion**                                         | **KFS**                                  | **HDP**                                  |
|-------------------------------------------------------|------------------------------------------|------------------------------------------|
| G1 rule relaxes                                       | Met. maxEE 3,3                           | Met. maxEE 3,2                           |
| C1 filter estimate within 2 points                    | Met. +0.05 (R), -0.03 (D), +0.06 (E)     | Met. +0.22 (R), -0.03 (D), +0.24 (E)     |
| C2 R merges 2 points more than D (primary)            | Met. +10.9 (95% CI 10.2 to 11.4)         | Met. +3.1 (95% CI 2.5 to 3.6)            |
| C3 yield estimate within 5 points                     | Met. +3.2 (R), +4.3 (D), +4.2 (E)        | Not met. +20.0 (R), +18.5 (D), +19.9 (E) |
| C4 genus profile, R against D, within noise (primary) | Met. 0.022 against noise 0.055           | Met. 0.020 against noise 0.069           |
| C5 top 10 genera, R against D                         | Met. Largest 0.80 (Phocaeicola)          | Met. Largest 0.41 (unclassified)         |
| C6 diversity, R against D                             | Met. Shannon +0.03, richness +3.4%       | Met. Shannon +0.004, richness 0.0%       |
| C7 new ASVs and chimeras, R against D                 | Met. 0.4%, chimeras +0.5                 | Met. 1.5%, chimeras -0.3                 |
| C8 same setting on a second draw                      | Met. Total cut differs by 1 nt           | Met. Same total cut and maxEE            |
| H1 R gives lower richness than D                      | Not supported. +3.4% (95% CI 1.6 to 6.3) | Not supported. 0.0% (95% CI -1.7 to 1.6) |

Signed differences are AmpliTrim's estimate minus DADA2, in percentage points of the 120,000 input pairs per dataset.

# What the larger setting maxEE 2,5 did

| **E against D**          | **KFS**                                 | **HDP**                            |
|--------------------------|-----------------------------------------|------------------------------------|
| Pairs merged             | +11.2 points                            | +6.8 points                        |
| C4 genus profile         | Met. 0.046 against noise 0.055          | Met. 0.042 against noise 0.069     |
| C5 top 10 genera         | Not met. Prevotella 1.73 points         | Met. Largest 0.85                  |
| C6 diversity             | Not met. Shannon -0.07, richness -10.7% | Met. Shannon -0.08, richness -7.7% |
| C7 new ASVs and chimeras | Not met. 2.0% new, chimeras +1.3        | Not met. 2.7% new, chimeras +2.3   |

# What DADA2 kept

| **Dataset and arm** | **Passed filter** | **Denoised (F)** | **Merged** | **After chimeras** | **ASVs** |
|---------------------|-------------------|------------------|------------|--------------------|----------|
| KFS R               | 71.6%             | 69.5%            | 65.9%      | 63.9%              | 488      |
| KFS D               | 60.5%             | 58.7%            | 55.0%      | 53.7%              | 466      |
| KFS E               | 74.5%             | 73.1%            | 66.2%      | 63.7%              | 455      |
| KFS Db              | 60.2%             | 58.6%            | 54.8%      | 53.1%              | 459      |
| HDP R               | 69.0%             | 60.6%            | 47.9%      | 39.5%              | 600      |
| HDP D               | 64.4%             | 58.0%            | 44.9%      | 36.8%              | 605      |
| HDP E               | 74.9%             | 71.8%            | 51.7%      | 41.2%              | 589      |
| HDP Db              | 64.5%             | 57.8%            | 44.5%      | 36.5%              | 602      |

# Interpretation

This is the first independent evidence on the rule itself. On two datasets where the reads needed it, the rule raised maxEE by one step, DADA2 kept clearly more reads, and the community a user would report was unchanged within the limits measured here. The gain was large in KFS and modest in HDP, where the lower bound of the interval (2.5 points) sits just above the 2-point margin.

The concern raised by the first test was not borne out for the rule's own setting. A one-step relaxation (3,3 or 3,2) left richness unchanged or slightly higher. The larger, uneven setting maxEE 2,5 lowered richness in three of the four datasets now tested (NIG, KFS and HDP) and added more new ASVs and chimeras. That supports the rule's design of relaxing only as far as the reads need, and argues against relaxing the reverse read to 5 by habit. Arm E also changes truncation, so the two effects cannot be fully separated.

The yield estimate is now the main weakness. It has failed C3 in two of four datasets (NIG by 6 to 9 points, HDP by 18 to 20). In HDP the loss is at merging. About 58% of pairs survive denoising at maxEE 2 but only 45% merge. The chosen cuts leave an overlap of roughly 12 to 40 nt over amplicons of up to 428 nt, and DADA2 merged here with no mismatches allowed. AmpliTrim's estimate appears to count pairs that DADA2 then fails to merge. HDP also had a high chimera share (about 18% of merged reads) and reads of uneven length, which AmpliTrim flagged.

# Deviations and notes

- Expectation H1 was wrong. The other written expectations (G1, C1 and C2 met) held.

- Reads come from the first 4,000,000 bytes of each file, as stated in the addendum. They may not represent each run as a whole.

- Draw-to-draw richness differed by 2% to 4% at the same setting. The R against D comparison uses the same reads, so it is not affected by this noise. It is given only for scale.

- No other changes were made to the protocol or addendum.

# Limitations

- These samples have no known composition, so the test measures yield and agreement between settings, not accuracy.

- Two datasets with relaxation, each 24 samples of 5,000 pairs, cannot establish general validity. Both use the same primer pair and the same sequencer.

- The thresholds for C4 to C7 were set by the investigator without an external standard.

# Files

Scripts, settings, per-sample tables, DADA2 outputs and AmpliTrim's reports are in the folder results2, next to this report.

# References

1.  Ho NT. Independent test of AmpliTrim 0.2.0 on infant gut 16S data: protocol and addendum 1. AmpliTrim issue \#1, 7 November 2026. <https://github.com/paytonyau/amplitrim/issues/1>

2.  European Nucleotide Archive. Study PRJDB8879, response of gut microbial community to fermented soybean paste. <https://www.ebi.ac.uk/ena/browser/view/PRJDB8879>

3.  European Nucleotide Archive. Study PRJNA714241, hemodialysis patients. <https://www.ebi.ac.uk/ena/browser/view/PRJNA714241>
