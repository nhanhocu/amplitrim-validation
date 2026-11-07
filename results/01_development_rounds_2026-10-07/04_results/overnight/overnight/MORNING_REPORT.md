# AmpliTrim overnight run: morning report

Started 2026-10-06 22:24, finished 2026-10-07 02:05; overnight.py exit code 0 (0 = no step failed).

## What the run did

| phase | outcome |
| --- | --- |
| find the folders and FIGARO | v4 |
| check the machine | ok |
| dataset v4 | already registered |
| dataset mcm_v46 | download failed (exit 1); run --download mcm_v46 to see why |
| dataset mcm_v12 | downloaded, trimmed and registered |
| overnight steps | exit code 0 |

## Steps

| step | status | minutes | criteria not met | datasets |
| --- | --- | --- | --- | --- |
| mock_grid | ok | 28.2 | 4 | - |
| asv_classify | ok | 0.1 | 0 | - |
| mock_clip250 | ok | 8.1 | 0 | - |
| figaro_mockA | ok | 5.1 | 0 | - |
| mock_dilutions | ok | 20.2 | 0 | - |
| coverage_levels | ok | 46.9 | 0 | mcm_v12, mockA_high, v1v2, v4 |
| landscape | ok | 51.0 | 1 | mcm_v12, mockA_high, v1v2, v4 |
| mock_miss_trace | ok | 3.0 | 0 | - |
| mock_pooled | ok | 8.9 | 0 | - |
| stability | ok | 24.8 | 0 | mcm_v12, mockA_all, mockA_high, v1v2, v4 |
| per_sample_rank | ok | 16.4 | 3 | mcm_v12, mockA_all, v1v2, v4 |
| its_chimeras | ok | 99.2 | 0 | - |
| figaro_v1v2 | ok | 11.4 | 0 | - |
| v1v2_fulldepth | ok | 37.6 | 1 | - |
| battery | ok | 29.9 | 0 | its, mockA_high, v1v2 |
| extra_datasets | ok | 21.6 | 1 | mcm_v12, v4 |

## Test tables

### 16S rRNA datasets

| Dataset | Region | Samples | AmpliTrim setting | Filter: AmpliTrim - DADA2 (points) | Yield estimate - merged (points) | Merged / estimate | Across maxEE settings: offset mean (range) | Across maxEE settings: rank correlation (settings) | AmpliTrim - no truncation (points, 95% interval) | AmpliTrim - FIGARO at its maxEE (points, 95% interval) | AmpliTrim default - FIGARO as shipped (points, 95% interval) | Coverage 1% -> 0.2%: merged (points) | Landscape: points below the best DADA2 setting | Stability: truncation spread (nt) | Per-sample rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mockA_high | V1-V3 | 6 | 255/262 (maxEE 2,6) | -1.1 | +3.9 | 0.95 | +2.4 (+0.3 to +3.9) | +1.00 (4) | +10.5 (+9.1 to +12.1) | -0.2 (-0.8 to +0.6) | -1.9 (-3.9 to -0.6) | -0.2, strains +1 | 0.3 | 0 | - |
| v1v2 | V1-V2 | 33 | 198/157 (maxEE 2) | +0.0 | +6.4 | 0.93 | +6.3 (+6.2 to +6.4) | +1.00 (4) | +55.0 (+53.6 to +56.4) | +0.1 (-0.4 to +0.6) | +2.0 (+1.5 to +2.5) | -0.4 | 0.1 | 1 | +0.63 |
| v4 | V4 | 36 | 124/114 (maxEE 2) | +0.0 | +30.6 | 0.69 | +30.4 (+29.5 to +30.9) | +1.00 (3) | +13.0 (+12.2 to +13.9) | +2.0 (+1.6 to +2.4) | +4.3 (+3.7 to +4.9) | +2.6 | 6.8 | 3 | +0.70 |
| mcm_v12 | V1-V2 | 6 | 155/170 (maxEE 2) | -0.1 | +0.2 | 1.00 | +0.2 (-0.1 to +0.4) | +1.00 (3) | +69.9 (+66.4 to +73.6) | -0.0 (-0.0 to +0.0) | +2.3 (+2.2 to +2.5) | +0.0 | 0.1 | 3 | - |
| mockB (independent mock, V1-V3) | | | not yet run | | | | | | | | | | | | |
| v4v5 (PRJNA971391, V4-V5) | | | not yet run | | | | | | | | | | | | |
| mcm_v46 (PRJEB34919, V4-V6, real tight overlap) | | | not yet run | | | | | | | | | | | | |
| sputum_v1v2 (PRJNA915241, V1-V2) | | | not yet run | | | | | | | | | | | | |
| sputum_v3v4 (PRJNA915241, V3-V4) | | | not yet run | | | | | | | | | | | | |
| sputum_v5v7 (PRJNA915241, V5-V7) | | | not yet run | | | | | | | | | | | | |
| sputum_v7v9 (PRJNA915241, V7-V9) | | | not yet run | | | | | | | | | | | | |
| v3v4 (V3-V4, tight overlap) | | | not yet run | | | | | | | | | | | | |

### ITS datasets

| Dataset | Region | Samples | maxEE | Filter: AmpliTrim - DADA2 (points) | Yield estimate - merged (points) | Merged / estimate | AmpliTrim (maxEE 2) - 200/200 truncation (points, 95% interval) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| its | ITS1 | 37 | 1 | +0.1 | +15.1 | 0.72 | +16.1 (+14.3 to +17.9) |
|  |  |  | 2 | +0.1 | +25.3 | 0.65 |  |
|  |  |  | 5 | -0.1 | +30.4 | 0.64 |  |

### Datasets with expected sequences (the same methods, scored against the expected sequences)

| Dataset | Method | Truncation | maxEE | Pairs merged | Variants recovered | Strains recovered | Reads in identical ASVs | ASVs outside the reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mockA_high | AmpliTrim (maxEE 2,6) | 255/262 | 2,6 | 74.6% | 29 | 10/13 | 99.75% | 6 |
| mockA_high | AmpliTrim (maxEE 1) | 277/240 | 1 | 42.6% | 28 | 10/13 | 99.70% | 3 |
| mockA_high | AmpliTrim (maxEE 5) | 273/244 | 5 | 84.2% | 32 | 11/13 | 99.81% | 4 |
| mockA_high | FIGARO (amplicon 505) | 273/244 | 3,4 | 76.4% | 31 | 10/13 | 99.77% | 4 |
| mockA_high | AmpliTrim (FIGARO's maxEE 3,4) | 269/248 | 3,4 | 76.1% | 30 | 10/13 | 99.77% | 4 |
| mockA_high | full | no truncation | 2,6 | 64.2% | 29 | 10/13 | 97.70% | 2 |

## Decision: the default of --allow-unmergeable (1% or 0.2%)

**UNDETERMINED**

- mockA_high   257/260 -> 257/263: merged pairs -0.2 points; variants +1, strains +1, ASVs outside the reference -4
- v1v2         196/159 -> 195/168: merged pairs -0.4 points; no expected sequences, cost only
- v4           120/118 -> 124/115: merged pairs +2.6 points; no expected sequences, cost only
- mcm_v12      160/165 -> 160/165: merged pairs -0.0 points; no expected sequences, cost only

needs a second dataset with expected sequences (an independent mock community: --download mockB, --prepare, --set-reference)

## What still needs you

- mockB (PRJEB67827): choose its runs (`--list-runs mockB`), and the Zymo reference FASTA (`--set-reference mockB=FILE`).
- mcm_v46 and mcm_v12: the expected sequences of the 15 bacteria of Table 1 of the paper as a FASTA (`--set-reference mcm_v46=FILE`), for the truth columns.
- V4-V5 (PRJNA971391): the primers, then `--download v4v5`, `--prepare v4v5`.
- The manuscript and release items on the board below.

## The board

```
== 1. Tests (overnight.py); results in C:\data\overnight
  DONE    mock_grid        2026-10-06 11:47  4 criterion not met
  DONE    asv_classify     2026-10-06 16:19
  DONE    mock_clip250     2026-10-06 11:55
  DONE    figaro_mockA     2026-10-06 19:05
  DONE    mock_dilutions   2026-10-06 12:15
  DONE    coverage_levels  2026-10-06 23:41
  DONE    landscape        2026-10-07 00:32  1 criterion not met
  DONE    mock_miss_trace  2026-10-06 16:53
  DONE    mock_pooled      2026-10-06 12:24
  DONE    stability        2026-10-07 00:57
  DONE    per_sample_rank  2026-10-07 01:13  3 criterion not met
  DONE    its_chimeras     2026-10-06 14:13
  DONE    figaro_v1v2      2026-10-06 19:44
  DONE    v1v2_fulldepth   2026-10-06 20:22  1 criterion not met
  DONE    battery          2026-10-07 01:43
  DONE    extra_datasets   2026-10-07 02:05  1 criterion not met

== 2. Decisions
  Default of --allow-unmergeable (1% -> 0.2%): UNDETERMINED
  mockA_high   257/260 -> 257/263: merged pairs -0.2 points; variants +1, strains +1, ASVs outside the reference -4
  v1v2         196/159 -> 195/168: merged pairs -0.4 points; no expected sequences, cost only
  v4           120/118 -> 124/115: merged pairs +2.6 points; no expected sequences, cost only
  mcm_v12      160/165 -> 160/165: merged pairs -0.0 points; no expected sequences, cost only
  needs a second dataset with expected sequences (an independent mock community: --download mockB, --prepare, --set-reference)

== 3. New data
  mockB  not prepared, reference MISSING   (an independent mock community (Zymo D6321, V1-V3))
  v4     registered   (V4, 36 soil samples (PRJNA574030): used in development, so run again with the final build)
  v4v5   not prepared   (V4-V5 reads (PRJNA971391))
  mcm_v46 not prepared, reference MISSING   (inter-laboratory mock communities MCM2a and MCM2b, V4-V6 (about 564 bp amplicon, MiSeq 2x300: a real tight-overlap case; 6 samples))
  mcm_v12 registered, reference MISSING   (inter-laboratory mock communities MCM2a and MCM2b, V1-V2 (about 337 bp amplicon, MiSeq 2x300; 6 samples))
  sputum_v1v2 not prepared   (sputum, region V1-V2 (PRJNA915241, QIAseq 16S/ITS panel, MiSeq 2x300; a held-out study: use --list-runs, then --select the runs of this region))
  sputum_v3v4 not prepared   (sputum, region V3-V4 (PRJNA915241, QIAseq 16S/ITS panel, MiSeq 2x300; a held-out study: use --list-runs, then --select the runs of this region))
  sputum_v5v7 not prepared   (sputum, region V5-V7 (PRJNA915241, QIAseq 16S/ITS panel, MiSeq 2x300; a held-out study: use --list-runs, then --select the runs of this region))
  sputum_v7v9 not prepared   (sputum, region V7-V9 (PRJNA915241, QIAseq 16S/ITS panel, MiSeq 2x300; a held-out study: use --list-runs, then --select the runs of this region))
  v3v4   not prepared   (V3-V4 2x250: tight overlap on real reads (the candidate runs of PRJEB58189))

== 4. Manuscript (things only you can complete)
  [ ] Title block: affiliation(s) and the target journal.
  [ ] Table 1: accessions and sizes of the two real V4 datasets (the NovaSeq run and the 36-sample soil study).
  [ ] Section 3: the R and vsearch versions (this script prints them; DADA2 1.40.0 and cutadapt 5.2 are in).
  [ ] Table 3: check the V1-V2 AmpliTrim truncation (198/157) against compare_methods.txt, and add the paired interval against FIGARO (step figaro_v1v2).
  [ ] Figures 3 and 5 and Table 9: their values were transcribed from the comparison outputs; regenerate them from the saved compare_methods.tsv files (V1-V2, ITS at 5,000 pairs and at full depth).
  [ ] Availability: repository URL, licence, the final build identifier, operating systems.
  [ ] Declarations: competing interests, the AI-tools statement (adapt to the journal's policy), funding, author contributions, acknowledgements, ethics.
  [ ] References: check all nine against the sources; add the titles of 2, 5, 7 and 8; add the reference for PRJEB42528 (9).
  [ ] After each batch of results: update Results, Table 10, the Discussion and the Abstract (send OVERNIGHT_SUMMARY.md).
  [ ] A last full run on the final build (python validation\check_build.py --run --fresh), so that the paper cites one build id; say that earlier ids depended on the file order.

== 5. Release
  [ ] Run the CI workflow (.github/workflows) once on GitHub and fix what it finds (it has never run).
  [ ] Push the repository to GitHub (needs your credentials) and put its URL in the manuscript and in CITATION.cff.
  [ ] Choose a licence and add the LICENSE file (the mock A reference is derived from a GPL-3.0 repository and is not bundled).
  [ ] Archive the release for a DOI (for example Zenodo from the GitHub release) and cite it.
  [ ] Test the install on a second machine or system (pip install -e . and python validation\check_build.py).

== Next, in this order
  1. python validation\check_build.py --list-runs mockB         (then --download mockB --select ..., --prepare mockB ..., --set-reference mockB=FILE)
  2. then send OVERNIGHT_SUMMARY.md, and work through sections 4 and 5
```

Every step's own report: C:\data\overnight\OVERNIGHT_SUMMARY.md. The log of this run: C:\data\overnight\overnight_all.log and C:\data\overnight\overnight.log.
