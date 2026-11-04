# Night 5: the rule without a cap, the floor-only cut, and reads lost to length

The criteria are in TEST_REGISTER.md, section 24, and were fixed before this ran.

## Verdicts

- **P39** NOT MET: the released package recommends what was tested on every dataset except mock B, where it is predicted to set maxEE 4,8.
- **P43** MET: the floor-only cut is the released cut on 8 of 11 datasets with a cut (at least 8 predicted).

## P39: the released rule against what DADA2 was shown

| dataset | tested | what was tested | released package | status |
|---|---|---|---|---|
| mockA_high | night 4b, arm H | 273/247, maxEE 2,3 | 273/247, maxEE 2,3 | same |
| v1v2 | night 3, arm A | 201/157, maxEE 2 | 195/168, maxEE 2 | **NO** |
| its | night 3, arm A | 0/0, maxEE 2 | 0/0, maxEE 2 | same |
| v4 | night 3, arm A | 124/115, maxEE 2 | 124/115, maxEE 2 | same |
| mcm_v12 | night 3, arm A | 155/170, maxEE 2 | 160/165, maxEE 2 | **NO** |
| mockB | night 4b, arm H | 277/250, maxEE 4,5 | 274/253, maxEE 4,8 | expected change: the cap is gone |
| mcm_v46 | night 4b, arm H | 271/267, maxEE 3 | 273/265, maxEE 4,3 | **NO** |
| d6300_V3-V4 | night 3, arm A | 224/218, maxEE 2 | 224/218, maxEE 2 | same |
| d6300_V4-V5 | night 4b, arm H | 282/280, maxEE 2,3 | 282/280, maxEE 2,3 | same |
| wastewater_V3-V4 | night 4b, arm H | 261/183, maxEE 4,3 | 260/182, maxEE 4,3 | **NO** |
| spikein_V3-V4 | night 3, arm A | 222/218, maxEE 2 | 229/210, maxEE 2 | **NO** |
| swabs_V3-V4 | night 3, arm A | 224/218, maxEE 2 | 224/218, maxEE 2 | same |

## P43: the floor-only cut

| dataset | floor (nt) | released cut | total | floor-only cut | the same cut |
|---|---|---|---|---|---|
| mockA_high | 520 | 273/247 | 520 | 274/246 | **no** |
| v1v2 | 363 | 195/168 | 363 | 195/168 | yes |
| its | 0 | 0/0 | 0 | - | - |
| v4 | 239 | 124/115 | 239 | 124/115 | yes |
| mcm_v12 | 325 | 160/165 | 325 | 160/165 | yes |
| mockB | 527 | 274/253 | 527 | 274/253 | yes |
| mcm_v46 | 538 | 273/265 | 538 | 274/264 | **no** |
| d6300_V3-V4 | 442 | 224/218 | 442 | 224/218 | yes |
| d6300_V4-V5 | 562 | 282/280 | 562 | 282/280 | yes |
| wastewater_V3-V4 | 440 | 260/182 | 442 | 254/186 | **no** |
| spikein_V3-V4 | 439 | 229/210 | 439 | 229/210 | yes |
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
| d6300_V4-V5 | 10.2%  (the package warns from 1%) |
| wastewater_V3-V4 | 0.2% |
| spikein_V3-V4 | 0.0% |
| swabs_V3-V4 | 7.7%  (the package warns from 1%) |

## DADA2 runs that cannot be done offline

P40 to P42, mock B at the released rule's setting (the expected sequences of the mock are given as in night 4b; the table is read with part 2):

```
python validation\compare_methods.py "C:\data\mock_V1-V3_mockB_PRJEB67827\prepared\all\ready" --out C:\data\runs\night5_mockB --amplitrim-max-ee 2 2,5 4,5 4,8 --pairs 5000 --reference "<the expected sequences of mock B, as in night 4b>"

python validation\nocap_check.py --dada2-table C:\data\runs\night5_mockB\compare_methods.tsv
```

P42 (descriptive): expected errors per kept read at the released cut and maxEE: 0.90 forward, 3.56 reverse (the offline estimate of the register: 1.02 and 3.31).

P44, DADA2 at the floor-only cut where it differs from the released cut (the first row is the released cut; the table compares the second with it):

```
python validation\compare_methods.py "C:\data\mock_V1-V3_mockA_PRJEB67797\prepared\high_input\ready" --out C:\data\runs\night5_mockA_high --amplitrim-max-ee 2,3 --pairs 5000 --setting floor_only=274,246,2,3
python validation\compare_methods.py "C:\data\mock_V4-V6_interlab_PRJEB34919\prepared\all\ready" --out C:\data\runs\night5_mcm_v46 --amplitrim-max-ee 4,3 --pairs 5000 --setting floor_only=274,264,4,3
python validation\compare_methods.py "C:\data\real_V3-V4_wastewater_PRJEB75155\prepared\all\ready" --out C:\data\runs\night5_wastewater_V3-V4 --amplitrim-max-ee 4,3 --pairs 5000 --setting floor_only=254,186,4,3
```

Next: send this file.
