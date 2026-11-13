# Issue #1 of paytonyau/amplitrim, as posted

The text of the issue and its five comments, copied on 9 November 2026 from https://github.com/paytonyau/amplitrim/issues/1. All posts are by nhanhocu (N. T. Ho). Times are those GitHub shows (UTC). Each text is checked against the posted one by the first 16 hex digits of its SHA-256 (line ends as LF, leading and trailing white space removed). Headings inside the posts are moved down two levels.

## Opening post: Independent test of AmpliTrim 0.2.0 on infant gut 16S data: protocol

Posted 2026-11-07T01:52:45Z. SHA-256 (first 16): `fd8d9d1f88577328`.

Payton, as offered by email, this is an independent test of the maxEE rule on infant gut data, posted before any analysis. Results will follow here.

Written on 6 November 2026, before any read file was downloaded. The 96 read files were then downloaded and checked against their MD5 sums on 6 November (finished 18:10 Vietnam time). They have not been opened or analysed, and AmpliTrim and DADA2 have not been run on them. Posted publicly on 7 November 2026, before any analysis.

Investigator: Nhan Thi Ho. Analysis assisted by Claude. The investigator is responsible for all analyses and contents.

#### Question

Does AmpliTrim's maxEE rule hold on independent human gut data, and does the choice of setting change the community profile a user would report?

The AmpliTrim validation states that the rule has not been tested on independent data and that the effect of noisier reads on abundances in rich real communities was not measured. The one independent attempt so far (PRJNA933120) could not decide this, because the deposited Illumina reads had only two quality values.

#### Datasets

Neither dataset was used in the design or validation of AmpliTrim, and neither has an AmpliTrim result yet.

| Label | Accession | Population | Region | Platform | Runs in archive |
|---|---|---|---|---|---|
| CBGS | PRJEB50418 | UK infants, Cambridge Baby Growth and Breastfeeding Study, stool | V3-V4 | MiSeq 2 x 300 | 380 (317 gut, 63 breast milk) |
| NIG | PRJEB31073 | Nigerian infants, stool | V1-V2 | MiSeq 2 x 300 | 169 |

#### What was seen before freezing

For each dataset, the first 1,600 to 3,700 reads of one forward and one reverse file were inspected in the browser for read length, the number of distinct quality values (32 to 33 in all four files) and the first bases of the reads. Archive metadata was read for sample type and read counts. Nothing else was looked at.

#### Sample selection (fixed rule)

1. Keep gut samples only (CBGS: sample title "human gut microbiome").
2. Keep runs with an archive read count of at least 10,000.
3. Sort by run accession, shuffle with a Fisher-Yates shuffle driven by a mulberry32 generator with seed 20261106, and take the first 24.

The chosen runs and their MD5 sums are in `manifest.tsv`. Any run with fewer than 5,000 pairs after primer removal is reported and dropped.

#### Read preparation

- **Primers, CBGS.** Reads appear to start with 341F (`CCTACGGGNGGCWGCAG`) and with a reverse primer lacking its first three bases (`TACNVGGGTATCTAATCC`). Remove both with cutadapt 5.2, anchored at the 5' end, error rate 0.1, discarding pairs without both. If fewer than 90% of pairs carry both, stop and report before going further.
- **Primers, NIG.** Reads appear to start after the primers (custom sequencing primers). Count reads starting with 27F or the 338R primer. If at most 1% do, no trimming. If more do, trim as above and record it.
- **Thinning.** For each sample, draw two disjoint random sets of pairs with a fixed seed: draw a (5,000 pairs) and draw b (up to 5,000 of the remaining pairs).
- **Quality check.** At least 20 distinct quality values must be present in every file, otherwise the sample is reported and dropped.

#### Arms

All arms use AmpliTrim 0.2.0 from PyPI with vsearch 2.32.0 and DADA2 1.38.0 in R, with `truncQ = 2`, `maxN = 0`, `minOverlap = 12`, `maxMismatch = 0`, per-sample inference and consensus chimera removal. Error models are learned per sequencing run if a dataset has more than one flow cell.

| Arm | Reads | Setting |
|---|---|---|
| R | draw a | AmpliTrim's released recommendation, truncation and maxEE |
| D | draw a | AmpliTrim's best truncation at maxEE 2 |
| E | draw a | AmpliTrim's best truncation at maxEE 2,5 |
| Db | draw b | The same truncation and maxEE as arm D. Used only to measure sampling noise |

AmpliTrim is also run on draw b with default settings, for the stability check. Genera are assigned with the RDP classifier 2.13 and its built-in training set at confidence 0.8, unclassified reads kept as their own group.

#### Criteria, set before running

Margins C1 and C2 are the ones in the AmpliTrim register (P46 and P47). The others are set here.

| ID | Check | Met if |
|---|---|---|
| C1 | Filter estimate against DADA2, in arms R, D and E | AmpliTrim's estimated share passing is within 2 points of DADA2's |
| C2 | Benefit of the rule, only if the rule relaxes maxEE above 2 | DADA2 merges at least 2 points more of the pairs in R than in D. If the rule stays at 2, this does not apply and gives no evidence about the rule |
| C3 | Yield estimate against DADA2, in arms R, D and E | AmpliTrim's estimated yield is within 5 points of DADA2's merged share |
| C4 (primary) | Genus profile, R against D and E against D | Median per-sample Bray-Curtis dissimilarity is no larger than the median for D against Db (sampling noise) |
| C5 | Abundant genera, same comparisons | Mean absolute difference in relative abundance is at most 1 percentage point for each of the 10 most abundant genera |
| C6 | Diversity, same comparisons | Median paired difference in ASV-level Shannon index is at most 0.10 in size, and in ASV richness rarefied to a common depth is at most 10% |
| C7 | New ASVs, same comparisons | ASVs absent from D hold at most 2% of the reads of the relaxed arm, and the share of merged reads removed as chimeras rises by at most 2 points |
| C8 | Stability, draw a against draw b | Total truncation differs by at most 10 nt and the maxEE is the same |

Per-sample differences are reported with a bootstrap 95% interval over samples (10,000 resamples, seed 1). If R and D are the same setting, the comparisons of R against D are not applicable and E against D is still reported.

#### Expectations, written before running

- C1 met on both datasets. The AmpliTrim estimate was within 0.8 points on its 12 earlier datasets.
- C3 is uncertain. The yield estimate has overshot by more than 20 points on diverse real samples.
- The reverse reads of both datasets fall to about Q10 to Q13 by base 300, so the rule may relax maxEE at least in NIG. No direction is predicted for C4.

#### How results will be read

- All results are reported whichever way they go, including any criterion not met and any change from this protocol.
- There is no known truth in these samples, so this test measures yield and agreement between settings, not accuracy. Agreement does not show that a setting is correct.
- Two datasets are two independent observations. They cannot show that the rule is valid in general.
- Results do not lead to any change in the released package without a separate decision by its author.

## Comment 1: Addendum 1

Posted 2026-11-07T03:00:03Z. SHA-256 (first 16): `2a7de6a14b4cffa5`.

### Addendum 1: testing the maxEE relaxation on datasets with poorer reads

Written on 7 November 2026, before any read file of these datasets was downloaded beyond the small slices used for screening (described below). AmpliTrim and DADA2 have not been run on them.

Investigator: Nhan Thi Ho. Analysis assisted by Claude. The investigator is responsible for all analyses and contents.

#### Why

In the first test (issue #1), AmpliTrim kept maxEE at 2 on both infant datasets, so criterion C2 could not be assessed. This addendum looks for human gut 16S datasets where the rule should relax, and tests it there. Everything in the original protocol applies unless changed below.

#### How the datasets were found

1. ENA was searched for read runs of human gut metagenome (taxon 408170), Illumina MiSeq, amplicon, paired. That returned 422,383 runs in 2,302 studies.
2. Eligible studies had at least 30 runs with 10,000 or more reads, a typical 2 x 250 or 2 x 300 read length (480 to 602 bases per spot), and were not used in AmpliTrim's validation or in issue #1. That left 1,387 studies.
3. The studies were sorted by accession and shuffled with a mulberry32 generator, seed 20261107. They were screened in that order, one run each, using the first 250 kB of each read file.
4. For each run, the screen measured the number of distinct quality values, estimated insert lengths from read overlap, set the total cut to the 99.5th percentile insert plus 12, found the split with the most pairs passing maxEE 2, and took the 75th percentile of expected errors in each read there. This mimics AmpliTrim's rule. On the two datasets of issue #1 it gave lower values than AmpliTrim's own measure (0.9 against 1.5 in NIG), so it is conservative.
5. The first two studies in that order with at least 20 distinct quality values, 16S rRNA gene amplicons and a screen value of 2 or more in either read were selected. One earlier hit (PRJNA703732, rank 29) was a fungal ITS study and was excluded, since AmpliTrim's rule does not apply to ITS.

The full screening log is in `screening_log.tsv`. Two studies were screened in parallel after the stop and are listed but played no part in the choice.

#### Datasets

| Label | Accession | Population | Region and primers | Screen at maxEE 2 (pass, p75 F/R) | Eligible runs |
|---|---|---|---|---|---|
| KFS | PRJDB8879 | Korean adults, fermented soybean paste trial, stool | V3-V4, 341F / 805R | 60.3%, 2.83 / 2.17 | 96 |
| HDP | PRJNA714241 | Hemodialysis patients, stool | V3-V4, 341F / 805R | 64.2%, 2.93 / 1.87 | 39 |

Both are MiSeq 2 x 300 with primers in the reads.

#### Sample selection

As in the original protocol, with seed 20261107: MiSeq paired runs with an archive read count of at least 10,000, sorted by run accession, shuffled, first 24 taken. The runs are listed in `manifest2.tsv`.

#### Changes to read preparation

- **Partial files.** The full files are about 0.8 GB (KFS) and 2.6 GB (HDP) for 24 samples, too large for the available connection. Only the first 4,000,000 bytes of each compressed file are downloaded. Incomplete trailing records are dropped, and pairs are kept only where forward and reverse read names match. These reads come from the start of each run, which is usually the first tile or tiles of the flow cell, and may differ in quality from the run as a whole. The screen used the same part of the files. MD5 sums cannot be checked on partial files, so the byte count is checked instead.
- **Primers.** Remove 341F (`CCTACGGGNGGCWGCAG`) and 805R (`GACTACHVGGGTATCTAATCC`) with cutadapt 5.2, anchored at the 5' end, error rate 0.1, discarding pairs without both. If fewer than 90% of pairs are kept in a dataset, stop and report.
- **Minimum reads.** A sample needs at least 10,000 pairs after primer removal (two draws of 5,000). Samples below that are reported and dropped. If fewer than 16 samples remain in a dataset, stop and report.

#### New gate

- **G1.** The rule must relax in arm R on draw a (recommended maxEE above 2 in at least one read). If it does not, the dataset is reported and C2 and the R against D comparisons do not apply.

#### Arms and criteria

Arms R, D, E and Db and criteria C1 to C8 are unchanged. In these datasets R and D should differ, so the comparisons of R against D apply.

- **Primary:** C2 (DADA2 merges at least 2 points more pairs in R than in D) and C4 for R against D (median genus Bray-Curtis no larger than D against Db).
- **H1, new and directional:** in the first test, maxEE 2,5 lowered rarefied ASV richness by 10.2% in NIG. Hypothesis: arm R gives lower rarefied ASV richness than arm D. Supported if the median paired difference is below 0 and its bootstrap 95% interval excludes 0. This is reported alongside C6, which keeps its original thresholds.

#### Expectations, written before running

- G1 met in both datasets.
- C1 met in both.
- C2 met in both. Only 60% to 64% of pairs passed maxEE 2 in the screen, so relaxing should keep clearly more.
- C3 uncertain.
- H1 supported in at least one dataset.
- No direction predicted for C4.

#### How results will be read

As in the original protocol. All results are reported, including any criterion not met. These samples have no known composition, so the test measures yield and agreement between settings, not accuracy.

## Comment 2: Results of the original protocol

Posted 2026-11-07T07:41:42Z. SHA-256 (first 16): `028aa0cd8da62596`.

#### Results

All 24 samples per dataset ran, with no changes to the protocol beyond the notes below. Full report, scripts and tables are available on request (or I can open a pull request on the validation archive).

**Settings chosen by AmpliTrim 0.2.0**

| | NIG (V1-V2) | CBGS (V3-V4) |
|---|---|---|
| R, recommended (same as D) | 207/231, maxEE 2 | 217/222, maxEE 2 |
| E, maxEE 2,5 | 180/258, maxEE 2,5 | 179/260, maxEE 2,5 |
| 75th percentile expected errors at cut (F/R) | 1.52 / 1.17 | 0.11 / 0.25 |

**Criteria**

| | NIG (V1-V2) | CBGS (V3-V4) |
|---|---|---|
| C1 filter estimate within 2 points | Met (+0.08, -0.03) | Met (-0.12, 0.00) |
| C2 relaxed rule merges 2 points more | Not applicable, rule kept maxEE 2 | Not applicable, rule kept maxEE 2 |
| C3 yield estimate within 5 points | **Not met** (+6.1 R/D, +9.0 E) | Met (+1.0, +0.4) |
| C4 genus profile E vs D within noise | Met (0.026 vs 0.032) | Met (0.003 vs 0.013) |
| C5 top 10 genera within 1 point | Met (max 0.94) | Met (max 0.25) |
| C6 Shannon and richness | **Not met**: richness -10.2% (95% CI -14.3 to -6.3), Shannon -0.04 | Met |
| C7 new ASVs, chimeras | Met (1.4%, -0.18) | Met (0.5%, -0.22) |
| C8 same setting on second draw | Met, identical | Met, identical |

**What this means**

- The relaxation itself was not tested. The rule stayed at maxEE 2 on both datasets, which looks right for these reads. A dataset with expected errors above 2 at the cut is still needed to test C2.
- The filter estimate was very accurate (within 0.12 points in all six comparisons), and the recommendation was identical on two independent draws.
- The yield estimate overshot by 6 to 9 points on V1-V2. The loss is between passing the filter (75.9%) and merging (69.7%).
- maxEE 2,5 kept more reads (+6.7 and +3.6 points merged) and left genus profiles within sampling noise. On NIG it gave about 10% fewer ASVs per sample (27.8 to 24.5), where two draws at the same setting differed by 0.9%. The 81 lost ASVs held 2.4% of reads. Truncation changed as well, so the two effects cannot be separated. This is a first measurement of the noisier-reads effect your validation lists as unmeasured.
- On NIG, REPORT.md warned that only 41% of pairs merged at full length and suggested amplicons longer than about 590 nt. The longest merged amplicon was 426 nt, so the warning wording may be worth a look for short amplicons.

**Notes:** cutadapt kept 95.0% to 96.2% of CBGS pairs (gate passed), although only 54% of reverse reads matched the primer exactly. The archive read count counts reads in CBGS and pairs in NIG, which did not affect the selection. My expectation that the rule might relax in NIG was wrong.

## Comment 3: Results of addendum 1

Posted 2026-11-07T07:42:05Z. SHA-256 (first 16): `a4e89235fdfe52d1`.

#### Results of addendum 1

The addendum's gates all passed: cutadapt kept at least 94.8% of pairs per sample, every sample had over 16,000 pairs, and the rule relaxed in both datasets (G1). No changes to the addendum.

**Settings chosen by AmpliTrim 0.2.0**

| | KFS (PRJDB8879) | HDP (PRJNA714241) |
|---|---|---|
| R, recommended | 248/192, maxEE 3,3 | 261/179, maxEE 3,2 |
| D, maxEE 2 | 247/193, maxEE 2 | 251/189, maxEE 2 |
| 75th percentile expected errors at the maxEE 2 cut (F/R) | 2.75 / 2.18 | 2.42 / 1.92 |

**Criteria (R against D unless stated)**

| | KFS | HDP |
|---|---|---|
| C1 filter estimate within 2 points | Met (within 0.06) | Met (within 0.25) |
| **C2 R merges 2 points more (primary)** | **Met: +10.9 (95% CI 10.2 to 11.4), 24 of 24 up** | **Met: +3.1 (2.5 to 3.6), 22 of 24 up** |
| C3 yield estimate within 5 points | Met (+3.2 to +4.3) | **Not met (+18.5 to +20.0)** |
| **C4 genus profile within noise (primary)** | **Met: 0.022 vs 0.055** | **Met: 0.020 vs 0.069** |
| C5 top 10 genera within 1 point | Met (max 0.80) | Met (max 0.41) |
| C6 Shannon and richness | Met (+0.03, +3.4%) | Met (+0.004, 0.0%) |
| C7 new ASVs, chimeras | Met (0.4%, +0.5) | Met (1.5%, -0.3) |
| C8 same setting on second draw | Met | Met |
| H1 R lowers richness | Not supported (+3.4%, CI 1.6 to 6.3) | Not supported (0.0%, CI -1.7 to 1.6) |

**What this means**

- This is the first independent evidence on the rule itself, and it is favourable. Where the reads needed it, a one-step relaxation kept clearly more reads and left the reported community unchanged within the limits measured.
- My hypothesis H1, carried over from the NIG result, was wrong for the rule's own setting. The larger setting maxEE 2,5 did lower richness again (KFS -10.7%, HDP -7.7%, NIG -10.2% earlier) and added more new ASVs and chimeras. That supports relaxing only as far as the reads need.
- The yield estimate is now the main weakness: it failed C3 in 2 of 4 datasets. In HDP, 58% of pairs survive denoising at maxEE 2 but only 45% merge, and the estimate does not seem to anticipate that loss. The cuts leave about 12 to 40 nt of overlap, and DADA2 here merges with no mismatches allowed.

**Notes:** reads are the first 4,000,000 bytes of each file, as the addendum states. HDP headers carry no flow cell, so one error model was learned for all samples. HDP also had a high chimera share (about 18% of merged reads).

## Comment 4: Addendum 2

Posted 2026-11-07T08:21:49Z. SHA-256 (first 16): `f38ac6f67a24bb9f`.

### Addendum 2: accuracy against a known truth, with simulated reads

Written on 7 November 2026, before AmpliTrim or DADA2 was run on the simulated datasets described here. Two pilot samples per arm, made with a different seed, were run through AmpliTrim only (not DADA2) to check that the rule relaxes. They are not part of the test.

Investigator: Nhan Thi Ho. Analysis assisted by Claude. The investigator is responsible for all analyses and contents.

#### Why

The original test and addendum 1 measured agreement between settings on real stool, where the true community is unknown. In addendum 1 the rule relaxed to maxEE 3,3 and 3,2, kept more reads and left the reported community unchanged. This addendum asks whether the relaxed setting is also correct, using reads simulated from a community whose every sequence and abundance is known. The AmpliTrim validation notes that its own simulations "lack the long tail of rare sequences". This design includes that tail and adds rare near-identical variants.

#### Truth communities

- **Sequences:** the 466 ASVs of arm D in KFS (addendum 1), real gut V3-V4 sequences of 401 to 428 nt, without primers.
- **Compositions:** the 24 KFS sample profiles from arm D, so each simulated sample has a realistic long tail.
- **Near-twins:** the 30 most abundant ASVs each get a variant 1, 2 or 3 substitutions away (10 of each), at 10% of the parent's abundance wherever the parent occurs. Each twin is at least as far from every other truth sequence as from its parent.
- **Chimeras:** 4% of each sample's reads come from 50 bimeras between abundance-weighted parents, with breakpoints at random between position 100 and 100 bases from the end.
- Seed 20261107 for the design and 20261108 for the reads. 10,000 pairs per sample.

#### Reads: two arms that differ only in how errors are made

Both arms take each read's quality string from a random real KFS read pair (primer-trimmed, draw a of addendum 1). So the quality profile, read lengths and AmpliTrim's view of the reads are the same as in real KFS data.

| Label | Errors |
|---|---|
| SIM-I (ideal) | A substitution with exactly the probability the quality score states, 10^(-Q/10), equally likely to each other base |
| SIM-T (realistic) | Substitutions at the rates DADA2 learned from KFS for that read's flow cell. At high quality these are 3 to 20 times the nominal rate (for example 0.3% to 0.7% at Q38 against 0.02% nominal) |

No indels are simulated. The difference between the arms tests the one thing maxEE depends on: whether quality scores describe the errors truthfully.

InSilicoSeq 2.0 was piloted first. Its built-in MiSeq error models gave reads too good for this amplicon (75th percentile expected errors at most 1.1 at the cut), so the rule did not relax and it was not used. Its substitutions also follow the quality scores, as in SIM-I.

#### Pipeline

Everything follows the original protocol (arms R, D, E, Db, the same DADA2 and AmpliTrim settings, two disjoint draws of 5,000 pairs per sample) except that there are no primers to remove. DADA2 learns one error model per arm, because each simulated sample mixes quality strings from several flow cells.

#### Gate

- **G1.** The rule must relax in arm R of each simulated arm (the pilot gave maxEE 3,3 in both). If it does not, the R against D comparisons do not apply.

#### Truth criteria (new), each comparing R with D on the same reads

A true sequence counts as present in a sample when it contributed at least 10 reads to that draw. An ASV counts as recovered only on an exact sequence match.

| ID | Measure | Met if |
|---|---|---|
| T1 | Recall of true sequences (excluding twins) | Median per-sample difference, R minus D, is at least -2 points |
| T2 | Spurious reads: share of reads in ASVs that are neither a true sequence nor a simulated chimera | Median difference at most +0.5 points |
| T3 (primary) | Bray-Curtis between the inferred and the true profile at sequence level | Median difference at most +0.01 |
| T4 | Near-twin recovery, pooled over samples | R recovers at most 5 points fewer twins than D |
| H2 (directional) | Arm E against D, near-twin recovery | E recovers fewer twins than D: median per-sample difference below 0, with a bootstrap 95% interval excluding 0 |

Criteria C1, C2, C3 and C8 of the original protocol are also reported. C4 to C7 are reported but are less relevant here, because the truth is known. Intervals are bootstrap 95% intervals over the 24 samples, with seed 1. Arm Db against the truth is reported to show sampling noise.

#### Expectations, written before running

- G1 met in both arms.
- C1 and C2 met in both.
- SIM-I: R no worse than D on T1 to T4, because errors behave exactly as maxEE assumes.
- SIM-T: uncertain. Reads that pass maxEE 3 carry more errors than their scores state, so some loss of accuracy is possible.
- H2 supported in at least one arm.

#### How results will be read

All results are reported. A simulation shows what happens when errors behave as modelled. It does not include PCR errors, contamination or the full complexity of a real run, so it complements a real mock community rather than replacing one.

## Comment 5: Results of addendum 2

Posted 2026-11-07T08:58:23Z. SHA-256 (first 16): `bb02901ef342af84`.

#### Results of addendum 2 (simulation with known truth)

Both arms passed G1: AmpliTrim chose maxEE 3,3 in each. Two bugs in the evaluation script were fixed after the first run, without changing any criterion: chimera names containing a near-twin's name were misread, and 89 of 1,200 simulated chimeras that are identical to a true sequence were counted as chimeras. They now count as that true sequence.

**R (recommended, maxEE 3,3) against D (maxEE 2), same reads**

| | SIM-I (errors match quality scores) | SIM-T (DADA2's learned, higher error rates) |
|---|---|---|
| T1 recall of true sequences | Met: 96.9% vs 95.1% | Met: 57.3% vs 55.5% |
| T2 reads in spurious ASVs | Met: 0.39% vs 0.41% | Met: 0.23% vs 0.11% |
| **T3 distance to truth (primary, median Bray-Curtis)** | **Met: 0.059 vs 0.069, closer in 21 of 24 samples** | **Met: 0.217 vs 0.205 (difference +0.001, CI -0.009 to 0.029)** |
| T4 near-twins recovered | Met: 33 vs 30 of 170 | Met: 3 vs 3 of 170 |
| C2 pairs merged | +10.6 points | +9.5 points |
| C1 / C3 / C8 | Met (within 0.07 / 0.7) | Met (within 0.08 / 4.1) |

**maxEE 2,5 (arm E) against D**

| | SIM-I | SIM-T |
|---|---|---|
| T1 recall | Not met: -2.4 points | **Not met: -12.6 points** |
| T2 spurious reads | Met: +0.4 | **Not met: +3.7 points** |
| T3 distance to truth | Met | **Not met: +0.082, worse in 23 of 24 samples** |

**What this means**

- Against a known truth, the rule's relaxed setting was at least as accurate as maxEE 2 and kept about 10 points more reads. With errors that match the scores, it was slightly more accurate.
- maxEE 2,5 was clearly harmful when real error rates exceed what the scores say, consistent with the richness loss it caused in three of four real datasets. This supports the rule's design of relaxing only as far as the reads need.
- H2 (2,5 loses near-twins) was not supported: near-twins at 10% of their parent were rarely recovered under any setting, so the test had little room to show a difference.
- The yield estimate was accurate in simulation, which suggests its overshoot on HDP and NIG comes from features of real runs (length variation, chimeras, merge failures) that the simulation does not include.

**Limits:** no indels, PCR errors or contamination. SIM-T's error rates include more than sequencing error, so its absolute accuracy is pessimistic. A real mock community with poor reads remains the stronger test.
