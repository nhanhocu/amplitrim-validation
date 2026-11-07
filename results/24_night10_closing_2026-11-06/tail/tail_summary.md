# The longest amplicons of ready

15000 pairs (at most 5000 per sample) gave 13675 merged sequences; lengths: median 374, longest 550.
Classified: the 103 sequences longer than 374 nt (the longest 1.0%), against a control of 103 sequences within 5 nt of the median.

| Group | Best hit in SILVA | n | share | median identity (%) |
| --- | --- | --- | --- | --- |
| long | Eukaryota | 101 | 98.1% | 99.8 |
| long | Bacteria | 2 | 1.9% | 99.8 |
| control | Bacteria | 103 | 100.0% | 100.0 |

How far to trust the hits (identity is that of the best hit of each query to SILVA; the merged reads are not quality filtered):

| Group | queries | hit lines | queries with a hit | identity at least 97% | identity at least 90% | most frequent best hits (last two fields of the SILVA label) |
| --- | --- | --- | --- | --- | --- | --- |
| long | 103 | 206 | 103 | 94% | 98% | Saccharomyces / Hordeum vulgare subsp. vulgare (domesticated barley) (85); Saccharomyces / Clostridium sp. D53t1_180928_C8 (11); Limosilactobacillus / Limosilactobacillus fermentum (1); Cryptococcus / Klebsiella pneumoniae (1); Salmonella / Salmonella sp. KF (1); Saccharomyces / Saccharomyces cerevisiae (1) |
| control | 103 | 206 | 103 | 95% | 100% | Bacillus / Bacillus subtilis (18); Escherichia-Shigella / Escherichia coli (14); Enterococcus / Enterococcus faecalis (11); Limosilactobacillus / Limosilactobacillus fermentum (11); Salmonella / Salmonella enterica subsp. enterica serovar Indiana (6); Staphylococcus / Staphylococcus aureus (4) |

Read it as: if the long group is mostly Eukaryota while the control is Bacteria, the long amplicons are 18S of eukaryotes amplified by the same primers; if both are Bacteria,
they are long 16S. A long group with mostly 'no hit' and a control with hits says the long sequences are not in SILVA (or are not rRNA); if the control has no hits either,
the search does not work on this dataset (check the SILVA file and the identity threshold).
