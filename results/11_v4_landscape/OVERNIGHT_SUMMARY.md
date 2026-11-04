# AmpliTrim overnight validation (full), written 2026-10-10 12:17

Margins fixed before the run: {"recovered_variants": 1, "recovered_strains": 1, "identical_points": 0.1, "extra_asvs": 2, "figaro_equivalence_points": 1.0, "stability_truncation_nt": 10, "stability_yield_points": 1.0, "per_sample_rho": 0.8, "landscape_regret_points": 1.0}

## Steps

| step | tier | status | minutes | note |
| --- | --- | --- | --- | --- |
| landscape | 1 | ok | 19.0 |  |

## Verdicts against the pre-set criteria

| step | criterion | outcome | detail |
| --- | --- | --- | --- |
| landscape | landscape (v4): AmpliTrim's recommendation is near the best setting that covers the amplicons | NOT MET | 4.7 points below the best of 9 DADA2 runs (margin 1.0) |

## landscape: Is the recommendation near the best of a DADA2 grid around it?

```
--- v4 (maxEE 2); AmpliTrim recommends 124/115 (coverage floor 239); share of pairs merged; * = AmpliTrim, . = total below the floor
  trF\trR     105     115     125
       114   64.8.   61.5.   58.1 
       124   67.1.   62.6*   58.1 
       134   67.3    62.9    58.4 
  best of the grid: 134/105 at 67.3%; best among settings that meet the floor: 134/105 at 67.3%; AmpliTrim 62.6%, so 4.7 points below the best that covers the amplicons

```

## Not testable with the data on hand

- An independent mock community (Zymo D6321, PRJEB67827, with Zymo's own reference sequences): no data on hand (python validation\check_build.py --download mockB).
- V3-V4 2x250 reads (tight overlap on real data) and V4-V5 (PRJNA971391): no data on hand (check_build.py --download v3v4 / v4v5); mock_clip250 is an emulation, not a replacement.
- Other platforms (binned quality scores): no data on hand beyond the exactness checks already made.
- Housekeeping: run the CI workflow, push to GitHub, choose a licence, archive for a DOI, test on Windows and Linux, regenerate Figures 3 and 5 and Table 6 from the saved tables, verify the references.
