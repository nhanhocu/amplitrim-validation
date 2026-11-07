# AmpliTrim test register

**One standard battery, run the same way on every dataset.** Every dataset (each region, each study, each mock community) goes through the same steps and produces the same
columns: AmpliTrim against DADA2 (filter and yield), against FIGARO (like for like and end to end), and against the simple DADA2 alternatives. A dataset with expected sequences
(a mock community) gets the same battery plus the same truth columns. Anything that does not fit this mould is an *additional analysis* (section 5): supplement or removed.

- **Stage.** `DEV` = used to build or verify the tool (section 7, supplement only). `TEST` = reported in the manuscript.
- **Where results are written.** `C:\data\overnight\OVERNIGHT_SUMMARY.md`; `python validation\check_build.py --table` writes the test tables (one for 16S, one for ITS, one for the
  expected sequences) to `TEST_TABLE.md`; `--todo` prints what is left; `--decide` applies the decision rule of section 6.
- **Provenance.** The overnight runs used the build printed as `bd4e64353c` on Windows (`6f3cb5c6f9` when its files are hashed in sorted order: the same code; earlier ids depended on the
  operating system's file order). Software: DADA2 1.40.0, cutadapt 5.2, Python 3.12; vsearch and R versions are printed by `python validation\check_build.py`. A last full run on the final
  build is listed in section 8.

---

## 1. Datasets

| ID | Dataset | Marker, region | Reads | Samples | Stage | Config key | Expected sequences |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D1 | DADA2 package example reads | 16S V4 | MiSeq 2x250 | 2 samples, 1,500 pairs each | DEV | - | - |
| D2 | Simulated communities (`validation\simulated\`) | 16S-like, ITS-like | 2x250 to 2x283 | 2 to 5 samples | DEV | - | yes (simulated) |
| D3 | PRJEB42528 | 16S V1-V2 (27F/338R) | MiSeq 2x300 | 33 samples, 1.43 million pairs | TEST | `v1v2` | - |
| D4 | PRJEB67797, mock community A | 16S V1-V3 (27F-YM/519R) | MiSeq 2x300 | 23 mock samples and 13 controls; 6 high-input samples | TEST | `mockA_high`, `mockA_all` | yes (rebuilt from the authors' repository; not independent) |
| D5 | PRJNA574030 | 16S V4 | see `--download v4` | 36 soil samples | TEST (used in development, so run again with the final build) | `v4` | - |
| D6 | PRJEB58189, UK Crop Microbiome Cryobank | ITS (ITS1-Fl2/ITS2) | MiSeq 2x250 | 37 spring-wheat samples; 8 at full depth | TEST (case study) | `its` | - |
| D7 | PRJEB67827, independent mock (Zymo D6321) | 16S V1-V3 | MiSeq 2x300 | 94 paired runs of several kinds | TEST | `mockB` | yes (Zymo's own sequences) |
| D8 | V3-V4 2x250 (candidates of PRJEB58189) | 16S V3-V4 | MiSeq 2x250 | - | TEST | `v3v4` | - |
| D9 | PRJNA971391 | 16S V4-V5 | - | - | TEST | `v4v5` | - |
| D10 | PRJNA915241, sputum, region V1-V2 (QIAseq 16S/ITS panel; the same 33 samples in every region) | 16S V1-V2 | MiSeq 2x300 | 33 sputum samples and a ZymoBIOMICS standard | NOT PLANNED (considered and dropped) | `sputum_v1v2` | the standard's own sequences, if its runs are in the project |
| D11 | PRJNA915241, sputum, region V3-V4 (QIAseq 16S/ITS panel; the same 33 samples in every region) | 16S V3-V4 | MiSeq 2x300 | 33 sputum samples and a ZymoBIOMICS standard | NOT PLANNED (considered and dropped) | `sputum_v3v4` | the standard's own sequences, if its runs are in the project |
| D12 | PRJNA915241, sputum, region V5-V7 (QIAseq 16S/ITS panel; the same 33 samples in every region) | 16S V5-V7 | MiSeq 2x300 | 33 sputum samples and a ZymoBIOMICS standard | NOT PLANNED (considered and dropped) | `sputum_v5v7` | the standard's own sequences, if its runs are in the project |
| D13 | PRJNA915241, sputum, region V7-V9 (QIAseq 16S/ITS panel; the same 33 samples in every region) | 16S V7-V9 | MiSeq 2x300 | 33 sputum samples and a ZymoBIOMICS standard | NOT PLANNED (considered and dropped) | `sputum_v7v9` | the standard's own sequences, if its runs are in the project |
| D14 | PRJEB34919, inter-laboratory mock communities MCM2a and MCM2b [O'Sullivan et al. 2021], V4-V6 (about 564 bp) | 16S V4-V6 | MiSeq 2x300 (a real tight-overlap case) | 6 samples (2 materials x 3 repeats); the shotgun runs of the project are left out | TEST (held-out) | `mcm_v46` | yes: the 15 bacteria, quantified by digital PCR; the sequences are built from their genomes |
| D15 | PRJEB34919, the same materials, V1-V2 (about 337 bp) | 16S V1-V2 | MiSeq 2x300 | 6 samples | TEST (held-out; optional) | `mcm_v12` | as D14 |

---

## 2. The standard battery (every TEST dataset)

One command runs it. The steps `battery`, `coverage_levels`, `landscape`, `per_sample_rank` and `stability` take every registered dataset; for the new datasets (`v4`, `mockB`, `v3v4`, `v4v5`, registered with `--download` and `--prepare`) the battery step is `--only extra_datasets`:

```bat
python validation\check_build.py --run --only battery,coverage_levels,landscape,per_sample_rank,stability
python validation\check_build.py --table
```

| ID | Question | Output (a column of the test table) | Condition | Criterion |
| --- | --- | --- | --- | --- |
| B1 | Does the filter prediction match DADA2's pass rate? | largest difference over the maxEE settings (points) | three maxEE settings (the dataset's own, 1 and 5; for ITS 1, 2 and 5) | C1: within 2 points |
| B2 | How far is the yield estimate from the share DADA2 merged, and does it rank the settings? | offset and ratio (mean, range) and the rank correlation across the same settings | at least three settings | C2: ranks agree; C3: offset constant |
| B3 | What do the simple DADA2 alternatives cost? | AmpliTrim minus no truncation (ITS: minus a 200/200 truncation), paired per sample, with the 95% interval | at least 10 samples for the interval | C4 for ITS: at least 10 points |
| B4 | AmpliTrim against FIGARO, (a) like for like at FIGARO's own maxEE and (b) end to end: AmpliTrim's default against FIGARO as it ships | both differences, paired per sample, with the 95% interval | 16S only (FIGARO cannot run on mixed-length ITS reads); the standalone steps (`--run --only figaro_mockA,figaro_v1v2`) run the same comparison | C11: like-for-like interval within +/-1 point |
| B5 | What does the share of the longest amplicons left out cost and buy? | merged points from 1% to 0.2% (and with expected sequences: variants and strains) | levels 1%, 0.5%, 0.2%, 0.1%, 0% | C14 (section 6) |
| B6 | Is the recommendation near the best of a DADA2 grid around it? | points below the best setting that still covers the amplicons | 5 x 5 grid in steps of 10 nt, DADA2 at every cell | C13: within 1 point |
| B7 | Does the estimate follow individual samples? | per-sample rank correlation | at least 10 samples, at AmpliTrim's recommendation | C8: at least 0.80 |
| B8 | Does the recommendation depend on the subsample? | spread of the recommended truncation (nt) and yield (points) | three subsample sizes, two strides | C7: 10 nt, 1 point |

**Truth add-on (a dataset with expected sequences; on automatically when a reference is registered).** The same methods of B3 and B4 (AmpliTrim, FIGARO, no truncation), every coverage level
of B5 and every cell of B6 are also scored: variants and strains recovered, reads in ASVs identical to an expected sequence, ASVs outside the reference. The test table prints them in a third table.
Criterion C6: no variant longer than total - 12 nt is ever recovered.

---

## 3. Outcome matrix (what has been run)

`done` = run with the battery or an earlier equivalent; `-` = not applicable; `pending` = to run. Numbers in section 4.

| Dataset | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 | Truth |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D3 V1-V2 | done | done | done | done (like for like +0.1; end to end +2.0) | done (0.4 points) | done (0.1) | done (0.63) | done (1 nt) | - |
| D4 mock A | done (-1.1) | done | done (+10.5) | done (-0.2; -1.9) | done | done (0.3) | done (0.60; 23 samples) | done (0 nt) | done |
| D5 V4 | done (+0.0) | done (offset +30.4) | done (+13.0) | done (+2.0; +4.3) | done (gain 2.6) | done (6.8: not met) | done (0.70) | done (3 nt) | - |
| D6 ITS | done | done | done | - | - | - | - | - | - |
| D7 mock B | pending | pending | pending | pending | pending | pending | pending | pending | pending |
| D8 V3-V4 | pending | pending | pending | pending | pending | pending | pending | pending | - |
| D9 V4-V5 | pending | pending | pending | pending | pending | pending | pending | pending | - |
| D10 to D13 sputum (PRJNA915241) | not planned | not planned | not planned | not planned | not planned | not planned | not planned | not planned | not planned |
| D14 mock V4-V6 (6 samples) | pending (one run of 12 failed to download) | pending | pending | pending | pending | pending | not possible (6 samples) | pending | pending |
| D15 mock V1-V2 (6 samples) | done (-0.1) | done (offset +0.2, ratio 1.00) | done (+69.9) | done (0.0; +2.3) | done (0.0) | done (0.1) | not possible (6 samples) | done (3 nt) | pending (no reference) |

---

## 4. Outcomes so far

| ID | Dataset | Outcome |
| --- | --- | --- |
| B1 | V1-V2 | within 0.1 points at 5 settings |
| B1 | ITS | within 0.1 (5 settings, 5,000 pairs per sample); within 0.2 (3 settings, full depth) |
| B1 | mock A (clipped to 2x250) | 1.2 to 1.4 points low |
| B2 | V1-V2 | offset +6.4 (5.7 to 7.7); ratio 0.92 (0.88 to 0.94); rank 1.00 |
| B2 | mock A | offset +2.3 at maxEE 2,6, ratio 0.97; clipped: -0.7 (-1.9 to 0.0), ratio 1.02 |
| B2 | ITS | 5,000 pairs: +22.9 (13.8 to 30.4), ratio 0.65, rank 1.00. Full depth: +8.5 (4.7 to 11.2), ratio 0.88, rank 1.00 |
| B3 | V1-V2 | 84.2% merged at AmpliTrim's setting; 77.1% at 230/200; 48.3% at 260/260 (fixed settings, not paired) |
| B3 | ITS | 200/200 costs 23.5 points (95% interval 21.8 to 25.2), in 37 of 37 samples |
| B4 | V1-V2 | like for like (maxEE 2,1): 82.3% against 82.2%, no interval; end to end 84.2% against 82.2% |
| B5 | mock A | 1% and 0.5%: 257/260 (78.4%, 35/39 variants, 11/13 strains); 0.2% and 0.1%: 257/263 (78.2%, 36/39, 12/13); 0%: 268/280 (73.2%, 36/39, 13/13) |
| B5 | V1-V2 | 1%: 196/159 (83.9% merged); 0.2%: 195/168 (83.5%), a cost of 0.4 points; 0%: 279/280 (29.4%), about 54 points (DADA2 at 5,000 pairs per sample; no expected sequences) |
| B6 | V1-V2 | 0.1 points below the best of 9 (196/159 82.6%, best 186/169 82.7%); merging falls to 71.8 to 72.0% at 10 nt below the floor of 355 nt and to 60.9% at 20 nt below (3,000 pairs per sample) |
| B7 | V1-V2 | 0.63 over 33 samples (criterion not met); offsets +1.4 to +14.2, mean +6.5 |
| B6 | mock A | 0.3 points below the best of 25 runs; merging collapses below the coverage floor (54% at 10 nt below, 76% at the floor) |
| B7 | mock A | 0.60 over 23 samples; offsets 0.0 to +10.3 (mean +2.6) |
| B8 | mock A | 277/240 in every run (six samples); 274/243 to 275/242 (23 samples); yield varies by 0.5 and 0.2 points |
| Truth | mock A | 10 settings: no variant longer than the limit recovered. 257/260 at maxEE 2,6: 35/39 variants, 11/13 strains, 15 ASVs outside; authors' 279/263: 37/39, 13/13, 7; 265/270: 36/39, 13/13, 12 |
| B1 | V4; inter-laboratory mock V1-V2; mock A at full length | +0.0; -0.1; -1.1 points at the default maxEE (final build, 5,000 pairs per sample) |
| B2 | V4 | offset +30.4 (+29.5 to +30.9), ratio 0.69, rank 1.00 over 3 settings (5,000 pairs per sample) |
| B2 | inter-laboratory mock V1-V2 | offset +0.2 (-0.1 to +0.4), ratio 1.00, rank 1.00 over 3 settings; about 28 ASVs |
| B2 | mock A; V1-V2 (final build) | +2.4 (+0.3 to +3.9), 0.95, rank 1.00 over 4 settings; +6.3 (+6.2 to +6.4), 0.93, rank 1.00 over 4 settings |
| B3 | AmpliTrim minus no truncation (ITS: minus 200/200) | mock A +10.5 (+9.1 to +12.1); V1-V2 +55.0 (+53.6 to +56.4); V4 +13.0 (+12.2 to +13.9); inter-laboratory mock +69.9 (+66.4 to +73.6); ITS +16.1 (+14.3 to +17.9), which differs from the earlier +23.5 (+21.8 to +25.2) and is to be reconciled |
| B4 | like for like (at FIGARO's maxEE) | V1-V2 +0.1 (-0.4 to +0.6); mock A -0.2 (-0.8 to +0.6); inter-laboratory mock 0.0; V4 +2.0 (+1.6 to +2.4). The two six-sample intervals are not reliable |
| B4 | end to end (AmpliTrim default minus FIGARO as shipped) | V1-V2 +2.0 (+1.5 to +2.5); mock A -1.9 (-3.9 to -0.6; FIGARO's maxEE 3,4 is looser than 2,6); V4 +4.3 (+3.7 to +4.9); inter-laboratory mock +2.3 (+2.2 to +2.5) |
| B5 | V4; inter-laboratory mock | V4: 120/118 to 124/115 gained 2.6 points (64.3% to 66.8%); inter-laboratory mock: 160/165 at both levels |
| B6 | V4; inter-laboratory mock | V4 59.6% against 66.4% for the best setting (130/108): 6.8 points below, criterion not met; inter-laboratory mock 0.1 points |
| B7 | V4 | 0.70 over 36 samples (criterion not met; third dataset below 0.80 after 0.60 and 0.63) |
| B8 | V1-V2; V4; inter-laboratory mock | 1, 3 and 3 nt |
| Truth | mock A at 5,000 pairs per sample (final build) | AmpliTrim maxEE 1 / 2,6 / 5: 28 / 29 / 32 variants, 10 / 10 / 11 of 13 strains, 42.6 / 74.6 / 84.2% merged; FIGARO 31 variants, 76.4%; no truncation 29 variants, 64.2% merged and 97.70% of reads in identical ASVs (99.75% with AmpliTrim's truncation) |

---

## 5. Additional analyses (not part of the standard battery) and what to do with them

| ID | Analysis | Command | Outcome | Disposition |
| --- | --- | --- | --- | --- |
| A1 | AmpliTrim's truncation against the authors' published one (mock A) | `--run --only mock_grid` | the pre-set non-inferiority test failed: 2 variants and 2 strains fewer, 8 more ASVs (mainly chimeras), 6.1 points more merged pairs | main text, as the truth comparison of mock communities (a published setting exists for mock A only); for mock B the published setting, if any, replaces it |
| A2 | Dilution series at three truncations | `--run --only mock_dilutions` | 185 of 198 present variants at 257/260; 11 of 13 misses longer than the limit; 193 and 194 at 265/270 and 279/263 | supplement (needs the authors' table; mock A only) |
| A3 | ASV classes (contaminant, chimera, error variant, unlisted variant) | `--run --only asv_classify` | the excess at 257/260 is mainly chimeras (5 against 1, 0.01% of reads) | supplement |
| A4 | Tracing the missed variants | `--run --only mock_miss_trace` | long variants lost at merging; two mergeable ones absorbed by a 1 or 2 edit neighbour | supplement |
| A5 | Mock A clipped to 2x250 (tight overlap, emulated) | `--run --only mock_clip250` | AmpliTrim 249/249 equals no truncation; 4 of 13 strains at any setting | supplement (an emulation; replace by real V3-V4, D8) |
| A6 | Pooled DADA2 inference | `--run --only mock_pooled` | recovery unchanged; full pooling adds 13 ASVs outside the reference | supplement |
| A7 | Chimera removal in ITS under other settings | `--run --only its_chimeras` | 0.2%, 0.6%, 1.5% against 13.9% in the authors' pipeline: not explained | supplement, or remove: it concerns the authors' pipeline, not AmpliTrim |
| A8 | Effect of maxEE on accuracy | (*as run:* `max_ee_sweep.py READY --trunc 257,260 --max-ee 2,2 2,3 2,5 2,6 3,5 --reference ...`) | merged 56.4% to 79.7%; reads in identical ASVs 99.76 to 99.79% | superseded by the three maxEE settings of the battery (B1, B2) and the truth add-on |
| A9 | Calibration at full depth (V1-V2, ITS) | `--run --only v1v2_fulldepth`; ITS: `compare_methods.py ... --marker its --amplitrim-max-ee 1 2 5 --only ERR... --pairs 0` | merged / filtered 0.84 at full depth, 0.63 at 5,000 pairs (0.81 in the authors' pipeline) | main text, as a depth variant of B2 on every dataset (a `--pairs 0` run of the battery) |

---

## 6. Decision rule for the default of --allow-unmergeable (C14)

Stated before the evidence: change the default from 1% to 0.2% if, on at least two datasets with expected sequences, it recovers at least one more strain on one and fewer variants or strains on none,
and across all datasets it costs a median of at most 2 points of merged pairs and at most 5 on any. `python validation\check_build.py --decide` applies it to the saved B5 results.
Today: **UNDETERMINED**: mock A passes (0.2 points, +1 variant, +1 strain, 4 fewer ASVs outside the reference), V1-V2 costs 0.4 points (196/159 to 195/168), V4 gains 2.6 points and the inter-laboratory mock costs 0.0, so the cost condition holds on all four datasets; only one dataset has expected sequences.

---

## 7. Development stage (supplement only)

Built and verified the tool; reproducible; **not** results of the manuscript.

| ID | Check | Data and command | Outcome |
| --- | --- | --- | --- |
| S1 | Exactness of the filter replica against DADA2's `filterAndTrim` | D1; `python validation\filter_grid_check.py` (`--quick` for a small grid); 2 samples x 5 x 5 truncations x 4 maxEE | 200 of 200 identical (pass rates 26.3% to 100%) |
| S2 | ITS mode: pairs kept, mean cut length, expected errors, errors of added reads | D2: `python validation\simulated\its_sim.py OUT`; the package test recomputes in plain Python | identical: 6,862, 8,611 and 4,721 pairs kept; cut lengths 210.00, 217.76 and 194.55 nt; 0.2901 and 3.0129 expected errors per added read |
| S3 | Coverage rule: the longest taxon DADA2 recovers against the total | D2: `python validation\simulated\coverage_sim.py OUT noisy_reverse`; DADA2 at totals 511, 505, 480, 470 | total - 12 nt at every total; none of 172 longer taxa recovered |
| S4 | "Beaten by" rule and FIGARO at equal maxEE on a simulated community | D2: `coverage_sim.py OUT both_degrade` | both chose 265/249 at maxEE 2,4 (75.1%); AmpliTrim's default chose 277/237 (55.9%) |
| S5 | What a looser maxEE keeps | D2: `python validation\simulated\staggered_mock_sim.py OUT` | relaxing the reverse limit 2 to 5 raised the share passing 78% to 96% |
| S6 | Chimera removal in variable-length reads | D2: `python validation\simulated\chimera_sim.py OUT` | 6.5% removed when 7.8% were planted |
| S7 | Primer removal | real reads, `real_data.py` | a single cutadapt pass let 0.10% of 3.09 million pairs through untrimmed; fixed |
| S8 | Effect of no truncation on real V4 reads | D5 | superseded by the battery on D5 (23% passed without truncation against 88% with it) |
| S9 | Software | `python -m pytest tests -q`; `python -m pyflakes amplitrim validation tests` | 250 tests; no findings |

---

## 8. Still to run, and further tests recommended

**To run: one command, overnight** (`python validation\check_build.py --overnight`). It finds the folders and FIGARO; checks the machine; downloads, trims and registers V4 (PRJNA574030) and both regions of
the inter-laboratory mock (PRJEB34919: the two regions share one download, the shotgun runs are left out by the MiSeq filter, and the primers are those of the paper's Table 3); runs every step (a step that
covered other datasets is repeated, finished ones are kept; one dataset failing does not lose the others); keeps Windows awake; and writes `MORNING_REPORT.md` (the step verdicts, the test tables, the decision,
what needs you). **Still by hand:** mock B (choose its runs, download and prepare them; its reference is Zymo's D6321 file: `python validation\check_build.py --make-reference mockB=D6321.refseq.zip` reads the rRNA gene files, cuts them between the primers, collapses identical copies and registers the result), the expected sequences of the inter-laboratory mock (a FASTA of the 15 bacteria, for the truth columns), V4-V5 (primers). Mock A keeps the reference rebuilt from the authors' repository (14 species); the D6300 standard has 8 bacteria of which 6 are in mock A, so it can check those six independently but cannot replace it.
A last full run on the final build (`--run --fresh`) so that the manuscript cites one build id.

**Further tests that would strengthen the evidence, in order of value:**

1. **Held-out datasets, in this order: D14 (the real tight-overlap case with an independent truth: it replaces the clipped-mock emulation A5 and the V3-V4 2x250 item D8), D7, D5, then D9.** Mock A informed design decisions and V4 was used in development. Only datasets that were never looked at give an unbiased test: D7, D8, D9. Run them with the margins fixed in advance.
   *Considered and dropped:* the sputum study (PRJNA915241, D10 to D13: four regions on the same 33 samples, a ZymoBIOMICS standard). It would add held-out regions, but the primers are not given in the paper (phased primers), the run names are unknown, the four regions are one study and not four, it gives no tight-overlap case, and the mock may not be in the project. Its catalog entries (`sputum_v1v2` to `sputum_v7v9`) remain in `check_build.py` if it is wanted later, for example if a reviewer asks for clinical samples.
2. **A second independent truth.** One mock with expected sequences that do not come from a DADA2 run (D7); ideally a second, with a different community and region.
3. **FIGARO on at least three datasets with paired intervals** (B4), so the "ties FIGARO" claim does not rest on one study.
4. **A "quality-plot rule" baseline** for B3: truncate each read where the median quality falls below Q30, as many users do, to compare AmpliTrim with common practice and not only with FIGARO and no truncation.
5. **Platform diversity.** A NovaSeq run (binned quality scores) and a 2x150 run, for the filter replica (B1) and the calibration (B2).
6. **Read-depth variants.** The battery at 5,000 pairs per sample and at full depth on every dataset (the depth effect on B2 is so far seen only in ITS).
7. **A second ITS study** if ITS claims are kept: B1, B2, B3 and the maxEE rows on another amplicon and platform.
8. **Runtime and memory** against the number of pairs and samples (a software-paper item).
