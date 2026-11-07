# Reviewer guide: where the evidence is

A reviewer asks about a claim; where do I look? "Section N" is a section of [`TEST_REGISTER.md`](TEST_REGISTER.md) (time order, criteria written before each run, contents table at its top). "Run NN" is a folder `results/NN_...`; the run numbers, the datasets with their accessions, and where the reads are, are in [`docs/DATA_LAYOUT.md`](docs/DATA_LAYOUT.md). Written on 7 November 2026.

## Start here

- **Software:** [`paytonyau/amplitrim`](https://github.com/paytonyau/amplitrim), PyPI `amplitrim`. Version 0.2.0 is the one in the paper (Zenodo 10.5281/zenodo.23962713; all versions 10.5281/zenodo.23860406).
- **Which build was tested:** nights 1 to 6 ran a development build (`amplitrim/` here); the final run (sections 29 and 30) ran the released 0.2.0 on every dataset. Sections 21, 24 and 28 check that the release recommends what was tested.
- **Not here:** the reads (public accessions), work folders and ASV files; the raw outputs of runs 01, 02 and 10 were not retained (their results are in sections 1 to 10 and 21).
- **Independent test:** the `maxEE` rule was also tested by N. T. Ho (second author), protocol posted publicly before each analysis (issue #1 on GitHub, [URL to add]). Her results, as reported, are in the last note of section 30; her full report is still to be archived.

## Likely questions

| Question | Short answer | Register | Results |
|---|---|---|---|
| Is the filter prediction right? | Within 0.8 points on 12 datasets (night 1); exact on both ITS studies; on the released package at most 1.4 points (mock A) | 11, 19, 30 (P57 a, P58) | runs 03, 08; `24_night10_closing_2026-11-06/coverage/*/`, `.../its_new/per_run_check.txt` |
| Is the recommended cut good? | Within 0.7 points of the best DADA2 setting on five of seven datasets; soil V4 4.7 points below; swabs not decided | 22, 30 (P59) | run 11; `.../grid/OVERNIGHT_SUMMARY.md` |
| How was the `maxEE` rule chosen; is it validated? | A percentile rule chosen by the author after seeing the data; it did not meet its adoption criteria in night 4b and is kept as a stated trade | 16 to 18, 24 | runs 06, 07, 13 |
| Is it tested on independent data? | Kept 2 on the MiSeq SOP mock; relaxed on two gut datasets in the independent test (+10.9 and +3.1 points merged, profiles within noise) | 30 | run 24 (`mocktests`); the last note of section 30 |
| Is 12 nt a safe minimum overlap? | Same ASVs as 10 nt on five mocks; the pre-set prediction failed on mock A and B and the default was kept, with reasons | 27, 30 (P63) | run 23; `.../overlap/overlap_results.md` |
| Why leave out 0.2% of the longest amplicons? | A rule fixed before the evidence adopted it; the final run shows the cost of other shares | 6, 11, 30 (P55, P56) | `.../coverage/`, `.../tail/` |
| How does it compare with FIGARO? | Same `maxEE`: within the 2-point margin on nine of ten datasets; FIGARO's `maxEE` choice was not matched | 12 to 17 | runs 04 to 06 |
| Does the release give what the nights tested? | Same settings on ten of 12 datasets; DADA2 was run at the released settings where they differ | 21, 24, 28, 30 (P64) | runs 13, 21; `.../accept/` |
| What about ITS? | Filter exact; the merge estimate overshoots DADA2 by 25.5 and 68.1 points; where the pairs go is in the last note of section 30 | 19, 20, 30 | runs 08, 09, `24_night10_its2_split_2026-11-07` |
| Time and memory? | 29 to 141 s, at most 352 MB on 12 datasets | 30 (P60) | `.../NIGHT10_SUMMARY.md`; run 22 |
| What was decided after seeing results, and what failed? | Each is written down as such; the final run has a timeline of commits. Not met: P59 on soil V4, P52 on mock A and B. Not decided: P59 on swabs, P57 (b) to (d). Two script defects were found and fixed before the affected steps were repeated | 6, 16 to 18, 24, 27, 29, 30 | `TEST_REGISTER.md` |
| Is accuracy tested? | Only on mock communities and on the independent simulation; the real samples and both ITS studies have no known truth | 3, 30 | `docs/validation.md` |

## Provenance

- **Final run:** package 0.2.0, code fingerprint `53857ca90f` (in `night10.log`); the driver `night10.py` SHA256 `559633be0ceb7f89733f4cd8ccfec702e3aa374460f7030f0a56fcd94a4fc7d6`; after the two defects, `compare_methods.py` SHA256 `7d8fadf30ed86c6229a182388f2408064b038793c813cdee222c3bd4bee43d8c` and `tail_classify.py` SHA256 `aac590d4cbd80d020393d4b5e9d09d46623ed90bf3ae0e38cf65d5ce9046cac3`, committed in `c59a0c8` before the repeat.
- **Tools:** DADA2 1.40.0, cutadapt 5.2, vsearch 2.32.0, Python 3.12; SILVA 144 SSU Ref NR99 (DOI 10.82364/144/SSU/Ref-NR99/FASTA/unaligned/truncated, MD5 `ccead7bba52075f5d8ba2bfab5adc4c1`).
- **When each criterion was committed:** `git log --date=iso -- TEST_REGISTER.md`. The closing run: `b0869d0` (section 29, after the pilot), `7808ccc` (addenda, during the run, before any result was read), `54050bf` (timeline), `df22f62` (section 30).
- **Seen before its criteria were committed:** one development-build run on the MiSeq SOP mock (97.1% merged at its own cut, 89.3% at the tutorial's 240/160): section 29, "Plan as run".
- **Results:** every text output is in `results/` with its sha256 in `results/MANIFEST.tsv`.

## Re-checking

```
python -m pytest tests -q                       # 651 passed, 4 skipped on 7 November 2026
python validation\organise_data.py --check-paths
python site-build\build_results.py              # then build_design.py; the site tests fail until they are rebuilt
```

To repeat the closing run use the command recorded at its start in `night10.log` and section 29 (a checkout of the 0.2.0 tag, the prepared datasets, the SILVA file, `--overlap-mock miseqsop_mock`, `--grid` on seven datasets). How to look after the repositories: [`MAINTAINING.md`](MAINTAINING.md). What is still open: [`FUTURE.md`](FUTURE.md).
