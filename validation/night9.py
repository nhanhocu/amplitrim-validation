"""Night 9: the Revio hold-out of the long-read work, on the PacBio Revio Kinnex-16S data of the ATCC MSA-1003 mock community.

Revio writes binned quality scores by default, Sequel II (the platform of Night 6 to Night 8) the full range up to Q93. This run asks whether what was found on Sequel II holds on Revio, for the same three
barcode pairs (the same wells), with a reference that was refined on Night 8 and has never been applied to the data it came from (msa1003_refined_variants.fasta).
The design, the predictions and the gates are in FUTURE.md of the archive ("Night 9, the Revio hold-out", written on 15 October 2026, before the data were downloaded).

Steps (--list shows which have finished, --redo STEP repeats one, --check tests the machine and the files first):
  quality   the highest quality score and the distinct scores of the Revio and the Sequel II files (are the Revio reads binned?)
  order     read_order_check.py on the Revio and the Sequel II files: is the order of the reads random? (the Revio files of the first run of Night 9 were not, and the first reads are then not a fair sample)
  tcal      T-cal (longread_calibration.py) for the Revio and the Sequel II reads, against the refined reference; T-cal-1 is the gate T-cal-R1 and T-cal-2 is T-cal-R2
  truth     the truth test (longread_truth.py) on the Revio reads against the refined reference: the error model is chosen from the quality scores; the gates T2, T3, T5 and T6 of Night 9
  summary   NIGHT9_SUMMARY.md: what ran, the gates, the three predictions, and what to send back

    python night9.py --check
    python night9.py --out C:\\data\\runs\\20_night9b_revio --only quality,order,tcal
    python night9.py --out C:\\data\\runs\\20_night9b_revio                     (resumes: finished steps are skipped)

The three Revio files go into <data>\\revio_monomer_fastq (see PUSH_TO_GITHUB.md); the Sequel II files of Night 7 are in <data>\\sq2_monomer_fastq; Night 7's genome_amplicons folder is --expected-dir.
Needs Python 3.9+, numpy, rapidfuzz, cutadapt (pip install cutadapt) and R with DADA2 (with makeBinnedQualErrfun for binned scores).
"""

import argparse
import csv
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
import read_order_check as roc  # noqa: E402
from night7 import DEFAULT_DATA, MONOMER_PAIRS, PRIMERS, Skip, md_lines, tool_version, versions  # noqa: E402
from night8 import DEFAULT_EXPECTED, linked_folder  # noqa: E402
from rtools import NOT_FOUND, find_rscript  # noqa: E402

STEPS = ["quality", "order", "tcal", "truth", "summary"]
REVIO_FOLDER, SQ2_FOLDER = "revio_monomer_fastq", "sq2_monomer_fastq"
REFINED, REPLICATE = HERE / "msa1003_refined_variants.fasta", HERE / "msa1003_night8_asv_set.txt"
NEEDED_GB = 2
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
        self.revio, self.sq2 = self.data / REVIO_FOLDER, self.data / SQ2_FOLDER
        self.fasta, self.strains = self.expected_dir / "expected_amplicons.fasta", self.expected_dir / "genome_amplicons.tsv"
        self.refined, self.replicate = Path(args.refined), Path(args.replicate_set)
        self.tcal_out, self.truth_out = self.out / "tcal", self.out / "truth"
        self.state_file, self.log_file = self.out / "night9_state.json", self.out / "night9.log"
        self.state = {"steps": {}}


def pair_files(folder: Path, what: str) -> list:
    files = lf.find_files(folder) if folder.is_dir() else []
    chosen = [p for p in files if any(pair in p.name for pair in MONOMER_PAIRS)]
    if len(chosen) < len(MONOMER_PAIRS):
        raise Skip(f"only {len(chosen)} of the {len(MONOMER_PAIRS)} {what} files are in {folder} ({', '.join(MONOMER_PAIRS)})")
    return chosen


def need_references(c: Ctx) -> None:
    for p, what in ((c.fasta, "the expected amplicons of Night 7"), (c.strains, "the table of the strains of Night 7"), (c.refined, "the refined reference"), (c.replicate, "the replication set")):
        if not p.is_file():
            raise Skip(f"{what} is missing: {p}")


def need_tools(r: bool) -> None:
    lc.check_cutadapt()
    if r and not find_rscript():
        raise SystemExit(NOT_FOUND)


# ----------------------------------------------------------------------------- the steps

def quality_rows(c: Ctx) -> list:
    rows = []
    for lib, files in (("Revio", pair_files(c.revio, "Revio")), ("SequelII", pair_files(c.sq2, "Sequel II"))):
        for p in files:
            top, values = lc.quality_profile(p, c.args.reads_tcal)
            rows.append((lib, p.name, top, len(values), " ".join(str(v) for v in values)))
    return rows


def describe_quality(rows: list) -> dict:
    """{library: (highest score, number of distinct scores, binned)} over the files of the library."""
    out = {}
    for lib in dict.fromkeys(r[0] for r in rows):
        top = max(r[2] for r in rows if r[0] == lib and r[2] is not None)
        values = sorted({int(v) for r in rows if r[0] == lib for v in r[4].split()})
        out[lib] = (top, len(values), top < 93 and len(values) <= lt.MAX_BINNED_VALUES)
    return out


def step_quality(c: Ctx) -> str:
    rows = quality_rows(c)
    c.out.mkdir(parents=True, exist_ok=True)
    with open(c.out / "quality.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["library", "file", "highest_quality", "distinct_values", "values"])
        w.writerows(rows)
    d = describe_quality(rows)
    return "; ".join(f"{lib}: highest Q {top}, {n} distinct values, {'binned' if binned else 'not binned'}" for lib, (top, n, binned) in d.items())


def step_order(c: Ctx) -> str:
    need_references(c)
    revio, sq2 = pair_files(c.revio, "Revio"), pair_files(c.sq2, "Sequel II")
    need_tools(False)
    results = roc.run(revio + sq2, c.refined, PRIMERS[0], PRIMERS[1], c.out / "order", blocks=10, per_block=400, keep=c.args.keep, log=say)
    libs = ["Revio"] * len(revio) + ["SequelII"] * len(sq2)
    with open(c.out / "order" / "order_by_library.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["library", "file", "v", "v_random_order", "verdict"])
        for lib, r in zip(libs, results):
            s = r["stats"]
            w.writerow([lib, r["file"], "" if s is None else round(s["v"], 4), "" if s is None else round(s["null_v"], 4), "not tested" if s is None else ("random" if s["random"] else "NOT RANDOM")])
    bad = lambda lib: sum(1 for l, r in zip(libs, results) if l == lib and r["stats"] is not None and not r["stats"]["random"])
    return f"Revio: {bad('Revio')} of {len(revio)} files NOT RANDOM; SequelII: {bad('SequelII')} of {len(sq2)} files NOT RANDOM"


def step_tcal(c: Ctx) -> str:
    need_references(c)
    revio, sq2 = pair_files(c.revio, "Revio"), pair_files(c.sq2, "Sequel II")
    need_tools(False)
    f1, f2 = linked_folder(revio, c.out / "tcal_revio_input"), linked_folder(sq2, c.out / "tcal_sq2_input")
    try:
        r = lcal.run({"Revio": f1, "SequelII": f2}, c.refined, PRIMERS[0], PRIMERS[1], c.tcal_out, reads=c.args.reads_tcal, strains_table=c.strains, keep=c.args.keep, log=say)
    finally:
        shutil.rmtree(f1, ignore_errors=True)
        shutil.rmtree(f2, ignore_errors=True)
    return "; ".join(f"{g} {s}" for g, (s, _) in r["gates"].items())


def step_truth(c: Ctx) -> str:
    need_references(c)
    revio = pair_files(c.revio, "Revio")
    need_tools(True)
    folder = linked_folder(revio, c.out / "truth_revio_input")
    try:
        r = lt.run({"Revio": folder}, c.fasta, c.strains, PRIMERS[0], PRIMERS[1], c.truth_out, reads=c.args.reads, grid=(2,), band=c.args.band_size, pool=c.args.pool, threads=c.args.threads,
                   keep=c.args.keep, log=say, refined_fasta=c.refined, replicate_file=c.replicate, extras=("dada2primers", "naive"), errfun=c.args.errfun)
    finally:
        shutil.rmtree(folder, ignore_errors=True)
    info = r["libraries"]["Revio"]
    return f"error model {info['errfun']}; the rule gives maxEE {info['rule']}; " + ", ".join(f"{k} {s}" for k, (s, _) in r["gates"]["Revio"].items())


# ----------------------------------------------------------------------------- the summary

def read_tsv(path: Path) -> list:
    if not Path(path).is_file():
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return [{k.strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(fh, delimiter="\t")]


def composition_agreement(c: Ctx) -> dict:
    """{Revio file: Spearman correlation} between the composition by strain that T-cal measured and the one that the truth test found, for the same file: the same reads should give the same composition."""
    comp = read_tsv(c.tcal_out / "composition.tsv")
    asvs = [a for a in read_tsv(c.truth_out / "truth_asvs_Revio_ee2.tsv") if a["chimera"] != "True"]
    if not comp or not asvs:
        return {}
    tc, tr = {}, {}
    for r in comp:
        if r["library"] == "Revio":
            tc.setdefault(r["file"], {})[r["strain"]] = int(r["reads"])
    for a in asvs:
        strain = a["nearest_variant"].split("|")[1]
        for part in a["reads_per_sample"].split(";"):
            if "=" in part:
                smp, n = part.rsplit("=", 1)
                tr.setdefault(smp, {})
                tr[smp][strain] = tr[smp].get(strain, 0) + int(n)
    out = {}
    for f in sorted(set(tc) & set(tr)):
        strains = sorted(set(tc[f]) | set(tr[f]))
        out[f] = lc.spearman([tc[f].get(s, 0) for s in strains], [tr[f].get(s, 0) for s in strains])
    return out


def predictions(c: Ctx) -> list:
    """The three predictions written before the data were seen, with what was found."""
    out = []
    q = read_tsv(c.out / "quality.tsv")
    if q:
        rows = [(r["library"], r["file"], int(r["highest_quality"]) if r["highest_quality"] else None, int(r["distinct_values"]), r["values"]) for r in q]
        top, n, binned = describe_quality(rows)["Revio"]
        out.append(f"1. The Revio reads are binned (highest Q at most 40 and at most 12 distinct values): highest Q {top}, {n} distinct values: " + ("as predicted" if binned and top <= 40 else "NOT as predicted") + ".")
    else:
        out.append("1. The Revio reads are binned: not known (the quality step did not finish).")
    cond = {r["condition"]: r for r in read_tsv(c.truth_out / "truth_conditions.tsv")}
    if "ee2" in cond and "ee2_naive" in cond:
        a, b = int(cond["ee2"]["replicated"]), int(cond["ee2_naive"]["replicated"])
        out.append(f"2. The binned model recovers at least as many of the replication set as the naive condition: {a} against {b}: " + ("as predicted" if a >= b else "NOT as predicted") + ".")
    else:
        out.append("2. The binned model against the naive condition: not known (no naive condition ran, which is the case when the reads are not binned, or the truth step did not finish).")
    if "ee2" in cond and int(cond["ee2"]["replicate_total"] or 0):
        a, t = int(cond["ee2"]["replicated"]), int(cond["ee2"]["replicate_total"])
        out.append(f"3. At least 90% of the replication set is found again: {a} of {t} ({100 * a / t:.1f}%): " + ("as predicted" if a >= 0.9 * t else "NOT as predicted") + ".")
    else:
        out.append("3. The replication of the 49 sequences: not known (the truth step did not finish).")
    order = read_tsv(c.out / "order" / "order_by_library.tsv")
    if order:
        n_r = [r for r in order if r["library"] == "Revio"]
        n_s = [r for r in order if r["library"] == "SequelII"]
        a, b = sum(r["verdict"] == "NOT RANDOM" for r in n_r), sum(r["verdict"] == "NOT RANDOM" for r in n_s)
        out.append(f"4. The order check flags the Revio files and not the Sequel II files: Revio {a} of {len(n_r)} NOT RANDOM, Sequel II {b} of {len(n_s)}: " + ("as predicted" if a == len(n_r) and b == 0 else "NOT as predicted") + ".")
    else:
        out.append("4. The order check on the Revio and the Sequel II files: not known (the order step did not run).")
    agree = composition_agreement(c)
    if agree:
        label = lambda f: (re.search(r"Fwd_\d+--Kinnex16S_Rev_\d+", f) or [f])[0]
        rhos = {label(f): r for f, r in agree.items()}
        out.append("5. T-cal and the truth test see the same composition in each Revio file (Spearman at least 0.9): " + ", ".join(f"{k} {'-' if r is None else format(r, '.2f')}" for k, r in rhos.items()) + ": "
                   + ("as predicted" if all(r is not None and r >= 0.9 for r in rhos.values()) else "NOT as predicted") + ".")
    else:
        out.append("5. T-cal and the truth test see the same composition: not known (T-cal or the truth step did not finish).")
    return out


def step_summary(c: Ctx) -> str:
    v = versions()
    lines = ["# Night 9: the Revio hold-out (quality scores, T-cal and the truth test on Revio Monomer reads of ATCC MSA-1003)", "",
             f"Run on {datetime.date.today()}; folder {c.out}. Design, predictions and gates: FUTURE.md of the archive (written on 15 October 2026, before the data were downloaded). "
             "Tools: " + "; ".join(f"{k} {x}" for k, x in v.items()) + ".", "", "## Steps", ""]
    for name in STEPS:
        if name == "summary":
            continue
        s = c.state["steps"].get(name)
        lines.append(f"- {name}: " + (f"{s['status']} in {max(1, round(s['seconds'] / 60))} min" + (f" ({s['detail'].splitlines()[0]})" if s["detail"] else "") if s else "not run"))
    lines += ["", "## Quality scores", ""]
    q = read_tsv(c.out / "quality.tsv")
    if q:
        lines += ["| library | file | highest | distinct values | values |", "|---|---|---|---|---|"] + [f"| {r['library']} | {r['file']} | {r['highest_quality']} | {r['distinct_values']} | {r['values'] if int(r['distinct_values']) <= 12 else '(many)'} |" for r in q]
    else:
        lines.append("No result (the step did not finish; see the steps above).")
    lines += ["", "## Order of the reads (is a file in random order?)", ""]
    body = md_lines(c.out / "order" / "ORDER_CHECK.md", "## ")
    lines += body if body else ["No result (the step did not run or did not finish; see the steps above)."]
    lines += ["", "## T-cal: Revio against Sequel II (reference: the refined set). T-cal-1 below is the gate T-cal-R1 and T-cal-2 is T-cal-R2", ""]
    tcal = c.tcal_out / "TCAL.md"
    if not md_lines(tcal, "**Gate"):
        lines.append("No result (the step did not finish; see the steps above).")
    else:
        lines += md_lines(tcal, "**Gate", "## ") + md_lines(tcal, "## Revio", "## Composition") + md_lines(tcal, "## Composition", "## Similarity") + md_lines(tcal, "## Similarity")
    lines += ["", "## Truth test: Revio", ""]
    body = md_lines(c.truth_out / "TRUTH.md", "## ")
    lines += body if body else ["No result (the step did not finish; see the steps above)."]
    lines += ["", "## The predictions (written before the data were seen)", ""] + predictions(c) + [""]
    lines += ["## Send back", "", f"- this file ({c.out / 'NIGHT9_SUMMARY.md'})", f"- {c.out / 'quality.tsv'}", f"- {c.tcal_out / 'TCAL.md'}", f"- {c.truth_out / 'TRUTH.md'}, its truth_conditions.tsv and truth_strains.tsv",
              f"- {c.log_file} if a step failed"]
    (c.out / "NIGHT9_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return "NIGHT9_SUMMARY.md written"


STEP_FUNCTIONS = {"quality": step_quality, "order": step_order, "tcal": step_tcal, "truth": step_truth, "summary": step_summary}


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
    except Exception:
        detail, status = traceback.format_exc(limit=6), "failed"
    c.state["steps"][name] = {"status": status, "seconds": int(time.time() - t0), "detail": (detail or "")[:3000], "finished": datetime.datetime.now().isoformat(timespec="seconds")}
    save_state(c)
    say(f"{name}: {status}" + (f" - {detail.splitlines()[0]}" if detail else ""))
    if status == "failed" and detail:
        say(detail)


# ----------------------------------------------------------------------------- --check and --list

def check_environment(c: Ctx) -> list:
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
            for fn in ("PacBioErrfun", "makeBinnedQualErrfun"):
                ok2, text2 = tool_version([rscript, "-e", f"suppressMessages(library(dada2)); cat(if (exists('{fn}')) 'yes' else 'no')"])
                good = bool(ok2) and text2.strip().endswith("yes")
                out.append((f"{fn} in DADA2", good, "present" if good else "this DADA2 lacks it: update DADA2"))
    try:
        free = shutil.disk_usage(c.out if c.out.exists() else (c.out.parent if c.out.parent.exists() else Path("."))).free / 1e9
        out.append((f"{NEEDED_GB} GB free", free >= NEEDED_GB, f"{free:.1f} GB free"))
    except OSError as err:
        out.append((f"{NEEDED_GB} GB free", False, str(err)))
    for p, what in ((c.fasta, "expected amplicons (Night 7)"), (c.strains, "table of the strains (Night 7)"), (c.refined, "refined reference"), (c.replicate, "replication set")):
        out.append((what, p.is_file(), str(p)))
    for folder, what in ((c.revio, "Revio files"), (c.sq2, "Sequel II files")):
        found = [p for p in (lf.find_files(folder) if folder.is_dir() else []) if any(pair in p.name for pair in MONOMER_PAIRS)]
        out.append((what, len(found) == len(MONOMER_PAIRS), f"{len(found)} of {len(MONOMER_PAIRS)} in {folder}"))
    return out


def list_steps(c: Ctx) -> None:
    for name in STEPS:
        s = c.state["steps"].get(name)
        print(f"  {name:10s} " + (f"{s['status']} ({s['finished']})" if s else "not run"))


def main(argv=None) -> int:
    global LOG
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=Path("night9_revio"), help="the folder for everything this run makes")
    ap.add_argument("--data", type=Path, default=DEFAULT_DATA, help=f"the folder of the downloaded data (default {DEFAULT_DATA})")
    ap.add_argument("--expected-dir", type=Path, default=DEFAULT_EXPECTED, help=f"the genome_amplicons folder that Night 7 wrote (default {DEFAULT_EXPECTED})")
    ap.add_argument("--refined", type=Path, default=REFINED, help="the refined reference (default: the one in this folder)")
    ap.add_argument("--replicate-set", type=Path, default=REPLICATE, help="the names of the 49 sequences of Night 8 (default: the file in this folder)")
    ap.add_argument("--reads", type=int, default=50000, help="reads per Revio file for the truth test (default 50000; 0 = all)")
    ap.add_argument("--reads-tcal", type=int, default=20000, help="reads per file for the quality step and T-cal (default 20000; 0 = all)")
    ap.add_argument("--errfun", help="PacBioErrfun or binned:<scores> (default: chosen from the quality scores of the reads)")
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
    say(f"Night 9, folder {c.out}")
    t0 = time.time()
    for name in STEPS:
        if name in wanted and name not in skipped:
            run_step(c, name, force=name in redo)
    say(f"Finished in {(time.time() - t0) / 60:.0f} minutes. Read {c.out / 'NIGHT9_SUMMARY.md'} first.")
    return 1 if any(s["status"] == "failed" for s in c.state["steps"].values()) else 0


if __name__ == "__main__":
    sys.exit(main())
