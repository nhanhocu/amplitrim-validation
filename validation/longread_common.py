"""Helpers shared by the long-read tests T-cal (longread_calibration.py) and the truth test (longread_truth.py).

Edit distances use rapidfuzz (conda install -c conda-forge rapidfuzz). Without it only short sequences (up to 400 nt) can be compared, by a slow Python routine
that exists for the tests; for reads of 1,500 nt the module stops and says to install rapidfuzz.
"""

import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from longread_describe import open_text  # noqa: E402

PYTHON_LIMIT = 400                       # the longest sequence the slow Python routine accepts


def check_cutadapt() -> None:
    res = subprocess.run([sys.executable, "-m", "cutadapt", "--version"], capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit("cutadapt is not installed in this Python: pip install cutadapt")


def read_fasta(path) -> list:
    """[(header without '>', sequence)] of a FASTA file (plain or gzipped)."""
    out, name, parts = [], None, []
    with open_text(Path(path)) as fh:
        for line in fh:
            if line.startswith(">"):
                if name is not None:
                    out.append((name, "".join(parts)))
                name, parts = line[1:].strip(), []
            else:
                parts.append(line.strip())
    if name is not None:
        out.append((name, "".join(parts)))
    return out


def iter_fastq(path):
    """(name up to the first space, sequence, quality line) of every read of a FASTQ file (plain or gzipped)."""
    with open_text(Path(path)) as fh:
        while True:
            header = fh.readline()
            if not header:
                return
            seq = fh.readline().strip()
            fh.readline()
            qual = fh.readline().strip()
            fields = header[1:].split()
            yield (fields[0] if fields else ""), seq, qual


def quality_profile(path, n_reads: int = 20000) -> tuple:
    """(the highest quality score, the sorted distinct scores) over the first n_reads reads of a FASTQ file (Phred+33)."""
    chars, n = set(), 0
    for _, _, qual in iter_fastq(path):
        chars.update(qual)
        n += 1
        if n_reads and n >= n_reads:
            break
    values = sorted(ord(ch) - 33 for ch in chars)
    return (max(values) if values else None), values


def expected_errors(qual: str) -> float:
    """The sum over the bases of the chance that each is wrong, 10^(-Q/10) (Phred+33)."""
    q = np.frombuffer(qual.encode("ascii"), dtype=np.uint8).astype(np.float64) - 33.0
    return float(np.sum(10.0 ** (-q / 10.0)))


def pick_evenly(items: list, n: int) -> list:
    """n items spread evenly over the list (all of them when n is 0 or not smaller than the list)."""
    if n <= 0 or n >= len(items):
        return list(items)
    positions = sorted({int(round(x)) for x in np.linspace(0, len(items) - 1, n)})
    return [items[i] for i in positions]


def strain_of(variant_name: str) -> str:
    """The strain of an expected variant named STRAIN_vN|STRAIN|N_copies (the name itself when it has no bars)."""
    fields = variant_name.split("|")
    return fields[1] if len(fields) > 1 else variant_name


def _levenshtein_python(a: str, b: str, cap: int) -> int:
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur, best = [i], i
        for j, cb in enumerate(b, 1):
            v = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
            cur.append(v)
            best = min(best, v)
        if best > cap:
            return cap + 1
        prev = cur
    return min(prev[-1], cap + 1)


def distance_matrix(queries: list, targets: list, cap: int = 50) -> np.ndarray:
    """Edit distances, one row per query and one column per target; a distance above cap is given as cap + 1."""
    try:
        from rapidfuzz import process
        from rapidfuzz.distance import Levenshtein
    except ImportError:
        process = Levenshtein = None
    if Levenshtein is not None:
        try:
            return np.asarray(process.cdist(queries, targets, scorer=Levenshtein.distance, score_cutoff=cap, workers=-1), dtype=np.int32)
        except (TypeError, AttributeError, ValueError):          # an older rapidfuzz without cdist or its options: one pair at a time
            m = np.empty((len(queries), len(targets)), dtype=np.int32)
            for i, q in enumerate(queries):
                for j, t in enumerate(targets):
                    m[i, j] = Levenshtein.distance(q, t, score_cutoff=cap)
            return m
    if any(len(x) > PYTHON_LIMIT for x in list(queries) + list(targets)):
        raise SystemExit("rapidfuzz is needed to compare reads of this length: conda install -c conda-forge rapidfuzz (or pip install rapidfuzz)")
    return np.array([[_levenshtein_python(q, t, cap) for t in targets] for q in queries], dtype=np.int32).reshape(len(queries), len(targets))


def nearest(queries: list, targets: list, cap: int = 50, chunk: int = 5000) -> tuple:
    """(distance, index) of the nearest target of each query; a distance above cap is cap + 1."""
    if not targets:
        raise SystemExit("There are no expected variants to compare with.")
    dist = np.empty(len(queries), dtype=np.int32)
    idx = np.empty(len(queries), dtype=np.int32)
    for s in range(0, len(queries), chunk):
        m = distance_matrix(queries[s:s + chunk], targets, cap)
        idx[s:s + chunk] = m.argmin(axis=1)
        dist[s:s + chunk] = m.min(axis=1)
    return dist, idx


def ranks(values) -> np.ndarray:
    """Ranks starting at 0, ties given the mean of their ranks."""
    v = np.asarray(values, dtype=float)
    order = np.argsort(v, kind="mergesort")
    r = np.empty(len(v))
    r[order] = np.arange(len(v), dtype=float)
    sv, i = v[order], 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and sv[j + 1] == sv[i]:
            j += 1
        if j > i:
            r[order[i:j + 1]] = (i + j) / 2.0
        i = j + 1
    return r


def spearman(x, y):
    """Spearman's rank correlation, or None when it cannot be computed (fewer than 3 pairs, or no variation)."""
    if len(x) < 3 or len(x) != len(y):
        return None
    rx, ry = ranks(x), ranks(y)
    sx, sy = rx.std(), ry.std()
    if sx == 0 or sy == 0:
        return None
    return float(np.mean((rx - rx.mean()) * (ry - ry.mean())) / (sx * sy))
