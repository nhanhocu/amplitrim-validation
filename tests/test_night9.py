"""validation/night9.py: the steps, the environment check, the quality step, a whole run with stand-ins for cutadapt, DADA2 and the edit distance, resume and redo, skipped and failed steps,
the reference of T-cal, and the evaluation of the three predictions."""
import ast
import json
import random
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "validation"))
import longread_common as lc  # noqa: E402
import longread_filter_check as lf  # noqa: E402
import longread_truth as lt  # noqa: E402
import night9 as n9  # noqa: E402
import test_longread_calibration as t_cal  # noqa: E402
import test_longread_filter_check as t4  # noqa: E402
import test_longread_truth as t_truth  # noqa: E402

REVIO_NAMES = [f"m84198_231017_000448_s1.Kinnex16S_{p}.hifi_reads.fastq.gz" for p in n9.MONOMER_PAIRS]
SQ2_NAMES = [f"m64004e_231016_235852.Kinnex16S_{p}.hifi_reads.fastq.gz" for p in n9.MONOMER_PAIRS]


def build(tmp_path, with_refs: bool = True):
    """Three Revio and three Sequel II files of a toy mock, Night 7's expected amplicons, a refined reference with one added variant, and a replication set.
    The Revio reads carry the single quality score 40 (binned); the Sequel II reads carry one base of Q93 inside the amplicon."""
    rng = random.Random(9)
    var = [(f"{s}_v{k}|{s}|{c}_copies", "".join(rng.choice("ACGT") for _ in range(150))) for s, k, c in (("X", 1, 2), ("X", 2, 1), ("Y", 1, 1), ("Z", 1, 1))]
    added = t_truth.substitute(var[2][1], 1, 40)
    data, exp = tmp_path / "data", tmp_path / "expected"
    for folder, names, with93 in ((data / "revio_monomer_fastq", REVIO_NAMES, False), (data / "sq2_monomer_fastq", SQ2_NAMES, True)):
        folder.mkdir(parents=True)
        for n in names:
            reads = []
            for k in range(3):                                       # 20 reads each of X_v1, X_v2 and Y_v1, then 10 of Z and 20 of the added variant, in that order
                reads += [t_truth.plain_read(var[k][1], rng, reverse=(i % 4 == 0)) for i in range(20)]
            reads += [t_truth.plain_read(var[3][1], rng) for _ in range(10)] + [t_truth.plain_read(added, rng) for _ in range(20)]
            if with93:                                               # the Sequel II files are shuffled; the Revio files stay sorted, like an ordered file
                random.Random(11).shuffle(reads)
                full, q = reads[1]
                reads[1] = (full, q[:60] + "~" + q[61:])             # the middle of the read lies inside the amplicon, in either orientation
            t4.write_fastq(folder / n, reads)
    exp.mkdir()
    refined, reps = tmp_path / "refined.fasta", tmp_path / "replicate.txt"
    if with_refs:
        (exp / "expected_amplicons.fasta").write_text("".join(f">{n}\n{s}\n" for n, s in var))
        (exp / "genome_amplicons.tsv").write_text("strain\ttier\tshare_genomic_percent\texpected_read_share_percent\nX\tA\t18\t70\nY\tA\t18\t25\nZ\tA\t0.18\t5\n")
        refined.write_text("".join(f">{n}\n{s}\n" for n, s in var) + f">Y_a1|Y|0_copies\n{added}\n")
        reps.write_text("\n".join([var[0][0], var[1][0], var[2][0], "Y_a1|Y|0_copies"]) + "\n")
    return data, exp, refined, reps


@pytest.fixture
def stand_ins(monkeypatch):
    monkeypatch.setattr(lf, "run_cutadapt", t_cal.named_stand_in_cutadapt)
    monkeypatch.setattr(lt, "run_dada2", t_truth.fake_dada2)
    monkeypatch.setattr(lc, "nearest", t_cal.hamming_nearest)
    monkeypatch.setattr(lc, "check_cutadapt", lambda: None)
    monkeypatch.setattr(n9, "find_rscript", lambda: "Rscript")
    monkeypatch.setattr(n9, "versions", lambda: {"Python": "3.12", "cutadapt": "5.2", "R and DADA2": "R 4.6.1 | DADA2 1.40.0"})
    t_truth.fake_dada2.calls.clear()


def args(tmp_path, data, exp, refined, reps, *extra):
    return ["--out", str(tmp_path / "out"), "--data", str(data), "--expected-dir", str(exp), "--refined", str(refined), "--replicate-set", str(reps), "--reads", "0", "--reads-tcal", "0", "--threads", "1", *extra]


def state(tmp_path):
    return json.loads((tmp_path / "out" / "night9_state.json").read_text())["steps"]


def test_the_steps_and_the_reference_files_of_the_archive():
    assert n9.STEPS == ["quality", "order", "tcal", "truth", "summary"] and n9.NEEDED_GB == 2
    assert n9.REFINED.name == "msa1003_refined_variants.fasta" and n9.REFINED.is_file() and n9.REPLICATE.name == "msa1003_night8_asv_set.txt" and n9.REPLICATE.is_file()
    refined = lc.read_fasta(n9.REFINED)
    names = [n for n, _ in refined]
    assert len(refined) == 69 and sum(n.split("|")[2].startswith("0_") for n in names) == 10 and len({s for _, s in refined}) == 69
    reps = lt.read_names(n9.REPLICATE)
    assert len(reps) == 49 and set(reps) <= set(names)                                              # the 38 recovered, the 10 added and the H. pylori sequence
    assert sum(1 for r in reps if r.split("|")[2].startswith("0_")) == 10


def test_the_environment_check_names_what_is_missing(tmp_path, monkeypatch):
    data, exp, refined, reps = build(tmp_path)
    monkeypatch.setattr(n9.shutil, "disk_usage", lambda path: SimpleNamespace(free=50e9))
    monkeypatch.setattr(n9, "find_rscript", lambda: "Rscript")
    monkeypatch.setattr(n9.importlib.util, "find_spec", lambda name: object())
    monkeypatch.setattr(n9, "tool_version", lambda cmd, timeout=60: (True, "yes" if "exists(" in " ".join(cmd) else "1.40.0"))
    ctx = n9.Ctx(SimpleNamespace(out=tmp_path / "out", data=data, expected_dir=exp, refined=refined, replicate_set=reps))
    results = {w: ok for w, ok, _ in n9.check_environment(ctx)}
    assert all(results.values()) and "makeBinnedQualErrfun in DADA2" in results and "Revio files" in results and "replication set" in results
    monkeypatch.setattr(n9.importlib.util, "find_spec", lambda name: None if name == "rapidfuzz" else object())
    monkeypatch.setattr(n9, "tool_version", lambda cmd, timeout=60: (True, "no") if "makeBinnedQualErrfun" in " ".join(cmd) else (True, "yes" if "exists(" in " ".join(cmd) else "1.40.0"))
    monkeypatch.setattr(n9.shutil, "disk_usage", lambda path: SimpleNamespace(free=1.5e9))
    ctx2 = n9.Ctx(SimpleNamespace(out=tmp_path / "out", data=tmp_path / "nowhere", expected_dir=tmp_path / "nowhere", refined=tmp_path / "none.fasta", replicate_set=reps))
    bad = {w for w, ok, _ in n9.check_environment(ctx2) if not ok}
    assert bad == {"rapidfuzz", "makeBinnedQualErrfun in DADA2", "2 GB free", "expected amplicons (Night 7)", "table of the strains (Night 7)", "refined reference", "Revio files", "Sequel II files"}


def test_the_quality_step_tells_binned_from_continuous_scores(tmp_path, stand_ins):
    data, exp, refined, reps = build(tmp_path)
    assert n9.main(args(tmp_path, data, exp, refined, reps, "--only", "quality")) == 0
    detail = state(tmp_path)["quality"]["detail"]
    assert "Revio: highest Q 40, 1 distinct values, binned" in detail and "SequelII: highest Q 93, 2 distinct values, not binned" in detail
    rows = [l.split("\t") for l in (tmp_path / "out" / "quality.tsv").read_text().splitlines()]
    assert rows[0] == ["library", "file", "highest_quality", "distinct_values", "values"] and len(rows) == 7
    assert n9.describe_quality([("A", "f", 40, 7, "3 10 17 22 27 35 40"), ("B", "g", 93, 94, " ".join(map(str, range(94))))]) == {"A": (40, 7, True), "B": (93, 94, False)}
    assert n9.describe_quality([("C", "f", 40, 30, " ".join(map(str, range(1, 31))))])["C"][2] is False         # many values and no Q93: not binned


def test_the_calibration_step_uses_the_refined_reference_and_both_libraries(tmp_path, stand_ins, monkeypatch):
    data, exp, refined, reps = build(tmp_path)
    seen = []
    monkeypatch.setattr(n9.lcal, "run", lambda libs, fasta, *a, **k: seen.append((sorted(libs), Path(fasta), k.get("strains_table"))) or {"gates": {"T-cal-1": ("NOT DECIDED", [])}})
    n9.main(args(tmp_path, data, exp, refined, reps, "--only", "tcal"))
    assert seen == [(["Revio", "SequelII"], refined, exp / "genome_amplicons.tsv")]
    assert not list((tmp_path / "out").glob("*_input"))                                                  # the linked inputs are removed again


def test_a_whole_run_does_every_step_and_evaluates_the_predictions(tmp_path, stand_ins):
    data, exp, refined, reps = build(tmp_path)
    assert n9.main(args(tmp_path, data, exp, refined, reps)) == 0
    s = state(tmp_path)
    assert {k: v["status"] for k, v in s.items()} == {"quality": "done", "order": "done", "tcal": "done", "truth": "done", "summary": "done"}
    out = tmp_path / "out"
    assert (out / "tcal" / "TCAL.md").is_file() and (out / "truth" / "TRUTH.md").is_file() and (out / "quality.tsv").is_file()
    text = (out / "NIGHT9_SUMMARY.md").read_text()
    for part in ("# Night 9", "## Quality scores", "## Order of the reads", "T-cal-1 below is the gate T-cal-R1", "**Gate (T-cal-1)", "## Revio", "## SequelII", "## Truth test: Revio", "**Gate (T2)", "error model: **binned:40**",
                 "## The predictions", "1. The Revio reads are binned", "as predicted", "2. The binned model recovers at least as many", "3. At least 90% of the replication set is found again: 4 of 4 (100.0%)", "## Send back"):
        assert part in text, part
    assert "error model binned:40; the rule gives maxEE 2" in s["truth"]["detail"]
    assert "4. The order check flags the Revio files and not the Sequel II files: Revio 3 of 3 NOT RANDOM, Sequel II 0 of 3: as predicted." in text
    line5 = [l for l in text.splitlines() if l.startswith("5. T-cal and the truth test see the same composition in each Revio file")]
    assert len(line5) == 1 and line5[0].count("Fwd_") == 3, line5                                  # one Spearman per Revio file
    assert "Fwd_04--Kinnex16S_Rev_22 1.00" in line5[0] and line5[0].endswith("as predicted.")
    calls = {c["tag"]: c for c in t_truth.fake_dada2.calls}
    assert set(calls) == {"ee2", "ee2_dada2primers", "ee2_naive"} and calls["ee2"]["errfun"] == "binned:40" and calls["ee2_naive"]["errfun"] == "PacBioErrfun"
    assert not list(out.glob("*_input"))


def test_the_predictions_say_when_they_are_not_met(tmp_path):
    data, exp, refined, reps = build(tmp_path)
    c = n9.Ctx(SimpleNamespace(out=tmp_path / "out", data=data, expected_dir=exp, refined=refined, replicate_set=reps))
    c.out.mkdir()
    (c.out / "quality.tsv").write_text("library\tfile\thighest_quality\tdistinct_values\tvalues\nRevio\tf\t93\t94\t" + " ".join(map(str, range(94))) + "\n")
    c.truth_out.mkdir()
    head = "library\tcondition\treplicated\treplicate_total\n"
    (c.truth_out / "truth_conditions.tsv").write_text(head + "Revio\tee2\t40\t49\nRevio\tee2_naive\t44\t49\n")
    p = n9.predictions(c)
    assert "NOT as predicted" in p[0] and "40 against 44: NOT as predicted" in p[1] and "40 of 49 (81.6%): NOT as predicted" in p[2]
    (c.truth_out / "truth_conditions.tsv").write_text(head + "Revio\tee2\t45\t49\n")
    p = n9.predictions(c)
    assert "45 of 49 (91.8%): as predicted" in p[2] and "not known" in p[1]                                 # no naive condition: not known
    (c.truth_out / "truth_conditions.tsv").write_text(head + "Revio\tee2\t44\t49\n")
    assert "44 of 49 (89.8%): NOT as predicted" in n9.predictions(c)[2]                                    # 90% of 49 is 44.1


def test_finished_steps_are_skipped_and_redo_repeats_a_step_and_the_summary(tmp_path, stand_ins):
    data, exp, refined, reps = build(tmp_path)
    n9.main(args(tmp_path, data, exp, refined, reps))
    first = {k: v["finished"] for k, v in state(tmp_path).items()}
    t_truth.fake_dada2.calls.clear()
    assert n9.main(args(tmp_path, data, exp, refined, reps)) == 0 and t_truth.fake_dada2.calls == []
    n9.main(args(tmp_path, data, exp, refined, reps, "--redo", "quality"))
    again = {k: v["finished"] for k, v in state(tmp_path).items()}
    assert t_truth.fake_dada2.calls == [] and again["truth"] == first["truth"] and again["quality"] >= first["quality"]
    n9.main(args(tmp_path, data, exp, refined, reps, "--redo", "truth"))
    assert {c["tag"] for c in t_truth.fake_dada2.calls} == {"ee2", "ee2_dada2primers", "ee2_naive"}


def test_steps_whose_inputs_are_missing_are_skipped_not_failed(tmp_path, stand_ins):
    data, exp, refined, reps = build(tmp_path, with_refs=False)
    assert n9.main(args(tmp_path, data, exp, refined, reps)) == 0
    s = state(tmp_path)
    assert s["quality"]["status"] == "done" and {s[k]["status"] for k in ("order", "tcal", "truth")} == {"skipped"} and s["summary"]["status"] == "done"
    assert "is missing" in s["tcal"]["detail"] and "No result" in (tmp_path / "out" / "NIGHT9_SUMMARY.md").read_text()
    data2, exp2, ref2, reps2 = build(tmp_path / "second")
    for p in (data2 / "revio_monomer_fastq").iterdir():
        if "Fwd_09" in p.name:
            p.unlink()
    n9.main(args(tmp_path / "second", data2, exp2, ref2, reps2, "--only", "quality"))
    assert "only 2 of the 3 Revio files" in json.loads((tmp_path / "second" / "out" / "night9_state.json").read_text())["steps"]["quality"]["detail"]


def test_a_crashing_step_is_recorded_and_the_others_go_on(tmp_path, stand_ins, monkeypatch):
    data, exp, refined, reps = build(tmp_path)
    monkeypatch.setattr(lt, "run_dada2", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("The DADA2 run failed: boom")))
    assert n9.main(args(tmp_path, data, exp, refined, reps)) == 1
    s = state(tmp_path)
    assert s["quality"]["status"] == "done" and s["tcal"]["status"] == "done" and s["truth"]["status"] == "failed" and "boom" in s["truth"]["detail"] and s["summary"]["status"] == "done"


def test_list_unknown_steps_and_the_check_code(tmp_path, stand_ins, monkeypatch, capsys):
    data, exp, refined, reps = build(tmp_path)
    n9.main(args(tmp_path, data, exp, refined, reps, "--only", "quality"))
    n9.main(args(tmp_path, data, exp, refined, reps, "--list"))
    out = capsys.readouterr().out
    assert "quality" in out and "done" in out and "truth" in out and "not run" in out
    assert n9.main(args(tmp_path, data, exp, refined, reps, "--only", "nonsense")) == 2
    monkeypatch.setattr(n9, "check_environment", lambda c: [("a", True, "fine"), ("b", False, "fix it")])
    assert n9.main(args(tmp_path, data, exp, refined, reps, "--check")) == 1 and "[NOT READY] b: fix it" in capsys.readouterr().out


def test_the_sampling_option_sets_the_shared_setting(tmp_path, monkeypatch):
    monkeypatch.setattr(lf, "SAMPLING", "spread")
    data, exp, refined, reps = build(tmp_path)
    n9.main(args(tmp_path, data, exp, refined, reps) + ["--list"])
    assert lf.SAMPLING == "spread"                                                                  # the default
    n9.main(args(tmp_path, data, exp, refined, reps) + ["--list", "--sampling", "first"])
    assert lf.SAMPLING == "first"


def test_the_order_step_flags_the_sorted_revio_files_and_not_the_shuffled_sequel_ii_files(tmp_path, stand_ins):
    data, exp, refined, reps = build(tmp_path)
    assert n9.main(args(tmp_path, data, exp, refined, reps, "--only", "order")) == 0
    assert state(tmp_path)["order"]["detail"] == "Revio: 3 of 3 files NOT RANDOM; SequelII: 0 of 3 files NOT RANDOM"
    rows = [l.split("\t") for l in (tmp_path / "out" / "order" / "order_by_library.tsv").read_text().splitlines()]
    assert rows[0] == ["library", "file", "v", "v_random_order", "verdict"] and len(rows) == 7
    assert {r[0]: {x[4] for x in rows[1:] if x[0] == r[0]} for r in rows[1:]} == {"Revio": {"NOT RANDOM"}, "SequelII": {"random"}}
    assert (tmp_path / "out" / "order" / "ORDER_CHECK.md").is_file() and (tmp_path / "out" / "order" / "order_summary.tsv").is_file()


def test_the_composition_of_tcal_and_of_the_truth_test_are_compared_per_file(tmp_path):
    data, exp, refined, reps = build(tmp_path)
    c = n9.Ctx(SimpleNamespace(out=tmp_path / "out", data=data, expected_dir=exp, refined=refined, replicate_set=reps))
    c.tcal_out.mkdir(parents=True)
    c.truth_out.mkdir(parents=True)
    f1, f2 = "m84198.Kinnex16S_Fwd_04--Kinnex16S_Rev_22.hifi_reads", "m84198.Kinnex16S_Fwd_07--Kinnex16S_Rev_30.hifi_reads"
    head = "library\tfile\tstrain\treads\tshare\n"
    rows = [("Revio", f1, "A", 600), ("Revio", f1, "B", 300), ("Revio", f1, "C", 100), ("Revio", f2, "A", 5), ("Revio", f2, "B", 300), ("Revio", f2, "C", 700), ("SequelII", f1, "A", 1)]
    (c.tcal_out / "composition.tsv").write_text(head + "".join(f"{l}\t{f}\t{s}\t{n}\t0\n" for l, f, s, n in rows))
    asv = "sequence\treads\tchimera\tmatch\tnearest_variant\tdistance\treads_per_sample\n"
    (c.truth_out / "truth_asvs_Revio_ee2.tsv").write_text(asv + "".join(
        f"S{i}\t{x}\tFalse\texact\t{s}_v1|{s}|1_copies\t0\t{f1}={a};{f2}={b}\n" for i, (s, a, b, x) in enumerate((("A", 6000, 900, 6900), ("B", 3000, 100, 3100), ("C", 1000, 50, 1050)))))
    (c.truth_out / "truth_asvs_Revio_ee2.tsv").write_text((c.truth_out / "truth_asvs_Revio_ee2.tsv").read_text() + "S9\t5\tTrue\tother\tA_v1|A|1_copies\t9\t" + f1 + "=5\n")        # a chimera is left out
    agree = n9.composition_agreement(c)
    assert set(agree) == {f1, f2}
    assert agree[f1] == pytest.approx(1.0)                                                          # the same order of strains: A > B > C in both
    assert agree[f2] == pytest.approx(-1.0)                                                         # reversed: T-cal sees C > B > A, the truth test A > B > C
    assert n9.composition_agreement(n9.Ctx(SimpleNamespace(out=tmp_path / "none", data=data, expected_dir=exp, refined=refined, replicate_set=reps))) == {}


def test_the_predictions_about_the_order_and_the_composition(tmp_path):
    data, exp, refined, reps = build(tmp_path)
    c = n9.Ctx(SimpleNamespace(out=tmp_path / "out", data=data, expected_dir=exp, refined=refined, replicate_set=reps))
    (c.out / "order").mkdir(parents=True)
    head = "library\tfile\tv\tv_random_order\tverdict\n"
    (c.out / "order" / "order_by_library.tsv").write_text(head + "Revio\tf1\t0.3\t0.05\tNOT RANDOM\nRevio\tf2\t0.3\t0.05\tNOT RANDOM\nSequelII\tg1\t0.04\t0.05\trandom\n")
    p = n9.predictions(c)
    assert "4. The order check flags the Revio files and not the Sequel II files: Revio 2 of 2 NOT RANDOM, Sequel II 0 of 1: as predicted." in p
    assert p[4].startswith("5. T-cal and the truth test see the same composition: not known")
    (c.out / "order" / "order_by_library.tsv").write_text(head + "Revio\tf1\t0.3\t0.05\tNOT RANDOM\nRevio\tf2\t0.04\t0.05\trandom\nSequelII\tg1\t0.3\t0.05\tNOT RANDOM\n")
    assert "Revio 1 of 2 NOT RANDOM, Sequel II 1 of 1: NOT as predicted." in n9.predictions(c)[3]
    assert n9.predictions(n9.Ctx(SimpleNamespace(out=tmp_path / "empty", data=data, expected_dir=exp, refined=refined, replicate_set=reps)))[3].startswith("4. The order check on the Revio and the Sequel II files: not known")


def test_the_script_parses_as_python_3_9():
    ast.parse(Path(n9.__file__).read_text(), feature_version=(3, 9))
