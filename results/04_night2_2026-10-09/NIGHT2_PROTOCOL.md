# Night 2 protocol (written 2026-10-09 12:08, before any analysis)

Question: when AmpliTrim chooses the maxEE as well as the truncation, does it end up where FIGARO ends up, with as many merged pairs and no noisier reads?

Every arm is a truncation and a maxEE, run through DADA2 on the same pairs with the same 12 nt overlap for both tools. FIGARO is run with -m 12 and given the longest amplicon AmpliTrim measured (and, when a tail of longer amplicons makes them differ, also the typical one); a FIGARO failure is reported as 'no result'.

| arm | what |
| --- | --- |
| A | AmpliTrim, maxEE 2 (the default) |
| B | AmpliTrim at its own quality-first maxEE, floor 50% |
| B2 | the same, floor 80% |
| B4 | AmpliTrim at 'mean expected errors at the cut + 1' (the rule FIGARO is documented to use) |
| D | AmpliTrim's truncation at FIGARO's maxEE |
| E | no truncation |
| F | median-Q30 cut |
| C | FIGARO's own pick |

Measures: the paired per-sample difference in the share of pairs DADA2 merges (an interval from 10 samples); the mean expected errors per kept read, forward and reverse, measured from the qualities at the arm's truncation and maxEE; on mocks the variants and strains recovered and the share of reads in exact ASVs.

Margins, fixed here: merged share 2 points; expected errors 0.02 per read; accuracy {'variants': 1, 'strains': 1, 'identical_points': 0.1} (the battery's margins); stability 10 nt.
Verdicts against FIGARO's pick: matches / better / worse / trade-off (more pairs but noisier, or fewer pairs but cleaner) / mixed noise / no result. 'Better' needs a gain on one axis and no loss on the other. On a mock, accuracy is reported beside the verdict and is what decides a disagreement. Where FIGARO has no result the arms are classified against A. No winner is declared on real data unless one pick is better on both axes.

AmpliTrim's maxEE grid stops at (5,5), so its picks cannot reach FIGARO's (6,9) on mock B; its quality-first pick is never stricter than 2.

Predictions, written before the run:
- P1. Where AmpliTrim's default keeps 80% or more of the pairs (V1-V2, soil V4, both inter-laboratory V1-V2 and the NovaSeq V3-V4 sets), the floors are not binding, so B and B2 equal A, and FIGARO's stricter maxEE gives 'trade-off: more pairs, noisier' for A against FIGARO.
- P2. On poor-quality reads (mock B, wastewater, inter-laboratory V4-V6) B merges fewer pairs than FIGARO by more than the margin, with cleaner reads (about 18 points on mock B); B2 narrows the gap and B4 comes nearer FIGARO than B does. AmpliTrim's grid stops at (5,5), so B and B2 cannot reach FIGARO's (6,9) on mock B.
- P3. On mock B the accuracy of B is lower than FIGARO's (fewer variants or fewer reads in exact ASVs).
- P4. On D6300 V4-V5 FIGARO runs at the typical amplicon length, chooses much shorter reads than AmpliTrim's default, and leaving out 1% of the longest amplicons raises AmpliTrim's merged share.
- P5. The picks of both tools hold across three sets of samples, except where read quality differs strongly between samples (wastewater).

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
