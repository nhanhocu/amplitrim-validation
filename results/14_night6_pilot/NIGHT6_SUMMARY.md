# Night 6: PRJNA933120 (Buetas et al. 2024)

Run on 2026-10-14; folder C:\data\runs\night6_pilot. Criteria: TEST_REGISTER.md, section 25. Margins: {"filter_estimate": 0.02, "rule_gain": 0.02, "both_primers": 0.9, "median_length": [1430, 1480], "within_10pct": 0.95, "distinct_q": 40, "max_q": 60, "end_vs_middle": 3.0}

## Illumina, 16S V3-V4: the released package against DADA2

The released package (version 0.1.0, C:\Users\<user>\OneDrive\Documents\GitHub\amplitrim\amplitrim) on the reads, thinned to at most 5000 pairs per sample:
- released: truncLenF 277, truncLenR 165, maxEE 2
- default: truncLenF 277, truncLenR 165, maxEE 2
- g25: truncLenF 277, truncLenR 165, maxEE 2,5

- **P46** not decided: no estimate and DADA2 measurement for: released, default
- **P47** not applicable: the rule kept the default setting (277/165, maxEE 2)
- **P48** descriptive: share of pairs merged by DADA2: default (maxEE 2) -, 2,5 -, released -
- **P49** descriptive: the development build chose 277/165 at maxEE 2, the released package 277/165: the same cut

The whole DADA2 table is in `dada2/compare_methods.txt`.

## PacBio, full-length 16S: description only

- **P50** NOT as expected: 85.5% of 31,995 reads have both primers (expected at least 90%)
- **P51** as expected: median length between the primers 1454 nt (expected 1430 to 1480); 99.5% within 10% of the median (expected at least 95%)
- **P52** as expected: fewest distinct quality values in a file 93 (expected at least 40); lowest maximum Q93 (expected at least Q60)
- **P53** as expected: first 50 bases Q31.3, middle half Q31.2, last 50 bases Q29.1 (expected within 3)

The table of every file, with what is unusual, is in `longread/LONGREAD_DESCRIBE.md`.

## Steps

- download: done in 0 min (4 runs downloaded and checked)
- describe: done in 0 min (describe_illumina.txt written)
- prepare: done in 0 min (2 samples ready in C:\data\runs\night6_pilot\illumina_thin)
- amplitrim: done in 0 min (released package 0.1.0: truncLenF 277, truncLenR 165, maxEE 2)
- dada2: done in 0 min (DADA2 ran at 2 setting(s): default 277/165 maxEE 2, g25 277/165 maxEE 2,5)
- longread: done in 0 min (2 files, 31,995 reads, 85.5% with both primers)
