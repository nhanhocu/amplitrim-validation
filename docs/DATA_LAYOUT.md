# Where the data of the validation are, and what is in this repository

The repository holds the scripts, the tests, the register, the written results and the site. It does **not** hold the reads, the DADA2 and vsearch
work folders, the ASV FASTA files or the long-read data: they are large and can be made again. This page says where each part is on the data drive
(`C:\data` in the runs of 2026) and how to rebuild what is missing. Sizes are those of 4 November 2026.

## The data drive

| folder | what it is | size |
|---|---|---|
| `01_...` to `12_...` | the 12 datasets, one folder each, named `NN_<kind>_<region>_<name>_<accession>` (the table: `python validation/organise_data.py --table`); dataset 13 is the dataset of night 6 (PRJNA933120) | 9.7 GB |
| `runs\` | the numbered runs, one or more folders each, named `NN_<what>_<date>` | 11.1 GB, of which 7.9 GB bulk |
| `longread\` | the long-read data of nights 7 to 9b | 4.5 GB |
| `_archive_2026-10\` | the outputs of the first rounds, from before the numbering; superseded by the numbered runs | 11.3 GB |
| `_release_acceptance\` | the rehearsal and the acceptance run of the PyPI release of 0.1.0 (not validation runs) | small |
| `_scratch\` | test folders and first looks that are not runs of the register | small |
| `backup\`, `_reports\`, `tools\` | copies of `amplitrim_paths.json`, the inventories and plans, and the helper scripts | small |

`amplitrim_paths.json` (the paths of the datasets, their primers and references) is machine specific and is **not** in the repository.

## The runs

The number of a run is its number in `validation/README.md` and in `python validation/organise_data.py --table`: the order of the register, not of the dates.
`organise_data.py` gives each folder its number and rewrites the names in `amplitrim_paths.json` in the same step; it plans first and has an undo.

| run | folders under `runs\` | register |
|---|---|---|
| 01, 02, 10 | no folder under `runs\` | 1-10, 21 |
| 03 | `03_night1_2026-10-09` | 11 |
| 04 | `04_night2_2026-10-09` | 12-13 |
| 05 | `05_night3_2026-10-09` | 14-15 |
| 06 | `06_night4_offline`, `06_night4b_offline`, `06_night4c_offline` | 16-17 |
| 07 | `07_night4_2026-10-10` (night 4b) | 18 |
| 08, 09 | `08_its_check`, `09_its_merge_check` | 19, 20 |
| 11 | `11_overmerge_v4`, `11_v4_landscape` | 22 |
| 12 | `12_estimate_check`, `12_estimate_check_cutoff` | 23 |
| 13 | `13_night5_*`, `13_nocap_check`, `13_nocap_check_mockB`, `13_nocap_check_nights` | 24 |
| 14 | `14_night6_pilot`, `14_night6_PRJNA933120` | 25-26 |
| 15, 16 | `15_longread_describe_sq2_monomer_all96`, `16_longread_describe_sq2_kinnex` | - (`FUTURE.md`) |
| 17 to 20 | `17_night7_longread`, `18_night8_truth`, `19_night9_revio`, `20_night9b_revio` | - (`FUTURE.md`) |
| 21 | `21_release_check_020` (release check of version 0.2.0) | 28 |
| 22 | `22_timing_0.2.0` (run time and memory of 0.2.0) | - |
| 23 | `23_overlap_test_2026-11-04` (the minimum-overlap test: 36 run folders, the batch files, the logs, `overlap_results.*`) | 27 |
| 24 | `24_night10_closing_<date>` (the closing run: the command line on every dataset, the coverage setting, the new datasets, the hold-out overlap test, the grid; `NIGHT10_SUMMARY.md`) | 29 |

Runs 15 to 20 were planned in `FUTURE.md` (the long-read test plan), not in numbered sections of the register.

## What is in the repository for each run

`results\` holds the text outputs of the runs: the reports, protocols, logs and result tables (`.md .tsv .json .log .txt`, at most 2 MB each), with their folder
structure, and `results\MANIFEST.tsv` (path, size, sha256) so that the record can be checked. `python validation/collect_results.py --runs C:\data\runs --out results --dry-run`
shows what it would copy; it leaves out reads, work folders and ASV FASTA files, and replaces `C:\Users\<name>` by `C:\Users\<user>`.
The ASV files are not kept; the overlap test keeps a fingerprint of every ASV set instead (`overlap_results_asv_sets.tsv`): equal fingerprints mean exactly equal ASVs.

## How to rebuild what is not here

1. The reads: `validation/download_ena.py` and the accessions of `docs/SUPPLEMENT.md`; `python validation/check_environment.py` checks the machine (R, DADA2, vsearch, cutadapt).
2. The prepared datasets (primer-trimmed pairs): the scripts of group B in `validation/README.md`; the primers and references of each dataset are in `amplitrim_paths.json`.
3. A run: the script of its row in the run table, with the command of its register section. The runs that took a 5,000-pair sample per sample say so in their section.
4. A new run gets the next number: `python validation/organise_data.py --base C:\data --next`.

## Keeping it in order

`python validation/inventory_data.py --base C:\data --repo <this repository> --out <report>` lists every folder with its size, its newest file, its bulk against its
results, and flags the run folders without a number, the scratch folders and the runs not yet collected into `results\`. It changes nothing.
