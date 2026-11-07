#!/usr/bin/env python
"""Night 1: fetch, check, prepare and register the new datasets, then run a fresh, complete head-to-head (the standard battery) on every dataset, unattended.

  python night1.py --dry-run         (prints the plan and the commands; changes nothing)
  python night1.py                   (the run: about 5 hours; safe to leave; every step is isolated, so one failure does not stop the others)
  python night1.py --no-battery      (only the data work, about an hour)
  python night1.py --new-only        (the battery on the new datasets only; needs about 3 GB free)
  python night1.py --repo C:\\amplitrim_v2\\amplitrim --runinfo-dir C:\\Users\\Admin\\Downloads

What it does, in this order (each step is logged; a failed step is noted and the run goes on):
  0. checks the free disk space (stops below 8 GB) and writes NIGHT1_PROTOCOL.md BEFORE any analysis: the datasets, their roles, the selection rule, and that no criterion was added or changed.
  1. for each new dataset: makes <data>\\<folder>\\raw, downloads the runs with download_ena.py (checksums are verified; files already there are kept), describes the reads with describe_reads.py and chooses the
     primer and orientation settings from what the reads show, prepares them with run_dataset.py into <data>\\<folder>\\prepared\\all, and (for the two Zymo D6300 mocks) cuts the expected sequences from the Zymo
     reference file with make_reference.py.
  2. registers the datasets that were prepared in amplitrim_paths.json (a copy is kept as amplitrim_paths.json.bak_before_night1). The names: d6300_V3-V4, d6300_V4-V5, wastewater_V3-V4, spikein_V3-V4, swabs_V3-V4.
  3. runs the standard battery (overnight.py --only battery,extra_datasets) on EVERY dataset, old and new, into <data>\\runs\\night1_<date>: a fresh, complete head-to-head run in one build, one folder and one default setting
     (it needs about 5 GB free before it starts, otherwise it is skipped and the report says how to run it later; --new-only runs the new datasets only, which needs about 3 GB).
  4. writes NIGHT1_REPORT.md there: what worked, what did not, the settings chosen, and the verdicts of the battery.
Swab samples (PRJNA1261676): the project table is fetched from ENA, controls and the D6300 mock are left out by a fixed rule (below), and 36 runs are taken evenly spaced over the sorted accessions.
"""
import argparse
import copy
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

V34_F, V34_R = "CCTACGGGNGGCWGCAG", "GACTACHVGGGTATCTAATCC"          # 341F and 805R (the R1/R2 consensus of the reads agrees)
V45_F, V45_R = "GTGYCAGCMGCCGCGGTAA", "CCGYCAATTYMTTTRAGTTT"          # 515F and 926R (the R1/R2 consensus of the D6300 MiSeq reads agrees)
SWAB_PROJECT, SWAB_N = "PRJNA1261676", 36
# runs of the swab project that are not swabs: the Zymo mock and controls (matched on the run's own labels, not on the study title)
EXCLUDE = re.compile(r"zymo|d6300|mock|\bmoc\s*\d|negative control|\bneg(ative)?\b|\bntc\b|blank|positive control|water control|pcr control|extraction control|standard", re.I)
MIN_FREE_START, MIN_FREE_BATTERY, MIN_FREE_BATTERY_NEW = 8e9, 5e9, 3e9      # the battery and extra_datasets steps were 0.7 GB for seven datasets: 5 GB is a wide margin for twelve


def gb(n: float) -> str:
    return f"{n / 1e9:.1f} GB"


def select_swabs(rows: list, fields, n: int = SWAB_N) -> tuple:
    """(accessions, notes): paired runs of the project that are not mock or control by their labels, NovaSeq when the table says so, evenly spaced over the sorted accessions."""
    keep, dropped = [], 0
    for r in rows:
        text = " ".join(r.get(k, "") for k in ("experiment_title", "sample_title", "library_name", "sample_alias"))
        if fields(r, "layout") and fields(r, "layout").upper() != "PAIRED":
            continue
        inst = fields(r, "instrument")
        if inst and "novaseq" not in inst.lower():
            continue
        if EXCLUDE.search(text):
            dropped += 1
            continue
        reads = fields(r, "reads")
        if reads and reads.replace(".", "", 1).isdigit() and float(reads) < 20000:
            continue
        keep.append(fields(r, "run"))
    keep = sorted(set(k for k in keep if k))
    if n <= 0 or n >= len(keep):
        chosen = keep
    else:
        step = (len(keep) - 1) / (n - 1) if n > 1 else 0
        chosen = [keep[round(i * step)] for i in range(n)]
    return chosen, [f"{len(rows)} runs in the project; {dropped} left out as mock or control by their labels; {len(keep)} eligible; {len(chosen)} taken (evenly spaced over the sorted accessions)"]


def primer_present(describe_text: str) -> bool:
    """True when the describer finds a known primer at the start of R1 or R2 in at least half of the samples (so the primers are still in the reads)."""
    rows = [ln for ln in describe_text.splitlines() if re.match(r"^\S+\s+[\d,]+\s+\d+\s+\d+\s", ln)]
    if not rows:
        return False
    hit = sum(1 for ln in rows if any(int(m) >= 50 for m in re.findall(r"\((\d+)%, -?\d+\)", ln)))
    return hit >= len(rows) / 2


def looks_v34(fastqs: list, n: int = 1500) -> float:
    """Share of reads with the conserved V3 start GGGAAT within the first 30 bases (what follows 341F in a V3-V4 amplicon whose primers were removed)."""
    import gzip
    seen = hit = 0
    for f in fastqs:
        k = 0
        with gzip.open(f, "rt") as fh:
            for i, line in enumerate(fh):
                if i % 4 == 1:
                    seen += 1
                    k += 1
                    hit += "GGGAAT" in line[:30]
                    if k >= n:
                        break
    return hit / seen if seen else 0.0


class Night:
    def __init__(self, repo: Path, runinfo_dir: Path, dry: bool, run=None, fetch=None, disk_free=None, now=time.strftime, battery_all: bool = True):
        self.repo, self.val, self.dry, self.battery_all = Path(repo), Path(repo) / "validation", dry, battery_all
        sys.path[:0] = [str(self.val), str(self.repo)]
        import check_build
        import round4
        import select_runs
        self.cb, self.r4, self.sr = check_build, round4, select_runs
        self.cfg_path = self.repo / "amplitrim_paths.json"
        self.cfg = check_build.load_config(self.cfg_path)
        self.data = Path(self.cfg["data"])
        self.runinfo_dir = Path(runinfo_dir)
        self.py = sys.executable
        self._exec = run or self._popen
        self.fetch = fetch or select_runs.fetch_table
        self.disk_free = disk_free or (lambda p: shutil.disk_usage(p).free)
        self.stamp = now("%Y-%m-%d")
        self.out = self.data / "runs" / f"night1_{self.stamp}"
        self.registered, self.report, self.problems = {}, [], []
        self.logf = None

    # ------------------------------------------------------------------ plumbing
    def log(self, msg: str = "") -> None:
        line = f"[{time.strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        if self.logf:
            self.logf.write(line + "\n")
            self.logf.flush()

    def note(self, msg: str, problem: bool = False) -> None:
        self.report.append(("- PROBLEM: " if problem else "- ") + msg)
        if problem:
            self.problems.append(msg)
        self.log(("PROBLEM: " if problem else "") + msg)

    def run_fn(self, cmd: list, capture: bool = False) -> tuple:
        """(return code, output text). Every command is logged; in a dry run none is executed, whatever runner was given."""
        self.log("$ " + " ".join(str(c) for c in cmd))
        if self.dry:
            return 0, ""
        return self._exec(cmd)

    def _popen(self, cmd: list) -> tuple:
        """Runs one command; its output is streamed to the screen and the log."""
        p = subprocess.Popen([str(c) for c in cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", bufsize=1)
        lines = []
        for line in p.stdout:
            line = line.rstrip("\n")
            lines.append(line)
            print("   " + line, flush=True)
            if self.logf:
                self.logf.write("   " + line + "\n")
        p.wait()
        return p.returncode, "\n".join(lines)

    # ------------------------------------------------------------------ datasets
    def datasets(self) -> list:
        d = self.data

        def folder(prefix: str, default: str) -> Path:
            found = sorted(p for p in d.glob(prefix + "*") if p.is_dir()) if d.is_dir() else []
            return found[0] if found else d / default
        zip_ = next((p for p in list(d.glob("_archive*/rescued/05_references/archives/ZymoBIOMICS.STD.refseq.v2.zip")) + [Path.home() / "Downloads" / "ZymoBIOMICS.STD.refseq.v2.zip"] if p.is_file()), None)
        ri = self.runinfo_dir
        return [
            {"key": "d6300_V3-V4", "folder": folder("mock_V3-V4_zymoD6300", "mock_V3-V4_zymoD6300_PRJNA1261676"), "kind": "mock",
             "runs": [f"SRR388119{n}" for n in range(30, 40)], "primers": "auto", "min_reads": 0, "zip": zip_, "ref_primers": (V34_F, V34_R)},
            {"key": "d6300_V4-V5", "folder": folder("mock_V4-V5_zymoD6300", "mock_V4-V5_zymoD6300_miseq"), "kind": "mock",
             "runs": ["SRR16961581", "SRR16961582", "SRR16961583"], "primers": (V45_F, V45_R), "min_reads": 0, "zip": zip_, "ref_primers": (V45_F, V45_R)},
            {"key": "wastewater_V3-V4", "folder": d / "real_V3-V4_wastewater_PRJEB75155", "kind": "real", "runs": ri / "PRJEB75155_SraRunInfo.csv", "primers": (V34_F, V34_R), "mixed": True, "min_reads": 5000, "pilot": d / "pilot_wastewater"},
            {"key": "spikein_V3-V4", "folder": d / "real_V3-V4_spikein_PRJNA1243306", "kind": "real", "runs": ri / "PRJNA1243306_SraRunInfo.csv", "primers": (V34_F, V34_R), "min_reads": 5000, "pilot": d / "pilot_spike"},
            {"key": "swabs_V3-V4", "folder": d / "real_V3-V4_swabs_PRJNA1261676", "kind": "real", "runs": "swabs", "primers": "auto", "min_reads": 5000},
        ]

    def process(self, ds: dict) -> None:
        key, root = ds["key"], ds["folder"]
        raw, prepared = root / "raw", root / "prepared"
        self.report.append(f"\n### {key}  ({root.name})")
        try:
            if not self.dry:
                for sub in ("raw", "metadata", "reference"):
                    (root / sub).mkdir(parents=True, exist_ok=True)
                pilot = ds.get("pilot")
                if pilot and Path(pilot).is_dir() and not any(raw.glob("*.fastq.gz")):
                    for f in Path(pilot).iterdir():
                        shutil.move(str(f), str(raw / f.name))
                    self.note(f"moved the pilot files of {pilot.name} into raw")
            # 1. which runs
            runs = ds["runs"]
            if runs == "swabs":
                table = self.fetch(SWAB_PROJECT)
                rows = self.sr.read_table(table)
                acc, notes = select_swabs(rows, self.sr.field)
                if not acc:
                    self.note("no swab run was selected: " + "; ".join(notes), True)
                    return
                lst = root / "metadata" / "selected_runs.txt"
                if not self.dry:
                    lst.write_text("\n".join(acc) + "\n", encoding="utf-8")
                    (root / "metadata" / "project_run_table.tsv").write_text(table, encoding="utf-8")
                for n in notes:
                    self.note(n)
                source = [str(lst)]
            elif isinstance(runs, Path):
                if not runs.is_file():
                    self.note(f"the run list {runs} is missing: put it in {self.runinfo_dir} or use --runinfo-dir", True)
                    return
                source = [str(runs)]
            else:
                source = list(runs)
            # 2. download (a repeat only checks what is there)
            rc, _ = self.run_fn([self.py, self.val / "download_ena.py", *source, "--out", raw])
            have = sorted(raw.glob("*_R1.fastq.gz")) if raw.is_dir() else []
            if rc != 0:
                self.note(f"the download ended with errors; {len(have)} runs are on disk" + ("" if not have else " (partial: the dataset goes on with what arrived)"), bool(have))
            if not have and not self.dry:
                self.note("no reads on disk: stopped for this dataset", True)
                return
            self.note(f"{len(have)} runs of reads in raw" if not self.dry else "(dry run) would download the runs")
            # 3. describe, and choose the settings from what the reads show
            rc, text = self.run_fn([self.py, self.val / "describe_reads.py", raw])
            if not self.dry:
                (root / "metadata" / "describe_raw.txt").write_text(text, encoding="utf-8")
            primers = ds["primers"]
            if primers == "auto":
                primers = (V34_F, V34_R) if primer_present(text) else None
                self.note("primers: " + ("still in the reads, removed with 341F and 805R" if primers else "already removed from the reads (used as they are)"))
            else:
                self.note("primers: " + ("341F/805R" if primers == (V34_F, V34_R) else "515F/926R"))
            mixed = bool(ds.get("mixed")) or "use --mixed-orientation" in text
            if mixed:
                self.note("some pairs are sequenced in the reverse orientation: --mixed-orientation")
            if ds["key"] in ("swabs_V3-V4", "d6300_V3-V4") and not self.dry:
                share = looks_v34(have[:5])
                self.note(f"share of reads with the conserved V3 start (GGGAAT in the first 30 bases): {share:.0%}" + ("" if share >= 0.3 else "  <- low: check the region"), share < 0.3)
            # 4. prepare
            cmd = [self.py, self.val / "run_dataset.py", "all", raw, "--out", prepared, "--error-rate", "0.15", "--pairs", "100000"]
            if primers:
                cmd += ["--primer-f", primers[0], "--primer-r", primers[1]]
            if mixed:
                cmd.append("--mixed-orientation")
            if ds.get("min_reads"):
                cmd += ["--min-reads", str(ds["min_reads"])]
            rc, _ = self.run_fn(cmd)
            ready = prepared / "all" / "ready"
            n_ready = len(list(ready.glob("*_R1.fastq.gz"))) if ready.is_dir() else 0
            if (rc != 0 or not n_ready) and not self.dry:
                self.note(f"the preparation failed (code {rc}; {n_ready} samples in ready)", True)
                return
            self.note(f"prepared: {n_ready} samples in {ready}" if not self.dry else f"(dry run) would prepare into {ready}")
            # 5. the expected sequences of the Zymo mocks
            ref = ""
            if ds.get("zip"):
                out_ref = root / "reference" / f"{key}_expected_sequences.fasta"
                rc, _ = self.run_fn([self.py, self.val / "make_reference.py", ds["zip"], "--primer-f", ds["ref_primers"][0], "--primer-r", ds["ref_primers"][1], "--exclude", "18S|ITS", "--out", out_ref])
                if (rc == 0 and out_ref.is_file() and out_ref.stat().st_size > 0) or self.dry:
                    ref = str(out_ref)
                    self.note(f"expected sequences: {out_ref}")
                else:
                    self.note("the expected sequences could not be cut from the Zymo file: the dataset is registered without a reference", True)
            elif key.startswith("d6300"):
                self.note("the Zymo reference file (ZymoBIOMICS.STD.refseq.v2.zip) was not found: no reference", True)
            self.registered[key] = {"ready": str(ready), "reference": ref}
        except SystemExit as e:                                                          # a tool that stops with a message
            self.note(f"stopped: {e}", True)
        except Exception as e:                                                           # nothing here may stop the other datasets
            self.note(f"failed: {type(e).__name__}: {e}", True)

    # ------------------------------------------------------------------ the run
    def protocol_text(self, ds_list: list) -> str:
        build = ""
        try:
            build = self.run_fn([self.py, self.val / "run_dataset.py", "--version"])[1].strip()
        except Exception:
            pass
        L = [f"# Night 1 protocol (written {time.strftime('%Y-%m-%d %H:%M')}, before any analysis)", "", f"Build: {build or 'unknown'}", "",
             "Purpose: a FRESH, COMPLETE head-to-head run: prepare the new datasets, then run the standard battery (criteria fixed in TEST_REGISTER.md, section 3) on " + ("EVERY dataset, old and new, in one build, one output folder and one default setting (--allow-unmergeable 0.2%), replacing the mixed numbers of earlier runs. " if self.battery_all else "the new datasets only. ")
             + "No criterion was added or changed for this run, and no result has been looked at.", "",
             "Arms (the standard battery's comparisons, run through DADA2 on the same reads): AmpliTrim's recommendation at maxEE 2 (and 1 and 5), AmpliTrim at FIGARO's own maxEE, FIGARO as shipped, and no truncation; paired per-sample differences with intervals. "
             "FIGARO cannot be run on ITS. Not in this run: the median-Q30 baseline and the skin dataset (no run table yet).", "", "| dataset | kind | role |", "| --- | --- | --- |"]
        roles = [("mockA_high", "mock", "development"), ("mockA_all", "mock", "development"), ("v4 (soil V4)", "real", "development"), ("mockB", "mock", "held out"), ("mcm_v12 (inter-lab V1-V2)", "mock", "held out"),
                 ("mcm_v46 (inter-lab V4-V6)", "mock", "held out"), ("v1v2", "real", "held out"), ("its", "real", "case study (no FIGARO)")] if self.battery_all else []
        for name, kind, role in roles:
            L.append(f"| {name} | {kind} | {role} |")
        for d in ds_list:
            L.append(f"| {d['key']} | {d['kind']} | held out (not used to design anything) |")
        L += ["", f"Swab selection rule (fixed here): paired NovaSeq runs of {SWAB_PROJECT}, leaving out runs whose own labels match the mock/control pattern `{EXCLUDE.pattern}`, with at least 20,000 reads; "
              f"{SWAB_N} runs evenly spaced over the sorted accessions. Samples under 5,000 read pairs are dropped at preparation.",
              "Primers and orientation are chosen from what describe_reads.py finds in the reads of each dataset, as written in night1.py.", "Expected sequences for the D6300 mocks: the Zymo reference file, cut between the primers.", ""]
        return "\n".join(L)

    def go(self, battery: bool) -> int:
        ds_list = self.datasets()
        self.log("night1_v2.py: " + ("a fresh, complete head-to-head run (the standard battery on EVERY dataset)" if self.battery_all else "the standard battery on the NEW datasets only"))
        free = self.disk_free(self.data if self.data.exists() else Path("."))
        self.log(f"free space on the data drive: {gb(free)}")
        if free < MIN_FREE_START:                                                        # checked first: a stop leaves nothing behind
            self.log(f"STOP: less than {gb(MIN_FREE_START)} free. Free some space first (slim_archive.py) and run again.")
            return 2
        if not self.dry:
            self.out.mkdir(parents=True, exist_ok=True)
            self.logf = open(self.out / "night1.log", "a", encoding="utf-8")
        if not self.dry:
            (self.out / "NIGHT1_PROTOCOL.md").write_text(self.protocol_text(ds_list), encoding="utf-8")
        else:
            self.log("(dry run: the protocol note would be written to " + str(self.out / "NIGHT1_PROTOCOL.md") + ")")
        with self.cb.keep_awake():
            for ds in ds_list:
                self.log(f"=== {ds['key']}")
                self.process(ds)
                self.log(f"free space: {gb(self.disk_free(self.data if self.data.exists() else Path('.')))}")
            self.register()
            if battery:
                self.battery()
        self.write_report()
        return 0

    def register(self) -> None:
        if not self.registered:
            self.note("no new dataset was prepared: nothing to register", True)
            return
        cfg = self.cfg
        if not self.dry:
            shutil.copy2(self.cfg_path, self.cfg_path.with_name(self.cfg_path.name + ".bak_before_night1"))
            for k, v in self.registered.items():
                cfg.setdefault("extras", {})[k] = v
            self.cb.save_config(self.cfg_path, cfg)
        self.note("registered in amplitrim_paths.json (copy kept as .bak_before_night1): " + ", ".join(self.registered))

    def battery(self) -> None:
        free, need = self.disk_free(self.data), (MIN_FREE_BATTERY if self.battery_all else MIN_FREE_BATTERY_NEW)
        if free < need:
            self.note(f"the battery was not started: only {gb(free)} free (at least {gb(need)} needed). The data work is done and registered: free some space (slim_archive.py) and run  python validation\\check_build.py --round4 --phases C", True)
            return
        cfg2 = copy.deepcopy(self.cfg)
        cfg2["out"] = str(self.out)                                                      # in memory only: the config's own out folder is left as it is
        if not self.battery_all:                                                         # --new-only: the old datasets are left out (a smaller run for a smaller disk)
            cfg2["extras"] = {}
        for k, v in self.registered.items():
            cfg2.setdefault("extras", {})[k] = v
        steps = "battery,extra_datasets" if self.battery_all else "extra_datasets"
        args = self.cb.overnight_args(cfg2, SimpleNamespace(only=steps, skip=None, quick=False, fresh=False))
        self.log("=== the standard battery on " + ("all datasets" if self.battery_all else "the new datasets only"))
        rc, _ = self.run_fn([self.py, self.val / "overnight.py", *args])
        self.note(f"the battery ended with code {rc}; results in {self.out}", rc != 0)
        for step in steps.split(","):
            try:
                self.report += ["", f"#### {step}"] + self.r4.step_lines(self.out, step)
            except Exception as e:
                self.note(f"could not read the verdicts of {step}: {e}", True)

    def write_report(self) -> None:
        head = [f"# Night 1 report ({time.strftime('%Y-%m-%d %H:%M')})", "", f"Problems: {len(self.problems)}" + ("" if not self.problems else "  (marked PROBLEM below)"), ""]
        text = "\n".join(head + self.report + ["", "Next: send this file and OVERNIGHT_SUMMARY.md from the same folder."]) + "\n"
        if self.dry:
            print("\n" + text)
        else:
            (self.out / "NIGHT1_REPORT.md").write_text(text, encoding="utf-8")
            self.log(f"report: {self.out / 'NIGHT1_REPORT.md'}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cwd = Path.cwd()
    ap.add_argument("--repo", type=Path, default=cwd if (cwd / "validation" / "check_build.py").is_file() else Path(r"C:\amplitrim_v2\amplitrim"))
    ap.add_argument("--runinfo-dir", type=Path, default=Path.home() / "Downloads", help="where PRJEB75155_SraRunInfo.csv and PRJNA1243306_SraRunInfo.csv are")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-battery", action="store_true")
    ap.add_argument("--new-only", action="store_true", help="run the battery on the new datasets only (needs about 3 GB free; the default is every dataset and needs about 5 GB)")
    args = ap.parse_args(argv)
    return Night(args.repo, args.runinfo_dir, args.dry_run, battery_all=not args.new_only).go(not args.no_battery)


if __name__ == "__main__":
    sys.exit(main())
