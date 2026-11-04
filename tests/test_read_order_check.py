"""validation/read_order_check.py: the blocks, the test of homogeneity, a shuffled and a sorted file, a drift of quality, and the outputs (stand-ins for cutadapt and the edit distance)."""
import ast
import random
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "validation"))
import longread_common as lc  # noqa: E402
import longread_filter_check as lf  # noqa: E402
import read_order_check as roc  # noqa: E402
import test_longread_calibration as t_cal  # noqa: E402
import test_longread_filter_check as t4  # noqa: E402
import test_longread_truth as t_truth  # noqa: E402

FWD, REV = t4.FWD, t4.REV


@pytest.fixture
def stand_ins(monkeypatch):
    monkeypatch.setattr(lf, "run_cutadapt", t_cal.named_stand_in_cutadapt)
    monkeypatch.setattr(lc, "nearest", t_cal.hamming_nearest)
    monkeypatch.setattr(lc, "check_cutadapt", lambda: None)


def expected_fasta(tmp_path):
    var = t_cal.make_variants(150)                                  # A_v1 and A_v2 (strain A), B_v1 (strain B)
    p = tmp_path / "expected.fasta"
    p.write_text("".join(f">{n}\n{s}\n" for n, s in var))
    return p, var


def reads_of(var, n=600, seed=5, quality_drift=False):
    """n reads: 40% A_v1, 20% A_v2, 40% B_v1, in a list that the callers shuffle or sort; with quality_drift the later half has a quality of Q20."""
    rng = random.Random(seed)
    kinds = [0] * int(0.4 * n) + [1] * int(0.2 * n) + [2] * (n - int(0.4 * n) - int(0.2 * n))
    return rng, kinds


def write(path, var, order, rng, drift=False):
    recs = []
    for i, k in enumerate(order):
        full, q = t_truth.plain_read(var[k][1], rng)
        if drift and i >= len(order) // 2:
            q = "5" * len(q)
        recs.append((full, q))
    t4.write_fastq(path, recs)
    return path


def test_homogeneity_of_a_uniform_and_of_a_separated_table():
    flat = roc.homogeneity(np.array([[50.0, 50.0, 50.0], [50.0, 50.0, 50.0]]))
    assert flat["chi2"] == 0 and flat["v"] == 0 and flat["random"] is True and flat["df"] == 2
    sep = roc.homogeneity(np.array([[100.0, 0.0, 0.0], [0.0, 100.0, 0.0], [0.0, 0.0, 100.0]]))
    assert sep["v"] == pytest.approx(1.0) and sep["random"] is False and sep["z"] > 4
    assert sep["null_v"] == pytest.approx((4 / (300 * 2)) ** 0.5)                          # the V that random order gives for 3 x 3 and 300 reads: sqrt(df / (n * k))


def test_the_blocks_are_the_first_reads_of_consecutive_stretches(tmp_path):
    path = tmp_path / "f.fastq"
    path.write_text("".join(f"@r{i}\nACGT\n+\nIIII\n" for i in range(40)))
    dest = tmp_path / "b.fastq.gz"
    total, size, take = roc.sample_blocks(path, 4, 3, dest)
    assert (total, size, take) == (40, 10, 3)
    assert [n for n, _, _ in lc.iter_fastq(dest)] == [f"b{b}_{k}" for b in range(4) for k in range(3)]
    assert roc.sample_blocks(path, 4, 50, tmp_path / "c.fastq.gz")[2] == 10                  # a block cannot give more reads than it holds
    tiny = tmp_path / "t.fastq"
    tiny.write_text("".join(f"@r{i}\nACGT\n+\nIIII\n" for i in range(3)))
    assert roc.sample_blocks(tiny, 10, 5, tmp_path / "d.fastq.gz") == (3, 1, 1) and len(list(lc.iter_fastq(tmp_path / "d.fastq.gz"))) == 3


def test_a_shuffled_file_is_random_and_the_same_reads_sorted_are_not(tmp_path, stand_ins):
    fasta, var = expected_fasta(tmp_path)
    rng, kinds = reads_of(var)
    shuffled = list(kinds)
    random.Random(1).shuffle(shuffled)
    f_random = write(tmp_path / "random.fastq.gz", var, shuffled, rng)
    f_sorted = write(tmp_path / "sorted.fastq.gz", var, sorted(kinds), rng)
    res = roc.run([f_random, f_sorted], fasta, FWD, REV, tmp_path / "out", blocks=6, per_block=50, log=lambda *_: None)
    rnd, srt = res
    assert rnd["stats"]["random"] is True and rnd["stats"]["z"] < 4 and rnd["stats"]["v"] < 2 * rnd["stats"]["null_v"]
    assert srt["stats"]["random"] is False and srt["stats"]["v"] > 0.5 and srt["stats"]["z"] > 4          # the first blocks hold only A_v1, the last only B_v1
    assert rnd["total"] == srt["total"] == 600 and rnd["block_size"] == 100 and rnd["per_block"] == 50
    first, last = srt["table"][:, 0], srt["table"][:, -1]
    names = srt["strains"]
    assert first[names.index("A")] == 50 and first[names.index("B")] == 0 and last[names.index("B")] == 50      # block 1 is all strain A, block 6 all strain B
    text = (tmp_path / "out" / "ORDER_CHECK.md").read_text()
    assert "## random" in text and "## sorted" in text and "**NOT RANDOM**" in text and "**consistent with random order**" in text and "| block | reads |" in text
    rows = [l.split("\t") for l in (tmp_path / "out" / "order_summary.tsv").read_text().splitlines()]
    assert rows[0][-1] == "verdict" and {r[0]: r[-1] for r in rows[1:]} == {"random": "random", "sorted": "NOT RANDOM"}
    blocks = [l.split("\t") for l in (tmp_path / "out" / "order_blocks.tsv").read_text().splitlines()]
    assert blocks[0][:4] == ["file", "block", "reads_assigned", "mean_expected_errors"] and len(blocks) == 1 + 2 * 6
    assert not (tmp_path / "out" / "work").exists()


def test_a_drift_of_quality_along_the_file_shows_in_the_blocks(tmp_path, stand_ins):
    fasta, var = expected_fasta(tmp_path)
    rng, kinds = reads_of(var)
    random.Random(2).shuffle(kinds)
    f = write(tmp_path / "drift.fastq.gz", var, kinds, rng, drift=True)
    r = roc.run([f], fasta, FWD, REV, tmp_path / "out", blocks=6, per_block=50, log=lambda *_: None)[0]
    ee = r["mean_ee"]
    assert ee[0] < 0.1 and ee[-1] > 1.0 and r["stats"]["random"] is True                      # the composition is even, the expected errors rise from Q40 to Q20 reads


def test_a_file_with_one_strain_or_few_reads_is_not_tested(tmp_path, stand_ins):
    fasta, var = expected_fasta(tmp_path)
    rng = random.Random(3)
    f = write(tmp_path / "one.fastq.gz", var, [0] * 5, rng)
    r = roc.run([f], fasta, FWD, REV, tmp_path / "out", blocks=10, per_block=5, log=lambda *_: None)[0]
    assert r["stats"] is None and r["total"] == 5
    assert "Not enough strains or blocks to test." in (tmp_path / "out" / "ORDER_CHECK.md").read_text() and "not tested" in (tmp_path / "out" / "order_summary.tsv").read_text()


def test_an_empty_reference_and_a_file_without_primers_are_refused(tmp_path, stand_ins):
    empty = tmp_path / "empty.fasta"
    empty.write_text("")
    with pytest.raises(SystemExit, match="No expected variants"):
        roc.run([tmp_path / "x.fastq"], empty, FWD, REV, tmp_path / "o", log=lambda *_: None)
    fasta, var = expected_fasta(tmp_path)
    t4.write_fastq(tmp_path / "noprimer.fastq.gz", [("ACGT" * 60, "I" * 240)] * 20)
    with pytest.raises(SystemExit, match="has both primers"):
        roc.run([tmp_path / "noprimer.fastq.gz"], fasta, FWD, REV, tmp_path / "o2", blocks=4, per_block=5, log=lambda *_: None)


def test_the_command_line(tmp_path, stand_ins):
    fasta, var = expected_fasta(tmp_path)
    rng, kinds = reads_of(var)
    f = write(tmp_path / "cli.fastq.gz", var, sorted(kinds), rng)
    rc = roc.main([str(f), "--expected", str(fasta), "--primer-f", FWD, "--primer-r", REV, "--out", str(tmp_path / "o"), "--blocks", "6", "--per-block", "50"])
    assert rc == 0 and (tmp_path / "o" / "ORDER_CHECK.md").is_file() and "NOT RANDOM" in (tmp_path / "o" / "order_summary.tsv").read_text()


def test_the_script_parses_as_python_3_9():
    ast.parse(Path(roc.__file__).read_text(), feature_version=(3, 9))
