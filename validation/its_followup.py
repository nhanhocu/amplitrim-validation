#!/usr/bin/env python
"""ITS follow-up: why does DADA2 refuse so many ITS pairs at the merge step, and is a mismatch limit above 0 a safe answer?

  python validation\\its_followup.py --dataset its2=C:\\data\\reads\\its2 --dataset its=C:\\data\\reads\\its --dataset v4=C:\\data\\reads\\v4 --trunc v4=124,115 --out C:\\data\\runs\\its_followup
  python validation\\its_followup.py --dataset arfken_its2=C:\\data\\reads\\arfken_its2_isolates --dataset arfken_its1=C:\\data\\reads\\arfken_its1_isolates --out ...

Needs R and DADA2. For every dataset it thins the reads (5,000 pairs per sample, as in the earlier runs), runs DADA2 once, then mergePairs on the same
denoised sequences at the mismatch limits 0, 1, 2 and 5; at the default limit (0) every pair is written with the length of its overlap. The labels matter:
its2 (the second ITS study), its (the first), v4 (soil V4, with --trunc v4=<forward>,<reverse> for AmpliTrim's cut), and arfken_its1 and arfken_its2
(the single-isolate libraries of Arfken et al. 2023, PRJNA693350); arfken_mix_its1 and arfken_mix_its2 are their mixes (validation\\its_truth.py). A label that is not run leaves its criteria 'not decided'.
Part of TEST_REGISTER.md (the section for this follow-up; criteria P68 to P75, fixed before the run). Writes ITS_FOLLOWUP_REPORT.md and, per
dataset, <label>_samples.tsv, <label>_pairs.tsv and <label>_seqs.tsv (the merged sequences at every limit) to --out.
"""
import argparse
import csv
import statistics
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path[:0] = [str(HERE), str(ROOT)]

MIN_LEN, MAX_EE, MIN_OVERLAP = 50, 2.0, 12
LIMITS = (0, 1, 2, 5)
DEFAULT_PAIRS = 5000
R_SCRIPT = HERE / "its_followup.R"
NEAR_MISS_SHARE = 0.5          # P68: allowing 2 mismatches merges at least this share of the pairs that the default refuses for mismatches or indels
LENGTH_POINTS = 15.0           # P69: refused-for-mismatch share, longest third of the overlaps minus shortest third, at least this many points
INDEL_SHARE = 0.20             # P70: at least this share of the pairs refused for mismatches or indels have an indel
ASV_RISE = 0.10                # P72: allowing 2 mismatches raises the median number of ASVs per sample by at most this share
PARTNERS = 0.5                 # P73 and P75: at least this share of the refused pairs have a forward and a reverse sequence that each occur in an accepted pair of the same sample
ISOLATE_RISE = 1               # P74: on the single-isolate libraries, allowing 2 mismatches adds at most this many ASVs per sample (median)
BASE = ["sample", "input", "filtered", "reach", "rej_short", "rej_mismatch", "rej_other"]
IDS = ["P68", "P69", "P70", "P71", "P72", "P73", "P74", "P75"]
ISOLATES = ("arfken_its1", "arfken_its2")      # the single-isolate libraries of P74; arfken_mix_its1 and arfken_mix_its2 are the mixes of validation\\its_truth.py


def columns(limits=LIMITS) -> list:
    return BASE + [f"{p}_k{k}" for k in limits for p in ("merged", "asv")]


def read_samples(path: Path, limits=LIMITS) -> list:
    with open(path, newline="", encoding="utf-8") as fh:
        rows = [{k: (float(v) if k != "sample" else v) for k, v in r.items()} for r in csv.DictReader(fh, delimiter="\t")]
    missing = [c for c in columns(limits) if rows and c not in rows[0]]
    if missing:
        raise RuntimeError(f"the table from R lacks the columns {missing}")
    return rows


def read_pairs(path: Path) -> list:
    """(abundance, accepted, matches, mismatches, indels) for every distinct pair of denoised sequences at the default limit."""
    with open(path, newline="", encoding="utf-8") as fh:
        return [(float(r["abundance"]), r["accept"].strip().upper() == "TRUE", int(float(r["nmatch"])), int(float(r["nmismatch"])), int(float(r["nindel"])))
                for r in csv.DictReader(fh, delimiter="\t")]


def read_partners(path: Path) -> list:
    """(sample, forward, reverse, abundance, accepted): which two denoised sequences each distinct pair joins."""
    with open(path, newline="", encoding="utf-8") as fh:
        return [(r["sample"], int(float(r["forward"])), int(float(r["reverse"])), float(r["abundance"]), r["accept"].strip().upper() == "TRUE")
                for r in csv.DictReader(fh, delimiter="\t")]


def partner_share(rows: list):
    """The share of the refused pairs (by abundance) whose forward sequence and whose reverse sequence each occur in an accepted pair of the same sample: the halves are
    good, the pairing is not. None when nothing was refused. A refused pair whose halves occur only in refused pairs looks like a pair that has no overlap to find."""
    acc_f, acc_r = {}, {}
    for s, f, r, a, ok in rows:
        if ok:
            acc_f.setdefault(s, set()).add(f)
            acc_r.setdefault(s, set()).add(r)
    refused = both = 0.0
    for s, f, r, a, ok in rows:
        if not ok:
            refused += a
            both += a if (f in acc_f.get(s, ()) and r in acc_r.get(s, ())) else 0.0
    return both / refused if refused > 0 else None


def refused_alignment(pairs: list) -> dict:
    """Of the pairs refused for any reason, the share whose alignment has no column at all (matches + mismatches + indels = 0): DADA2 found nothing to line up."""
    total = sum(a for a, ok, *_ in pairs if not ok)
    if total <= 0:
        return {}
    return {"refused": total, "zero_share": sum(a for a, ok, m, mm, ind in pairs if not ok and m + mm + ind == 0) / total}


def flow(rows: list, limits=LIMITS) -> dict:
    """Shares of the input pairs: through the filter, into the merge step, refused by reason, merged at each limit; the share of the pairs refused at limit 0
    for mismatches or indels that merge at each higher limit; the median number of ASVs per sample at each limit."""
    inp = sum(r["input"] for r in rows)
    if inp <= 0:
        return {}
    tot = lambda key: sum(r[key] for r in rows)
    out = {"samples": len(rows), "input": inp, "filtered": tot("filtered") / inp, "reach": tot("reach") / inp, "rej_short": tot("rej_short") / inp,
           "rej_mismatch": tot("rej_mismatch") / inp, "rej_other": tot("rej_other") / inp}
    out["merged"] = {k: tot(f"merged_k{k}") / inp for k in limits}
    out["asv"] = {k: statistics.median(r[f"asv_k{k}"] for r in rows) for k in limits}
    refused = tot("rej_mismatch")
    out["recovered"] = {k: ((tot(f"merged_k{k}") - tot("merged_k0")) / refused if refused > 0 else None) for k in limits if k > 0}
    # on a short overlap the alignment drops an overlap that has a mismatch, so such pairs are filed as 'short' at the default; this share is of every refused pair
    every = tot("rej_short") + tot("rej_mismatch") + tot("rej_other")
    out["recovered_all"] = {k: ((tot(f"merged_k{k}") - tot("merged_k0")) / every if every > 0 else None) for k in limits if k > 0}
    return out


def overlap_profile(pairs: list, min_overlap: int = MIN_OVERLAP) -> dict:
    """Among the pairs with an overlap of at least min_overlap (the length of the overlap is its matches plus mismatches plus indels, so a pair with fewer than
    min_overlap matching bases that is long enough counts here, and is refused for its mismatches): the median overlap, the share refused for
    mismatches or indels in the shortest and in the longest third of the pairs (thirds by pair count, ordered by overlap), and the share of those refusals that involve an indel."""
    kept = sorted(((m + mm + ind, a, ok, mm, ind) for a, ok, m, mm, ind in pairs if m + mm + ind >= min_overlap), key=lambda p: p[0])
    total = sum(p[1] for p in kept)
    if total <= 0:
        return {}
    cum, median, low, high = 0.0, None, [0.0, 0.0, None], [0.0, 0.0, None]
    refused = refused_indel = 0.0
    for ov, a, ok, mm, ind in kept:
        bad = (not ok) and (mm > 0 or ind > 0)
        if median is None and cum + a >= total / 2:
            median = ov
        if cum < total / 3:
            low[0] += a
            low[1] += a if bad else 0.0
            low[2] = ov
        elif cum >= 2 * total / 3:
            high[0] += a
            high[1] += a if bad else 0.0
            high[2] = ov if high[2] is None else high[2]
        if bad:
            refused += a
            refused_indel += a if ind > 0 else 0.0
        cum += a
    return {"pairs": total, "median_overlap": median, "low_share": low[1] / low[0] if low[0] else None, "high_share": high[1] / high[0] if high[0] else None,
            "low_max_overlap": low[2], "high_min_overlap": high[2], "indel_share": refused_indel / refused if refused > 0 else None}


def _rise(f: dict, limit: int):
    base = f["asv"][0]
    return None if base <= 0 else (f["asv"][limit] - base) / base


def verdicts(res: dict) -> list:
    """res: label -> {'flow': ..., 'overlap': ...}. Returns (id, text, True/False/None) for P68 to P74; None means not decided."""
    nd = lambda why: f"not decided: {why}"
    out = []
    s2 = res.get("its2")
    if not s2 or not s2["flow"]:
        out += [(p, nd("the second ITS study was not run"), None) for p in ("P68", "P69", "P70")]
    else:
        rec = s2["flow"]["recovered"].get(2)
        out.append(("P68", f"On the second ITS study, allowing 2 mismatches merges at least {NEAR_MISS_SHARE:.0%} of the pairs that the default refuses for mismatches or indels: "
                           + ("no pair was refused for them" if rec is None else f"{rec:.1%}"), None if rec is None else rec >= NEAR_MISS_SHARE))
        o = s2["overlap"]
        if not o or o.get("low_share") is None or o.get("high_share") is None:
            out += [("P69", nd("no overlap data"), None), ("P70", nd("no overlap data"), None)]
        else:
            gap = (o["high_share"] - o["low_share"]) * 100
            out.append(("P69", f"On the second ITS study, the share of pairs refused for mismatches or indels is at least {LENGTH_POINTS:g} points higher in the longest third of the overlaps "
                               f"(from {o['high_min_overlap']} nt) than in the shortest third (up to {o['low_max_overlap']} nt): {o['high_share']:.1%} against {o['low_share']:.1%} ({gap:+.1f} points)",
                        gap >= LENGTH_POINTS))
            out.append(("P70", f"On the second ITS study, at least {INDEL_SHARE:.0%} of the pairs refused for mismatches or indels have an indel: "
                               + ("none were refused" if o["indel_share"] is None else f"{o['indel_share']:.1%}"), None if o["indel_share"] is None else o["indel_share"] >= INDEL_SHARE))
    s1 = res.get("its")
    a, b = (s2 or {}).get("overlap"), (s1 or {}).get("overlap")
    if not a or not b or a.get("median_overlap") is None or b.get("median_overlap") is None:
        out.append(("P71", nd("both ITS studies are needed"), None))
    else:
        out.append(("P71", f"The median overlap of the pairs that enter the merge step is longer on the second ITS study than on the first: {a['median_overlap']} nt against {b['median_overlap']} nt",
                    a["median_overlap"] > b["median_overlap"]))
    rises = {name: _rise(r["flow"], 2) for name, r in (("second ITS study", s2), ("first ITS study", s1)) if r and r["flow"]}
    if len(rises) < 2 or any(v is None for v in rises.values()):
        out.append(("P72", nd("both ITS studies are needed, each with ASVs at the default"), None))
    else:
        out.append(("P72", f"Allowing 2 mismatches raises the median number of ASVs per sample by at most {ASV_RISE:.0%} on both ITS studies: "
                           + ", ".join(f"{n} {v:+.1%}" for n, v in rises.items()), all(v <= ASV_RISE for v in rises.values())))
    v4 = res.get("v4")
    if not v4 or not v4["flow"]:
        out.append(("P73", nd("soil V4 was not run"), None))
    else:
        share = v4.get("partners")
        out.append(("P73", f"On soil V4 at AmpliTrim's cut, at least {PARTNERS:.0%} of the pairs that mergePairs refuses have a forward and a reverse sequence that each occur in an "
                           "accepted pair of the same sample (the halves are good, the pairing is not): " + ("no pair was refused" if share is None else f"{share:.1%}"),
                    None if share is None else share >= PARTNERS))
    iso = {lab: r for lab, r in res.items() if lab in ISOLATES and r["flow"]}                # the mixes (arfken_mix_*) are not isolates
    if not iso:
        out.append(("P74", nd("the single-isolate libraries were not run"), None))
    else:
        adds = {lab: r["flow"]["asv"][2] - r["flow"]["asv"][0] for lab, r in iso.items()}
        out.append(("P74", f"On the single-isolate libraries, allowing 2 mismatches adds at most {ISOLATE_RISE} ASV per sample (median): "
                           + ", ".join(f"{lab} {v:+g}" for lab, v in adds.items()), all(v <= ISOLATE_RISE for v in adds.values())))
    if not s2 or not s2["flow"]:
        out.append(("P75", nd("the second ITS study was not run"), None))
    else:
        share = s2.get("partners")
        out.append(("P75", f"On the second ITS study, at least {PARTNERS:.0%} of the pairs that mergePairs refuses have a forward and a reverse sequence that each occur in an accepted "
                           "pair of the same sample: " + ("no pair was refused" if share is None else f"{share:.1%}"), None if share is None else share >= PARTNERS))
    return out


def report_lines(res: dict, reads_used: dict, limits=LIMITS) -> list:
    L = ["# ITS follow-up", "", "The criteria (P68 to P75) are in TEST_REGISTER.md and were fixed before this ran.", "", "## Verdicts", ""]
    for p, txt, ok in verdicts(res):
        L.append(f"- **{p}** {txt}" if ok is None else f"- **{p}** {'MET' if ok else 'NOT MET'}: {txt}")      # the text of an undecided criterion already says so
    for label, r in res.items():
        f, o = r["flow"], r["overlap"]
        if not f:
            L += ["", f"## {label}", "", "No pairs were given to DADA2."]
            continue
        L += ["", f"## {label} ({f['samples']} samples, {f['input']:,.0f} input pairs; {reads_used.get(label, '')})", ""]
        L += ["| step | share of the input pairs |", "|---|---|", f"| pass the filter | {f['filtered']:.2%} |", f"| enter the merge step | {f['reach']:.2%} |",
              f"| refused: overlap shorter than {MIN_OVERLAP} nt | {f['rej_short']:.2%} |", f"| refused: mismatches or indels in the overlap | {f['rej_mismatch']:.2%} |",
              f"| refused: a clean overlap that is still refused | {f['rej_other']:.2%} |", "", "| mismatches allowed | merged (share of the input pairs) | of the default's mismatch refusals | of all the default's refused pairs | median ASVs per sample |", "|---|---|---|---|---|"]
        for k in limits:
            rec = "" if k == 0 else ("" if f["recovered"][k] is None else f"{f['recovered'][k]:.1%}")
            rec_all = "" if k == 0 else ("" if f["recovered_all"][k] is None else f"{f['recovered_all'][k]:.1%}")
            L.append(f"| {k}{' (default)' if k == 0 else ''} | {f['merged'][k]:.2%} | {rec} | {rec_all} | {f['asv'][k]:g} |")
        extra = []
        if r.get("partners") is not None:
            extra.append(f"- Of the pairs refused for any reason, {r['partners']:.1%} have a forward and a reverse sequence that each occur in an accepted pair of the same sample.")
        if r.get("alignment"):
            extra.append(f"- Of the pairs refused for any reason, {r['alignment']['zero_share']:.1%} have no overlap at all in the alignment (0 columns).")
        L += [""] + extra if extra else []
        if o and o.get("median_overlap") is not None:
            pct = lambda v: "none" if v is None else f"{v:.1%}"
            L += ["", f"- Median overlap of the pairs that enter the merge step: {o['median_overlap']} nt (shortest third up to {o['low_max_overlap']} nt, longest third from {o['high_min_overlap']} nt).",
                  f"- Refused for mismatches or indels: {pct(o.get('low_share'))} in the shortest third, {pct(o.get('high_share'))} in the longest.",
                  f"- Of the pairs refused for mismatches or indels, {pct(o.get('indel_share'))} have an indel."]
    return L + ["", "Next: send this file."]


def parse_pairs(items, what: str) -> dict:
    out = {}
    for item in items or []:
        label, sep, value = item.partition("=")
        if not sep or not label or not value:
            raise SystemExit(f"{what} wants LABEL=VALUE, not {item!r}")
        out[label] = value
    return out


def main(argv=None, run=subprocess.run, find_rscript=None, thin=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dataset", action="append", metavar="LABEL=FOLDER", help="a folder of paired FASTQs; repeat for each dataset")
    ap.add_argument("--trunc", action="append", metavar="LABEL=F,R", help="truncLen for a dataset (default: none, as for ITS)")
    ap.add_argument("--pairs", type=int, default=DEFAULT_PAIRS, help=f"pairs per sample given to DADA2 (default {DEFAULT_PAIRS}; 0 for all)")
    ap.add_argument("--out", type=Path, default=Path("its_followup_out"))
    a = ap.parse_args(argv)
    datasets, trunc = parse_pairs(a.dataset, "--dataset"), parse_pairs(a.trunc, "--trunc")
    if not datasets:
        print("Give at least one --dataset LABEL=FOLDER.")
        return 2
    cuts = {}
    for label, value in trunc.items():
        try:
            f, r = (int(x) for x in value.split(","))
        except ValueError:
            raise SystemExit(f"--trunc wants LABEL=F,R with two whole numbers, not {label}={value}")
        cuts[label] = (f, r)
    unknown = [lab for lab in cuts if lab not in datasets]
    if unknown:
        raise SystemExit(f"--trunc names a dataset that is not given: {unknown}")
    import os
    try:
        import rtools                                    # the archive's own helper; absent when this file is tried outside the archive
    except ImportError:
        rtools = None
    if find_rscript is None and rtools is not None:
        find_rscript = rtools.find_rscript
    rscript = find_rscript() if find_rscript else None
    if not rscript:
        print(rtools.NOT_FOUND if rtools is not None else "R with the DADA2 package was not found.")
        return 2
    if thin is None:
        from real_data import thin_reads as thin
    a.out.mkdir(parents=True, exist_ok=True)
    res, used = {}, {}
    for label, folder in datasets.items():
        folder = Path(os.path.expandvars(folder))
        if not folder.is_dir():
            print(f"{label}: the folder {folder} was not found.")
            return 2
        reads = thin(folder, a.out / f"{label}_reads", a.pairs) if a.pairs else folder
        tf, tr = cuts.get(label, (0, 0))
        samples, pairs, seqs = a.out / f"{label}_samples.tsv", a.out / f"{label}_pairs.tsv", a.out / f"{label}_seqs.tsv"
        p = run([rscript, str(R_SCRIPT), str(reads), str(MIN_LEN), f"{MAX_EE:g}", str(MIN_OVERLAP), str(tf), str(tr), ",".join(str(k) for k in LIMITS), str(samples), str(pairs), str(seqs)],
                capture_output=True, text=True)
        if p.returncode != 0 or not samples.is_file() or not pairs.is_file() or not seqs.is_file():
            print(f"{label}: DADA2 could not run: {(p.stderr or '').strip()[-500:]}")
            return 2
        pair_rows = read_pairs(pairs)
        res[label] = {"flow": flow(read_samples(samples)), "overlap": overlap_profile(pair_rows), "partners": partner_share(read_partners(pairs)), "alignment": refused_alignment(pair_rows)}
        used[label] = f"truncLen {tf},{tr}" if (tf or tr) else "no truncation"
    L = report_lines(res, used)
    (a.out / "ITS_FOLLOWUP_REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:next((i for i, x in enumerate(L) if x.startswith("## ") and x != "## Verdicts"), len(L))]))      # the heading and every verdict
    print(f"\nwritten: {a.out / 'ITS_FOLLOWUP_REPORT.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
