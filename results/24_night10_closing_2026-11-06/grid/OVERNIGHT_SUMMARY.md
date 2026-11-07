# AmpliTrim overnight validation (full), written 2026-11-07 02:51

Margins fixed before the run: {"recovered_variants": 1, "recovered_strains": 1, "identical_points": 0.1, "extra_asvs": 2, "figaro_equivalence_points": 1.0, "stability_truncation_nt": 10, "stability_yield_points": 1.0, "per_sample_rho": 0.8, "landscape_regret_points": 1.0}

## Steps

| step | tier | status | minutes | note |
| --- | --- | --- | --- | --- |
| landscape | 1 | ok | 41.1 |  |

## Verdicts against the pre-set criteria

| step | criterion | outcome | detail |
| --- | --- | --- | --- |
| landscape | landscape (v4): AmpliTrim's recommendation is near the best setting that covers the amplicons | NOT MET | 4.7 points below the best of 9 DADA2 runs (margin 1.0) |
| landscape | landscape (mcm_v12): AmpliTrim's recommendation is near the best setting that covers the amplicons | met | 0.1 points below the best of 9 DADA2 runs (margin 1.0) |
| landscape | landscape (mcm_v46): AmpliTrim's recommendation is near the best setting that covers the amplicons | met | 0.0 points below the best of 6 DADA2 runs (margin 1.0) |
| landscape | landscape (wastewater_V3-V4): AmpliTrim's recommendation is near the best setting that covers the amplicons | met | 0.0 points below the best of 9 DADA2 runs (margin 1.0) |
| landscape | landscape (spikein_V3-V4): AmpliTrim's recommendation is near the best setting that covers the amplicons | met | 0.7 points below the best of 6 DADA2 runs (margin 1.0) |
| landscape | landscape (swabs_V3-V4) ran | NOT MET | Dada2Error: DADA2 could not learn an error model from these quality scores (it stopped with 'Error matrix is NULL'). That happens when the quality scores take too few distinct values, for example in a simplified- |
| landscape | landscape (miseqsop_mock): AmpliTrim's recommendation is near the best setting that covers the amplicons | met | 0.0 points below the best of 9 DADA2 runs (margin 1.0) |

## landscape: Is the recommendation near the best of a DADA2 grid around it?

```
--- v4 (maxEE 2); AmpliTrim recommends 124/115 (coverage floor 239); share of pairs merged; * = AmpliTrim, . = total below the floor
  trF\trR     105     115     125
       114   64.8.   61.5.   58.1 
       124   67.1.   62.6*   58.1 
       134   67.3    62.9    58.4 
  best of the grid: 134/105 at 67.3%; best among settings that meet the floor: 134/105 at 67.3%; AmpliTrim 62.6%, so 4.7 points below the best that covers the amplicons

--- mcm_v12 (maxEE 2); AmpliTrim recommends 160/165 (coverage floor 325); share of pairs merged; * = AmpliTrim, . = total below the floor
  trF\trR     155     165     175
       150   25.3.   94.1.   95.9 
       160   94.0.   95.9*   95.7 
       170   95.7    95.6    95.5 
  best of the grid: 150/175 at 95.9%; best among settings that meet the floor: 150/175 at 95.9%; AmpliTrim 95.9%, so 0.1 points below the best that covers the amplicons

--- mcm_v46 (maxEE 2); AmpliTrim recommends 273/265 (coverage floor 538); share of pairs merged; * = AmpliTrim, . = total below the floor
  trF\trR     255     265     275
       263    0.0.    0.0.   40.0 
       273    0.0.   41.3*   35.6 
  best of the grid: 273/265 at 41.3%; best among settings that meet the floor: 273/265 at 41.3%; AmpliTrim 41.3%, so 0.0 points below the best that covers the amplicons

--- wastewater_V3-V4 (maxEE 2); AmpliTrim recommends 254/186 (coverage floor 440); share of pairs merged; * = AmpliTrim, . = total below the floor
  trF\trR     176     186     196
       244   20.0.   19.3.   38.6 
       254   17.9.   40.9*   35.8 
       264   37.0    34.3    31.0 
  best of the grid: 254/186 at 40.9%; best among settings that meet the floor: 254/186 at 40.9%; AmpliTrim 40.9%, so 0.0 points below the best that covers the amplicons

--- spikein_V3-V4 (maxEE 2); AmpliTrim recommends 229/210 (coverage floor 439); share of pairs merged; * = AmpliTrim, . = total below the floor
  trF\trR     200     210     220
       219    8.0.   10.1.   82.3 
       229   10.2.   81.6*   80.9 
  best of the grid: 219/220 at 82.3%; best among settings that meet the floor: 219/220 at 82.3%; AmpliTrim 81.6%, so 0.7 points below the best that covers the amplicons

--- swabs_V3-V4: landscape FAILED: Dada2Error: DADA2 could not learn an error model from these quality scores (it stopped with 'Error matrix is NULL'). That happens when the quality scores take too few distinct values, for example in a simplified-

--- miseqsop_mock (maxEE 2); AmpliTrim recommends 132/134 (coverage floor 266); share of pairs merged; * = AmpliTrim, . = total below the floor
  trF\trR     124     134     144
       122    0.0.    0.0.   96.6 
       132    0.0.   96.9*   96.4 
       142   96.1    96.3    96.0 
  best of the grid: 132/134 at 96.9%; best among settings that meet the floor: 132/134 at 96.9%; AmpliTrim 96.9%, so 0.0 points below the best that covers the amplicons
  recovered: AmpliTrim 19/32 variants, 19/21 strains; the best feasible setting 19/32, 19/21

```

## Not testable with the data on hand

- An independent mock community (Zymo D6321, PRJEB67827, with Zymo's own reference sequences): no data on hand (python validation\check_build.py --download mockB).
- V3-V4 2x250 reads (tight overlap on real data) and V4-V5 (PRJNA971391): no data on hand (check_build.py --download v3v4 / v4v5); mock_clip250 is an emulation, not a replacement.
- Other platforms (binned quality scores): no data on hand beyond the exactness checks already made.
- Housekeeping: run the CI workflow, push to GitHub, choose a licence, archive for a DOI, test on Windows and Linux, regenerate Figures 3 and 5 and Table 6 from the saved tables, verify the references.
