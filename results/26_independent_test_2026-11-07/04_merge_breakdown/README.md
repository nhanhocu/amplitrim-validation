# Where DADA2 loses the pairs that the yield estimate counts (exploratory, 9 November 2026)

Run after the results of issue #1, at the author's request (`FUTURE.md`, item A2), to give the data for a merge estimate that follows DADA2's merge. No criterion was set and nothing here is a test.

**What was run.** `validation/independent_test/merge_breakdown.R` on draw a (24 samples of 5,000 pairs) of the four real datasets, at AmpliTrim's recommendation (arm R) and, where it differs, at maxEE 2 (arm D). The same DADA2 settings as the test (`truncQ = 2`, `maxN = 0`, error models per flow cell, `minOverlap = 12`, `maxMismatch = 0`). `mergePairs` was run with `returnRejects = TRUE`. DADA2 reports every refused pair with 0 matches, whatever the reason, so the overlap of each refused pair was measured again from its two denoised sequences: the overlap of 12 nt or more with the lowest share of mismatches. Then `probe_refused.R` aligned the refused pairs of six HDP samples (arm R) with end gaps free, so that overhangs and indels are allowed, and recorded which pairs merged.

**Files.** `<dataset>_<arm>.tsv`, one row per sample; `breakdown_summary.tsv` and `.md`, per 100 input pairs (written by `breakdown_summary.py`); `probe_HDP_R.tsv` (every refused pair of the six samples, with both sequences) and `probe_HDP_R_accepted.tsv` (the pairs that merged).

## Per 100 input pairs

| Dataset, arm | Cut, maxEE | Fail the filter | Lost in denoising | Refused, close overlap | Refused, poor or no overlap | Merged | AmpliTrim's yield estimate | Estimate minus merged |
|---|---|---|---|---|---|---|---|---|
| NIG R | 207/231, 2,2 | 24.1 | 3.8 | 2.2 | 0.1 | 69.7 | 75.8 | 6.1 |
| CBGS R | 217/222, 2,2 | 12.1 | 0.7 | 0.3 | 0.3 | 86.6 | 87.6 | 1.0 |
| KFS R | 248/192, 3,3 | 28.4 | 3.2 | 1.1 | 1.4 | 65.9 | 69.0 | 3.2 |
| KFS D | 247/193, 2,2 | 39.5 | 2.8 | 1.3 | 1.4 | 55.0 | 59.4 | 4.3 |
| HDP R | 261/179, 3,2 | 31.0 | 10.3 | 2.3 | 8.5 | 47.9 | 68.0 | 20.0 |
| HDP D | 251/189, 2,2 | 35.6 | 8.5 | 1.9 | 9.1 | 44.9 | 63.3 | 18.5 |

'Close overlap': an overlap of 12 nt or more with 1 to 10% mismatches between the two denoised sequences (mostly a single mismatch). 'Poor or no overlap': no overlap of 12 nt or more with at most 10% mismatches. AmpliTrim's filter estimate (est_pass) was within 0.25 points of DADA2's pass rate in every row, so the whole gap lies after the filter. AmpliTrim already expects 0.2 to 2.6 of every 100 pairs not to merge (est_pass minus est_yield); the gap is what it does not foresee.

## What it shows

1. **Long amplicons are not the cause.** No dataset has amplicons longer than its cut can cover. A loose merge of the raw reads (vsearch, up to 25% differences) put the 99.8th percentile of merged lengths at 426 to 428 nt, the length the cut covers. The refused HDP pairs that align over 12 nt or more imply amplicons of 401 to 427 nt (1st to 99th percentile).
2. **The gap has two parts of similar size: denoising and the merge.** In NIG and KFS, most of it is reads lost in denoising (2.8 to 3.8 per 100), with 2.3 to 2.7 refused at merge. In HDP both are large: 8.5 to 10.3 lost in denoising and 10.8 to 11.0 refused.
3. **In HDP, most refused pairs are two halves of different merged sequences.** In the six samples probed, 18.7% of the pairs that reached the merge were refused (3,101 of 16,586 reads). Of these, 21% had a close overlap (median 33 nt, one mismatch), 56% an overlap with more than 10% mismatches (median 18 nt, four mismatches, which lie a median of 10 to 13 nt from the 3' end of either read) and 23% no overlap of 12 nt at all. In 86% of them, by reads, the forward sequence also merged with another reverse sequence in the same sample and the reverse sequence with another forward one. Where both halves merged elsewhere, the refused combination held a median of 7% (interquartile range 4% to 14%) of the merged reads of the rarer half. That is the pattern expected of chimeras, or of pairs whose two reads were denoised toward different sequences. HDP also had the highest chimera share of the four datasets (about 18% of merged reads were removed as chimeras).
4. **The raw reads of the refused pairs merge, and most are chimeras (added 11 November 2026, below).** So an estimate made from raw reads counts these pairs, and DADA2 refuses them at the merge instead of removing them later as chimeras.

## Added on 11 November 2026: vsearch on the raw reads of the refused pairs

Asked for by the author before the chimera explanation is recorded as more than a hypothesis. `validation/independent_test/raw_merge_refused.R` filtered all 24 HDP samples at arm R (261/179, maxEE 3,2), learned one error model per read direction, denoised and merged as before, and then traced every filtered read pair to its pair of denoised sequences. It found the same counts as the breakdown: of 82,791 pairs that passed the filter, 12,306 were lost in denoising, 57,516 merged and 12,969 were refused (10.3, 47.9 and 10.8 per 100 input pairs). The filtered reads of the refused pairs, and of the merged pairs as a control, were then merged by vsearch with AmpliTrim's two settings, and `raw_merge_summary.py` compared each tolerant merge with that sample's merged DADA2 sequences. Files: `raw_merge_HDP_R/`.

| | Refused by DADA2 | Merged by DADA2 (control) |
|---|---|---|
| Read pairs | 12,969 | 57,516 |
| Merged by vsearch, tolerant (AmpliTrim's estimate) | 97.5% | 98.4% |
| Merged by vsearch, strict (no difference in the overlap) | 69.7% | 74.9% |
| Of the tolerant merges, by reads: chimera of the sample's merged sequences (`uchime_ref`) | 80.5% | 13.4% |
| within 3 differences of one of the sample's merged sequences | 2.5% | 71.7% |
| under 90% identity to every one | 24.9% | 0% |

- **AmpliTrim's estimate counts these pairs.** vsearch merges the reads of 97.5% of them with the tolerant setting, about as often as the reads of the pairs DADA2 merges. With the strict setting it merges 69.7%: in most refused pairs the two reads agree base for base in the overlap. The disagreement appears only after each read is denoised on its own.
- **Most of them are chimeras.** 80.5% of their merged reads are chimeras of the sample's merged DADA2 sequences by `uchime_ref`, against 13.4% of the control. The control's share is close to the 17.5% of merged reads that DADA2's own chimera removal took out in HDP, which suggests the check is not over-calling. Only 2.5% are within 3 differences of a merged DADA2 sequence, so few are ordinary sequences whose reads were denoised inconsistently. vsearch merged both kinds of refusal alike: those where the two denoised sequences had a close overlap (21% of refused pairs, 98.2% to 99.7% merged) and those with a poor one (79%, 97.1% to 98.5%).
- **For the estimate.** In HDP, about 9 of the 20 points of the gap (80% of the 10.8 refused) are chimeric pairs that a raw-read merge counts and DADA2 refuses at the merge. They would have been lost at chimera removal anyway, so they matter for an estimate of merged reads but not for an estimate of the reads left after chimera removal. A chimera check on the tolerant vsearch merges (for example `uchime_denovo`) might predict this part. Most of the rest (10.3 points) are reads lost in denoising.

## Limits

The overlap of a refused pair was measured on the denoised sequences, not on the reads, and indels were not counted in the 24-sample tables (the probe allowed them: 1.6% of refused reads). The probe covers six HDP samples at one setting, with one error model for the six. The raw-read check covers HDP at arm R only. `uchime_ref` was run on reads that still carry sequencing errors, against the sample's own merged sequences, so it measures likeness to a chimera of those sequences, not chimera formation in PCR. The reads of KFS and HDP come from the first 4,000,000 bytes of each file.
