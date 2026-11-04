# Over-merging on real reads

The criteria (P31 to P33) are in TEST_REGISTER.md, section 22, and were fixed before this ran.

## Verdicts

- **P31** MET: At each cut that matters (124/115, 120/118, 130/108) at most 1% of the merges are at the wrong length: the highest is 0.00% at 124/115
- **P32** MET: Wrong-length merges do not tell 120/118 from 130/108 (they differ by at most 1 point of the reference pairs): 0.00% against 0.00%, 0.00 points apart
- **P33** MET: (exploratory) The overlap of 130/108 carries fewer expected errors than that of 120/118: 0.056 against 0.059 per pair

## The cuts (49,720 pairs analysed; 48,227 reference pairs, whose full-length reads overlap by at least 40 nt)

Shares of the reference pairs. 'Correct' is merged at the reference length; 'wrong' is merged at another length (a false join). 'No mismatch' is vsearch with no difference allowed in the raw overlap. Overlap errors are the expected errors in the overlap of the two reads, per pair.

| cut | total | pass the filter | correct | wrong | wrong, of the merged | correct, no mismatch | wrong, no mismatch | overlap errors, mean | overlap errors >= 1 |
|---|---|---|---|---|---|---|---|---|---|
| 110/108 | 218 | 100.0% | 2.9% | 0.00% | 0.00% | 2.8% | 0.00% | 0.024 | 0.0% |
| 110/118 | 228 | 99.9% | 98.2% | 0.00% | 0.00% | 92.2% | 0.00% | 0.043 | 0.0% |
| 110/128 | 238 | 99.8% | 99.2% | 0.00% | 0.00% | 91.5% | 0.00% | 0.069 | 0.2% |
| 114/105 | 219 | 100.0% | 91.0% | 0.00% | 0.00% | 90.4% | 0.00% | 0.020 | 0.0% |
| 114/115 | 229 | 99.9% | 98.2% | 0.00% | 0.00% | 92.5% | 0.00% | 0.041 | 0.0% |
| 114/125 | 239 | 99.9% | 99.7% | 0.00% | 0.00% | 92.5% | 0.00% | 0.065 | 0.1% |
| 120/108 | 228 | 99.9% | 98.2% | 0.00% | 0.00% | 94.2% | 0.00% | 0.038 | 0.0% |
| 120/118 (round B6 recommendation) | 238 | 99.9% | 99.3% | 0.00% | 0.00% | 92.4% | 0.00% | 0.059 | 0.1% |
| 120/128 | 248 | 99.8% | 99.8% | 0.00% | 0.00% | 91.2% | 0.00% | 0.084 | 0.4% |
| 124/105 | 229 | 99.9% | 98.2% | 0.00% | 0.00% | 95.3% | 0.00% | 0.036 | 0.0% |
| 124/115 (recommended now) | 239 | 99.9% | 99.7% | 0.00% | 0.00% | 92.9% | 0.00% | 0.058 | 0.1% |
| 124/125 | 249 | 99.9% | 99.9% | 0.00% | 0.00% | 91.5% | 0.00% | 0.082 | 0.4% |
| 130/108 (best cell of the B6 grid) | 238 | 99.9% | 99.3% | 0.00% | 0.00% | 94.4% | 0.00% | 0.056 | 0.1% |
| 130/118 | 248 | 99.9% | 99.9% | 0.00% | 0.00% | 92.1% | 0.00% | 0.076 | 0.4% |
| 130/128 | 258 | 99.8% | 99.8% | 0.00% | 0.00% | 90.4% | 0.00% | 0.101 | 0.8% |
| 134/105 | 239 | 99.9% | 99.7% | 0.00% | 0.00% | 95.7% | 0.00% | 0.055 | 0.1% |
| 134/115 | 249 | 99.9% | 99.9% | 0.00% | 0.00% | 92.0% | 0.00% | 0.077 | 0.4% |
| 134/125 | 259 | 99.9% | 99.9% | 0.00% | 0.00% | 90.7% | 0.00% | 0.100 | 0.8% |

- What vsearch sees of the gap of round B6: 130/108 merged 99.3% of the reference pairs correctly against 99.3% for 120/118 (-0.0 points); DADA2 measured 66.4% against 59.6% (+6.8 points).

Next: send this file.
