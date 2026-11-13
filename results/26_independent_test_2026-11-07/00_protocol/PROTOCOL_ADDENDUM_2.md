# Addendum 2: accuracy against a known truth, with simulated reads

Written on 7 November 2026, before AmpliTrim or DADA2 was run on the simulated datasets described here. Two pilot samples per arm, made with a different seed, were run through AmpliTrim only (not DADA2) to check that the rule relaxes. They are not part of the test.

Investigator: Nhan Thi Ho. Analysis assisted by Claude, which wrote this addendum, the simulator and the scripts. The investigator is responsible for all analyses and contents.

## Why

The original test and addendum 1 measured agreement between settings on real stool, where the true community is unknown. In addendum 1 the rule relaxed to maxEE 3,3 and 3,2, kept more reads and left the reported community unchanged. This addendum asks whether the relaxed setting is also correct, using reads simulated from a community whose every sequence and abundance is known. The AmpliTrim validation notes that its own simulations "lack the long tail of rare sequences". This design includes that tail and adds rare near-identical variants.

## Truth communities

- **Sequences:** the 466 ASVs of arm D in KFS (addendum 1), real gut V3-V4 sequences of 401 to 428 nt, without primers.
- **Compositions:** the 24 KFS sample profiles from arm D, so each simulated sample has a realistic long tail.
- **Near-twins:** the 30 most abundant ASVs each get a variant 1, 2 or 3 substitutions away (10 of each), at 10% of the parent's abundance wherever the parent occurs. Each twin is at least as far from every other truth sequence as from its parent.
- **Chimeras:** 4% of each sample's reads come from 50 bimeras between abundance-weighted parents, with breakpoints at random between position 100 and 100 bases from the end.
- Seed 20261107 for the design and 20261108 for the reads. 10,000 pairs per sample.

## Reads: two arms that differ only in how errors are made

Both arms take each read's quality string from a random real KFS read pair (primer-trimmed, draw a of addendum 1). So the quality profile, read lengths and AmpliTrim's view of the reads are the same as in real KFS data.

| Label | Errors |
|---|---|
| SIM-I (ideal) | A substitution with exactly the probability the quality score states, 10^(-Q/10), equally likely to each other base |
| SIM-T (realistic) | Substitutions at the rates DADA2 learned from KFS for that read's flow cell. At high quality these are 3 to 20 times the nominal rate (for example 0.3% to 0.7% at Q38 against 0.02% nominal) |

No indels are simulated. The difference between the arms tests the one thing maxEE depends on: whether quality scores describe the errors truthfully.

InSilicoSeq 2.0 was piloted first. Its built-in MiSeq error models gave reads too good for this amplicon (75th percentile expected errors at most 1.1 at the cut), so the rule did not relax and it was not used. Its substitutions also follow the quality scores, as in SIM-I.

## Pipeline

Everything follows the original protocol (arms R, D, E, Db, the same DADA2 and AmpliTrim settings, two disjoint draws of 5,000 pairs per sample) except that there are no primers to remove. DADA2 learns one error model per arm, because each simulated sample mixes quality strings from several flow cells.

## Gate

- **G1.** The rule must relax in arm R of each simulated arm (the pilot gave maxEE 3,3 in both). If it does not, the R against D comparisons do not apply.

## Truth criteria (new), each comparing R with D on the same reads

A true sequence counts as present in a sample when it contributed at least 10 reads to that draw. An ASV counts as recovered only on an exact sequence match.

| ID | Measure | Met if |
|---|---|---|
| T1 | Recall of true sequences (excluding twins) | Median per-sample difference, R minus D, is at least -2 points |
| T2 | Spurious reads: share of reads in ASVs that are neither a true sequence nor a simulated chimera | Median difference at most +0.5 points |
| T3 (primary) | Bray-Curtis between the inferred and the true profile at sequence level | Median difference at most +0.01 |
| T4 | Near-twin recovery, pooled over samples | R recovers at most 5 points fewer twins than D |
| H2 (directional) | Arm E against D, near-twin recovery | E recovers fewer twins than D: median per-sample difference below 0, with a bootstrap 95% interval excluding 0 |

Criteria C1, C2, C3 and C8 of the original protocol are also reported. C4 to C7 are reported but are less relevant here, because the truth is known. Intervals are bootstrap 95% intervals over the 24 samples, with seed 1. Arm Db against the truth is reported to show sampling noise.

## Expectations, written before running

- G1 met in both arms.
- C1 and C2 met in both.
- SIM-I: R no worse than D on T1 to T4, because errors behave exactly as maxEE assumes.
- SIM-T: uncertain. Reads that pass maxEE 3 carry more errors than their scores state, so some loss of accuracy is possible.
- H2 supported in at least one arm.

## How results will be read

All results are reported. A simulation shows what happens when errors behave as modelled. It does not include PCR errors, contamination or the full complexity of a real run, so it complements a real mock community rather than replacing one.
