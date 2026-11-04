# Truth test: DADA2 on long reads against the known variants of a mock community

Primers AGRGTTYGATYMTGGCTCAG and RGYTACCTTGTTACGACTT; all reads; DADA2 with the PacBio error model, band size 32, pool = pseudo; an ASV is exact when it equals an expected variant, near when it is within 2 edits of one, chimeric when DADA2 flags it, other otherwise.

## Monomer

101,206 reads between the primers; median length 1473 nt, window 1320 to 1630 nt; the 75th percentile of the expected errors is 0.86, so the package's rule gives **maxEE 2**.

**Gate (T2): NOT MET.** 14 of 15 strains of the three highest tiers have an exact variant (needed: 14); 15 of 19 expected variants of 1% or more recovered exactly (needed: 80%).
**Gate (T3): NOT MET.** 2.93% of the final reads are in 'other' ASVs (at most 2%).
**Gate (T5): MET.** Spearman 0.95 over 17 strains (at least 0.7).
**Gate (T6): MET.** the rule gives maxEE 2, the same condition as the standard.

| condition | maxEE | window | primers | reads kept % | final ASVs | exact | near | other | chimeric ASVs | exact reads % | other reads % | chimeric reads % | variants recovered | top strains | big variants | Spearman | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ee1 | 1 | yes | cutadapt | 76.4 | 49 | 38 | 9 | 2 | 3 | 88.9 | 2.94 | 0.21 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 15.0 |
| ee2 | 2 | yes | cutadapt | 82.6 | 49 | 38 | 9 | 2 | 3 | 88.9 | 2.93 | 0.20 | 38 of 60 | 14 of 15 | 15 of 19 | 0.95 | 12.8 |
| ee3 | 3 | yes | cutadapt | 86.2 | 49 | 38 | 9 | 2 | 3 | 88.8 | 2.94 | 0.20 | 38 of 60 | 14 of 15 | 15 of 19 | 0.95 | 16.4 |
| ee5 | 5 | yes | cutadapt | 90.7 | 49 | 38 | 9 | 2 | 3 | 88.8 | 2.94 | 0.20 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 15.0 |
| ee10 | 10 | yes | cutadapt | 96.7 | 49 | 38 | 9 | 2 | 3 | 88.8 | 2.95 | 0.20 | 38 of 60 | 14 of 15 | 15 of 19 | 0.96 | 22.2 |
| ee2_nowindow | 2 | no | cutadapt | 82.7 | 49 | 38 | 9 | 2 | 3 | 88.9 | 2.93 | 0.20 | 38 of 60 | 14 of 15 | 15 of 19 | 0.95 | 13.1 |
| ee2_dada2primers | 2 | yes | dada2 | 84.1 | 48 | 37 | 9 | 2 | 3 | 88.8 | 2.96 | 0.17 | 37 of 60 | 14 of 15 | 15 of 19 | 0.95 | 13.2 |

The tables of every strain and every ASV are in truth_strains.tsv and truth_asvs_*.tsv. 'Top strains' are those with a genomic share of 0.18% or more; 'big variants' are the expected variants with an expected read share of 1% or more.

