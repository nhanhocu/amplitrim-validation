# Maintaining AmpliTrim and its validation archive

For whoever looks after the two repositories. It replaces the October push guide (steps that are done are not repeated here). Written on 7 November 2026.

## The two repositories

| Repository | What it is | Holds | Does not hold |
|---|---|---|---|
| [`amplitrim`](https://github.com/paytonyau/amplitrim) | the software people install | the package, its tests, `README.md`, `docs/usage.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `CITATION.cff`, CI | the evidence, validation scripts, reads |
| [`amplitrim-validation`](https://github.com/paytonyau/amplitrim-validation) | the research record | the register, the scripts, the tests, the written results and website (`docs/`), `results/`, the development build that was tested, `FUTURE.md` | the reads (public accessions), work folders, ASV files |

Users meet only the first. Its README links to the evidence page in the second, so push the archive first (or together) when a link is new.

## Environments and the config

- `amplitrim_paths.json` (dataset folders, primers, references) is machine specific and not in either repository; scripts take it with `--config`.
- The development build (`amplitrim/` in the archive) has options the release does not (`--max-ee`, `--marker`, ...). Dataset-preparation scripts (`real_data.py`, `run_dataset.py`, ...) call those options and run from the development folder. Every run that is meant to test the **release** runs from a clean environment that has only the released package, from a checkout of its tag (on the author's machine `C:\amplitrim_020`, a git worktree of the 0.2.0 tag with `validation\` copied in).
- Where the data are and how they are numbered: [`docs/DATA_LAYOUT.md`](docs/DATA_LAYOUT.md). Which evidence answers which question: [`REVIEWER_GUIDE.md`](REVIEWER_GUIDE.md).

## Everyday jobs

Each ends with the tests of the repository you changed (`python -m pytest tests -q`) and a commit that says what changed.

1. **Change the text of the results site.** Edit `docs/FINDINGS.md` or `docs/validation.md` (or the builders in `site-build/`), then `python site-build\build_results.py` and `python site-build\build_design.py` (the second reads the software repository next to this one). The site tests fail until the pages are rebuilt, and the generated files in `docs/` are committed. [`site-build/README.md`](site-build/README.md) has the details, including the software's own site.
2. **After a validation run.** Name the folder so that `organise_data.py` numbers it, then `python validation\organise_data.py --base C:\data` (a plan; nothing changes), `--apply`, and `python validation\collect_results.py --runs C:\data\runs --out results --dry-run` before the real collection. Write the register section before the run (criteria first, committed) and its outcomes after; `tests/test_archive_order.py` counts the register sections and checks the run table, so it fails until both are updated, and `docs/DATA_LAYOUT.md` gets the run.
3. **Add a dataset.** Folder `NN_<kind>_<region>_<n>_<accession>`, an entry in `amplitrim_paths.json`, a row in the datasets table of `docs/DATA_LAYOUT.md`. The results site is built for exactly 12 datasets (`site-build/results_data.py`, `len(ORDER) == 12`, and the tests), so a 13th needs code and test changes.
4. **Look at the state.** `git status` and `git log -1` in both repositories, the tests in both, `python validation\organise_data.py --check-paths`, and `python validation\inventory_data.py` for the data drive. Once in a while, clone the archive fresh into an empty folder and run its tests there: a file that git ignores exists on your disk, so the tests pass for you and fail for everyone else.

## Releasing the software

Order: documents ready, tests and CI green, TestPyPI, an acceptance run, PyPI, the GitHub release, then the DOI into `CITATION.cff`.

- **A PyPI version can never be reused.** Build once (`python -m build`, `twine check dist\*`) and upload exactly those files to TestPyPI first, then to PyPI. Use project-scoped API tokens and two-factor authentication.
- **The version is written in one place,** `amplitrim/__init__.py`. `tests/test_metadata.py` then fails until `CITATION.cff`, the top heading of `CHANGELOG.md`, the example output in `README.md` and the example output and footer of `docs/index.html` say the same.
- **Acceptance run** in a clean environment, `pip install` from the index being tested, then `amplitrim --input-dir <mock B ready folder> ...`: exit code 0, and `summary.json` recommends **274/253 with maxEE 4,8** (what 0.2.0 gave, register section 28). If a later release changes the rule, change this expectation and say why in the register.
- **Zenodo:** switch it on for the repository before the GitHub release, or no DOI is made. Tag on the commit you built from.
- **Which number to bump:** a change of wording only is a patch (0.2.x); a new option or a changed report or recommendation is a minor version (0.3.0). Documents-only commits (the user guide, the citation file) need no release. Before the paper's validation claims are carried to a new version, run the release check of section 28 on it.
- **Bioconda:** after each release, update the recipe (it needs the sha256 of the PyPI source archive); the first recipe is pull request 71098 of `bioconda-recipes`. The Galaxy wrapper lacks `--min-overlap`.

## Releasing the archive

Switch Zenodo on for `amplitrim-validation` and publish a GitHub release; the DOI goes into the paper's data statement and the README. It freezes the files, so do it after the independent test's full report is archived (register section 31). Pages: *Settings*, *Pages* should show *Deploy from a branch*, `main`, `/docs`; rebuild before each push.

`paper/` is the earlier JOSS draft, with its test (`tests/test_paper.py`) and workflow. The submitted manuscript is a separate document, exported at submission. If the draft is removed, remove its test and workflow with it.

## What is open

Everything that is not done is in [`FUTURE.md`](FUTURE.md), with what each item needs: the changes for 0.3.0, the open validation, the independent test to archive, and the logistics (the Zenodo token, the repository's location).
