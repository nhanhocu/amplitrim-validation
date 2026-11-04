# Estimate check

The criteria (P36 to P38) are in TEST_REGISTER.md, section 23, and were fixed before this ran.

## Verdicts

- **P36** NOT MET: The strict estimate is closer to DADA2's merged share than the tolerant one, as the mean over the datasets of the mean absolute difference: 12.5 against 6.5 points (5 of 12 datasets closer)
- **P37** NOT MET: The strict estimate ranks the settings at least as well as the tolerant one (within 0.05), mean rank correlation over the 10 datasets with at least 4 settings: +0.76 against +0.92
- **P38** not run (give --cutoff)

## A. The two estimates against DADA2 (98 settings on 12 datasets; points of the input pairs)

| dataset | settings | tolerant minus DADA2 | strict minus DADA2 | closer | rank correlation, tolerant | rank correlation, strict |
|---|---|---|---|---|---|---|
| d6300_V3-V4 | 4 | +3.1 | +0.1 | strict | +1.00 | +1.00 |
| d6300_V4-V5 | 9 | +6.4 | -6.1 | tolerant | +1.00 | +1.00 |
| its | 1 | +13.7 | +2.4 | strict | - | - |
| mcm_v12 | 7 | +0.3 | -4.3 | tolerant | +1.00 | +0.86 |
| mcm_v46 | 8 | -2.0 | -17.6 | tolerant | +0.98 | +0.74 |
| mockA_high | 8 | +0.8 | -23.1 | tolerant | +1.00 | +0.74 |
| mockB | 12 | -2.2 | -37.8 | tolerant | +0.99 | +0.41 |
| spikein_V3-V4 | 5 | +3.3 | -4.7 | tolerant | +1.00 | +0.70 |
| swabs_V3-V4 | 3 | +7.1 | +1.7 | strict | - | - |
| v1v2 | 8 | +6.1 | -5.5 | strict | +1.00 | +0.93 |
| v4 | 8 | +26.5 | +17.7 | strict | +0.26 | +0.83 |
| wastewater_V3-V4 | 11 | +3.9 | -26.9 | tolerant | +0.94 | +0.43 |
Next: send this file.
