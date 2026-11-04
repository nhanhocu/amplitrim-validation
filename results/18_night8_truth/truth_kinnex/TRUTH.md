# Truth test: DADA2 on long reads against the known variants of a mock community

Primers AGRGTTYGATYMTGGCTCAG and RGYTACCTTGTTACGACTT; the first 50,000 reads of each file; DADA2 with the PacBio error model, band size 32, pool = pseudo; an ASV is exact when it equals an expected variant, near when it is within 2 edits of one, chimeric when DADA2 flags it, other otherwise.

## Kinnex

149,931 reads between the primers; median length 1471 nt, window 1320 to 1620 nt; the 75th percentile of the expected errors is 2.66, so the package's rule gives **maxEE 3**.

**Gate (T2): NOT MET.** 14 of 15 strains of the three highest tiers have an exact variant (needed: 14); 15 of 19 expected variants of 1% or more recovered exactly (needed: 80%).
**Gate (T3): NOT MET.** 3.14% of the final reads are in 'other' ASVs (at most 2%).
**Gate (T5): MET.** Spearman 0.96 over 17 strains (at least 0.7).
**Gate (T6): MET.** the rule gives maxEE 3: 38 exact variants against 38 at maxEE 2; 'other' share 3.14% against 3.14% (at most 0.5 points more).

| condition | maxEE | window | primers | reads kept % | final ASVs | exact | near | other | chimeric ASVs | exact reads % | other reads % | chimeric reads % | variants recovered | top strains | big variants | Spearman | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ee1 | 1 | yes | cutadapt | 57.8 | 49 | 38 | 9 | 2 | 6 | 87.9 | 3.11 | 0.04 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 19.3 |
| ee2 | 2 | yes | cutadapt | 70.3 | 49 | 38 | 9 | 2 | 6 | 88.0 | 3.14 | 0.04 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 21.7 |
| ee3 | 3 | yes | cutadapt | 77.0 | 49 | 38 | 9 | 2 | 6 | 88.0 | 3.14 | 0.03 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 24.8 |
| ee5 | 5 | yes | cutadapt | 85.4 | 49 | 38 | 9 | 2 | 8 | 87.9 | 3.14 | 0.04 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 78.2 |
| ee10 | 10 | yes | cutadapt | 94.5 | 49 | 38 | 9 | 2 | 8 | 88.0 | 3.14 | 0.04 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 30.8 |
| ee2_nowindow | 2 | no | cutadapt | 70.3 | 49 | 38 | 9 | 2 | 6 | 88.0 | 3.14 | 0.04 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 21.6 |
| ee2_dada2primers | 2 | yes | dada2 | 72.2 | 49 | 38 | 9 | 2 | 6 | 87.9 | 3.15 | 0.04 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 20.7 |

The tables of every strain and every ASV are in truth_strains.tsv and truth_asvs_*.tsv. 'Top strains' are those with a genomic share of 0.18% or more; 'big variants' are the expected variants with an expected read share of 1% or more.

