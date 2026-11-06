"""The closing run (register section 29): the driver's pure helpers, its wiring (datasets, commands, a dry run, the refusals, resume, a failing dataset, the version stop) and
the long-amplicon classifier, the latter end to end with real vsearch on small synthetic reads (skipped where vsearch is not installed)."""
import gzip
import json
import random
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "validation"))
import night10 as n10  # noqa: E402
import tail_classify as tc  # noqa: E402


def config(tmp_path, with_its=True):
    cfg = {"mockA_high": str(tmp_path / "mockA"), "reference": str(tmp_path / "ref.fa"), "v1v2": str(tmp_path / "v1v2"),
           "extras": {"indep_mock": {"ready": str(tmp_path / "im"), "reference": str(tmp_path / "im.fa")}, "indep_v3v4": {"ready": str(tmp_path / "iv")}}}
    if with_its:
        cfg["its"] = str(tmp_path / "its")
    path = tmp_path / "paths.json"
    path.write_text(json.dumps(cfg), encoding="utf-8")
    return path


def summary(tf=273, tr=247, ef=2, er=3, k=12, insert=None, warnings=()):
    return {"schema_version": 1, "recommended": {"truncLenF": tf, "truncLenR": tr, "maxEE_f": ef, "maxEE_r": er, "minOverlap": k, "longest_mergeable_insert": tf + tr - k if insert is None else insert},
            "maxEE_table": [[2, 70.0]], "longest_amplicon": 508, "pairs_analysed": 43922, "warnings": list(warnings)}


# ------------------------------------------------------------------------------------------------------------------ pure helpers
def test_the_datasets_are_read_as_the_nights_read_them(tmp_path):
    ds = n10.datasets(n10.load_config(config(tmp_path)))
    assert [d["name"] for d in ds] == ["mockA_high", "v1v2", "its", "indep_mock", "indep_v3v4"]
    assert [d["marker"] for d in ds] == ["16s", "16s", "its", "16s", "16s"]
    assert ds[0]["reference"].name == "ref.fa" and ds[1]["reference"] is None and ds[3]["reference"].name == "im.fa"
    assert [d["name"] for d in n10.datasets(n10.load_config(config(tmp_path)), ["v1v2"])] == ["v1v2"]


def test_the_coverage_command_runs_the_default_and_0_1_and_5_percent_at_maxee_2(tmp_path):
    ds = {d["name"]: d for d in n10.datasets(n10.load_config(config(tmp_path)))}
    cmd = [str(x) for x in n10.coverage_command("py", ds["mockA_high"], "out", None)]
    assert cmd[cmd.index("--allow-unmergeable") + 1:cmd.index("--allow-unmergeable") + 4] == ["0", "0.01", "0.05"]
    assert cmd[cmd.index("--amplitrim-max-ee") + 1] == "2"
    assert cmd[cmd.index("--pairs") + 1] == "0" and "--reference" in cmd                         # mock A: all reads, with its expected sequences
    other = [str(x) for x in n10.coverage_command("py", ds["v1v2"], "out", None)]
    assert other[other.index("--pairs") + 1] == "5000" and "--reference" not in other
    pilot = [str(x) for x in n10.coverage_command("py", ds["mockA_high"], "out", n10.PILOT_PAIRS)]
    assert pilot[pilot.index("--pairs") + 1] == "1000"                                           # a pilot thins even mock A


def test_the_its_grid_and_cli_commands(tmp_path):
    its = [str(x) for x in n10.its_command("py", tmp_path / "its2", "out")]
    assert its[its.index("--marker") + 1] == "its"
    ds = n10.datasets(n10.load_config(config(tmp_path)), ["indep_mock", "indep_v3v4"])
    cmd = [str(x) for x in n10.grid_command("py", ds, "out")]
    assert cmd[cmd.index("--only") + 1] == "landscape"
    extras = [cmd[i + 1] for i, x in enumerate(cmd) if x == "--extra"]
    assert extras[0].startswith("indep_mock=") and "|" in extras[0] and extras[1].startswith("indep_v3v4=") and "|" not in extras[1]
    cli = [str(x) for x in n10.cli_command("py", "r", "w", "o", its=True, min_overlap=15)]
    assert cli[1:3] == ["-m", "amplitrim.cli"] and "--its" in cli and cli[cli.index("--min-overlap") + 1] == "15"
    assert "--its" not in [str(x) for x in n10.cli_command("py", "r", "w", "o")]
    timed = [str(x) for x in n10.timed_command("py", "lab", n10.cli_command("py", "r", "w", "o"))]
    assert timed[2:5] == ["--label", "lab", "--"] and timed[5] == "py"


def test_the_settings_are_read_from_summary_json_and_a_missing_recommendation_is_handled():
    s = n10.settings_of(summary(274, 253, 4, 8))
    assert (s["truncF"], s["truncR"], s["maxEE"], s["minOverlap"], s["longest_insert"], s["warnings"]) == (274, 253, "4,8", 12, 515, 0)
    assert n10.settings_of(summary(273, 247, 2, 2))["maxEE"] == "2"                               # both reads the same: one number, as in the register
    assert n10.settings_of({"recommended": None, "pairs_analysed": 10})["truncF"] is None
    assert n10.ee_text(2.0, 2.5) == "2,2.5"


def test_a_repeat_run_is_the_same_unless_a_setting_differs():
    a, b = summary(), summary()
    assert n10.compare_summaries(a, b) == []
    b["recommended"]["truncLenF"] = 274
    assert n10.compare_summaries(a, b) == ["recommended"]


def test_the_min_overlap_option_is_checked_against_the_total_length_rule():
    assert n10.check_min_overlap(summary(273, 250, k=15), 15) == []
    assert any("minOverlap is 12" in p for p in n10.check_min_overlap(summary(273, 250, k=12), 15))
    assert any("longest_mergeable_insert" in p for p in n10.check_min_overlap(summary(273, 250, k=20, insert=999), 20))
    assert n10.check_min_overlap({"recommended": None}, 15)[0].startswith("no recommendation")


def test_the_overlap_table_row_of_a_mock_comes_from_its_released_cut(tmp_path):
    ds = {d["name"]: d for d in n10.datasets(n10.load_config(config(tmp_path)))}["indep_mock"]
    row = n10.overlap_row(ds, summary(270, 242, 2, 3))
    assert (row["F"], row["amplicon"], row["maxee"], row["pairs"]) == (270, 500, "2,3", 5000) and row["reference"].endswith("im.fa")
    with pytest.raises(ValueError, match="no recommendation"):
        n10.overlap_row(ds, {"recommended": None})


def test_the_coverage_rows_get_their_share_and_the_estimate_is_compared_with_dada2():
    assert n10.level_label("AmpliTrim (maxEE 2)") == "0.2% (default)"
    assert [n10.level_label(f"AmpliTrim (maxEE 2, leave out {x})") for x in ("0.0%", "1.0%", "5.0%")] == ["0%", "1%", "5%"]
    assert n10.points(0.57, 0.64) == "+7.0" and n10.points(57.2, 64.2) == "+7.0" and n10.points(None, 0.5) == "-"
    assert n10.pct(0.572) == "57.2%" and n10.pct(57.2) == "57.2%" and n10.pct("") == "-"


def test_the_fingerprint_tells_identical_code_from_changed_code_and_ignores_line_endings(tmp_path):
    a, b, c = tmp_path / "a", tmp_path / "b", tmp_path / "c"
    for d, text in ((a, b"x = 1\n"), (b, b"x = 1\r\n"), (c, b"x = 2\n")):
        (d / "pkg").mkdir(parents=True)
        (d / "pkg" / "m.py").write_bytes(text)
    assert n10.package_fingerprint(a / "pkg") == n10.package_fingerprint(b / "pkg")                # a Windows checkout and a wheel
    assert n10.package_fingerprint(a / "pkg") != n10.package_fingerprint(c / "pkg")


# ---------------------------------------------------------------------------------------------------------------------- the driver
def run_main(args):
    old = list(sys.path)
    try:
        return n10.main(args)
    finally:
        sys.path[:] = old


def test_a_dry_run_prints_every_command_in_order_and_writes_nothing(tmp_path, capsys):
    out = tmp_path / "out"
    rc = run_main(["--dry-run", "--out", str(out), "--repo", str(tmp_path), "--config", str(config(tmp_path)), "--silva", str(tmp_path / "s.fa"), "--tail-dataset", "v1v2",
                   "--night3", str(tmp_path / "n3"), "--night4", str(tmp_path / "n4"), "--new", "indep_mock", "indep_v3v4", "--its-new", str(tmp_path / "its2"),
                   "--overlap-mock", "indep_mock", "--grid", "indep_mock"])
    text = capsys.readouterr().out
    assert rc == 0 and not out.exists()
    for needle in ("release_check.py", "time_amplitrim.py", "amplitrim.cli", "--min-overlap", "tail_classify.py", "--allow-unmergeable", "night4.py", "--only indep_mock indep_v3v4",
                   "--marker its", "make_overlap_commands.py", "overnight.py", "landscape"):
        assert needle in text, needle
    order = [text.index(f"--- {s}") for s in ("version", "accept", "cli", "tail", "coverage", "battery", "its", "overlap", "grid")]
    assert order == sorted(order)


def test_steps_that_lack_their_inputs_are_skipped_with_the_reason(tmp_path, capsys):
    out = tmp_path / "out"
    rc = run_main(["--out", str(out), "--repo", str(tmp_path), "--config", str(config(tmp_path)), "--only", "accept,tail,battery,its,overlap,grid"])
    text = capsys.readouterr().out
    assert rc == 0
    for reason in ("give the folders of Night 3", "give --tail-dataset", "give the new 16S datasets with --new", "give a second ITS dataset", "give the hold-out mock", "give the datasets that need a grid"):
        assert reason in text
    assert "skipped" in (out / "state" / "tail.json").read_text(encoding="utf-8")


def test_the_dataset_listing_finds_a_wrong_path_before_the_night(tmp_path, capsys):
    make_reads(tmp_path)
    (tmp_path / "ref.fa").write_text(">a\nACGT\n")
    (tmp_path / "im.fa").write_text(">a\nACGT\n")
    args = ["--datasets", "--repo", str(tmp_path), "--config", str(config(tmp_path)), "--its-new", str(tmp_path / "its")]
    assert run_main(args) == 0
    text = capsys.readouterr().out
    assert "All paths exist." in text and "its_new" in text and "indep_mock" in text
    shutil.rmtree(tmp_path / "iv")
    assert run_main(args) == 1
    out = capsys.readouterr().out
    line = [l for l in out.splitlines() if l.startswith("indep_v3v4")][0]
    assert "MISSING" in line and "1 path(s) missing" in out


def test_a_wrong_step_name_is_refused(capsys):
    assert n10.main(["--only", "nonsense"]) == 2
    assert "Unknown step" in capsys.readouterr().out


EMPTY_RC = 3


def fake_cli(monkeypatch, outcomes):
    """Replace the subprocess runner: every command-line run writes summary.json, REPORT.md and timing.jsonl as AmpliTrim and time_amplitrim.py would."""
    def run(self, cmd, cwd=None, shell=False):
        self.say("$ " + " ".join(str(c) for c in cmd))
        cmd = [str(c) for c in cmd]
        if "time_amplitrim.py" in " ".join(cmd):
            label = cmd[cmd.index("--label") + 1]
            with open(self.out / "cli" / "timing.jsonl", "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"label": label, "exit_code": 0, "wall_seconds": 41.2, "peak_memory_mb": 250}) + "\n")
            cmd = cmd[cmd.index("--") + 1:]
        if "amplitrim.cli" in " ".join(cmd) and "_empty_input" in " ".join(cmd):
            return (EMPTY_RC, "Error: no paired FASTQ files in the input folder" if EMPTY_RC == 3 else "Traceback (most recent call last):")
        if "amplitrim.cli" in " ".join(cmd):
            out = Path(cmd[cmd.index("--out-dir") + 1])
            name = out.parent.name
            k = int(cmd[cmd.index("--min-overlap") + 1]) if "--min-overlap" in cmd else 12
            result = outcomes(name, k)
            if result is not None:
                out.mkdir(parents=True, exist_ok=True)
                (out / "summary.json").write_text(json.dumps(result), encoding="utf-8")
                (out / "REPORT.md").write_text("report", encoding="utf-8")
        return 0, ""
    monkeypatch.setattr(n10.Ctx, "run", run)


def make_reads(tmp_path):
    for name in ("mockA", "v1v2", "its", "im", "iv"):
        (tmp_path / name).mkdir(exist_ok=True)


def test_the_command_line_step_records_time_checks_the_repeat_and_the_option_and_resumes(tmp_path, monkeypatch, capsys):
    make_reads(tmp_path)
    fake_cli(monkeypatch, lambda name, k: summary(273, 235 + k, k=k))
    out = tmp_path / "out"
    args = ["--out", str(out), "--repo", str(tmp_path), "--config", str(config(tmp_path)), "--only", "cli", "--limit", "2"]
    assert run_main(args) == 0
    rows = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (out / "state").glob("cli_*.json")}
    assert set(rows) == {"cli_mockA_high", "cli_v1v2", "cli__negative"} and rows["cli__negative"]["status"] == "done"
    r = rows["cli_mockA_high"]["row"]
    assert (r["seconds"], r["peak_mb"], r["truncF"], r["maxEE"], r["minOverlap"]) == (41.2, 250, 273, "2,3", 12)
    assert r["checks"]["repeat"] == "same" and r["checks"]["min_overlap_15"] == "ok" and r["checks"]["min_overlap_20"] == "ok" and r["checks"]["cut_20"] == "273/255"
    text = (out / "NIGHT10_SUMMARY.md").read_text(encoding="utf-8")
    assert "| mockA_high | 0 | 41.2 | 250 |" in text and "min_overlap_15: ok" in text
    capsys.readouterr()
    assert run_main(args) == 0                                                                  # a second start keeps what finished
    assert capsys.readouterr().out.count("finished in an earlier start") == 2


def test_a_command_line_run_that_breaks_the_rule_or_gives_another_answer_is_a_problem(tmp_path, monkeypatch):
    make_reads(tmp_path)
    calls = {"n": 0}

    def outcomes(name, k):
        calls["n"] += 1
        if k == 20:
            return summary(273, 255, k=12)                                                       # --min-overlap 20 ignored
        return summary(273 + (calls["n"] % 2), 247)                                                # a different cut on every other run
    fake_cli(monkeypatch, outcomes)
    out = tmp_path / "out"
    rc = run_main(["--out", str(out), "--repo", str(tmp_path), "--config", str(config(tmp_path)), "--only", "cli", "--limit", "1"])
    state = json.loads((out / "state" / "cli_mockA_high.json").read_text(encoding="utf-8"))
    assert rc == 1 and state["status"] == "failed"
    assert "DIFFERENT" in state["info"] or "PROBLEM" in state["info"]


def test_a_command_line_that_crashes_on_an_empty_folder_is_a_problem(tmp_path, monkeypatch):
    make_reads(tmp_path)
    fake_cli(monkeypatch, lambda name, k: summary(k=k, tr=235 + k))
    monkeypatch.setattr(sys.modules[__name__], "EMPTY_RC", 1)
    out = tmp_path / "out"
    rc = run_main(["--out", str(out), "--repo", str(tmp_path), "--config", str(config(tmp_path)), "--only", "cli", "--limit", "1", "--repeat", "0", "--min-overlap-datasets", "0"])
    state = json.loads((out / "state" / "cli__negative.json").read_text(encoding="utf-8"))
    assert rc == 1 and state["status"] == "failed" and "a traceback" in state["info"]


def test_a_dataset_without_a_report_fails_alone_and_the_others_still_run(tmp_path, monkeypatch):
    make_reads(tmp_path)
    fake_cli(monkeypatch, lambda name, k: None if name == "mockA_high" else summary(k=k, tr=235 + k))
    out = tmp_path / "out"
    rc = run_main(["--out", str(out), "--repo", str(tmp_path), "--config", str(config(tmp_path)), "--only", "cli", "--limit", "2", "--repeat", "0", "--min-overlap-datasets", "0"])
    assert rc == 1
    assert json.loads((out / "state" / "cli_mockA_high.json").read_text(encoding="utf-8"))["status"] == "failed"
    assert json.loads((out / "state" / "cli_v1v2.json").read_text(encoding="utf-8"))["status"] == "done"


def test_the_coverage_step_keeps_one_marker_per_dataset_and_the_summary_reads_the_tables(tmp_path, monkeypatch):
    make_reads(tmp_path)

    def run(self, cmd, cwd=None, shell=False):
        cmd = [str(c) for c in cmd]
        out = Path(cmd[cmd.index("--out") + 1])
        out.mkdir(parents=True, exist_ok=True)
        (out / "compare_methods.tsv").write_text("name\ttruncF\ttruncR\tmaxEE\town\tpass\tmerged\tstrains\tidentical\n"
                                                "AmpliTrim (maxEE 2)\t282\t280\t2\t0.60\t0.80\t0.572\t\t\n"
                                                "AmpliTrim (maxEE 2, leave out 1.0%)\t268\t118\t2\t0.92\t0.97\t0.898\t\t\n", encoding="utf-8")
        return 0, ""
    monkeypatch.setattr(n10.Ctx, "run", run)
    out = tmp_path / "out"
    assert run_main(["--out", str(out), "--repo", str(tmp_path), "--config", str(config(tmp_path)), "--only", "coverage", "--limit", "2"]) == 0
    assert {p.stem for p in (out / "state").glob("coverage_*.json")} == {"coverage_mockA_high", "coverage_v1v2"}
    text = (out / "NIGHT10_SUMMARY.md").read_text(encoding="utf-8")
    assert "| v1v2 | 0.2% (default) | 282/280 | 80.0% | 60.0% | 57.2% | +2.8 |" in text and "| v1v2 | 1% | 268/118 | 97.0% | 92.0% | 89.8% | +2.2 |" in text


def test_the_version_step_stops_the_run_when_the_two_imports_differ(tmp_path, monkeypatch):
    repo, other = tmp_path / "repo", tmp_path / "other"
    for d, v in ((repo, "0.2.0"), (other, "0.2.1")):
        (d / "amplitrim").mkdir(parents=True)
        (d / "amplitrim" / "__init__.py").write_text(f'__version__ = "{v}"\n', encoding="utf-8")

    def run(self, cmd, cwd=None, shell=False):
        cmd = [str(c) for c in cmd]
        if "import amplitrim, sys" in " ".join(cmd):
            return 0, f"0.2.1\n{other / 'amplitrim' / '__init__.py'}\n"
        return 0, "ok 1.0"
    monkeypatch.setattr(n10.Ctx, "run", run)
    saved = sys.modules.pop("amplitrim", None)
    out = tmp_path / "out"
    try:
        rc = run_main(["--check", "--out", str(out), "--repo", str(repo), "--config", str(config(tmp_path))])
    finally:
        sys.modules.pop("amplitrim", None)
        if saved is not None:
            sys.modules["amplitrim"] = saved
    state = json.loads((out / "state" / "version.json").read_text(encoding="utf-8"))
    assert rc == 1 and state["status"] == "stopped" and "not 0.2.0" in state["info"] and "not the same code" in state["info"]


# ------------------------------------------------------------------------------------------------------ the classifier (needs vsearch)
needs_vsearch = pytest.mark.skipif(shutil.which("vsearch") is None, reason="vsearch is not installed")


def rc(s):
    return s[::-1].translate(str.maketrans("ACGT", "TGCA"))


def write_pairs(folder, sample, amplicons, read_len=300):
    folder.mkdir(parents=True, exist_ok=True)
    with gzip.open(folder / f"{sample}_R1.fastq.gz", "wt") as o1, gzip.open(folder / f"{sample}_R2.fastq.gz", "wt") as o2:
        for i, amp in enumerate(amplicons):
            a, b = amp[:read_len], rc(amp[-read_len:])
            o1.write(f"@r{i}\n{a}\n+\n{'I' * len(a)}\n")
            o2.write(f"@r{i}\n{b}\n+\n{'I' * len(b)}\n")


def test_the_pairs_are_found_and_a_domain_is_read_from_a_silva_header(tmp_path):
    write_pairs(tmp_path, "s1", ["ACGT" * 100])
    write_pairs(tmp_path, "s2", ["ACGT" * 100])
    (tmp_path / "lonely_R1.fastq.gz").write_bytes(b"")                                        # no R2: not a pair
    assert [p[0] for p in tc.find_pairs(tmp_path)] == ["s1", "s2"]
    assert tc.domain_of("AB001445.1.1471 Eukaryota;Opisthokonta;Fungi") == "Eukaryota"
    assert tc.domain_of("AB001445.1.1471") == "unknown"


def test_the_long_group_and_the_control_are_chosen_by_length():
    seqs = [(f"a{i}", "A" * 400) for i in range(95)] + [(f"b{i}", "C" * 550) for i in range(5)]
    long_, control, thr = tc.choose(seqs, top_share=0.05)
    assert thr == 550 and len(long_) == 5 and all(len(s) == 550 for _, s in long_)
    assert len(control) == 5 and all(len(s) == 400 for _, s in control)
    long2, _, thr2 = tc.choose(seqs, min_len=500)
    assert thr2 == 500 and len(long2) == 5


def test_the_hits_are_summarised_with_the_missing_ones_counted(tmp_path):
    hits = tmp_path / "h.tsv"
    hits.write_text("q1\t98.0\tX1 Bacteria;A\nq2\t96.0\tX2 Bacteria;B\nq3\t90.0\tX3 Eukaryota;C\n", encoding="utf-8")
    doms, med = tc.summarise_hits(hits, 5)
    assert doms == {"Bacteria": 2, "Eukaryota": 1, "no hit": 2} and med == 96.0


@needs_vsearch
def test_end_to_end_the_long_amplicons_are_eukaryotic_the_control_is_bacterial_and_the_big_files_go(tmp_path):
    rng = random.Random(7)
    bact = ["".join(rng.choice("ACGT") for _ in range(1500)) for _ in range(2)]
    euk = "".join(rng.choice("ACGT") for _ in range(1800))
    silva = tmp_path / "silva.fasta"
    rna = lambda s: s.replace("T", "U")                                                          # SILVA is written in the RNA alphabet  # noqa: E731
    silva.write_text(f">B1.1.1500 Bacteria;Firmicutes;X\n{rna(bact[0])}\n>B2.1.1500 Bacteria;Proteobacteria;Y\n{rna(bact[1])}\n>E1.1.1800 Eukaryota;Fungi;Z\n{rna(euk)}\n", encoding="utf-8")
    amplicons = [bact[i % 2][100:500] for i in range(190)] + [euk[100:660] for _ in range(10)]   # 400 nt and 560 nt; 300 nt reads overlap by 40 nt on the long ones
    reads = tmp_path / "ready"
    write_pairs(reads, "s1", amplicons)
    out = tmp_path / "out"
    assert tc.main([str(reads), "--silva", str(silva), "--out", str(out), "--top-share", "0.05", "--threads", "1"]) == 0
    rows = {(r.split("\t")[0], r.split("\t")[1]): r.split("\t") for r in (out / "tail_summary.tsv").read_text(encoding="utf-8").splitlines()[1:]}
    assert float(rows[("long", "Eukaryota")][3]) == 1.0                                          # all of the long group
    assert float(rows[("control", "Bacteria")][3]) == 1.0                                        # all of the control
    assert "Eukaryota" in (out / "tail_summary.md").read_text(encoding="utf-8")
    assert not (out / "merged.fq").exists() and not (out / "thin_R1.fq").exists() and (out / "long.fa").exists()
