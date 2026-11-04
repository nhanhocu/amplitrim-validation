# Night 3 protocol (written 2026-10-09 18:12, before any analysis)

Fixed in TEST_REGISTER.md, section 14, before the run.

Question: where AmpliTrim's default maxEE of 2 is too strict, does maxEE (2,5), DADA2's own suggestion for the reverse read, recover most of what FIGARO's looser pick gains, without losing accuracy on the mocks; and what does a careful manual cut give?

| arm | what |
| --- | --- |
| A | AmpliTrim, maxEE 2 (the default; the control) |
| G | AmpliTrim's best truncation at maxEE (2,5), DADA2's own suggestion for the reverse read |
| R | a rule, no extra run: G where A passes under 70% of the pairs, otherwise A |
| F2 | a careful manual cut (post hoc): the median-Q30 cut, never longer than the reads, never too short for the amplicon; maxEE 2, relaxed to (2,5) under 60% pass |
| C | FIGARO's own pick at the longest amplicon length |

F2, exactly: (1) each read cut where its median quality first falls below 30; (2) capped at the length that 90% of the reads reach; (3) if forward + reverse is under the longest amplicon + 12 nt, the missing nucleotides are added half to each read (the forward takes the odd one), up to each cap, and what one read cannot take goes to the other; (4) maxEE (2,2), relaxed to (2,5) when fewer than 60% of the pairs pass at (2,2). Rule R uses (2,5) where A passes under 70%.

Margins as in night 2: merged share 2 points; expected errors 0.02 per read; accuracy {'variants': 1, 'strains': 1, 'identical_points': 0.1}. FIGARO is run with -m 12 at the longest amplicon length; a FIGARO failure is 'no result'. Fewer than 10 samples: point estimates only.

Predictions, written before the run:
- P6. Where A passes under 70% of the pairs (mock A, mock B, inter-laboratory V4-V6, wastewater, D6300 V4-V5), G merges more pairs than A by more than the margin, with noisier reads.
- P7. G is within 10 points of FIGARO's pick on mock A, wastewater and inter-laboratory V4-V6, and 15 or more points behind it on mock B (the cap is 5; FIGARO used 6,9).
- P8. Where A passes at least 80% of the pairs (V1-V2, soil V4, both V1-V2/V3-V4 mocks, spike-in, swabs), G merges at most 3 points more pairs than A, with a noisier reverse read.
- P9. G is as accurate as A, or more accurate, on every mock with expected sequences; on mock B its share of reads in exact ASVs is at least 3 points above A's.
- P10. F2 relaxes to (2,5) on mock B and wastewater.
- P11. F2 never merges more pairs than the better of A and G by more than the margin on any 16S dataset.
- P12. F2 runs on every 16S dataset and merges at least 20 points more pairs than F did in night 2 wherever F merged under 25% or gave no result (a failed F counts as 0%).

What follows: if P7 and P9 hold, the planned warning offers (2,5) as its alternative; if either fails, it shows the table without naming one. F2 is a post hoc baseline and changes nothing.

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
