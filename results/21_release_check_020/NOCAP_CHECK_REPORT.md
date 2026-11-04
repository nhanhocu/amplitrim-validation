# Night 5: the rule without a cap, the floor-only cut, and reads lost to length

The criteria are in TEST_REGISTER.md, section 24, and were fixed before this ran.

**The pairs:** the ones the nights gave AmpliTrim (every dataset thinned to 5,000 pairs per sample, mock A not thinned, as compare_methods.py does); this is P39b.

## Verdicts

- **P39** NOT MET: the released package recommends what was tested on every dataset except mock B, where it is predicted to set maxEE 4,8.
- **P43** NOT MET: the floor-only cut is the released cut on 7 of 11 datasets with a cut (at least 8 predicted).

## P39: the released rule against what DADA2 was shown

| dataset | tested | what was tested | released package | status |
|---|---|---|---|---|
| mockA_high | night 4b, arm H | 273/247, maxEE 2,3 | 273/247, maxEE 2,3 | same |
| v1v2 | night 3, arm A | 201/157, maxEE 2 | 201/157, maxEE 2 | same |
| its | night 3, arm A | 0/0, maxEE 2 | 0/0, maxEE 2 | same |
| v4 | night 3, arm A | 124/115, maxEE 2 | 124/115, maxEE 2 | same |
| mcm_v12 | night 3, arm A | 155/170, maxEE 2 | 155/170, maxEE 2 | same |
| mockB | night 4b, arm H | 277/250, maxEE 4,5 | 274/253, maxEE 4,8 | expected change: the cap is gone |
| mcm_v46 | night 4b, arm H | 271/267, maxEE 3 | 273/265, maxEE 4,3 | **NO** |
| d6300_V3-V4 | night 3, arm A | 224/218, maxEE 2 | 224/218, maxEE 2 | same |
| d6300_V4-V5 | night 4b, arm H | 282/280, maxEE 2,3 | 282/280, maxEE 2,3 | same |
| wastewater_V3-V4 | night 4b, arm H | 261/183, maxEE 4,3 | 261/183, maxEE 4,3 | same |
| spikein_V3-V4 | night 3, arm A | 222/218, maxEE 2 | 222/218, maxEE 2 | same |
| swabs_V3-V4 | night 3, arm A | 224/218, maxEE 2 | 224/218, maxEE 2 | same |

## P43: the floor-only cut

| dataset | floor (nt) | released cut | total | floor-only cut | the same cut |
|---|---|---|---|---|---|
| mockA_high | 520 | 273/247 | 520 | 274/246 | **no** |
| v1v2 | 358 | 201/157 | 358 | 201/157 | yes |
| its | 0 | 0/0 | 0 | - | - |
| v4 | 239 | 124/115 | 239 | 124/115 | yes |
| mcm_v12 | 325 | 155/170 | 325 | 155/170 | yes |
| mockB | 527 | 274/253 | 527 | 274/253 | yes |
| mcm_v46 | 538 | 273/265 | 538 | 274/264 | **no** |
| d6300_V3-V4 | 442 | 224/218 | 442 | 224/218 | yes |
| d6300_V4-V5 | 562 | 282/280 | 562 | 282/280 | yes |
| wastewater_V3-V4 | 440 | 261/183 | 444 | 254/186 | **no** |
| spikein_V3-V4 | 440 | 222/218 | 440 | 216/224 | **no** |
| swabs_V3-V4 | 442 | 224/218 | 442 | 224/218 | yes |

## P45: read pairs shorter than the recommended cut (descriptive)

| dataset | pairs lost because a read is shorter than the cut |
|---|---|
| mockA_high | 0.0% |
| v1v2 | 0.0% |
| its | 0.0% |
| v4 | 0.0% |
| mcm_v12 | 0.0% |
| mockB | 0.2% |
| mcm_v46 | 0.0% |
| d6300_V3-V4 | 0.0% |
| d6300_V4-V5 | 10.4%  (the package warns from 1%) |
| wastewater_V3-V4 | 0.6% |
| spikein_V3-V4 | 0.0% |
| swabs_V3-V4 | 8.3%  (the package warns from 1%) |

## DADA2 runs that cannot be done offline

P40 to P42, mock B at the released rule's setting (the expected sequences of the mock are given as in night 4b; the table is read with part 2):

```
python validation\compare_methods.py "C:\data\02_mock_V1-V3_mockB_PRJEB67827\prepared\all\ready" --out C:\data\runs\night5_mockB --amplitrim-max-ee 2 2,5 4,5 4,8 --pairs 5000 --reference "<the expected sequences of mock B, as in night 4b>"

python validation\nocap_check.py --dada2-table C:\data\runs\night5_mockB\compare_methods.tsv
```

P42 (descriptive): expected errors per kept read at the released cut and maxEE: 0.91 forward, 3.48 reverse (the offline estimate of the register: 1.02 and 3.31).

P44, DADA2 at the floor-only cut where it differs from the released cut. The table lists 'released' and 'floor_only' and compares every row with 'released' (--baseline), so the line for 'floor_only' is floor-only minus released: at least -2 points on every dataset is MET.

```
python validation\compare_methods.py "C:\data\01_mock_V1-V3_mockA_PRJEB67797\prepared\high_input\ready" --out C:\data\runs\night5_mockA_high --amplitrim-max-ee 2,3 --setting released=273,247,2,3 --setting floor_only=274,246,2,3 --baseline released
python validation\compare_methods.py "C:\data\04_mock_V4-V6_interlab_PRJEB34919\prepared\all\ready" --out C:\data\runs\night5_mcm_v46 --amplitrim-max-ee 4,3 --pairs 5000 --setting released=273,265,4,3 --setting floor_only=274,264,4,3 --baseline released
python validation\compare_methods.py "C:\data\10_real_V3-V4_wastewater_PRJEB75155\prepared\all\ready" --out C:\data\runs\night5_wastewater_V3-V4 --amplitrim-max-ee 4,3 --pairs 5000 --setting released=261,183,4,3 --setting floor_only=254,186,4,3 --baseline released
python validation\compare_methods.py "C:\data\11_real_V3-V4_spikein_PRJNA1243306\prepared\all\ready" --out C:\data\runs\night5_spikein_V3-V4 --amplitrim-max-ee 2 --pairs 5000 --setting released=222,218,2 --setting floor_only=216,224,2 --baseline released
```

Next: send this file.
