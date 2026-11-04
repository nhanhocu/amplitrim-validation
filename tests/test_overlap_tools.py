"""The tools of the minimum-overlap test (register section 27) and of the tidy-up of the data drive: the command generator, the collector with its
verdicts, the inventory, the comparison of two release-check tables and the timer. All on small synthetic folders."""
import csv
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "validation"))
import collect_overlap_results as cor  # noqa: E402
import compare_nocap_tsv as cnt  # noqa: E402
import inventory_data as inv  # noqa: E402
import make_overlap_commands as moc  # noqa: E402

HEADER = ["name", "truncF", "truncR", "maxEE", "own", "own_what", "est_yield", "est_pass", "est_strict", "strains", "pass", "merged", "nonchim", "asvs",
          "top15", "n01", "tail", "found", "identical", "extra", "error"]


def write_table(path, rows):
    path.write_text("name\tready_dir\treference\tF\tamplicon\tmaxee\tpairs\n" + "".join("\t".join(r) + "\n" for r in rows), encoding="utf-8")
    return path


def test_the_generator_ties_the_cut_to_the_overlap_and_keeps_the_12_cut_in_arm_s(tmp_path):
    table = write_table(tmp_path / "t.tsv", [("mockA", "C:\\a", "C:\\a.fa", "273", "508", "2,3", "0")])
    lines = [x for x in moc.commands(moc.read_rows(table), "C:\\out", moc.OVERLAPS, None) if x.startswith("python")]
    assert len(lines) == 9                                              # five arm T runs and four arm S runs (k = 12 is only in T)
    text = "\n".join(lines)
    for k, reverse in ((10, 245), (12, 247), (15, 250), (20, 255), (25, 260)):
        assert f"--setting t{k}=273,{reverse},2,3" in text and f"--min-overlap {k} " in text
    for k in (10, 15, 20, 25):
        assert f"--setting s{k}=273,247,2,3" in text                    # the cut of k = 12 stays, only minOverlap changes
    assert "s12" not in text and "--pairs" not in text                 # pairs 0 = all


def test_only_the_chosen_lines_have_to_be_filled_in_and_a_wrong_name_is_refused(tmp_path):
    table = write_table(tmp_path / "t.tsv", [("mockA", "C:\\a", "C:\\a.fa", "273", "508", "2,3", "0"), ("d6300", "<FILL IN>", "<FILL IN>", "224", "430", "2", "5000")])
    assert [r["name"] for r in moc.read_rows(table, ["mockA"])] == ["mockA", "d6300"]
    with pytest.raises(SystemExit, match="fill in ready_dir for d6300"):
        moc.read_rows(table, ["d6300"])
    with pytest.raises(SystemExit, match="no line named"):
        moc.read_rows(table, ["mockC"])


def test_set_writes_values_into_the_table_with_tabs_and_keeps_a_path_with_spaces(tmp_path):
    table = write_table(tmp_path / "t.tsv", [("mockA", "<FILL IN>", "<FILL IN>", "273", "508", "2,3", "0")])
    moc.set_values(table, ["mockA.ready_dir=C:\\data\\a b\\ready", 'mockA.reference="C:\\data\\ref.fasta"'])
    row = next(csv.DictReader(open(table, encoding="utf-8"), delimiter="\t"))
    assert row["ready_dir"] == "C:\\data\\a b\\ready" and row["reference"] == "C:\\data\\ref.fasta" and row["F"] == "273"
    with pytest.raises(SystemExit, match="no column"):
        moc.set_values(table, ["mockA.nothing=1"])


def test_slim_keeps_the_results_and_refuses_a_run_that_did_not_finish(tmp_path):
    done, undone = tmp_path / "overlap_mockA_T_k12", tmp_path / "overlap_mockA_T_k15"
    for name, size in (("compare_methods.tsv", 10), ("compare_methods.txt", 10), ("asvs_t12.fasta", 10), ("track_t12.tsv", 10), ("filtered.fastq.gz", 5000), ("sub/work.bin", 5000)):
        (done / name).parent.mkdir(parents=True, exist_ok=True)
        (done / name).write_bytes(b"x" * size)
    undone.mkdir()
    (undone / "big.bin").write_bytes(b"x" * 100)
    assert moc.slim_folder(done) == 0
    assert sorted(p.name for p in done.rglob("*") if p.is_file()) == ["asvs_t12.fasta", "compare_methods.tsv", "compare_methods.txt", "track_t12.tsv"]
    assert not (done / "sub").exists()
    with pytest.raises(SystemExit, match="did not finish"):
        moc.slim_folder(undone)
    assert (undone / "big.bin").exists()                                # nothing is deleted from an unfinished run


def test_the_slim_step_is_added_to_each_command_only_with_the_option(tmp_path):
    table = write_table(tmp_path / "t.tsv", [("mockA", "C:\\a", "C:\\a.fa", "273", "508", "2,3", "5000")])
    rows = moc.read_rows(table)
    plain = [x for x in moc.commands(rows, "C:\\out", [12], None) if x.startswith("python")]
    slim = [x for x in moc.commands(rows, "C:\\out", [12], None, slim=True) if x.startswith("python")]
    assert "--slim-folder" not in plain[0] and "--pairs 5000" in plain[0]
    assert slim[0].startswith(plain[0] + " && python ") and '--slim-folder "C:\\out\\overlap_mockA_T_k12"' in slim[0]


def make_run(root, dataset, arm, k, merged, identical, extra, asvs=("ACGT",), ok=True, error=""):
    folder = Path(root) / f"overlap_{dataset}_{arm}_k{k}"
    folder.mkdir(parents=True)
    tag = f"{arm.lower()}{k}"
    row = {"name": tag, "truncF": 273, "truncR": 247, "maxEE": "2,3", "error": error}
    if ok:
        row.update({"pass": merged + 2, "merged": merged, "strains": "12/14", "found": 36, "identical": identical, "extra": extra, "asvs": len(asvs)})
    with open(folder / "compare_methods.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=HEADER, delimiter="\t")
        w.writeheader()
        w.writerow(row)
    (folder / f"asvs_{tag}.fasta").write_text("".join(f">a{i}\n{s}\n" for i, s in enumerate(asvs)), encoding="utf-8")


def make_mock(root, dataset, extra12, extra20, differ_at_10=False):
    same = ("AAAA", "CCCC")
    for k, merged in ((10, 70.0), (12, 69.5), (15, 68.5), (20, 66.6), (25, 65.4)):
        make_run(root, dataset, "T", k, merged, 0.998, {12: extra12, 20: extra20}.get(k, 5), same)
        if k != 12:
            make_run(root, dataset, "S", k, 69.5 if k == 10 else 60.0, 0.998, 5, same + (("GGGG",) if differ_at_10 and k == 10 else ()))


def test_the_collector_judges_the_predictions_by_the_rules_of_the_register(tmp_path):
    for ds in ("a", "b", "c", "d"):
        make_mock(tmp_path / "ok", ds, extra12=1, extra20=1)
    rows, unfinished = cor.collect(tmp_path / "ok")
    assert not unfinished and len(rows) == 36
    text = "\n".join(cor.judge(rows))
    assert "P-O1 MET" in text and "P-O2 MET" in text and "P-O3 MET" in text
    make_mock(tmp_path / "one", "e", extra12=16, extra20=11)           # 12 nt has 5 more unexpected ASVs than 20 nt: more than the 2 allowed
    rows, _ = cor.collect(tmp_path / "one")
    assert "P-O3 NOT MET" in "\n".join(cor.judge(rows))                # a failure is a failure, however few datasets there are
    for ds in ("a", "b", "c"):
        make_mock(tmp_path / "three", ds, extra12=1, extra20=1)
    rows, _ = cor.collect(tmp_path / "three")
    assert "P-O3 not judged: only 3 of 4 datasets" in "\n".join(cor.judge(rows))   # a pass needs all four mock communities


def test_an_extra_asv_at_k_10_with_the_12_cut_fails_the_first_prediction(tmp_path):
    for ds in ("a", "b", "c"):
        make_mock(tmp_path, ds, extra12=1, extra20=1)
    make_mock(tmp_path, "d", extra12=1, extra20=1, differ_at_10=True)
    rows, _ = cor.collect(tmp_path)
    assert "P-O1 NOT MET" in "\n".join(cor.judge(rows))


def test_a_run_without_a_result_is_labelled_and_takes_no_part_in_the_verdicts(tmp_path):
    for ds in ("a", "b", "c", "d"):
        make_mock(tmp_path, ds, extra12=1, extra20=1)
    import shutil
    shutil.rmtree(tmp_path / "overlap_d_T_k20")
    make_run(tmp_path, "d", "T", 20, 0, 0, 0, ok=False, error="DADA2 failed: r removed all reads: C:\\Users\\Admin\\AppData\\Temp\\x not written.")
    rows, _ = cor.collect(tmp_path)
    broken = [x for x in rows if x["dataset"] == "d" and x["arm"] == "T" and x["k"] == 20][0]
    assert broken["note"] == "no result: the cut is longer than the reads (DADA2 removed all reads)"
    assert "Admin" not in broken["note"]
    assert "P-O3 not judged" in "\n".join(cor.judge(rows))             # dataset d has no k = 20 to compare with: only three datasets are judged


def test_the_collector_writes_a_fingerprint_of_every_asv_set_and_equal_sets_have_equal_fingerprints(tmp_path):
    make_mock(tmp_path, "a", extra12=1, extra20=1, differ_at_10=True)
    for ds in ("b", "c", "d"):
        make_mock(tmp_path, ds, extra12=1, extra20=1)
    out = tmp_path / "res"
    assert cor.main([str(tmp_path), "--out", str(out)]) == 0
    rows = list(csv.DictReader(open(str(out) + "_asv_sets.tsv", encoding="utf-8"), delimiter="\t"))
    prints = {(r["dataset"], r["arm"], r["k"]): r["sha256_of_sorted_asvs"] for r in rows}
    assert len(rows) == 36 and all(len(r["sha256_of_sorted_asvs"]) == 16 for r in rows)
    assert prints[("b", "S", "10")] == prints[("b", "T", "12")]          # the same ASVs: the same fingerprint
    assert prints[("a", "S", "10")] != prints[("a", "T", "12")]          # one more ASV: another fingerprint
    text = Path(str(out) + ".md").read_text(encoding="utf-8")
    assert "## Verdicts" in text and "| note |" in text and "P-O1 NOT MET" in text


def test_the_inventory_classifies_folders_and_flags_what_needs_attention(tmp_path, capsys):
    data, repo = tmp_path / "data", tmp_path / "repo"
    for rel, size in (("01_mock_V1-V3_mockA_PRJEB67797/prepared/a.fastq.gz", 300), ("runs/03_night1_2026-10-09/battery/reads/r.fastq.gz", 800), ("runs/03_night1_2026-10-09/REPORT.md", 50),
                      ("runs/pypi_test/work/x.bin", 100), ("runs/overlap_mockA_T_k12/compare_methods.tsv", 10), ("_archive_2026-10/o.fasta", 200), ("misc/z.txt", 5)):
        (data / rel).parent.mkdir(parents=True, exist_ok=True)
        (data / rel).write_bytes(b"x" * size)
    (repo / "results" / "03_night1_2026-10-09").mkdir(parents=True)
    assert inv.main(["--base", str(data), "--repo", str(repo), "--out", str(tmp_path / "rep" / "inv")]) == 0
    capsys.readouterr()
    md = (tmp_path / "rep" / "inv.md").read_text(encoding="utf-8")
    assert "| misc | UNKNOWN |" in md and "| 01_mock_V1-V3_mockA_PRJEB67797 | dataset |" in md and "| _archive_2026-10 | old archive |" in md
    line = [x for x in md.splitlines() if x.startswith("| pypi_test |")][0]
    assert "no number" in line and "scratch?" in line and "not in results/" in line
    assert "not in results/" not in [x for x in md.splitlines() if x.startswith("| 03_night1_2026-10-09 |")][0]   # collected: not flagged
    assert "part of the overlap test" in [x for x in md.splitlines() if x.startswith("| overlap_mockA_T_k12 |")][0]
    rows = list(csv.DictReader(open(tmp_path / "rep" / "inv.tsv", encoding="utf-8"), delimiter="\t"))
    night = [r for r in rows if r["folder"] == "03_night1_2026-10-09"][0]
    assert night["files"] == "2" and night["kind"] == ""


def test_two_release_check_tables_are_compared_dataset_by_dataset(tmp_path, capsys):
    header = ["dataset", "released_truncF", "released_truncR", "released_maxEE", "floor", "floor_only_F", "floor_only_R", "short_lost", "noise_F", "noise_R"]
    rows = [["mockA", "273", "247", "2,3", "520", "274", "246", "0", "1", "1"], ["mockB", "274", "253", "4,8", "527", "274", "253", "0.2", "1", "3.5"]]
    paths = []
    for name, change in (("old", None), ("new", None), ("diff", ("mockB", 1, "250"))):
        p = tmp_path / f"{name}.tsv"
        with open(p, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh, delimiter="\t")
            w.writerow(header)
            for r in rows:
                r = list(r)
                if change and r[0] == change[0]:
                    r[change[1] + 1] = change[2]
                w.writerow(r)
        paths.append(str(p))
    assert cnt.main([paths[0], paths[1]]) == 0 and "2 of 2 datasets identical" in capsys.readouterr().out
    assert cnt.main([paths[0], paths[2]]) == 1 and "mockB: DIFFERENT" in capsys.readouterr().out


def test_the_timer_records_wall_time_memory_and_the_machine(tmp_path):
    pytest.importorskip("psutil")
    import time_amplitrim as ta
    log = tmp_path / "timing.jsonl"
    assert ta.main(["--label", "test", "--log", str(log), "--", sys.executable, "-c", "x = bytearray(20 * 1024 * 1024); import time; time.sleep(1.2)"]) == 0
    record = json.loads(log.read_text(encoding="utf-8").splitlines()[-1])
    assert record["label"] == "test" and record["exit_code"] == 0 and record["wall_seconds"] >= 0 and record["peak_memory_mb"] >= 15
    assert record["cpu_cores"] >= 1 and record["python"] and record["os"]
