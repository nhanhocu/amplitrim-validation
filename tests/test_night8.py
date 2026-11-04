"""validation/night8.py: the steps, the environment check, a whole run with stand-ins for cutadapt, DADA2 and the edit distance, resume and redo, steps that skip, and the summary."""
import ast
import json
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "validation"))
import longread_common as lc  # noqa: E402
import longread_filter_check as lf  # noqa: E402
import longread_truth as lt  # noqa: E402
import night8 as n8  # noqa: E402
import test_longread_calibration as t_cal  # noqa: E402
import test_longread_filter_check as t4  # noqa: E402
import test_longread_truth as t_truth  # noqa: E402

FWD, REV = t4.FWD, t4.REV
MONOMER_NAMES = [f"m64004e_231016_235852.Kinnex16S_{p}.hifi_reads.fastq.gz" for p in n8.MONOMER_PAIRS]
KINNEX_NAMES = [f"m64004e_231003_184443.Kinnex16S_{p}.hifi_reads.fastq.gz" for p in n8.MONOMER_PAIRS]


def build(tmp_path, with_expected: bool = True):
    """The data folder of the long-read work (three Monomer and three Kinnex files) and the genome_amplicons folder of Night 7, for a toy mock of three strains."""
    rng = random.Random(4)
    var = [(f"{s}_v{k}|{s}|{c}_copies", "".join(rng.choice("ACGT") for _ in range(150))) for s, k, c in (("X", 1, 2), ("X", 2, 1), ("Y", 1, 1), ("Z", 1, 1))]
    data, exp = tmp_path / "data", tmp_path / "expected"
    for folder, names in ((data / "sq2_monomer_fastq", MONOMER_NAMES), (data / "sq2_kinnex_fastq", KINNEX_NAMES)):
        folder.mkdir(parents=True)
        for n in names:
            reads = [t_truth.plain_read(var[i % 3][1], rng, reverse=(i % 4 == 0)) for i in range(60)]
            t4.write_fastq(folder / n, reads)
    if with_expected:
        exp.mkdir()
        (exp / "expected_amplicons.fasta").write_text("".join(f">{n}\n{s}\n" for n, s in var))
        (exp / "genome_amplicons.tsv").write_text("strain\ttier\tshare_genomic_percent\texpected_read_share_percent\nX\tA\t18\t70\nY\tA\t18\t25\nZ\tA\t0.18\t5\n")
    return data, exp


@pytest.fixture
def stand_ins(monkeypatch):
    monkeypatch.setattr(lf, "run_cutadapt", t_cal.named_stand_in_cutadapt)
    monkeypatch.setattr(lt, "run_dada2", t_truth.fake_dada2)
    monkeypatch.setattr(lc, "nearest", t_cal.hamming_nearest)
    monkeypatch.setattr(lc, "check_cutadapt", lambda: None)
    monkeypatch.setattr(n8, "find_rscript", lambda: "Rscript")
    monkeypatch.setattr(n8, "versions", lambda: {"Python": "3.12", "cutadapt": "5.2", "R and DADA2": "R 4.6.1 | DADA2 1.40.0"})
    t_truth.fake_dada2.calls.clear()


def args(tmp_path, data, exp, *extra):
    return ["--out", str(tmp_path / "out"), "--data", str(data), "--expected-dir", str(exp), "--reads", "0", "--reads-tcal", "0", "--reads-pilot", "0", "--threads", "1", *extra]


def state(tmp_path):
    return json.loads((tmp_path / "out" / "night8_state.json").read_text())["steps"]


def test_the_steps_and_what_the_rule_is_predicted_to_give():
    assert n8.STEPS == ["pilot", "tcal", "truth_monomer", "truth_kinnex", "summary"] and n8.PREDICTION == {"Monomer": 2, "Kinnex": 3}
    assert str(n8.DEFAULT_EXPECTED).endswith("17_night7_longread\\genome_amplicons") and n8.PRIMERS == ("AGRGTTYGATYMTGGCTCAG", "RGYTACCTTGTTACGACTT") and len(n8.MONOMER_PAIRS) == 3


def test_the_environment_check_names_what_is_missing(tmp_path, monkeypatch):
    data, exp = build(tmp_path)
    from types import SimpleNamespace
    monkeypatch.setattr(n8.shutil, "disk_usage", lambda path: SimpleNamespace(free=50e9))          # the test must not depend on the free space of the disk it runs on
    monkeypatch.setattr(n8, "find_rscript", lambda: "Rscript")
    monkeypatch.setattr(n8.importlib.util, "find_spec", lambda name: object())
    monkeypatch.setattr(n8, "tool_version", lambda cmd, timeout=60: (True, "yes" if "PacBioErrfun" in " ".join(cmd) else "1.40.0"))
    a = n8.argparse.Namespace(out=tmp_path / "out", data=data, expected_dir=exp, grid=[1, 2], reads=0)
    c = n8.Ctx(a)
    results = {w: ok for w, ok, _ in n8.check_environment(c)}
    assert all(results.values()) and "PacBioErrfun in DADA2" in results and "rapidfuzz" in results
    monkeypatch.setattr(n8.importlib.util, "find_spec", lambda name: None if name == "rapidfuzz" else object())
    monkeypatch.setattr(n8, "tool_version", lambda cmd, timeout=60: (True, "no") if "PacBioErrfun" in " ".join(cmd) else (True, "1.40.0"))
    c2 = n8.Ctx(n8.argparse.Namespace(out=tmp_path / "out", data=data, expected_dir=tmp_path / "nowhere", grid=[1, 2], reads=0))
    bad = {w for w, ok, _ in n8.check_environment(c2) if not ok}
    assert bad == {"rapidfuzz", "PacBioErrfun in DADA2", "expected amplicons (Night 7)", "table of the strains (Night 7)"}


def test_the_environment_check_flags_a_disk_with_too_little_free_space(tmp_path, monkeypatch):
    from types import SimpleNamespace
    data, exp = build(tmp_path)
    monkeypatch.setattr(n8.shutil, "disk_usage", lambda path: SimpleNamespace(free=1.5e9))
    monkeypatch.setattr(n8, "find_rscript", lambda: "Rscript")
    monkeypatch.setattr(n8.importlib.util, "find_spec", lambda name: object())
    monkeypatch.setattr(n8, "tool_version", lambda cmd, timeout=60: (True, "yes" if "PacBioErrfun" in " ".join(cmd) else "1.40.0"))
    c = n8.Ctx(n8.argparse.Namespace(out=tmp_path / "out", data=data, expected_dir=exp, grid=[1, 2], reads=0))
    assert {w: d for w, ok, d in n8.check_environment(c) if not ok} == {"2 GB free": "1.5 GB free"}


def test_the_check_command_returns_a_code(tmp_path, monkeypatch, capsys):
    data, exp = build(tmp_path)
    monkeypatch.setattr(n8, "check_environment", lambda c: [("a", True, "fine"), ("b", False, "fix it")])
    assert n8.main(args(tmp_path, data, exp, "--check")) == 1
    assert "[NOT READY] b: fix it" in capsys.readouterr().out
    monkeypatch.setattr(n8, "check_environment", lambda c: [("a", True, "fine")])
    assert n8.main(args(tmp_path, data, exp, "--check")) == 0


def test_a_whole_run_does_every_step_and_writes_the_summary(tmp_path, stand_ins):
    data, exp = build(tmp_path)
    assert n8.main(args(tmp_path, data, exp)) == 0
    s = state(tmp_path)
    assert {k: v["status"] for k, v in s.items()} == {"pilot": "done", "tcal": "done", "truth_monomer": "done", "truth_kinnex": "done", "summary": "done"}
    out = tmp_path / "out"
    assert (out / "tcal" / "TCAL.md").is_file() and (out / "truth_monomer" / "TRUTH.md").is_file() and (out / "truth_kinnex" / "TRUTH.md").is_file() and (out / "pilot" / "TRUTH.md").is_file()
    text = (out / "NIGHT8_SUMMARY.md").read_text()
    for part in ("# Night 8", "## T-cal: are the expected errors calibrated?", "**Gate (T-cal-1)", "## Monomer", "## Kinnex", "## Truth test: Monomer", "## Truth test: Kinnex", "**Gate (T2)", "## The prediction of the rule",
                 "## Send back", "R and DADA2 R 4.6.1 | DADA2 1.40.0"):
        assert part in text, part
    assert "one DADA2 run on" in s["pilot"]["detail"] and "took" in s["pilot"]["detail"] and " h" in s["pilot"]["detail"]
    tags = [c["tag"] for c in t_truth.fake_dada2.calls]
    assert tags.count("ee2") == 3 and tags.count("ee2_dada2primers") == 2                              # the pilot, Monomer and Kinnex run ee2; Monomer and Kinnex also the two extras
    assert not list(out.glob("*_input")) and not (out / "tcal" / "work").exists()


def test_the_pilot_uses_only_the_smallest_monomer_file(tmp_path, stand_ins):
    data, exp = build(tmp_path)
    n8.main(args(tmp_path, data, exp, "--only", "pilot"))
    calls = t_truth.fake_dada2.calls
    assert len(calls) == 1 and calls[0]["tag"] == "ee2"
    assert (tmp_path / "out" / "pilot" / "truth_conditions.tsv").read_text().count("\n") == 2          # the header and one condition


def test_the_summary_compares_the_rule_with_the_prediction(tmp_path, stand_ins):
    data, exp = build(tmp_path)
    n8.main(args(tmp_path, data, exp))
    text = (tmp_path / "out" / "NIGHT8_SUMMARY.md").read_text()
    assert "Monomer 2 (as predicted)" in text and "Kinnex 2 (NOT as predicted)" in text               # perfect toy reads: the rule gives 2 for both; 3 was predicted for Kinnex
    assert n8.rule_of(tmp_path / "out" / "truth_kinnex" / "TRUTH.md") == 2 and n8.rule_of(tmp_path / "nothing.md") is None


def test_finished_steps_are_skipped_and_redo_repeats_one_step_and_the_summary(tmp_path, stand_ins):
    data, exp = build(tmp_path)
    n8.main(args(tmp_path, data, exp))
    first = {k: v["finished"] for k, v in state(tmp_path).items()}
    t_truth.fake_dada2.calls.clear()
    assert n8.main(args(tmp_path, data, exp)) == 0 and t_truth.fake_dada2.calls == []                  # nothing is run again
    n8.main(args(tmp_path, data, exp, "--redo", "tcal"))
    again = {k: v["finished"] for k, v in state(tmp_path).items()}
    assert t_truth.fake_dada2.calls == [] and again["pilot"] == first["pilot"] and again["truth_kinnex"] == first["truth_kinnex"]       # the truth steps were not repeated
    assert again["tcal"] >= first["tcal"] and again["summary"] >= first["summary"]
    n8.main(args(tmp_path, data, exp, "--redo", "truth_kinnex"))
    assert {c["tag"] for c in t_truth.fake_dada2.calls} >= {"ee2", "ee1"} and len(t_truth.fake_dada2.calls) == 7        # one library type: its 7 conditions


def test_steps_whose_inputs_are_missing_are_skipped_not_failed(tmp_path, stand_ins):
    data, exp = build(tmp_path, with_expected=False)
    assert n8.main(args(tmp_path, data, tmp_path / "no_expected")) == 0
    s = state(tmp_path)
    assert {k: v["status"] for k, v in s.items()} == {"pilot": "skipped", "tcal": "skipped", "truth_monomer": "skipped", "truth_kinnex": "skipped", "summary": "done"}
    assert "expected amplicons are missing" in s["tcal"]["detail"]
    assert "No result" in (tmp_path / "out" / "NIGHT8_SUMMARY.md").read_text()
    data2, exp2 = build(tmp_path / "second")
    for p in (data2 / "sq2_monomer_fastq").iterdir():
        if "Fwd_09" in p.name:
            p.unlink()
    n8.main(args(tmp_path / "second", data2, exp2, "--only", "tcal"))
    assert "only 2 of the 3 Monomer files" in json.loads((tmp_path / "second" / "out" / "night8_state.json").read_text())["steps"]["tcal"]["detail"]


def test_a_crashing_step_is_recorded_and_the_others_go_on(tmp_path, stand_ins, monkeypatch):
    data, exp = build(tmp_path)
    monkeypatch.setattr(lt, "run_dada2", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("The DADA2 run failed: boom")))
    assert n8.main(args(tmp_path, data, exp)) == 1
    s = state(tmp_path)
    assert s["tcal"]["status"] == "done" and s["pilot"]["status"] == "failed" and "boom" in s["truth_monomer"]["detail"] and s["summary"]["status"] == "done"


def test_list_and_unknown_steps(tmp_path, stand_ins, capsys):
    data, exp = build(tmp_path)
    n8.main(args(tmp_path, data, exp, "--only", "tcal"))
    n8.main(args(tmp_path, data, exp, "--list"))
    out = capsys.readouterr().out
    assert "tcal" in out and "done" in out and "pilot" in out and "not run" in out
    assert n8.main(args(tmp_path, data, exp, "--only", "nonsense")) == 2


def test_the_sampling_option_sets_the_shared_setting(tmp_path, monkeypatch):
    monkeypatch.setattr(lf, "SAMPLING", "spread")
    data, exp = build(tmp_path)
    n8.main(args(tmp_path, data, exp) + ["--list"])
    assert lf.SAMPLING == "spread"                                                                  # the default
    n8.main(args(tmp_path, data, exp) + ["--list", "--sampling", "first"])
    assert lf.SAMPLING == "first"


def test_the_script_parses_as_python_3_9():
    ast.parse(Path(n8.__file__).read_text(), feature_version=(3, 9))
