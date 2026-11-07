# The longest amplicons of ready

15000 pairs (at most 5000 per sample) gave 13675 merged sequences; lengths: median 374, longest 550.
Classified: the 9215 sequences of at least 374 nt (the longest 1.0%), against a control of 9215 sequences within 5 nt of the median.

| Group | Best hit in SILVA | n | share | median identity (%) |
| --- | --- | --- | --- | --- |
| long | Bacteria | 9114 | 98.9% | 100.0 |
| long | Eukaryota | 101 | 1.1% | 100.0 |
| control | Bacteria | 9215 | 100.0% | 100.0 |

How far to trust the hits (identity is that of the best hit of each query to SILVA; the merged reads are not quality filtered):

| Group | queries | hit lines | queries with a hit | identity at least 97% | identity at least 90% | most frequent best hits (last two fields of the SILVA label) |
| --- | --- | --- | --- | --- | --- | --- |
| long | 9215 | 18430 | 9215 | 95% | 100% | Bacillus / Bacillus subtilis (2641); Enterococcus / Enterococcus faecalis (1173); Limosilactobacillus / Limosilactobacillus fermentum (1125); Listeria / Listeria monocytogenes (871); Staphylococcus / Staphylococcus aureus (633); Bacillus / Bacillus sp. QLPB08 (211) |
| control | 9215 | 18430 | 9215 | 95% | 100% | Bacillus / Bacillus subtilis (1822); Escherichia-Shigella / Escherichia coli (820); Enterococcus / Enterococcus faecalis (816); Limosilactobacillus / Limosilactobacillus fermentum (773); Salmonella / Salmonella enterica subsp. enterica serovar Indiana (622); Listeria / Listeria monocytogenes (620) |

Read it as: if the long group is mostly Eukaryota while the control is Bacteria, the long amplicons are 18S of eukaryotes amplified by the same primers; if both are Bacteria,
they are long 16S. A long group with mostly 'no hit' and a control with hits says the long sequences are not in SILVA (or are not rRNA); if the control has no hits either,
the search does not work on this dataset (check the SILVA file and the identity threshold).
