# Run 26: the independent test of the `maxEE` rule (N. T. Ho, 6 to 11 November 2026)

Register section 33. The protocol and two addenda were posted publicly on AmpliTrim issue #1 (https://github.com/paytonyau/amplitrim/issues/1) before each analysis. The text of the issue, with the time and a hash of each post, is in `ISSUE_1.md`. The analysis was run on Linux with AmpliTrim 0.2.0 from PyPI, DADA2 1.38.0, cutadapt 5.2, vsearch 2.32.0 and the RDP classifier 2.13. The scripts are in `validation/independent_test/`.

Investigator: Nhan Thi Ho. Analysis assisted by Claude, an AI assistant, which wrote the scripts. The investigator is responsible for all analyses and contents.

## What is where

| Folder or file | What it holds |
|---|---|
| `ISSUE_1.md` | The opening post (protocol) and the five comments (addendum 1, results, addendum 1 results, addendum 2, addendum 2 results), as posted |
| `00_protocol/` | `PROTOCOL.md`, `PROTOCOL_ADDENDUM_1.md`, `PROTOCOL_ADDENDUM_2.md` as frozen; `manifest.tsv` and `manifest2.tsv` (the runs chosen, with MD5 sums or byte counts); `screening_log.tsv` (the seeded screen of addendum 1) |
| `01_original/NIG`, `01_original/CBGS` | The original protocol: PRJEB31073 (V1-V2) and PRJEB50418 (V3-V4) |
| `02_addendum1/KFS`, `02_addendum1/HDP` | Addendum 1, datasets where the rule relaxes: PRJDB8879 and PRJNA714241 (both V3-V4) |
| `03_addendum2/SIMI`, `03_addendum2/SIMT`, `03_addendum2/design` | Addendum 2, reads simulated from a known community: ideal errors (SIM-I) and the error rates DADA2 learned from KFS (SIM-T); `design/truth.fa` and `design/design.json` are the truth |
| `04_merge_breakdown/` | Exploratory, 9 November 2026, after the results: where DADA2 loses the pairs that AmpliTrim's yield estimate counts. No criterion |
| `reports/` | The three reports of 7 November 2026, as Markdown (converted from the Word files sent to the author). Their 'Files' sections name the folders of the original delivery (`results`, `results2`, `results3`), which are `01_original`, `02_addendum1` and `03_addendum2` here |

In each dataset folder: `settings.json` (AmpliTrim's settings and estimates for each arm), `results.json` (every criterion), `per_sample.tsv`, `<arm>_track.tsv` (DADA2's counts per step), `<arm>_seqtab.tsv` (the ASV tables, sequences as column names), `rdp.tsv` (genus assignments), `asv_ids.json`, `prepare.json` (primer step and draws), `run.log`, and AmpliTrim's own `AmpliTrim_REPORT_draw_a.md` and `_draw_b.md`. The simulated folders add `truth_per_sample.tsv` and `truth_results.json`. The arms are R (AmpliTrim's recommendation), D (AmpliTrim's best cut at maxEE 2), E (its best cut at maxEE 2,5) and Db (arm D on the second draw of reads).

## Not here

The reads (public accessions, listed in the manifests), the simulated reads (they can be made again with `sim_reads.py` and the seeds of addendum 2), DADA2's work folders and the ASV FASTA files (the sequences are the column names of the seqtab files). `design/truth.fa` is kept because it is the truth the simulation was scored against.

## Reproducing a dataset

```
bash validation/independent_test/run_test_dataset.sh KFS <folder with the reads> <work folder> 5000
```

`run_test_dataset.sh` needs Python with AmpliTrim, numpy and pandas, R with DADA2, cutadapt, vsearch and the RDP classifier (`rdp_classifier` on the PATH). The simulation: `sim_build.py` (the truth, from arm D of KFS), `export_err.R` (DADA2's learned error rates), `sim_reads.py` (mode `nom` for SIM-I, `tq` for SIM-T), then `run_test_dataset.sh` with the label SIMI or SIMT (`prepare.py` removes primers only for CBGS, KFS and HDP), and `sim_eval.py` for criteria T1 to T4. Each script states its arguments in its first lines.
