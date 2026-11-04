# Night 6: PRJNA933120 (Buetas et al. 2024)

Run on 2026-10-14; folder C:\data\runs\night6_PRJNA933120. Criteria: TEST_REGISTER.md, section 25. Margins: {"filter_estimate": 0.02, "rule_gain": 0.02, "both_primers": 0.9, "median_length": [1430, 1480], "within_10pct": 0.95, "distinct_q": 40, "max_q": 60, "end_vs_middle": 3.0}

## Illumina, 16S V3-V4: the released package against DADA2

The released package (version 0.1.0, C:\Users\<user>\OneDrive\Documents\GitHub\amplitrim\amplitrim) on the reads, thinned to at most 5000 pairs per sample:
- released: truncLenF 251, truncLenR 191, maxEE 2
- default: truncLenF 251, truncLenR 191, maxEE 2
- g25: truncLenF 251, truncLenR 191, maxEE 2,5

Distinct quality values per sample in the Illumina reads: 2 to 2 (26 samples).

- **P46 to P49 cannot be decided on this copy of the reads.** Every sample has at most 2 distinct quality values, so the per-base quality is missing (as in the SRA 'lite' format) and DADA2 cannot learn an error model from it. AmpliTrim's recommendation above was computed from the same scores, so it is no more informative than they are, and P47 'does not apply' carries no evidence about the rule. The criteria of section 25 stay as they are for a copy of these reads, or another dataset, with the original quality scores.

## PacBio, full-length 16S: description only

- **P50** as expected: 99.7% of 606,658 reads have both primers (expected at least 90%)
- **P51** as expected: median length between the primers 1454 nt (expected 1430 to 1480); 99.6% within 10% of the median (expected at least 95%)
- **P52** as expected: fewest distinct quality values in a file 92 (expected at least 40); lowest maximum Q93 (expected at least Q60)
- **P53** as expected: first 50 bases Q29.9, middle half Q29.9, last 50 bases Q27.5 (expected within 3)

The table of every file, with what is unusual, is in `longread/LONGREAD_DESCRIBE.md`.

## Steps

- download: not run
- describe: not run
- prepare: not run
- amplitrim: not run
- dada2: skipped in 0 min (the Illumina reads have at most 2 distinct quality values in each of 26 samples (a simplified-quality copy, as in the SRA 'lite' format): DADA2 cannot learn an error model from them. Get files with the original quality scores.)
- longread: not run
