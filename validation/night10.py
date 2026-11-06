#!/usr/bin/env python
"""Night 10: the closing run (register section 29): the tests that fill the gaps left by Nights 1 to 9 and the release checks, in one command, on the RELEASED package (0.2.0).

  python validation/night10.py --datasets [--repo REPO]      the datasets of the paths file: do their folders and references exist? then stop
  python validation/night10.py --check [--repo REPO]         the machine, the tools and the package version, then stop
  python validation/night10.py --list [--out DIR]            the steps and which have finished
  python validation/night10.py --dry-run [options]           prints every command; runs nothing
  python validation/night10.py --limit 2 --out SCRATCH ...   a pilot: two datasets, 1,000 pairs per sample (about 30 to 45 minutes); the real run is the same command without --limit
  python validation/night10.py --out C:\\data\\runs\\night10_closing_2026-11-07 --repo C:\\amplitrim_020 --config C:\\amplitrim_020\\amplitrim_paths.json \\
        --silva C:\\data\\tools\\silva\\SILVA_138.2_SSURef_NR99_tax_silva.fasta --tail-dataset d6300_V4-V5 --night3 C:\\data\\runs\\05_night3_2026-10-09 \\
        --night4 C:\\data\\runs\\07_night4_2026-10-10 --new indep_mock indep_v3v4 --its-new C:\\data\\ready_new\\its_second\\ready \\
        --overlap-mock indep_mock --grid indep_mock indep_v3v4 v4

Steps, in the order of value per hour (the grid last: it is the step left undone if the night runs short). `--only a,b` runs only those, `--skip a,b` leaves some out,
`--redo a,b` repeats finished ones, `--fresh` repeats everything. A dataset that fails is recorded and the run goes on; a step that finished is not repeated.
  version    the package every script will import: its version (must be the expected one) and a hash of its code, as the night scripts import it and as compare_methods.py does
  accept     the release check on the installed package: release_check.py (no DADA2) on a few datasets against the settings of Nights 3 and 4b (needs --night3 and --night4)
  cli        the AmpliTrim command line end to end on EVERY registered dataset and the new ones: exit status, files written, run time and peak memory (time_amplitrim.py: the data of
             Supplementary Table S4), the same run again on two datasets (is the answer the same?), --min-overlap 15 and 20 on two datasets (does the option do what it says?) and an empty input folder (exit 3, no traceback)
  tail       what are the longest amplicons of D6300 V4-V5 (16S or 18S)? tail_classify.py against SILVA (descriptive)
  coverage   the share of the longest amplicons left out: 0 (cover every amplicon), 0.2 (the default), 1 and 5%, at maxEE 2, DADA2 on the same pairs, on every 16S dataset;
             AmpliTrim's own estimate for each row is kept, so the estimate can be compared with DADA2's merged share (descriptive)
  battery    the new 16S datasets (--new): night4.py: AmpliTrim's maxEE rule against the default, 2,5 and FIGARO (the independent test; criteria in section 29)
  its        a second ITS dataset (--its-new): compare_methods.py --marker its: AmpliTrim's filter estimate against DADA2's pass rate on ITS (criterion in section 29)
  overlap    the minimum-overlap test of section 27 on a hold-out mock community (--overlap-mock): 9 DADA2 runs, judged by collect_overlap_results.py (Windows: it runs a batch file)
  grid       the truncation grid on the final build for the datasets named with --grid: overnight.py --only landscape (3 x 3 around the recommendation; criterion in section 29)
  summary    NIGHT10_SUMMARY.md: what ran, what failed, the tables, and where the output of the other scripts is

`--repo` is the folder that holds the amplitrim package of the release and validation/ (the night scripts import the package from there); the package that compare_methods.py and the
command line import is the one installed in the environment. The `version` step stops the run if their code differs (it compares a hash of every .py file) or is not the expected version.
"""
import argparse
import csv
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = ["version", "accept", "cli", "tail", "coverage", "battery", "its", "overlap", "grid", "summary"]
LEVELS = ["0", "0.01", "0.05"]               # compare_methods.py always runs the default (0.002) first, so the rows are 0.2%, 0, 1 and 5%
PAIRS = {"mockA_high": 0}                    # as in night2.py: DADA2 gets all the reads of mock A (six samples), every other dataset 5,000 pairs per sample
DEFAULT_PAIRS = 5000
PILOT_PAIRS = 1000
EXPECTED_VERSION = "0.2.0"
ACCEPT_DEFAULT = ["mockB", "v4", "its"]      # release_check.py names (keys of amplitrim_paths.json)
MIN_OVERLAP_CHECKS = (15, 20)
SUMMARY_KEYS = ("recommended", "maxEE_table", "longest_amplicon", "pairs_analysed")    # what a second run must reproduce


class Skip(Exception):
    """A step that cannot run with what it was given: recorded as skipped, with the reason."""


class Stop(Exception):
    """Nothing after this can be trusted: the run ends."""


# ------------------------------------------------------------------------------------------------------------ pure helpers (unit-tested)
def load_config(path):
    return json.loads(Path(path).read_text(encoding="utf-8")) if path and Path(path).is_file() else {}


def datasets(cfg, names=None):
    """The datasets of amplitrim_paths.json, as night2.py reads them: mockA_high, v1v2, its and the `extras`. A name list keeps only those."""
    out = []
    for key, marker in (("mockA_high", "16s"), ("v1v2", "16s"), ("its", "its")):
        if cfg.get(key):
            ref = cfg.get("reference") if key == "mockA_high" else None
            out.append({"name": key, "reads": Path(cfg[key]), "reference": Path(ref) if ref else None, "marker": marker})
    for name, e in (cfg.get("extras") or {}).items():
        if e.get("ready"):
            out.append({"name": name, "reads": Path(e["ready"]), "reference": Path(e["reference"]) if e.get("reference") else None, "marker": "16s"})
    return [d for d in out if not names or d["name"] in names]


def coverage_command(py, ds, out, pairs=None):
    """compare_methods.py at maxEE 2 with AmpliTrim rows at the default share (0.2%) and at 0, 1 and 5%."""
    n = pairs if pairs is not None else PAIRS.get(ds["name"], DEFAULT_PAIRS)
    cmd = [py, HERE / "compare_methods.py", ds["reads"], "--out", out, "--amplitrim-max-ee", "2", "--allow-unmergeable", *LEVELS, "--pairs", str(n)]
    if ds["reference"]:
        cmd += ["--reference", ds["reference"]]
    return cmd


def its_command(py, reads, out, pairs=None):
    return [py, HERE / "compare_methods.py", reads, "--out", out, "--marker", "its", "--amplitrim-max-ee", "2", "--pairs", str(pairs if pairs is not None else DEFAULT_PAIRS)]


def grid_command(py, items, out):
    """overnight.py --only landscape with one --extra NAME=READY|REFERENCE per dataset."""
    cmd = [py, HERE / "overnight.py", "--out", out, "--only", "landscape"]
    for ds in items:
        cmd += ["--extra", f"{ds['name']}={ds['reads']}" + (f"|{ds['reference']}" if ds["reference"] else "")]
    return cmd


def cli_command(py, reads, work, out, its=False, min_overlap=None):
    """The AmpliTrim command line (python -m amplitrim.cli: the package has no __main__)."""
    cmd = [py, "-m", "amplitrim.cli", "--input-dir", reads, "--work-dir", work, "--out-dir", out]
    if its:
        cmd.append("--its")
    if min_overlap:
        cmd += ["--min-overlap", str(min_overlap)]
    return cmd


def timed_command(py, label, cmd):
    return [py, HERE / "time_amplitrim.py", "--label", label, "--", *cmd]


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def ee_text(f, r):
    def one(x):
        return str(int(x)) if float(x) == int(float(x)) else f"{float(x):g}"
    return one(f) if f == r else f"{one(f)},{one(r)}"


def settings_of(summary):
    """What the report recommends, in the flat form the tables use (None where nothing was recommended)."""
    rec = summary.get("recommended")
    if not rec:
        return {"truncF": None, "truncR": None, "maxEE": None, "minOverlap": None, "longest_insert": None, "pairs": summary.get("pairs_analysed"),
                "warnings": len(summary.get("warnings") or [])}
    return {"truncF": rec["truncLenF"], "truncR": rec["truncLenR"], "maxEE": ee_text(rec["maxEE_f"], rec["maxEE_r"]), "minOverlap": rec.get("minOverlap"),
            "longest_insert": rec.get("longest_mergeable_insert"), "pairs": summary.get("pairs_analysed"), "warnings": len(summary.get("warnings") or [])}


def compare_summaries(a, b):
    """The differences between two summary.json of the same reads (empty: the second run gave the same answer)."""
    return [k for k in SUMMARY_KEYS if a.get(k) != b.get(k)]


def check_min_overlap(summary, k):
    """Problems with a run at --min-overlap k: the setting must be k, and the longest amplicon the cut can merge is the total length minus k (pipeline.py: total - min_overlap)."""
    rec = summary.get("recommended")
    if not rec:
        return [f"no recommendation at --min-overlap {k}"]
    out = []
    if rec.get("minOverlap") != k:
        out.append(f"minOverlap is {rec.get('minOverlap')}, not {k}")
    if rec.get("truncLenF") and rec.get("truncLenR") and rec["truncLenF"] + rec["truncLenR"] - k != rec.get("longest_mergeable_insert"):
        out.append(f"truncLenF + truncLenR - {k} = {rec['truncLenF'] + rec['truncLenR'] - k}, but longest_mergeable_insert is {rec.get('longest_mergeable_insert')}")
    return out


def overlap_row(ds, summary, pairs=DEFAULT_PAIRS):
    """One line of overlap_datasets.tsv (make_overlap_commands.py): the released cut of a mock community. amplicon = the longest amplicon the cut merges (total - 12)."""
    rec = summary.get("recommended")
    if not rec:
        raise ValueError(f"{ds['name']}: AmpliTrim gave no recommendation, so there is no released cut to build the overlap test on")
    return {"name": ds["name"], "ready_dir": str(ds["reads"]), "reference": str(ds["reference"]), "F": rec["truncLenF"], "amplicon": rec["longest_mergeable_insert"],
            "maxee": ee_text(rec["maxEE_f"], rec["maxEE_r"]), "pairs": pairs}


def level_label(row_name):
    """compare_methods.py names the rows 'AmpliTrim (maxEE 2)' (the default share, 0.2%) and 'AmpliTrim (maxEE 2, leave out 1.0%)'."""
    m = re.search(r"leave out ([0-9.]+)%", row_name or "")
    return f"{float(m.group(1)):g}%" if m else "0.2% (default)"


def pct(v):
    if v in (None, ""):
        return "-"
    try:
        x = float(v)
    except ValueError:
        return str(v)
    return f"{100 * x:.1f}%" if x <= 1.5 else f"{x:.1f}%"


def points(a, b):
    """b minus a in percentage points, from two shares (fractions or percents), or '-'."""
    try:
        x, y = float(a), float(b)
    except (TypeError, ValueError):
        return "-"
    x, y = (100 * x if x <= 1.5 else x), (100 * y if y <= 1.5 else y)
    return f"{y - x:+.1f}"


def package_fingerprint(folder):
    """A short hash of the code of an amplitrim package folder: every .py file, names and contents, line endings ignored."""
    import hashlib
    h = hashlib.sha256()
    for f in sorted(Path(folder).rglob("*.py")):
        if "__pycache__" in f.parts:
            continue
        h.update(f.relative_to(folder).as_posix().encode() + b"\0" + f.read_bytes().replace(b"\r\n", b"\n") + b"\0")
    return h.hexdigest()[:10]


# ------------------------------------------------------------------------------------------------------------------ the run context
class Ctx:
    def __init__(self, a):
        self.a, self.dry = a, a.dry_run
        self.repo = Path(a.repo)
        self.cfg_path = Path(a.config) if a.config else self.repo / "amplitrim_paths.json"
        self.cfg = load_config(self.cfg_path)
        self.out = Path(a.out)
        self.state = self.out / "state"
        self.py = sys.executable
        self.pairs = PILOT_PAIRS if a.limit else None
        self.logf = None
        self.notes = {}
        self.redo = set()

    def say(self, text):
        line = f"[{time.strftime('%H:%M:%S')}] {text}"
        print(line, flush=True)
        if self.logf:
            self.logf.write(line + "\n")
            self.logf.flush()

    def run(self, cmd, cwd=None, shell=False):
        self.say("$ " + (cmd if isinstance(cmd, str) else " ".join(str(c) for c in cmd)))
        if self.dry:
            return 0, ""
        try:
            p = subprocess.Popen(cmd if shell else [str(c) for c in cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace",
                                 bufsize=1, cwd=cwd, shell=shell)
        except OSError as err:
            self.say(f"   cannot start {cmd if isinstance(cmd, str) else cmd[0]}: {err}")
            return 127, str(err)
        lines = []
        for line in p.stdout:
            lines.append(line.rstrip("\n"))
            print("   " + lines[-1], flush=True)
            if self.logf:
                self.logf.write("   " + lines[-1] + "\n")
        p.wait()
        return p.returncode, "\n".join(lines)

    def mark_file(self, step, key=""):
        return self.state / (f"{step}{'_' + key if key else ''}.json")

    def finished(self, step, key=""):
        f = self.mark_file(step, key)
        return f.is_file() and read_json(f).get("status") == "done" and not self.a.fresh and step not in self.redo

    def mark(self, step, status, info="", key="", **extra):
        if self.dry:
            return
        self.state.mkdir(parents=True, exist_ok=True)
        self.mark_file(step, key).write_text(json.dumps({"status": status, "info": info, "when": time.strftime("%Y-%m-%d %H:%M:%S"), **extra}, indent=1), encoding="utf-8")

    def lim(self, items):
        return items[:self.a.limit] if self.a.limit else items

    def datasets16(self):
        return self.lim([d for d in datasets(self.cfg) if d["marker"] == "16s"])

    def datasets_all(self):
        """Every registered dataset, plus the second ITS dataset, for the command-line test."""
        ds = datasets(self.cfg)
        if self.a.its_new:
            ds.append({"name": "its_new", "reads": Path(self.a.its_new), "reference": None, "marker": "its"})
        return self.lim(ds)

    def summary_of(self, key, sub=""):
        f = self.out / "cli" / (key + sub) / "report" / "summary.json"
        return read_json(f) if f.is_file() else None


# ------------------------------------------------------------------------------------------------------------------ the steps
def step_version(c):
    code = "import amplitrim, sys; print(amplitrim.__version__); print(amplitrim.__file__)"
    seen = []
    sys.path[:0] = [str(HERE), str(c.repo)]                       # as the night scripts do
    if c.dry:
        c.say(f"(dry run) would import amplitrim in this process and in a fresh one and expect {EXPECTED_VERSION}")
        return "dry run"
    try:
        import amplitrim
        seen.append(("as the night scripts import it", amplitrim.__version__, str(Path(amplitrim.__file__).parent)))
    except Exception as err:                                        # noqa: BLE001
        raise Stop(f"amplitrim cannot be imported from {c.repo}: {err}")
    rc, text = c.run([c.py, "-c", code], cwd=str(c.out))
    lines = text.strip().splitlines()
    if rc or len(lines) < 2:
        raise Stop(f"a fresh Python cannot import amplitrim (this is what compare_methods.py needs): {text[-300:]}")
    seen.append(("as compare_methods.py imports it", lines[0], str(Path(lines[1]).parent)))
    for what, v, f in seen:
        c.say(f"amplitrim {v} ({what}): {f}")
    prints = [package_fingerprint(f) for _, _, f in seen]
    c.say(f"code fingerprint of the two imports: {prints[0]} and {prints[1]}" + (" (the same code)" if prints[0] == prints[1] else " (DIFFERENT)"))
    c.notes["version"] = "; ".join(f"{v} {f}" for _, v, f in seen) + f"; fingerprints {prints[0]} / {prints[1]}"
    problems = []
    if any(v != c.a.expect_version for _, v, _ in seen):
        problems.append(f"the version is not {c.a.expect_version}")
    if seen[0][1] != seen[1][1] or prints[0] != prints[1]:
        problems.append("the two imports are not the same code (the night scripts and compare_methods.py would test different packages: install the release with pip install amplitrim=="
                        + c.a.expect_version + " and point --repo at a checkout of the same tag)")
    rc, text = c.run([c.py, "-c", "import numpy, psutil"])
    if rc:
        problems.append("numpy or psutil cannot be imported in this Python (pip install numpy psutil)")
    for tool, args in (("vsearch", ["--version"]), ("Rscript", ["-e", "cat(as.character(packageVersion('dada2')))"])):
        rc, text = c.run([tool, *args])
        c.say(f"{tool}: {text.strip().splitlines()[0] if rc == 0 and text.strip() else 'NOT FOUND OR FAILED'}")
        if rc:
            problems.append(f"{tool} does not run")
    if problems and not c.a.allow_other_version:
        raise Stop("; ".join(problems) + " (--allow-other-version continues anyway, and the summary says so)")
    return "ok" if not problems else "continued with: " + "; ".join(problems)


def step_accept(c):
    if not (c.a.night3 and c.a.night4):
        raise Skip("give the folders of Night 3 and Night 4b with --night3 and --night4 (the settings that DADA2 was run at)")
    only = c.a.accept_only or ACCEPT_DEFAULT
    cmd = [c.py, HERE / "release_check.py", "--package", c.repo, "--config", c.cfg_path, "--night3", c.a.night3, "--night4", c.a.night4, "--only", *only, "--out", c.out / "accept"]
    rc, text = c.run(cmd)
    if rc:
        raise RuntimeError("release_check.py failed: " + text[-400:])
    return f"{', '.join(only)}: {c.out / 'accept' / 'RELEASE_CHECK_REPORT.md'}"


def run_cli(c, ds, sub="", min_overlap=None, timed=False):
    """One run of the command line; (exit code, output, the summary.json or None)."""
    key = ds["name"]
    folder = c.out / "cli"
    out, work = folder / (key + sub) / "report", folder / (key + sub) / "work"
    cmd = cli_command(c.py, ds["reads"], work, out, its=(ds["marker"] == "its"), min_overlap=min_overlap)
    rc, text = c.run(timed_command(c.py, key + sub, cmd) if timed else cmd, cwd=None if c.dry else str(folder))
    return rc, text, (None if c.dry else c.summary_of(key, sub))


def timing_of(c, label):
    f = c.out / "cli" / "timing.jsonl"
    if not f.is_file():
        return {}
    rows = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows = [r for r in rows if r.get("label") == label]
    return rows[-1] if rows else {}


def step_cli(c):
    items = c.datasets_all()
    if not c.dry:
        (c.out / "cli").mkdir(parents=True, exist_ok=True)
    problems = []
    for n, ds in enumerate(items):
        key = ds["name"]
        if c.finished("cli", key):
            c.say(f"{key}: finished in an earlier start (kept; --redo cli repeats it)")
            continue
        if not ds["reads"].is_dir() and not c.dry:
            problems.append(f"{key}: the reads folder {ds['reads']} does not exist")
            continue
        try:
            rc, text, summ = run_cli(c, ds, timed=True)
            if c.dry:                                                         # show the whole plan: the repeat and the --min-overlap runs
                if n < c.a.repeat:
                    run_cli(c, ds, sub="_repeat")
                if ds["marker"] == "16s" and n < c.a.min_overlap_datasets:
                    for k in MIN_OVERLAP_CHECKS:
                        run_cli(c, ds, sub=f"_ov{k}", min_overlap=k)
                continue
            t = timing_of(c, key)
            row = {"dataset": key, "marker": ds["marker"], "exit": t.get("exit_code", rc), "seconds": t.get("wall_seconds"), "peak_mb": t.get("peak_memory_mb")}
            issues = []
            if summ is None:
                issues.append("no summary.json written")
            else:
                row.update(settings_of(summ))
                if not (c.out / "cli" / key / "report" / "REPORT.md").is_file():
                    issues.append("REPORT.md not written")
                if ds["marker"] == "16s" and not summ.get("recommended"):
                    issues.append("no recommendation (exit status 2)")
            checks = {}
            if n < c.a.repeat and summ is not None:                           # the same reads again: the same answer?
                _, _, summ2 = run_cli(c, ds, sub="_repeat")
                diff = compare_summaries(summ, summ2) if summ2 else ["second run wrote no summary.json"]
                checks["repeat"] = "same" if not diff else "DIFFERENT: " + ", ".join(diff)
            if ds["marker"] == "16s" and n < c.a.min_overlap_datasets and summ is not None:
                for k in MIN_OVERLAP_CHECKS:                                  # does --min-overlap do what it says?
                    _, _, s3 = run_cli(c, ds, sub=f"_ov{k}", min_overlap=k)
                    bad = check_min_overlap(s3, k) if s3 else ["no summary.json"]
                    checks[f"min_overlap_{k}"] = "ok" if not bad else "PROBLEM: " + "; ".join(bad)
                    if s3 and s3.get("recommended"):
                        checks[f"cut_{k}"] = f"{s3['recommended']['truncLenF']}/{s3['recommended']['truncLenR']}"
            row["checks"] = checks
            bad = [f"{k}: {v}" for k, v in checks.items() if "DIFFERENT" in v or "PROBLEM" in v]
            c.mark("cli", "failed" if issues or bad else "done", "; ".join(issues + bad), key, row=row)
            if issues or bad:
                problems.append(f"{key}: " + "; ".join(issues + bad))
        except Exception as err:                                           # noqa: BLE001
            problems.append(f"{key}: {err}")
            c.mark("cli", "failed", str(err)[:300], key)
    if not c.finished("cli", "_negative"):
        result = negative_check(c)
        if result is not None:
            c.mark("cli", "failed" if result.startswith("PROBLEM") else "done", result, "_negative")
            if result.startswith("PROBLEM"):
                problems.append("empty input folder: " + result)
    if problems:
        raise RuntimeError("; ".join(problems))
    return f"{len(items)} datasets"


def negative_check(c):
    """The command line on an empty input folder: exit status 3 and a message on stderr, no Python traceback (docs/usage.md)."""
    empty = c.out / "cli" / "_empty_input"
    if not c.dry:
        empty.mkdir(parents=True, exist_ok=True)
    rc, text = c.run(cli_command(c.py, empty, c.out / "cli" / "_empty_work", c.out / "cli" / "_empty_report"))
    if c.dry:
        return None
    if rc == 3 and "Traceback" not in text and "Error" in text:
        return "ok: exit 3 and a message, no traceback"
    return f"PROBLEM: exit {rc}, {'a traceback' if 'Traceback' in text else 'no traceback'}, {'a message' if 'Error' in text else 'no message'}"


def step_tail(c):
    if not c.a.tail_dataset or not c.a.silva:
        raise Skip("give --tail-dataset NAME (a dataset of amplitrim_paths.json) and --silva FILE (a SILVA SSU NR99 FASTA, not gzipped)")
    ds = datasets(c.cfg, [c.a.tail_dataset])
    if not ds:
        raise Skip(f"{c.a.tail_dataset} is not in {c.cfg_path}")
    out = c.out / "tail"
    cmd = [c.py, HERE / "tail_classify.py", ds[0]["reads"], "--silva", c.a.silva, "--out", out]
    if c.a.limit:
        cmd += ["--per-sample", str(PILOT_PAIRS)]
    rc, text = c.run(cmd)
    if rc:
        raise RuntimeError("tail_classify.py failed: " + text[-400:])
    return str(out / "tail_summary.md")


def step_coverage(c):
    failed = []
    for ds in c.datasets16():
        if c.finished("coverage", ds["name"]):
            c.say(f"{ds['name']}: finished in an earlier start (kept; --redo coverage repeats it)")
            continue
        if not ds["reads"].is_dir() and not c.dry:
            failed.append(f"{ds['name']}: the reads folder {ds['reads']} does not exist")
            continue
        out = c.out / "coverage" / ds["name"]
        rc, text = c.run(coverage_command(c.py, ds, out, c.pairs))
        if rc or (not c.dry and not (out / "compare_methods.tsv").is_file()):
            failed.append(f"{ds['name']}: compare_methods.py failed ({text[-200:].strip()})")
            c.mark("coverage", "failed", failed[-1], ds["name"])
        else:
            c.mark("coverage", "done", "", ds["name"])
    if failed:
        raise RuntimeError("; ".join(failed))
    return f"{len(c.datasets16())} datasets"


def step_battery(c):
    if not c.a.new:
        raise Skip("give the new 16S datasets with --new NAME ... (names registered in amplitrim_paths.json)")
    known = {d["name"] for d in datasets(c.cfg)}
    missing = [n for n in c.a.new if n not in known]
    if missing:
        raise Skip(f"not in {c.cfg_path}: {', '.join(missing)}")
    cmd = [c.py, HERE / "night4.py", "--repo", c.repo, "--config", c.cfg_path, "--only", *c.a.new]
    if c.dry:
        cmd.append("--dry-run")
    rc, text = c.run(cmd)
    if rc:
        raise RuntimeError("night4.py failed: " + text[-400:])
    return "night4.py wrote its own NIGHT4_REPORT.md; the folder is printed in the log"


def step_its(c):
    if not c.a.its_new:
        raise Skip("give a second ITS dataset with --its-new READY (a folder of primer-free pairs)")
    out = c.out / "its_new"
    rc, text = c.run(its_command(c.py, Path(c.a.its_new), out, c.pairs))
    if rc or (not c.dry and not (out / "compare_methods.tsv").is_file()):
        raise RuntimeError("compare_methods.py --marker its failed: " + text[-400:])
    return str(out / "compare_methods.txt")


def step_overlap(c):
    if not c.a.overlap_mock:
        raise Skip("give the hold-out mock communities with --overlap-mock NAME ... (registered with expected sequences)")
    if os.name != "nt" and not c.dry:
        raise Skip("the overlap test runs a Windows batch file (make_overlap_commands.py writes one); run this step on the Windows machine")
    items = datasets(c.cfg, c.a.overlap_mock)
    missing = [n for n in c.a.overlap_mock if n not in {d["name"] for d in items}]
    if missing:
        raise Skip(f"not in {c.cfg_path}: {', '.join(missing)}")
    items = [d for d in items if d["reference"]]
    if not items:
        raise Skip("none of the --overlap-mock datasets has expected sequences ('reference' in amplitrim_paths.json)")
    out = c.out / "overlap"
    rows = []
    for ds in items:
        summ = c.summary_of(ds["name"])
        if summ is None and not c.dry:
            raise Skip(f"{ds['name']} has no cli result: run the cli step first (--only cli,overlap); its summary.json gives the released cut")
        rows.append(overlap_row(ds, summ, c.pairs or DEFAULT_PAIRS) if summ else {"name": ds["name"], "ready_dir": str(ds["reads"]), "reference": str(ds["reference"]),
                                                                                  "F": "<F>", "amplicon": "<amplicon>", "maxee": "<maxEE>", "pairs": c.pairs or DEFAULT_PAIRS})
    table, bat = out / "overlap_datasets.tsv", out / "run_overlap.bat"
    if not c.dry:
        out.mkdir(parents=True, exist_ok=True)
        with open(table, "w", newline="", encoding="utf-8") as fh:
            fh.write("name\tready_dir\treference\tF\tamplicon\tmaxee\tpairs\n")
            for r in rows:
                fh.write("\t".join(str(r[k]) for k in ("name", "ready_dir", "reference", "F", "amplicon", "maxee", "pairs")) + "\n")
    gen = [c.py, HERE / "make_overlap_commands.py", table, "--out", out, "--only", *[r["name"] for r in rows], "--slim"]
    rc, text = c.run(gen)
    if c.dry:
        return "dry run"
    if rc:
        raise RuntimeError("make_overlap_commands.py failed: " + text[-300:])
    bat.write_text(text.replace("\n", "\r\n"), encoding="utf-8")
    c.run(f'cmd /c "{bat}"', cwd=str(c.repo), shell=True)
    rc2, text2 = c.run([c.py, HERE / "collect_overlap_results.py", out, "--out", out / "overlap_results"])
    if rc2:
        raise RuntimeError("collect_overlap_results.py failed: " + text2[-300:])
    return str(out / "overlap_results.md")


def step_grid(c):
    if not c.a.grid:
        raise Skip("give the datasets that need a grid with --grid NAME ... (names registered in amplitrim_paths.json)")
    items = datasets(c.cfg, c.a.grid)
    unknown = [n for n in c.a.grid if n not in {d["name"] for d in items}]
    if unknown:
        raise Skip(f"not in {c.cfg_path}: {', '.join(unknown)}")
    cmd = grid_command(c.py, items, c.out / "grid")
    if c.a.limit:
        cmd.append("--quick")
    rc, text = c.run(cmd)
    if rc:
        raise RuntimeError("overnight.py --only landscape failed: " + text[-400:])
    return str(c.out / "grid")


def step_summary(c):
    L = ["# Night 10: the closing run", "", f"Written {time.strftime('%Y-%m-%d %H:%M')}. Package: {c.notes.get('version', 'not checked in this start (see the log)')}.",
         f"Pilot: {'yes (--limit %d, %d pairs per sample): do not use these numbers' % (c.a.limit, PILOT_PAIRS) if c.a.limit else 'no'}.", "", "## Steps", "", "| Step | Status | Detail |", "| --- | --- | --- |"]
    for s in STEPS[:-1]:
        files = sorted(c.state.glob(f"{s}*.json")) if c.state.is_dir() else []
        if not files:
            L.append(f"| {s} | not run | |")
        for f in files:
            d = read_json(f)
            L.append(f"| {f.stem} | {d['status']} | {str(d.get('info', ''))[:160].replace('|', '/')} |")
    rows = [read_json(f).get("row") for f in sorted(c.state.glob("cli_*.json"))] if c.state.is_dir() else []
    rows = [r for r in rows if r]
    L += ["", "## The command line on every dataset (Supplementary Table S4: run time and memory; the repeat and --min-overlap checks)", "",
          "| Dataset | Exit | Seconds | Peak MB | Pairs analysed | Cut F/R | maxEE | minOverlap | Warnings | Checks |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in rows:
        chk = "; ".join(f"{k}: {v}" for k, v in (r.get("checks") or {}).items()) or "-"
        L.append(f"| {r['dataset']} | {r.get('exit')} | {r.get('seconds')} | {r.get('peak_mb')} | {r.get('pairs')} | {r.get('truncF')}/{r.get('truncR')} | {r.get('maxEE')} | {r.get('minOverlap')} | {r.get('warnings')} | {chk} |")
    L += ["", "## The coverage setting (share of the longest amplicons left out), maxEE 2: DADA2's merged share, and AmpliTrim's own estimate for the same row", "",
          "| Dataset | Share left out | Cut F/R | Filter pass | AmpliTrim's estimate | DADA2 merged | Estimate minus merged (points) | Strains | Reads in exact ASVs |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for f in sorted((c.out / "coverage").glob("*/compare_methods.tsv")) if (c.out / "coverage").is_dir() else []:
        with open(f, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                if "AmpliTrim" not in (r.get("name") or ""):
                    continue
                L.append(f"| {f.parent.name} | {level_label(r.get('name'))} | {r.get('truncF', '')}/{r.get('truncR', '')} | {pct(r.get('pass'))} | {pct(r.get('own'))} | {pct(r.get('merged'))} | "
                         f"{points(r.get('merged'), r.get('own'))} | {r.get('strains') or '-'} | {pct(r.get('identical'))} |")
    for title, rel, fence in (("The longest amplicons", Path("tail") / "tail_summary.md", False), ("A second ITS dataset", Path("its_new") / "compare_methods.txt", True),
                              ("The minimum overlap on a hold-out mock", Path("overlap") / "overlap_results.md", False),
                              ("The release check on the installed package", Path("accept") / "RELEASE_CHECK_REPORT.md", False)):
        f = c.out / rel
        body = f.read_text(encoding="utf-8") if f.is_file() else "Not run (see the steps table)."
        L += ["", f"## {title}", "", ("```\n" + body + "```") if fence and f.is_file() else body]
    L += ["", "## Where the other scripts wrote", "", f"- battery (night4.py): its own folder and NIGHT4_REPORT.md, printed in {c.out / 'night10.log'}",
          f"- grid (overnight.py --only landscape): {c.out / 'grid'} (OVERNIGHT_SUMMARY.md)", "",
          "The criteria are in TEST_REGISTER.md, section 29; the verdicts are written there as section 30, after this file has been read, not here."]
    if c.dry:
        return "dry run"
    (c.out / "NIGHT10_SUMMARY.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return str(c.out / "NIGHT10_SUMMARY.md")


FUNCS = {"version": step_version, "accept": step_accept, "cli": step_cli, "tail": step_tail, "coverage": step_coverage, "battery": step_battery, "its": step_its,
         "overlap": step_overlap, "grid": step_grid, "summary": step_summary}
PER_ITEM = ("coverage", "cli")               # steps that keep one marker per dataset (their own)


def build_parser():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=Path("night10_out"))
    ap.add_argument("--repo", type=Path, default=HERE.parent, help="the folder with the amplitrim package of the release and validation/ (default: the parent of this folder)")
    ap.add_argument("--config", type=Path, help="amplitrim_paths.json (default: the one in --repo)")
    ap.add_argument("--silva", type=Path, help="SILVA SSU NR99 FASTA, not gzipped (step tail)")
    ap.add_argument("--tail-dataset", help="the dataset of amplitrim_paths.json whose longest amplicons are classified (D6300 V4-V5)")
    ap.add_argument("--night3", type=Path, help="the run folder of Night 3 (step accept)")
    ap.add_argument("--night4", type=Path, help="the run folder of Night 4b (step accept)")
    ap.add_argument("--accept-only", nargs="+", help="datasets for the release check (default: " + " ".join(ACCEPT_DEFAULT) + ")")
    ap.add_argument("--new", nargs="+", help="new 16S datasets (names in amplitrim_paths.json) for the battery")
    ap.add_argument("--its-new", type=Path, help="a second ITS dataset: a folder of primer-free pairs")
    ap.add_argument("--overlap-mock", nargs="+", help="hold-out mock communities (names in amplitrim_paths.json, with expected sequences) for the minimum-overlap test")
    ap.add_argument("--grid", nargs="+", help="datasets (names in amplitrim_paths.json) that get the truncation grid")
    ap.add_argument("--repeat", type=int, default=2, help="the command line is run twice on this many datasets (default 2)")
    ap.add_argument("--min-overlap-datasets", type=int, default=2, help="--min-overlap 15 and 20 are run on this many 16S datasets (default 2)")
    ap.add_argument("--expect-version", default=EXPECTED_VERSION)
    ap.add_argument("--allow-other-version", action="store_true")
    ap.add_argument("--limit", type=int, help="a pilot: only the first N datasets in the steps that loop over datasets, 1,000 pairs per sample, --quick for the grid")
    ap.add_argument("--only"), ap.add_argument("--skip"), ap.add_argument("--redo")
    ap.add_argument("--fresh", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true", help="only the version step, then stop")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--datasets", action="store_true", help="list the datasets of the paths file (and --its-new), say whether their folders and references exist, then stop")
    return ap


def list_datasets(c):
    """Every dataset the run would use, with a check of its folders: the way to find a wrong path before the night."""
    bad = 0
    print(f"{c.cfg_path}\n{'name':24s} {'marker':6s} {'reads folder':12s} reference")
    for d in c.datasets_all():
        reads = "ok" if d["reads"].is_dir() else "MISSING"
        ref = "-" if not d["reference"] else ("ok" if d["reference"].is_file() else "MISSING")
        bad += (reads != "ok") + (ref == "MISSING")
        print(f"{d['name']:24s} {d['marker']:6s} {reads:12s} {ref}")
    print("\nAll paths exist." if not bad else f"\n{bad} path(s) missing: correct them in the paths file.")
    return 1 if bad else 0


def main(argv=None):
    a = build_parser().parse_args(argv)
    for opt in ("only", "skip", "redo"):
        names = [s.strip() for s in (getattr(a, opt) or "").split(",") if s.strip()]
        bad = [s for s in names if s not in STEPS]
        if bad:
            print(f"Unknown step(s): {', '.join(bad)}. The steps are: {', '.join(STEPS)}")
            return 2
        setattr(a, opt, names)
    if a.limit and a.out == Path("night10_out"):
        a.out = Path("night10_pilot")
    c = Ctx(a)
    c.redo = set(a.redo)
    if a.datasets:
        return list_datasets(c)
    if a.list:
        for s in STEPS:
            files = sorted(c.state.glob(f"{s}*.json")) if c.state.is_dir() else []
            print(f"{s:10s} " + (", ".join(f"{f.stem}: {read_json(f)['status']}" for f in files) or "not run"))
        return 0
    wanted = ["version"] if a.check else (a.only or list(STEPS))
    wanted = [s for s in STEPS if s in wanted and s not in a.skip]
    if not c.dry:
        c.out.mkdir(parents=True, exist_ok=True)
        c.logf = open(c.out / "night10.log", "a", encoding="utf-8")
    c.say(f"Night 10 {'(dry run) ' if c.dry else ''}-> {c.out}; steps: {', '.join(wanted)}")
    problems = []
    for step in wanted:
        if step not in PER_ITEM and step != "summary" and c.finished(step):
            c.say(f"{step}: finished in an earlier start (kept; --redo {step} repeats it)")
            continue
        c.say(f"--- {step}")
        t0 = time.time()
        try:
            info = FUNCS[step](c)
            if step not in PER_ITEM:
                c.mark(step, "done", info)
            c.say(f"{step}: done in {time.time() - t0:.0f} s. {info}")
        except Skip as why:
            c.mark(step, "skipped", str(why))
            c.say(f"{step}: skipped: {why}")
        except Stop as why:
            c.mark(step, "stopped", str(why))
            c.say(f"{step}: STOP: {why}")
            problems.append(f"{step}: {why}")
            break
        except Exception as err:                                      # noqa: BLE001
            if step not in PER_ITEM:
                c.mark(step, "failed", str(err)[:500])
            c.say(f"{step}: FAILED: {err}")
            problems.append(f"{step}: {err}")
    if "summary" not in wanted and not a.check and not c.dry and any(s != "version" for s in wanted):
        try:
            c.say("summary: " + step_summary(c))
        except Exception as err:                                      # noqa: BLE001
            c.say(f"summary: FAILED: {err}")
    if c.logf:
        c.logf.close()
    print("\nProblems:\n  " + "\n  ".join(problems) if problems else "\nNo step failed.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
