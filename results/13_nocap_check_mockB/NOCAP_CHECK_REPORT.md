# Night 5: the rule without a cap, the floor-only cut, and reads lost to length

The criteria are in TEST_REGISTER.md, section 24, and were fixed before this ran.

## Verdicts

- **P39** not decided (not all 12 datasets were run, or a tested result was not found): the released package recommends what was tested on every dataset except mock B, where it is predicted to set maxEE 4,8.
- **P43** not decided (not all 12 datasets were run, or a tested result was not found): the floor-only cut is the released cut on 1 of 1 datasets with a cut (at least 8 predicted).

## P39: the released rule against what DADA2 was shown

| dataset | tested | what was tested | released package | status |
|---|---|---|---|---|
| mockB | night 4b, arm H | 277/250, maxEE 4,5 | 274/253, maxEE 4,8 | expected change: the cap is gone |

## P43: the floor-only cut

| dataset | floor (nt) | released cut | total | floor-only cut | the same cut |
|---|---|---|---|---|---|
| mockB | 527 | 274/253 | 527 | 274/253 | yes |

## P45: read pairs shorter than the recommended cut (descriptive)

| dataset | pairs lost because a read is shorter than the cut |
|---|---|
| mockB | 0.2% |

## DADA2 runs that cannot be done offline

P40 to P42, mock B at the released rule's setting (the expected sequences of the mock are given as in night 4b; the table is read with part 2):

```
python validation\compare_methods.py "C:\data\mock_V1-V3_mockB_PRJEB67827\prepared\all\ready" --out C:\data\runs\night5_mockB --amplitrim-max-ee 2 2,5 4,5 4,8 --pairs 5000 --reference "<the expected sequences of mock B, as in night 4b>"

python validation\nocap_check.py --dada2-table C:\data\runs\night5_mockB\compare_methods.tsv
```

P42 (descriptive): expected errors per kept read at the released cut and maxEE: 0.90 forward, 3.56 reverse (the offline estimate of the register: 1.02 and 3.31).

P44: the floor-only cut is the released cut on every dataset, so DADA2 would give the same result at both: nothing to run.

Next: send this file.
