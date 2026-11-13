Nhan Thi Ho, Vinmec International Hospital and VinUniversity, Hanoi. 7 November 2026.

The addendum was posted publicly on AmpliTrim issue \#1 before AmpliTrim or DADA2 was run on the simulated data \[1\]. The analysis was designed, scripted and run with Claude, an AI assistant, and reviewed by the investigator.

# Summary

- **The relaxed setting was at least as accurate as maxEE 2.** In both simulated arms AmpliTrim chose maxEE 3,3, and every truth criterion (T1 to T4) was met. With errors that match the quality scores, it was closer to the true community in 21 of 24 samples (median Bray-Curtis 0.059 against 0.069). With realistic, higher error rates, accuracy was the same within sampling noise.

- **It kept about 10 points more reads.** DADA2 merged 10.6 points more pairs in the ideal arm and 9.5 more in the realistic arm (C2 met in both).

- **The common habit of maxEE 2,5 was harmful under realistic errors.** It recovered 12.6 points fewer true sequences, put 3.7 points more reads into spurious ASVs and moved the profile further from the truth in 23 of 24 samples. This matches the richness loss seen with 2,5 in three of four real datasets.

- **Hypothesis H2 could not be confirmed.** Near-identical rare variants were hard for DADA2 under every setting (18% to 25% recovered with ideal errors, 2% to 3% with realistic errors). maxEE 2,5 recovered slightly more, not fewer.

- **AmpliTrim's estimates held in simulation.** The filter estimate was within 0.08 points (C1), the yield estimate within 4.1 points (C3), and the setting was the same on a second draw (C8).

# Design

The truth was built from real data: the 466 ASVs and 24 sample profiles of arm D in the Korean dataset of addendum 1 (PRJDB8879), with a long tail of rare sequences. Thirty abundant sequences each got a near-twin 1, 2 or 3 substitutions away at 10% of the parent's abundance, and 4% of reads were chimeras. Each sample had 10,000 read pairs, giving two draws of 5,000.

Both arms used real quality strings from the Korean reads, so read quality, read lengths and AmpliTrim's view of the data were the same as in real data. Only the errors differed. In SIM-I each base was wrong with exactly the probability its quality score states. In SIM-T, errors followed the rates DADA2 had learned from the same real runs, which are 3 to 20 times the nominal rate at high quality. Those learned rates also absorb PCR errors and fine biological variation, so SIM-T is a harsh scenario. A true sequence counted as recovered only on an exact match, and as present when it contributed at least 10 reads to a draw (a median of 45 per sample).

# Settings chosen by AmpliTrim

| **Arm**        | **SIM-I (ideal errors)** | **SIM-T (realistic errors)** |
|----------------|--------------------------|------------------------------|
| R, recommended | 243/198, maxEE 3,3       | 245/198, maxEE 3,3           |
| D, maxEE 2     | 246/193, maxEE 2         | 247/194, maxEE 2             |
| E, maxEE 2,5   | 222/219, maxEE 2,5       | 222/221, maxEE 2,5           |

# Accuracy against the truth

| **Arm**  | **Recall of true sequences** | **Distance to truth (Bray-Curtis)** | **Reads in spurious ASVs** | **Near-twins recovered** |
|----------|------------------------------|-------------------------------------|----------------------------|--------------------------|
| SIM-I R  | 96.9%                        | 0.059                               | 0.39%                      | 33 of 170                |
| SIM-I D  | 95.1%                        | 0.069                               | 0.41%                      | 30 of 170                |
| SIM-I E  | 92.9%                        | 0.068                               | 0.69%                      | 43 of 170                |
| SIM-I Db | 96.4%                        | 0.066                               | 0.28%                      | 32 of 170                |
| SIM-T R  | 57.3%                        | 0.217                               | 0.23%                      | 3 of 170                 |
| SIM-T D  | 55.5%                        | 0.205                               | 0.11%                      | 3 of 170                 |
| SIM-T E  | 44.5%                        | 0.280                               | 4.51%                      | 5 of 170                 |
| SIM-T Db | 57.9%                        | 0.231                               | 0.00%                      | 3 of 170                 |

Medians over 24 samples, except near-twins, which are pooled. Db is arm D on a second draw of reads and shows sampling noise.

# Results against the frozen criteria

| **Criterion, R against D**                   | **SIM-I**                                          | **SIM-T**                     |
|----------------------------------------------|----------------------------------------------------|-------------------------------|
| G1 rule relaxes                              | Met. maxEE 3,3                                     | Met. maxEE 3,3                |
| T1 recall at least -2 points                 | Met. +1.3 (95% CI 0.0 to 2.5)                      | Met. +0.6 (-1.8 to 2.5)       |
| T2 spurious reads at most +0.5 points        | Met. 0.0                                           | Met. 0.0                      |
| T3 distance to truth at most +0.01 (primary) | Met. -0.006 (-0.015 to -0.003), closer in 21 of 24 | Met. +0.001 (-0.009 to 0.029) |
| T4 near-twins at most 5 points fewer         | Met. +1.8 points pooled                            | Met. 0.0                      |
| C1 filter estimate within 2 points           | Met. Within 0.07                                   | Met. Within 0.08              |
| C2 R merges 2 points more                    | Met. +10.6 (10.3 to 10.8)                          | Met. +9.5 (8.8 to 10.1)       |
| C3 yield estimate within 5 points            | Met. Within 0.7                                    | Met. Within 4.1               |
| C8 same setting on a second draw             | Met                                                | Met                           |

| **E (maxEE 2,5) against D**    | **SIM-I**                           | **SIM-T**                                           |
|--------------------------------|-------------------------------------|-----------------------------------------------------|
| T1 recall                      | Not met. -2.4 (-3.8 to 0.0)         | Not met. -12.6 (-14.8 to -10.0)                     |
| T2 spurious reads              | Met. +0.4                           | Not met. +3.7 (2.4 to 5.1)                          |
| T3 distance to truth           | Met. -0.002                         | Not met. +0.082 (0.030 to 0.110), worse in 23 of 24 |
| H2 E recovers fewer near-twins | Not supported. 43 against 30 pooled | Not supported. 5 against 3 pooled                   |

# Interpretation

This is the first test of the rule against a known truth. Where the reads needed it, AmpliTrim relaxed maxEE by one step, DADA2 kept about 10 points more reads, and the result was no less accurate. With errors that behave as the quality scores say, it was slightly more accurate, probably because more reads gave DADA2 more evidence for rare sequences. With realistic errors the gain in reads did not change accuracy, so the extra reads cost nothing.

The comparison with maxEE 2,5 is the clearest result. Relaxing the reverse read to 5 by habit lets in reads whose errors DADA2 cannot fully correct when the true error rate is higher than the scores suggest. True sequences were lost and spurious ones appeared. That is the risk AmpliTrim's rule is designed to avoid by relaxing only as far as three quarters of reads need. Together with the real data, where 2,5 lowered richness in three of four datasets, it argues against using 2,5 as a default.

The near-twin test did not work as intended. At 10% of their parent's abundance, variants 1 to 3 bases away were mostly absorbed by DADA2 under every setting, so there was little room to see a difference. A future test should place twins at higher relative abundance.

AmpliTrim's yield estimate was accurate here, unlike in two real datasets. The simulation has no length variation from submitter trimming, no unusual chimera rates and no merge failures beyond read errors. That points to those real-data features as the cause of the overshoot seen in HDP and NIG.

# Deviations and notes

- Two bugs in the evaluation script were fixed after the first run, without changing any criterion. Chimera names that contain a near-twin's name were not read correctly. Also, 89 of 1,200 simulated chimeras were identical to a true sequence, and these were first counted as chimeras, which wrongly made surviving chimeras look like 18% to 25% of reads. They are now counted as the true sequence they reproduce, and surviving chimeras are 0.0% to 0.4%. No other result changed.

- Expectation H2 was wrong. The other written expectations (G1, C1 and C2 met, SIM-I no worse) held.

- DADA2 learned one error model per arm, as the addendum states.

# Limitations

- A simulation shows what happens when errors behave as modelled. It leaves out indels, PCR errors, contamination and other features of real runs. A real mock community with poor reads remains the stronger test.

- SIM-T uses error rates that include more than sequencing error, so DADA2's absolute accuracy there is pessimistic. Comparisons between settings are the point, not the absolute values.

- The truth sequences came from DADA2 output on real data, so they are realistic but are not independently verified organisms.

# Files

Simulation scripts, settings, per-sample truth tables and DADA2 outputs are in the folder results3, next to this report.

# References

1.  Ho NT. Independent test of AmpliTrim 0.2.0: protocol, addendum 1 and addendum 2. AmpliTrim issue \#1, 7 November 2026. <https://github.com/paytonyau/amplitrim/issues/1>
