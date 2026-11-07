# Release check

The criterion (P30) is in TEST_REGISTER.md, section 21, and was fixed before this ran.

## Verdict

- **P30** not decided (not all 12 datasets were run, or a tested result was not found): the released package recommends exactly the settings that were run through DADA2 on every dataset: 2 of 3 the same, 1 different.

| dataset | tested | what was tested | released package | the same |
|---|---|---|---|---|
| its | night 3, arm A | 0/0, maxEE 2 | 0/0, maxEE 2 | yes |
| v4 | night 3, arm A | 124/115, maxEE 2 | 124/115, maxEE 2 | yes |
| mockB | night 4b, arm H | 277/250, maxEE 4,5 | 274/253, maxEE 4,8 | **NO** |

Where the settings differ, the DADA2 results of the nights are not claimed for the released package: DADA2 has to be run at the released settings.

Next: send this file.
