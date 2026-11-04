"""Night 8: the calibration test (T-cal) and the truth test of the long-read work, on the PacBio Kinnex-16S data of the ATCC MSA-1003 mock community, in one run.

Steps (--list shows which have finished, --redo STEP repeats one, --check tests the machine and the files first):
  pilot           one DADA2 run (maxEE 2) on the smallest Monomer file: how long it takes, and so how long the truth test will take
  tcal            T-cal (longread_calibration.py): are the expected errors calibrated, in Monomer and in Kinnex reads, and for the reads that only an indel-tolerant primer search finds?
  truth_monomer   the truth test (longread_truth.py) on the three Monomer files: DADA2 over a grid of conditions against the known variants of the mock community
  truth_kinnex    the same on the three Kinnex files (the first N reads of each)
  summary         NIGHT8_SUMMARY.md: what ran, the gates, the prediction of the rule, and what to send back

The gates are in FUTURE.md of the archive (written on 15 October 2026, before the run) and in the docstrings of longread_calibration.py and longread_truth.py.

    python night8.py --check
    python night8.py --out C:\\data\\runs\\18_night8_truth --only pilot,tcal          (T-cal takes minutes and needs no R; the pilot says how long the rest will take)
    python night8.py --out C:\\data\\runs\\18_night8_truth                            (resumes: finished steps are skipped)

It needs the output of Night 7 (--expected-dir: expected_amplicons.fasta and genome_amplicons.tsv) and its data (--data: sq2_monomer_fastq and sq2_kinnex_fastq).
Needs Python 3.9+, numpy, rapidfuzz, cutadapt (pip install cutadapt) and R with DADA2 (the truth test and the pilot).
"""

import argparse
import datetime
import importlib.util
import json
import re
import shutil
import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import longread_calibration as lcal  # noqa: E402
import longread_common as lc  # noqa: E402
import longread_filter_check as lf  # noqa: E402
import longread_truth as lt  # noqa: E402
from night7 import DEFAULT_DATA, MONOMER_PAIRS, PRIMERS, Skip, link_or_copy, md_lines, tool_version, versions  # noqa: E402
from rtools import NOT_FOUND, find_rscript  # noqa: E402

STEPS = ["pilot", "tcal", "truth_monomer", "truth_kinnex", "summary"]
DEFAULT_EXPECTED = Path(r"C:\data\runs\17_night7_longread\genome_amplicons")
SMALLEST_MONOMER = MONOMER_PAIRS[0]                         # Fwd_07--Rev_30, the smallest of the three Monomer files
NEEDED_GB = 2
PREDICTION = {"Monomer": 2, "Kinnex": 3}                    # what the percentile rule is predicted to give (FUTURE.md, 15 October 2026)

LOG = None


def say(message="") -> None:
    line = f"{datetime.datetime.now():%H:%M:%S}  {message}" if message else ""
    print(line, flush=True)
    if LOG is not None:
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


class Ctx:
    def __init__(self, args):
        self.args = args
        self.out, self.data, self.expected_dir = Path(args.out), Path(args.data), Path(args.expected_dir)
        self.monomer, self.kinnex = self.data / "sq2_monomer_fastq", self.data / "sq2_kinnex_fastq"
        self.fasta, self.strains = self.expected_dir / "expected_amplicons.fasta", self.expected_dir / "genome_amplicons.tsv"
        self.tcal_out, self.pilot_out = self.out / "tcal", self.out / "pilot"
        self.truth_monomer_out, self.truth_kinnex_out = self.out / "truth_monomer", self.out / "truth_kinnex"
        self.state_file, self.log_file = self.out / "night8_state.json", self.out / "night8.log"
        self.state = {"steps": {}}
        self.grid = tuple(args.grid)


# ----------------------------------------------------------------------------- what the steps need

def need_expected(c: Ctx) -> None:
    for p, what in ((c.fasta, "the expected amplicons"), (c.strains, "the table of the strains")):
        if not p.is_file():
            raise Skip(f"{what} are missing: {p} (Night 7 writes them; --expected-dir says where they are)")


def need_files(folder: Path, what: str) -> list:
    files = lf.find_files(folder) if folder.is_dir() else []
    if not files:
        raise Skip(f"no FASTQ files in {folder} ({what})")
    return files


def monomer_files(c: Ctx, pairs=MONOMER_PAIRS) -> list:
    files = need_files(c.monomer, "the Monomer files")
    chosen = [p for p in files if any(pair in p.name for pair in pairs)]
    if len(chosen) < len(pairs):
        raise Skip(f"only {len(chosen)} of the {len(pairs)} Monomer files are in {c.monomer} ({', '.join(pairs)})")
    return chosen


def linked_folder(files: list, folder: Path) -> Path:
    """A folder of hard links to the files (no second copy of the data); removed again by the caller."""
    folder.mkdir(parents=True, exist_ok=True)
    for p in files:
        link_or_copy(p, folder / p.name)
    return folder


def need_dada2() -> None:
    lc.check_cutadapt()
    if not find_rscript():
        raise SystemExit(NOT_FOUND)


def truth_args(c: Ctx) -> dict:
    return {"grid": c.grid, "band": c.args.band_size, "pool": c.args.pool, "threads": c.args.threads, "keep": c.args.keep, "log": say}


# ----------------------------------------------------------------------------- the steps

def step_pilot(c: Ctx) -> str:
    need_expected(c)
    chosen = monomer_files(c, (SMALLEST_MONOMER,))
    need_dada2()
    folder = linked_folder(chosen, c.out / "pilot_input")
    try:
        r = lt.run({"Pilot": folder}, c.fasta, c.strains, PRIMERS[0], PRIMERS[1], c.pilot_out, reads=c.args.reads_pilot, only=["ee2"], **truth_args(c))
    finally:
        shutil.rmtree(folder, ignore_errors=True)
    m = r["by_lib"]["Pilot"]["ee2"]
    minutes = m["seconds"] / 60
    n_cond = len(lt.build_conditions(c.grid, r["rules"]["Pilot"]))
    per_100k = minutes * 100000 / max(1, m["reads_in"])
    return (f"one DADA2 run on {m['reads_in']:,} reads took {minutes:.1f} min; a run of about 100,000 reads would take at least {per_100k:.0f} min if the time grew linearly (it grows faster), "
            f"so the {n_cond} conditions of the truth test on two library types need at least {per_100k * n_cond * 2 / 60:.1f} h")


def step_tcal(c: Ctx) -> str:
    need_expected(c)
    chosen = monomer_files(c)
    need_files(c.kinnex, "the Kinnex files")
    lc.check_cutadapt()
    folder = linked_folder(chosen, c.out / "tcal_monomer_input")
    try:
        r = lcal.run({"Monomer": folder, "Kinnex": c.kinnex}, c.fasta, PRIMERS[0], PRIMERS[1], c.tcal_out, reads=c.args.reads_tcal, strains_table=c.strains, keep=c.args.keep, log=say)
    finally:
        shutil.rmtree(folder, ignore_errors=True)
    return "; ".join(f"{g} {s}" for g, (s, _) in r["gates"].items())


def truth_step(c: Ctx, library: str, folder: Path, files: list, out: Path, reads: int) -> str:
    need_expected(c)
    need_dada2()
    use = linked_folder(files, c.out / f"truth_{library.lower()}_input") if files else folder
    try:
        r = lt.run({library: use}, c.fasta, c.strains, PRIMERS[0], PRIMERS[1], out, reads=reads, **truth_args(c))
    finally:
        if files:
            shutil.rmtree(use, ignore_errors=True)
    g = r["gates"][library]
    return f"rule gives maxEE {r['rules'][library]}; " + ", ".join(f"{k} {s}" for k, (s, _) in g.items())


def step_truth_monomer(c: Ctx) -> str:
    return truth_step(c, "Monomer", c.monomer, monomer_files(c), c.truth_monomer_out, c.args.reads_monomer)


def step_truth_kinnex(c: Ctx) -> str:
    need_files(c.kinnex, "the Kinnex files")
    return truth_step(c, "Kinnex", c.kinnex, [], c.truth_kinnex_out, c.args.reads)


# ----------------------------------------------------------------------------- the summary

def rule_of(path: Path):
    """The maxEE that the percentile rule gave, from a TRUTH.md."""
    if not Path(path).is_file():
        return None
    m = re.search(r"so the package's rule gives \*\*maxEE (\d+)\*\*", Path(path).read_text(encoding="utf-8"))
    return int(m.group(1)) if m else None


def step_summary(c: Ctx) -> str:
    v = versions()
    lines = ["# Night 8: calibration of the expected errors (T-cal) and the truth test, on the Kinnex-16S data of ATCC MSA-1003", "",
             f"Run on {datetime.date.today()}; folder {c.out}. Gates and predictions: FUTURE.md of the archive (written on 15 October 2026, before the run). "
             "Tools: " + "; ".join(f"{k} {x}" for k, x in v.items()) + ".", "", "## Steps", ""]
    for name in STEPS:
        if name == "summary":
            continue
        s = c.state["steps"].get(name)
        lines.append(f"- {name}: " + (f"{s['status']} in {max(1, round(s['seconds'] / 60))} min" + (f" ({s['detail'].splitlines()[0]})" if s["detail"] else "") if s else "not run"))
    lines += ["", "## T-cal: are the expected errors calibrated?", ""]
    tcal = c.tcal_out / "TCAL.md"
    if not md_lines(tcal, "**Gate"):
        lines.append("No result (the step did not finish; see the steps above).")
    else:
        lines += md_lines(tcal, "**Gate", "## ") + md_lines(tcal, "## Monomer", "## Composition") + md_lines(tcal, "## Composition", "## Similarity") + md_lines(tcal, "## Similarity")
    for lib, out in (("Monomer", c.truth_monomer_out), ("Kinnex", c.truth_kinnex_out)):
        lines += ["", f"## Truth test: {lib}", ""]
        body = md_lines(out / "TRUTH.md", "## ")
        lines += body if body else ["No result (the step did not finish; see the steps above)."]
    got = {lib: rule_of(out / "TRUTH.md") for lib, out in (("Monomer", c.truth_monomer_out), ("Kinnex", c.truth_kinnex_out))}
    lines += ["", "## The prediction of the rule", "",
              "Written before the run: the package's percentile rule gives maxEE " + " and ".join(f"{p} for {lib}" for lib, p in PREDICTION.items()) + ". It gave: "
              + "; ".join(f"{lib} {'not known' if g is None else g}" + ("" if g is None else (" (as predicted)" if g == PREDICTION[lib] else " (NOT as predicted)")) for lib, g in got.items()) + ".", ""]
    lines += ["## Send back", "", f"- this file ({c.out / 'NIGHT8_SUMMARY.md'})", f"- {c.tcal_out / 'TCAL.md'}", f"- {c.truth_monomer_out / 'TRUTH.md'} and {c.truth_kinnex_out / 'TRUTH.md'}",
              f"- the two truth_conditions.tsv files, and {c.tcal_out / 'bias.tsv'}", f"- {c.log_file} if a step failed"]
    (c.out / "NIGHT8_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return "NIGHT8_SUMMARY.md written"


STEP_FUNCTIONS = {"pilot": step_pilot, "tcal": step_tcal, "truth_monomer": step_truth_monomer, "truth_kinnex": step_truth_kinnex, "summary": step_summary}


def save_state(c: Ctx) -> None:
    c.out.mkdir(parents=True, exist_ok=True)
    c.state_file.write_text(json.dumps(c.state, indent=1), encoding="utf-8")


def run_step(c: Ctx, name: str, force: bool = False) -> None:
    done = c.state["steps"].get(name, {})
    if done.get("status") == "done" and not c.args.fresh and not force and name != "summary":
        say(f"{name}: finished earlier, skipped (--redo {name} repeats it)")
        return
    say(f"=== {name} ===")
    t0 = time.time()
    try:
        detail, status = STEP_FUNCTIONS[name](c), "done"
    except Skip as err:
        detail, status = str(err), "skipped"
    except SystemExit as err:
        detail, status = str(err), "failed"
    except Exception:                                                  # a bug or a tool that crashed: record it and go on with the other steps
        detail, status = traceback.format_exc(limit=6), "failed"
    c.state["steps"][name] = {"status": status, "seconds": int(time.time() - t0), "detail": (detail or "")[:3000], "finished": datetime.datetime.now().isoformat(timespec="seconds")}
    save_state(c)
    say(f"{name}: {status}" + (f" - {detail.splitlines()[0]}" if detail else ""))
    if status == "failed" and detail:
        say(detail)


# ----------------------------------------------------------------------------- --check and --list

def check_environment(c: Ctx) -> list:
    """[(what, ok, detail)] for everything the run needs."""
    out = [("Python 3.9 or later", sys.version_info >= (3, 9), sys.version.split()[0])]
    for mod, hint in (("numpy", "pip install numpy"), ("rapidfuzz", "conda install -c conda-forge rapidfuzz (or pip install rapidfuzz)")):
        have = importlib.util.find_spec(mod) is not None
        out.append((mod, have, "installed" if have else hint))
    ok, text = tool_version([sys.executable, "-m", "cutadapt", "--version"])
    out.append(("cutadapt", bool(ok), ("version " + text) if ok else "pip install cutadapt"))
    rscript = find_rscript()
    out.append(("Rscript", bool(rscript), rscript or NOT_FOUND.splitlines()[0]))
    if rscript:
        ok, text = tool_version([rscript, "-e", "cat(as.character(packageVersion('dada2')))"])
        out.append(("DADA2 in R", bool(ok), ("version " + text) if ok else "install it in R: BiocManager::install('dada2')"))
        if ok:
            ok2, text2 = tool_version([rscript, "-e", "suppressMessages(library(dada2)); cat(if (is.function(PacBioErrfun)) 'yes' else 'no')"])
            out.append(("PacBioErrfun in DADA2", bool(ok2) and text2.strip().endswith("yes"), "the PacBio error model is there" if ok2 and text2.strip().endswith("yes") else "this DADA2 has no PacBioErrfun: update DADA2"))
    try:
        free = shutil.disk_usage(c.out if c.out.exists() else (c.out.parent if c.out.parent.exists() else Path("."))).free / 1e9
        out.append((f"{NEEDED_GB} GB free", free >= NEEDED_GB, f"{free:.1f} GB free"))
    except OSError as err:
        out.append((f"{NEEDED_GB} GB free", False, str(err)))
    out.append(("expected amplicons (Night 7)", c.fasta.is_file(), str(c.fasta)))
    out.append(("table of the strains (Night 7)", c.strains.is_file(), str(c.strains)))
    monomer = lf.find_files(c.monomer) if c.monomer.is_dir() else []
    found = [p for p in monomer if any(pair in p.name for pair in MONOMER_PAIRS)]
    out.append(("Monomer files", len(found) == len(MONOMER_PAIRS), f"{len(found)} of {len(MONOMER_PAIRS)} in {c.monomer}"))
    kinnex = lf.find_files(c.kinnex) if c.kinnex.is_dir() else []
    out.append(("Kinnex files", bool(kinnex), f"{len(kinnex)} in {c.kinnex}"))
    return out


def list_steps(c: Ctx) -> None:
    for name in STEPS:
        s = c.state["steps"].get(name)
        print(f"  {name:15s} " + (f"{s['status']} ({s['finished']})" if s else "not run"))


def main(argv=None) -> int:
    global LOG
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=Path("night8_truth"), help="the folder for everything this run makes")
    ap.add_argument("--data", type=Path, default=DEFAULT_DATA, help=f"the folder of the downloaded data (default {DEFAULT_DATA})")
    ap.add_argument("--expected-dir", type=Path, default=DEFAULT_EXPECTED, help=f"the genome_amplicons folder that Night 7 wrote (default {DEFAULT_EXPECTED})")
    ap.add_argument("--reads", type=int, default=50000, help="reads per Kinnex file for the truth test (default 50000; 0 = all)")
    ap.add_argument("--reads-monomer", type=int, default=0, help="reads per Monomer file for the truth test (default: all)")
    ap.add_argument("--reads-tcal", type=int, default=20000, help="reads per file for T-cal (default 20000; 0 = all)")
    ap.add_argument("--reads-pilot", type=int, default=20000, help="reads of the pilot file (default 20000)")
    ap.add_argument("--grid", type=float, nargs="+", default=list(lt.DEFAULT_GRID), help="maxEE values of the truth test (default 1 2 3 5 10)")
    ap.add_argument("--band-size", type=int, default=32, help="DADA2's BAND_SIZE (default 32)")
    ap.add_argument("--pool", default="pseudo", choices=["pseudo", "TRUE", "FALSE"], help="DADA2's pooling (default pseudo)")
    ap.add_argument("--threads", type=int, default=0, help="DADA2 threads: 1 = one, anything else = all cores (default)")
    ap.add_argument("--keep", action="store_true", help="keep the intermediate files")
    ap.add_argument("--only", help="comma-separated steps to run")
    ap.add_argument("--skip", help="comma-separated steps to leave out")
    ap.add_argument("--redo", help="comma-separated steps to repeat even though they finished; the summary is written again")
    ap.add_argument("--fresh", action="store_true", help="repeat every step")
    ap.add_argument("--check", action="store_true", help="check the machine, the tools and the files, then stop")
    ap.add_argument("--list", action="store_true", help="show the steps and which have finished, then stop")
    ap.add_argument("--sampling", choices=["spread", "first"], default="spread", help="which reads --reads keeps: spread evenly over each file (default) or the first N (the setting of the runs up to 15 October 2026)")
    a = ap.parse_args(argv)
    lf.SAMPLING = a.sampling
    c = Ctx(a)
    if a.check:
        results = check_environment(c)
        for what, ok, detail in results:
            print(f"  [{'ok' if ok else 'NOT READY'}] {what}: {detail}")
        bad = [w for w, ok, _ in results if not ok]
        print("\nEverything is ready." if not bad else f"\n{len(bad)} thing(s) to fix before the run: " + "; ".join(bad))
        return 0 if not bad else 1
    c.out.mkdir(parents=True, exist_ok=True)
    LOG = c.log_file
    if c.state_file.is_file() and not a.fresh:
        c.state = json.loads(c.state_file.read_text(encoding="utf-8"))
    if a.list:
        list_steps(c)
        return 0
    wanted = [s.strip() for s in a.only.split(",")] if a.only else list(STEPS)
    skipped = [s.strip() for s in a.skip.split(",")] if a.skip else []
    redo = [s.strip() for s in a.redo.split(",")] if a.redo else []
    if redo and not a.only:
        wanted = redo + ["summary"]
    unknown = [s for s in wanted + skipped + redo if s not in STEPS]
    if unknown:
        print(f"Unknown step(s): {', '.join(unknown)}. The steps are: {', '.join(STEPS)}")
        return 2
    say(f"Night 8, folder {c.out}")
    t0 = time.time()
    for name in STEPS:
        if name in wanted and name not in skipped:
            run_step(c, name, force=name in redo)
    say(f"Finished in {(time.time() - t0) / 60:.0f} minutes. Read {c.out / 'NIGHT8_SUMMARY.md'} first.")
    failed = [n for n, s in c.state["steps"].items() if s["status"] == "failed"]
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
