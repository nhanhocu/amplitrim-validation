# Truth test: DADA2 on long reads against the known variants of a mock community

Primers AGRGTTYGATYMTGGCTCAG and RGYTACCTTGTTACGACTT; the first 20,000 reads of each file; DADA2 with the PacBio error model, band size 32, pool = pseudo; an ASV is exact when it equals an expected variant, near when it is within 2 edits of one, chimeric when DADA2 flags it, other otherwise.

## Pilot

19,965 reads between the primers; median length 1466 nt, window 1310 to 1620 nt; the 75th percentile of the expected errors is 0.88, so the package's rule gives **maxEE 2**.

**Gate (T2): NOT MET.** 14 of 15 strains of the three highest tiers have an exact variant (needed: 14); 15 of 19 expected variants of 1% or more recovered exactly (needed: 80%).
**Gate (T3): NOT MET.** 3.54% of the final reads are in 'other' ASVs (at most 2%).
**Gate (T5): MET.** Spearman 0.97 over 17 strains (at least 0.7).
**Gate (T6): MET.** the rule gives maxEE 2, the same condition as the standard.

| condition | maxEE | window | primers | reads kept % | final ASVs | exact | near | other | chimeric ASVs | exact reads % | other reads % | chimeric reads % | variants recovered | top strains | big variants | Spearman | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ee2 | 2 | yes | cutadapt | 82.6 | 47 | 37 | 8 | 2 | 0 | 86.6 | 3.54 | 0.00 | 37 of 60 | 14 of 15 | 15 of 19 | 0.97 | 1.8 |

The tables of every strain and every ASV are in truth_strains.tsv and truth_asvs_*.tsv. 'Top strains' are those with a genomic share of 0.18% or more; 'big variants' are the expected variants with an expected read share of 1% or more.

