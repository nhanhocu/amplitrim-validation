"""validation/longread_common.py: the readers, the expected errors, the edit distances (with a fake rapidfuzz and without one), nearest and the rank correlation."""
import ast
import gzip
import sys
import types
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "validation"))
import longread_common as lc  # noqa: E402


def fake_rapidfuzz(monkeypatch, cdist_works: bool = True, calls: list = None):
    """A stand-in for rapidfuzz with the documented behaviour: a distance above score_cutoff is returned as score_cutoff + 1."""
    def distance(a, b, score_cutoff=None):
        cap = 10 ** 9 if score_cutoff is None else score_cutoff
        return lc._levenshtein_python(a, b, cap)

    def cdist(queries, choices, scorer=None, score_cutoff=None, workers=1, **kw):
        if calls is not None:
            calls.append(("cdist", score_cutoff, workers))
        if not cdist_works:
            raise TypeError("this rapidfuzz has no such option")
        return [[scorer(q, c, score_cutoff=score_cutoff) for c in choices] for q in queries]

    lev = types.SimpleNamespace(distance=distance)
    top = types.ModuleType("rapidfuzz")
    top.process = types.SimpleNamespace(cdist=cdist)
    sub = types.ModuleType("rapidfuzz.distance")
    sub.Levenshtein = lev
    monkeypatch.setitem(sys.modules, "rapidfuzz", top)
    monkeypatch.setitem(sys.modules, "rapidfuzz.distance", sub)


def no_rapidfuzz(monkeypatch):
    monkeypatch.setitem(sys.modules, "rapidfuzz", None)                 # an import of None raises ImportError
    monkeypatch.setitem(sys.modules, "rapidfuzz.distance", None)


def test_the_readers_for_fasta_and_fastq_plain_and_gzipped(tmp_path):
    (tmp_path / "a.fasta").write_text(">x_v1|X|2_copies\nACGT\nACGT\n>y\nTTTT\n")
    assert lc.read_fasta(tmp_path / "a.fasta") == [("x_v1|X|2_copies", "ACGTACGT"), ("y", "TTTT")]
    with gzip.open(tmp_path / "r.fastq.gz", "wt") as fh:
        fh.write("@r1 rc\nACGT\n+\nIIII\n@r2\nGG\n+\n!!\n")
    assert list(lc.iter_fastq(tmp_path / "r.fastq.gz")) == [("r1", "ACGT", "IIII"), ("r2", "GG", "!!")]
    (tmp_path / "e.fastq").write_text("")
    assert list(lc.iter_fastq(tmp_path / "e.fastq")) == []


def test_expected_errors_are_the_sum_of_the_error_probabilities():
    assert lc.expected_errors("!") == pytest.approx(1.0)                                  # Q0: the base is surely wrong
    assert lc.expected_errors("5") == pytest.approx(0.01)                                 # Q20
    assert lc.expected_errors("II") == pytest.approx(2e-4)                                # two bases of Q40
    assert lc.expected_errors("!5I") == pytest.approx(1.0 + 0.01 + 1e-4)


def test_pick_evenly_and_strain_of():
    items = list(range(10))
    assert lc.pick_evenly(items, 0) == items and lc.pick_evenly(items, 20) == items
    assert lc.pick_evenly(items, 3) == [0, 4, 9] or lc.pick_evenly(items, 3) == [0, 5, 9]
    assert lc.pick_evenly(items, 1) == [0] and len(lc.pick_evenly(items, 4)) == 4
    assert lc.strain_of("Escherichia_coli_ATCC700926_v3|Escherichia_coli_ATCC700926|2_copies") == "Escherichia_coli_ATCC700926" and lc.strain_of("plain") == "plain"


def test_the_python_levenshtein_and_its_cap():
    f = lc._levenshtein_python
    assert f("ACGT", "ACGT", 5) == 0 and f("ACGT", "ACCT", 5) == 1 and f("ACGT", "ACGGT", 5) == 1 and f("ACGT", "AGT", 5) == 1 and f("", "AC", 5) == 2
    assert f("AAAA", "TTTT", 2) == 3                                                       # above the cap: cap + 1
    assert f("A" * 10, "A", 3) == 4                                                        # lengths differ by more than the cap


def test_distances_without_rapidfuzz_use_the_python_routine_for_short_sequences_only(monkeypatch):
    no_rapidfuzz(monkeypatch)
    m = lc.distance_matrix(["ACGT", "AAAA"], ["ACGT", "ACGA", "TTTT"], cap=5)
    assert m.shape == (2, 3) and m.dtype == np.int32 and m.tolist() == [[0, 1, 3], [3, 2, 4]]
    with pytest.raises(SystemExit, match="rapidfuzz is needed"):
        lc.distance_matrix(["A" * 500], ["A" * 500], cap=5)
    assert lc.distance_matrix([], ["ACGT"], cap=5).shape == (0, 1)


def test_distances_with_rapidfuzz_are_asked_for_with_the_cap_and_all_cores(monkeypatch):
    calls = []
    fake_rapidfuzz(monkeypatch, calls=calls)
    m = lc.distance_matrix(["ACGT", "AAAA"], ["ACGT", "TTTT"], cap=2)
    assert m.tolist() == [[0, 3], [3, 3]] and calls == [("cdist", 2, -1)]                 # TTTT is above the cap: 3 = cap + 1


def test_an_older_rapidfuzz_without_cdist_options_is_used_one_pair_at_a_time(monkeypatch):
    calls = []
    fake_rapidfuzz(monkeypatch, cdist_works=False, calls=calls)
    m = lc.distance_matrix(["ACGT"], ["ACGT", "ACGA"], cap=5)
    assert m.tolist() == [[0, 1]] and calls == [("cdist", 5, -1)]


def test_nearest_returns_the_closest_target_and_flags_those_beyond_the_cap(monkeypatch):
    no_rapidfuzz(monkeypatch)
    d, i = lc.nearest(["ACGTACGT", "ACGTACGA", "GGGGGGGG"], ["ACGTACGT", "TTTTTTTT"], cap=3, chunk=2)
    assert d.tolist() == [0, 1, 4] and i[:2].tolist() == [0, 0]                           # the third read is more than 3 edits from both
    with pytest.raises(SystemExit, match="no expected variants"):
        lc.nearest(["A"], [], cap=3)


def test_ranks_and_spearman():
    assert lc.ranks([10, 30, 20]).tolist() == [0.0, 2.0, 1.0]
    assert lc.ranks([1, 1, 3]).tolist() == [0.5, 0.5, 2.0]                                 # ties share the mean rank
    assert lc.spearman([1, 2, 3, 4], [10, 20, 30, 40]) == pytest.approx(1.0)
    assert lc.spearman([1, 2, 3, 4], [4, 3, 2, 1]) == pytest.approx(-1.0)
    assert lc.spearman([1, 2], [1, 2]) is None and lc.spearman([1, 1, 1], [1, 2, 3]) is None


def test_the_quality_profile_gives_the_highest_score_and_the_distinct_scores(tmp_path):
    p = tmp_path / "q.fastq"
    p.write_text("@r1\nACGT\n+\n!5I~\n@r2\nACGT\n+\nIIII\n@r3\nAC\n+\n#I\n")
    top, values = lc.quality_profile(p, 0)
    assert top == 93 and values == [0, 2, 20, 40, 93]                                           # ! is 0, # is 2, 5 is 20, I is 40, ~ is 93
    assert lc.quality_profile(p, 2) == (93, [0, 20, 40, 93])                                    # only the first two reads
    empty = tmp_path / "e.fastq"
    empty.write_text("")
    assert lc.quality_profile(empty) == (None, [])


def test_the_cutadapt_check_names_the_remedy(monkeypatch):
    import subprocess
    monkeypatch.setattr(subprocess, "run", lambda cmd, **kw: subprocess.CompletedProcess(cmd, 1, "", "No module named cutadapt"))
    with pytest.raises(SystemExit, match="pip install cutadapt"):
        lc.check_cutadapt()
    monkeypatch.setattr(subprocess, "run", lambda cmd, **kw: subprocess.CompletedProcess(cmd, 0, "5.2\n", ""))
    lc.check_cutadapt()


def test_the_module_parses_as_python_3_9():
    ast.parse(Path(lc.__file__).read_text(), feature_version=(3, 9))
