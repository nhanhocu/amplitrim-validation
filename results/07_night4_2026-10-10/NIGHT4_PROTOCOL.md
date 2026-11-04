# Night 4b protocol (written 2026-10-10 01:46, before any analysis)

Fixed in TEST_REGISTER.md, section 18, before the run.

Question: does the percentile rule chosen for the release (q = 0.75, never above 5) merge at least as many pairs as rule R's relaxed setting (2,5), without losing accuracy on the mocks?

| arm | what |
| --- | --- |
| A | AmpliTrim, maxEE 2 (the default; the control) |
| G | AmpliTrim's best truncation at maxEE (2,5): rule R's relaxed setting, the one to beat |
| H | AmpliTrim's best truncation at the percentile rule's maxEE, q = 0.75, never below 2 and never above 5 (the rule chosen for the release) |
| H80 | the same at q = 0.8 with no cap (the rule of section 17: it shows what the cap costs) |
| C | FIGARO's own pick at the longest amplicon length |

The rule, exactly: per read, int(q-th percentile of the expected errors of the reads at AmpliTrim's cut at maxEE 2) + 1, never below 2; H: q = 0.75 and never above 5; H80: q = 0.8, no cap; the search is then repeated at that maxEE. Where both are (2,2), the arm is A and nothing is run. ITS is not tested.

Margins as in night 2: merged share 2 points; expected errors 0.02 per read; accuracy {'variants': 1, 'strains': 1, 'identical_points': 0.1}. FIGARO is run with -m 12 at the longest amplicon length; a FIGARO failure is 'no result'. Fewer than 10 samples: point estimates only. For accuracy, only 'as accurate' and 'more accurate' pass.

Predictions, written before the run:
- P19. On every dataset that was run, H merges at least as many pairs as G within the margin (H minus G at least -2 points). Offline, H is expected to FAIL this on mock A ((2,3) passes 71.5% of the pairs against 79.0% for (2,5)) and probably on inter-laboratory V4-V6 ((3,3): 59.7% against 62.5%): q = 0.75 relaxes less than (2,5) there. It is registered because adoption was fixed before the run.
- P20. On every mock with expected sequences that was run (mock A, mock B, D6300 V4-V5), H is as accurate as G or more accurate (variants and strains within 1, reads in identical ASVs within 0.1 points; 'mixed' fails).
- P21. H merges more pairs than G by more than the margin (2 points) on wastewater (offline: (4,3) passes 75.8% against 67.8%) and on mock B (offline for the uncapped (4,8): 69.5% against 50.9%; the capped (4,5) is not measured offline).
- P22 (exploratory). Where the uncapped rule gives a maxEE above 5 on a read (expected: mock B), H80 merges more pairs than H by more than the margin: that is what the cap costs.

What follows: if P19 and P20 hold, the percentile rule (q = 0.75, cap 5) replaces rule R in the release, with its post hoc status stated. P19 is expected to fail on mock A and probably on V4-V6: then the rule is NOT shown to be at least as good as R, and it is not adopted on the strength of arm H80 or of any other q chosen after this run (that would be a new post hoc rule). It may still be chosen for the release as a stated trade, conformity with DADA2's guidance and cleaner reads against fewer pairs, but not as a validated improvement over R. If P20 fails, rule R stays. Rule R is the rule of the release until this has been read. P21 and P22 are descriptions.

Datasets:

- mockA_high (mock, 16S)
- v1v2 (real, 16S)
- its (real, ITS)
- v4 (real, 16S)
- mcm_v12 (mock, 16S)
- mockB (mock, 16S)
- mcm_v46 (mock, 16S)
- d6300_V3-V4 (mock, 16S)
- d6300_V4-V5 (mock, 16S)
- wastewater_V3-V4 (real, 16S)
- spikein_V3-V4 (real, 16S)
- swabs_V3-V4 (real, 16S)
