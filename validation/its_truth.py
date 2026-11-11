#!/usr/bin/env python
"""ITS truth test: the single isolates of Arfken et al. 2023 give the true sequences, the mixes of the same isolates are checked against them.

  python validation\\its_truth.py --out C:\\data\\runs\\26_its_followup_arfken

Reads what validation\\its_followup.py wrote to --out for these labels (run it first, with --dataset for each, 5,000 pairs per sample):
  arfken_its1 and arfken_its2         the isolates (C, K, M, P, T in triplicate)      arfken_mix_its1 and arfken_mix_its2      the mixes MixA (KCTPM), MixB (KC), MixC (KT)
For each marker the reference is the set of merged sequences of the isolates at the default limit (0) that hold at least 1% of an isolate's merged pairs (the three replicates pooled).
A merged sequence of a mix is *true* when it is within 2 edits (mismatches or indels) of a reference sequence of any isolate, and *spurious* otherwise.
For every mismatch limit it gives the share of the merged pairs of the mixes that sit in spurious sequences, the share of the reference sequences of the isolates in the mix that are found
(each holding at least 0.1% of the merged pairs of the sample), and the share of the input pairs that merge. Part of TEST_REGISTER.md (the section for this follow-up; criteria P80 to P82).
Writes ITS_TRUTH_REPORT.md to --out.
"""
import argparse
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]

import its_followup as F                                                  # noqa: E402  (the readers of its tables)

MIXES = {"MixA": "KCTPM", "MixB": "KC", "MixC": "KT"}                      # the isolates in each mix (M is the Mucor / Lichtheimia isolate), Table 4 of the paper
MARKERS = ("its1", "its2")
REF_SHARE = 0.01          # a sequence is part of an isolate's reference when it holds at least this share of the isolate's merged pairs
SEEN_SHARE = 0.001        # a reference sequence is found in a mix sample when a true sequence within EDIT edits holds at least this share of the sample's merged pairs
EDIT = 2                  # edits (mismatches or indels) allowed between a merged sequence and a reference sequence
SPURIOUS_RISE = 1.0       # P80: allowing 2 mismatches raises the spurious share by at most this many points, on every marker
GAIN = 2.0                # P82: allowing 2 mismatches merges at least this many points more of the input pairs, on at least one marker


def read_seqs(path: Path) -> list:
    """(sample, limit, sequence, merged pairs) for every merged sequence."""
    rows = []
    with open(path, encoding="utf-8") as fh:
        head = fh.readline().rstrip("\n").split("\t")
        if head != ["sample", "k", "sequence", "abundance"]:
            raise RuntimeError(f"{path} does not have the columns sample, k, sequence, abundance")
        for line in fh:
            s, k, q, a = line.rstrip("\n").split("\t")
            rows.append((s, int(float(k)), q, float(a)))
    return rows


def within_edits(a: str, b: str, k: int = EDIT) -> bool:
    """True when the edit distance (mismatches, insertions, deletions) of a and b is at most k. Banded, so it is fast for long sequences."""
    if a == b:
        return True
    n, m = len(a), len(b)
    if abs(n - m) > k:
        return False
    big = k + 1
    prev = {j: j for j in range(0, min(m, k) + 1)}
    for i in range(1, n + 1):
        cur = {}
        for j in range(max(0, i - k), min(m, i + k) + 1):
            if j == 0:
                cur[0] = i
                continue
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(prev.get(j - 1, big) + cost, prev.get(j, big) + 1, cur.get(j - 1, big) + 1)
        if not cur or min(cur.values()) > k:
            return False
        prev = cur
    return prev.get(m, big) <= k


def isolate_of(sample: str) -> str:
    return sample.split("-")[0]                                            # C-ITS1a -> C


def mix_of(sample: str) -> str:
    return sample.split("-")[0]                                            # MixB-ITS1a -> MixB


def reference(rows: list, share: float = REF_SHARE) -> dict:
    """isolate letter -> set of sequences holding at least `share` of that isolate's merged pairs at limit 0, the replicates pooled."""
    total, per = defaultdict(float), defaultdict(lambda: defaultdict(float))
    for s, k, q, a in rows:
        if k == 0:
            iso = isolate_of(s)
            total[iso] += a
            per[iso][q] += a
    return {iso: {q for q, a in seqs.items() if a >= share * total[iso]} for iso, seqs in per.items() if total[iso] > 0}


class Truth:
    """Decides, with a memory, whether a merged sequence is within EDIT edits of a reference sequence."""

    def __init__(self, ref: dict):
        self.ref, self.every, self.memo = ref, sorted({q for v in ref.values() for q in v}), {}

    def is_true(self, seq: str) -> bool:
        if seq not in self.memo:
            self.memo[seq] = any(within_edits(seq, r) for r in self.every)
        return self.memo[seq]

    def covers(self, ref_seq: str, seq: str) -> bool:
        return within_edits(seq, ref_seq)


def mix_profile(seq_rows: list, sample_rows: list, ref: dict, limits=F.LIMITS) -> dict:
    """For the mixes of one marker: per limit the mean share of merged pairs in spurious sequences (over samples), the mean share of the reference sequences found, and the share of the
    input pairs that merge."""
    truth = Truth(ref)
    by = defaultdict(lambda: defaultdict(list))
    for s, k, q, a in seq_rows:
        by[k][s].append((q, a))
    out = {"spurious": {}, "recall": {}, "merged": {}, "samples": 0}
    inp = sum(r["input"] for r in sample_rows) or 1
    for k in limits:
        sp, rc = [], []
        for s, seqs in by[k].items():
            total = sum(a for _, a in seqs)
            if total <= 0:
                continue
            sp.append(sum(a for q, a in seqs if not truth.is_true(q)) / total)
            expected = set().union(*(ref.get(i, set()) for i in MIXES.get(mix_of(s), "")))
            if expected:
                seen = [q for q, a in seqs if a >= SEEN_SHARE * total]
                rc.append(sum(any(truth.covers(r, q) for q in seen) for r in expected) / len(expected))
        out["spurious"][k] = sum(sp) / len(sp) if sp else None
        out["recall"][k] = sum(rc) / len(rc) if rc else None
        out["merged"][k] = sum(r[f"merged_k{k}"] for r in sample_rows) / inp
        out["samples"] = max(out["samples"], len(sp))
    return out


def verdicts(res: dict) -> list:
    """res: marker -> mix_profile or None. P80 and P81 need every marker that was run, P82 at least one."""
    run = {m: p for m, p in res.items() if p and p["spurious"].get(0) is not None and p["spurious"].get(2) is not None}
    if not run:
        return [(p, "not decided: the mixes were not run", None) for p in ("P80", "P81", "P82")]
    rise = {m: (p["spurious"][2] - p["spurious"][0]) * 100 for m, p in run.items()}
    out = [("P80", f"On the mixes, allowing 2 mismatches raises the share of merged pairs in spurious sequences by at most {SPURIOUS_RISE:g} point on every marker: "
                   + ", ".join(f"{m} {v:+.2f} points ({run[m]['spurious'][0]:.2%} to {run[m]['spurious'][2]:.2%})" for m, v in rise.items()), all(v <= SPURIOUS_RISE for v in rise.values()))]
    rc = {m: p for m, p in run.items() if p["recall"].get(0) is not None and p["recall"].get(2) is not None}
    out.append(("P81", "On the mixes, allowing 2 mismatches does not lower the share of the reference sequences that are found, on any marker: "
                       + (", ".join(f"{m} {p['recall'][0]:.1%} to {p['recall'][2]:.1%}" for m, p in rc.items()) if rc else "no reference sequence was expected"),
                None if not rc else all(p["recall"][2] >= p["recall"][0] for p in rc.values())))
    gain = {m: (p["merged"][2] - p["merged"][0]) * 100 for m, p in run.items()}
    out.append(("P82", f"On the mixes, allowing 2 mismatches merges at least {GAIN:g} points more of the input pairs on at least one marker: " + ", ".join(f"{m} {v:+.1f} points" for m, v in gain.items()),
                any(v >= GAIN for v in gain.values())))
    return out


def report_lines(res: dict, refs: dict, limits=F.LIMITS) -> list:
    L = ["# ITS truth test", "", "The criteria (P80 to P82) are in TEST_REGISTER.md and were fixed before this ran.", "", "## Verdicts", ""]
    for p, txt, ok in verdicts(res):
        L.append(f"- **{p}** {txt}" if ok is None else f"- **{p}** {'MET' if ok else 'NOT MET'}: {txt}")
    for m, prof in res.items():
        L += ["", f"## {m.upper()} mixes", ""]
        if not prof:
            L.append("Not run.")
            continue
        L += [f"Reference sequences per isolate: " + ", ".join(f"{i} {len(v)}" for i, v in sorted(refs[m].items())) + f". Mix samples: {prof['samples']}.", "",
              "| mismatches allowed | merged (share of the input pairs) | merged pairs in spurious sequences | reference sequences found |", "|---|---|---|---|"]
        pct = lambda v: "" if v is None else f"{v:.2%}"
        for k in limits:
            L.append(f"| {k}{' (default)' if k == 0 else ''} | {prof['merged'][k]:.2%} | {pct(prof['spurious'][k])} | {pct(prof['recall'][k])} |")
    return L + ["", "Next: send this file."]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, required=True, help="the --out folder of validation\\its_followup.py")
    a = ap.parse_args(argv)
    res, refs = {}, {}
    for m in MARKERS:
        iso, mix = a.out / f"arfken_{m}_seqs.tsv", a.out / f"arfken_mix_{m}_seqs.tsv"
        if not (iso.is_file() and mix.is_file()):
            res[m] = None
            continue
        refs[m] = reference(read_seqs(iso))
        res[m] = mix_profile(read_seqs(mix), F.read_samples(a.out / f"arfken_mix_{m}_samples.tsv"), refs[m])
    if not any(res.values()):
        print(f"No marker has both its isolates and its mixes in {a.out}: run validation\\its_followup.py for arfken_its1, arfken_its2, arfken_mix_its1 and arfken_mix_its2 first.")
        return 2
    L = report_lines(res, refs)
    (a.out / "ITS_TRUTH_REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:next(i for i, x in enumerate(L) if x.startswith("## ") and x != "## Verdicts")]))
    print(f"\nwritten: {a.out / 'ITS_TRUTH_REPORT.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
