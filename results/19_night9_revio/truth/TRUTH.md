# Truth test: DADA2 on long reads against the known variants of a mock community

Primers AGRGTTYGATYMTGGCTCAG and RGYTACCTTGTTACGACTT; the first 50,000 reads of each file; DADA2 with the error model named for each library below, band size 32, pool = pseudo; an ASV is exact when it equals an expected variant, added when it equals a variant added by the refinement rule, near when it is within 2 edits of one, chimeric when DADA2 flags it, other otherwise. The reference is the refined set; the original variants are scored in a second table, without a gate.

## Revio

149,901 reads between the primers; median length 1473 nt, window 1320 to 1630 nt; the 75th percentile of the expected errors is 0.75, so the package's rule gives **maxEE 2**.

Quality scores: highest 40, 7 distinct values (3, 10, 17, 22, 27, 35, 40); error model: **binned:3,10,17,22,27,35,40**.

**Gate (T2): MET.** 15 of 15 strains of the three highest tiers have an exact or an added ASV (needed: 14); 49 of 49 sequences of the replication set recovered (needed: 90%).
**Gate (T3): MET.** 0.00% of the final reads are in ASVs that are neither exact nor added (at most 2%).
**Gate (T5): MET.** Spearman 0.96 over 17 strains (at least 0.7).
**Gate (T6): MET.** the rule gives maxEE 2, the same condition as the standard.

| condition | maxEE | window | primers | error model | reads kept % | final ASVs | exact | added | near | other | chimeric ASVs | exact reads % | unexplained reads % | chimeric reads % | reference variants recovered | top strains | replicated | Spearman | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ee2 | 2 | yes | cutadapt | binned:3,10,17,22,27,35,40 | 82.9 | 53 | 43 | 10 | 0 | 0 | 8 | 94.1 | 0.00 | 0.17 | 53 of 69 | 15 of 15 | 49 of 49 | 0.96 | 10.2 |
| ee2_dada2primers | 2 | yes | dada2 | binned:3,10,17,22,27,35,40 | 83.5 | 57 | 42 | 10 | 1 | 4 | 5 | 94.2 | 0.06 | 0.15 | 52 of 69 | 15 of 15 | 49 of 49 | 0.96 | 13.1 |
| ee2_naive | 2 | yes | cutadapt | PacBioErrfun | 82.9 | 53 | 43 | 10 | 0 | 0 | 8 | 94.1 | 0.00 | 0.17 | 53 of 69 | 15 of 15 | 49 of 49 | 0.96 | 11.7 |

Scored against the original variants (no gate):

| condition | variants recovered | 'other' reads % | top strains | big variants |
|---|---|---|---|---|
| ee2 | 42 of 60 | 1.19 | 14 of 15 | 15 of 19 |
| ee2_dada2primers | 41 of 60 | 1.22 | 14 of 15 | 15 of 19 |
| ee2_naive | 42 of 60 | 1.19 | 14 of 15 | 15 of 19 |

The tables of every strain and every ASV are in truth_strains.tsv and truth_asvs_*.tsv. 'Top strains' are those with a genomic share of 0.18% or more; 'unexplained' reads are those in ASVs that are neither exact nor added; 'replicated' counts the sequences of the replication set that were recovered.

