"""The truth test for long reads: which settings recover the variants that a mock community is known to hold, and which invent others?

For each library type (for example Monomer and Kinnex) the reads are cut between the primers (cutadapt, insertions and deletions allowed, orientation corrected). For each condition
DADA2 then runs on the trimmed files (a filter with only maxEE and a length window of 0.9 to 1.1 times the median rounded to 10 nt, no truncation; the PacBio error model with band
size 32; pseudo-pooling; chimeras flagged by removeBimeraDenovo). These DADA2 settings are from memory and are not checked against PacBio's own. Each ASV is classed against the
expected variants of genome_amplicons.py: exact (equal to one), near (not exact, within 2 edits of one), chimeric (flagged) or other.

Conditions: maxEE 1, 2, 3, 5 and 10 and the value that the package's percentile rule gives on these reads (max(2, int(75th percentile of the expected errors) + 1)), all with the window and
cutadapt's primer removal; and two extra conditions at maxEE 2: no window ("ee2_nowindow"), and DADA2's own removePrimers instead of cutadapt ("ee2_dada2primers").

Gates (written in FUTURE.md on 15 October 2026, before the first run), for each library type, at maxEE 2 with the window and cutadapt:
  T2  recall: at least 14 of the 15 strains of the three highest tiers (a genomic share of 0.18% or more) have at least one exact expected variant among the final ASVs, and at least 80% of the
      expected variants with an expected read share of 1% or more are recovered exactly;
  T3  extra variants: at most 2% of the final reads are in 'other' ASVs;
  T5  abundance, qualitative: the Spearman correlation between the expected and the observed read share, across the strains with a complete genome of tier A, is at least 0.7;
  T6  the rule: the maxEE that the rule gives recovers at least as many exact variants as maxEE 2 and has an 'other' read share not more than 0.5 points above that of maxEE 2.
Reported without a gate: the whole grid (T7), the effect of the window and of the primer removal (T8), the chimeras (T4), and the library types against each other.

Night 9 (the Revio hold-out; gates in FUTURE.md) adds: the error model chosen from the quality scores of the reads (PacBioErrfun with the score 93, makeBinnedQualErrfun for binned scores),
scoring against a refined reference (--refined, with the class 'added' for the variants that the refinement rule added) and against a replication set (--replicate-set), the gates in judge_refined,
and the extra condition ee2_naive (PacBioErrfun on binned reads).

    python validation\\longread_truth.py --expected ...\\expected_amplicons.fasta --strains-table ...\\genome_amplicons.tsv --library Monomer=C:\\...\\l4_monomer --library Kinnex=C:\\...\\sq2_kinnex_fastq
        --primer-f AGRGTTYGATYMTGGCTCAG --primer-r RGYTACCTTGTTACGACTT --out C:\\data\\runs\\18_night8\\truth [--reads N] [--max-files N] [--only ee2] [--threads 1]

Writes truth_conditions.tsv, truth_strains.tsv, one truth_asvs_<library>_<condition>.tsv each and TRUTH.md. Needs numpy, cutadapt, rapidfuzz, and R with DADA2.
"""

import argparse
import csv
import math
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import longread_common as lc  # noqa: E402
import longread_filter_check as lf  # noqa: E402
from longread_describe import find_files, sample_name  # noqa: E402
from rtools import NOT_FOUND, find_rscript  # noqa: E402

TRUTH_R = HERE / "truth_dada2.R"
DEFAULT_GRID = (1, 2, 3, 5, 10)
NEAR = 2
TOP_SHARE = 0.18                                  # genomic share (%) from which a strain belongs to the three highest tiers
BIG_VARIANT = 1.0                                 # expected read share (%) from which a variant counts in T2 (b)
THRESHOLDS = {"top_strains": 14, "big_fraction": 0.8, "other_max": 0.02, "rho_min": 0.7, "rule_slack": 0.005}
# the gates of Night 9, scored against the refined reference (registered in FUTURE.md on 15 October 2026)
THRESHOLDS_REFINED = {"top_strains": 14, "replicate_fraction": 0.9, "unexplained_max": 0.02, "rho_min": 0.7, "rule_slack": 0.005}
MAX_BINNED_VALUES = 12                            # at most this many distinct quality scores count as binned


def run_r(args: list) -> None:
    rscript = find_rscript()
    if not rscript:
        raise SystemExit(NOT_FOUND)
    res = subprocess.run([rscript, str(TRUTH_R), *[str(a) for a in args]], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError("The DADA2 run failed: " + (res.stderr or res.stdout).strip()[-1200:])


def run_dada2(files: list, prefix, max_ee: float, min_len: int, max_len, band: int, pool: str, threads: int, primers=None, errfun: str = "PacBioErrfun") -> dict:
    """One DADA2 run: {'asv': path, 'filter': path} of the two tables that truth_dada2.R writes."""
    prefix = Path(prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    listing = Path(f"{prefix}_files.txt")
    listing.write_text("\n".join(str(Path(f)) for f in files) + "\n")
    args = [listing, prefix, f"{max_ee:g}", min_len, ("Inf" if not max_len else max_len), band, pool, threads, errfun]
    if primers:
        args += list(primers)
    run_r(args)
    return {"asv": Path(f"{prefix}_asv.tsv"), "filter": Path(f"{prefix}_filter.tsv")}


def read_asv(path) -> list:
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        rdr = csv.reader(fh, delimiter="\t")
        header = next(rdr)
        for r in rdr:
            counts = [int(float(x)) for x in r[2:]]
            rows.append({"sequence": r[0], "chimera": r[1].strip().upper() == "TRUE", "reads": sum(counts), "counts": dict(zip(header[2:], counts))})
    return rows


def read_filter(path) -> tuple:
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    return sum(int(float(r["reads_in"])) for r in rows), sum(int(float(r["reads_out"])) for r in rows)


def choose_errfun(max_q, values: list) -> str:
    """PacBioErrfun when the score 93 is present; the binned model for a handful of distinct scores (Revio); otherwise PacBioErrfun, which then falls back to standard fitting."""
    if max_q is not None and max_q >= 93:
        return "PacBioErrfun"
    if values and len(values) <= MAX_BINNED_VALUES:
        return "binned:" + ",".join(str(v) for v in values if v > 0)
    return "PacBioErrfun"


def prepare_library(name: str, folder: Path, work: Path, primer_f: str, primer_r: str, reads: int, max_files: int, error_rate: float, log=print, errfun: str = None) -> dict:
    """The raw and the trimmed files of a library type, with the expected errors and lengths of its trimmed reads, the value of the percentile rule and the window."""
    files = lc.pick_evenly(find_files(Path(folder)), max_files)
    if not files:
        raise SystemExit(f"No FASTQ files in {folder} (library {name})")
    raw_dir, trim_dir = work / name / "raw", work / name / "trimmed"
    raw, trimmed, ee, lengths, chars = [], [], [], [], set()
    for p in files:
        s = sample_name(p)
        r = lf.subset(p, reads, raw_dir / f"{s}.fastq.gz")
        t = trim_dir / f"{s}.fastq.gz"
        trim_dir.mkdir(parents=True, exist_ok=True)
        lf.run_cutadapt(r, t, primer_f, primer_r, error_rate, True)
        n = 0
        for _, seq, qual in lc.iter_fastq(t):
            ee.append(lc.expected_errors(qual))
            lengths.append(len(seq))
            chars.update(qual)
            n += 1
        raw.append(r)
        trimmed.append(t)
        log(f"{name} {s}: {lf.count_reads(r):,} reads, {n:,} cut between the primers")
    if not ee:
        raise SystemExit(f"No read of library {name} has both primers.")
    ee, lengths = np.array(ee), np.array(lengths)
    median = float(np.median(lengths))
    values = sorted(ord(ch) - 33 for ch in chars)
    return {"name": name, "max_q": max(values), "quality_values": values, "errfun": errfun or choose_errfun(max(values), values), "raw": raw, "trimmed": trimmed, "reads": int(len(ee)), "median_length": median,
            "window": (int(math.floor(0.9 * median / 10) * 10), int(math.ceil(1.1 * median / 10) * 10)),
            "p75": float(np.percentile(ee, 75)), "rule": max(2, int(np.percentile(ee, 75)) + 1)}


def build_conditions(grid, rule: int, extras=("nowindow", "dada2primers"), binned: bool = False) -> list:
    """The grid of maxEE values with the value of the rule, then the extra conditions at maxEE 2: no window, DADA2's own primer removal, and (only for binned scores) PacBioErrfun, DADA2's fallback."""
    values = sorted({float(g) for g in grid} | {float(rule)})
    conds = [{"tag": f"ee{v:g}", "max_ee": v, "window": True, "primers": "cutadapt", "errfun": "auto"} for v in values]
    if "nowindow" in extras:
        conds.append({"tag": "ee2_nowindow", "max_ee": 2.0, "window": False, "primers": "cutadapt", "errfun": "auto"})
    if "dada2primers" in extras:
        conds.append({"tag": "ee2_dada2primers", "max_ee": 2.0, "window": True, "primers": "dada2", "errfun": "auto"})
    if "naive" in extras and binned:
        conds.append({"tag": "ee2_naive", "max_ee": 2.0, "window": True, "primers": "cutadapt", "errfun": "naive"})
    return conds


def read_strains(path) -> dict:
    """{strain: {'share': genomic share %, 'expected': expected read share %, 'tier': tier, 'eligible': tier A and not a draft}} from genome_amplicons.tsv."""
    out = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            tier = r.get("tier", "") or ""
            out[r["strain"]] = {"share": float(r["share_genomic_percent"]) if r.get("share_genomic_percent") not in (None, "") else 0.0,
                                "expected": float(r["expected_read_share_percent"]) if r.get("expected_read_share_percent") not in (None, "") else 0.0,
                                "tier": tier, "eligible": tier.strip().upper().startswith("A") and "draft" not in tier.lower()}
    return out


def variant_shares(names: list, strains: dict) -> dict:
    """{variant: expected read share %}: the share of its strain times its copies, as a share of the copies of the strain."""
    def n_copies(name: str) -> int:
        try:
            return int(name.split("|")[2].split("_")[0])
        except (IndexError, ValueError):                 # a header without STRAIN_vN|STRAIN|N_copies: one copy
            return 1
    copies = {n: n_copies(n) for n in names}
    total = {}
    for n in names:
        total[lc.strain_of(n)] = total.get(lc.strain_of(n), 0) + copies[n]
    return {n: strains.get(lc.strain_of(n), {}).get("expected", 0.0) * copies[n] / total[lc.strain_of(n)] for n in names}


def classify(asvs: list, names: list, seqs: list, near: int = NEAR, cap: int = 100) -> list:
    """Each ASV with its match (exact, added, near or other), the nearest variant and its true distance (cap + 1 stands for 'more than cap').
    The distance is searched up to `cap`, not only up to `near`: with a cut-off at `near` every distance beyond it is the same number, and the 'nearest' variant of an 'other' ASV is then the first one of the file."""
    exact = {s: i for i, s in enumerate(seqs)}
    out, pending = [], []
    for a in asvs:
        i = exact.get(a["sequence"])
        if i is not None:
            fields = names[i].split("|")
            added = len(fields) > 2 and fields[2].startswith("0_")        # a variant added by the refinement rule carries no copies
            out.append(dict(a, match="added" if added else "exact", variant=names[i], distance=0))
        else:
            pending.append(a)
    if pending:
        dist, idx = lc.nearest([a["sequence"] for a in pending], seqs, max(cap, near))
        for a, d, j in zip(pending, dist, idx):
            out.append(dict(a, match="near" if d <= near else "other", variant=names[j], distance=int(d)))
    return out


def metrics(classified: list, names: list, strains: dict, vshare: dict, replicate=None) -> dict:
    final = [a for a in classified if not a["chimera"]]
    flagged = [a for a in classified if a["chimera"]]
    reads_final = sum(a["reads"] for a in final)
    reads_all = sum(a["reads"] for a in classified)
    exact_variants = {a["variant"] for a in final if a["match"] in ("exact", "added")}
    found = {lc.strain_of(v) for v in exact_variants}
    top = [s for s, i in strains.items() if i["share"] >= TOP_SHARE]
    big = [v for v, sh in vshare.items() if sh >= BIG_VARIANT]
    obs = {}
    for a in final:
        if a["match"] in ("exact", "added", "near"):
            obs[lc.strain_of(a["variant"])] = obs.get(lc.strain_of(a["variant"]), 0) + a["reads"]
    share = {s: (obs.get(s, 0) / reads_final if reads_final else 0.0) for s in strains}
    eligible = [s for s, i in strains.items() if i["eligible"]]
    rho = lc.spearman([strains[s]["expected"] for s in eligible], [share[s] for s in eligible]) if eligible else None
    by = lambda m: sum(a["reads"] for a in final if a["match"] == m)
    return {"asvs_final": len(final), "asvs_exact": sum(a["match"] == "exact" for a in final), "asvs_near": sum(a["match"] == "near" for a in final), "asvs_other": sum(a["match"] == "other" for a in final),
            "asvs_chimeric": len(flagged), "asvs_added": sum(a["match"] == "added" for a in final), "reads_added": by("added"),
            "unexplained_share": ((by("near") + by("other")) / reads_final if reads_final else None),
            "replicate_total": len(replicate) if replicate else 0, "replicated": len(set(replicate) & exact_variants) if replicate else 0, "reads_final": reads_final, "reads_exact": by("exact"), "reads_near": by("near"), "reads_other": by("other"),
            "other_share": (by("other") / reads_final if reads_final else None), "chimera_share": (sum(a["reads"] for a in flagged) / reads_all if reads_all else None),
            "exact_flagged": len({a["variant"] for a in flagged if a["match"] == "exact"}), "variants_recovered": len(exact_variants), "variants_total": len(names),
            "top_total": len(top), "top_recovered": sum(1 for s in top if s in found), "big_total": len(big), "big_recovered": sum(1 for v in big if v in exact_variants),
            "rho": rho, "rho_strains": len(eligible), "strain_share": share, "strain_variants": {s: sum(1 for v in exact_variants if lc.strain_of(v) == s) for s in strains}}


def judge(by_lib: dict, rules: dict, th: dict = None) -> dict:
    """{library: {gate: (status, note)}} for T2, T3, T5 and T6, from by_lib[library][tag] = metrics and rules[library] = the value of the percentile rule."""
    th = th or THRESHOLDS
    out = {}
    for lib, conds in by_lib.items():
        g, std = {}, conds.get("ee2")
        if std is None:
            g = {k: ("NOT DECIDED", "the condition ee2 was not run") for k in ("T2", "T3", "T5", "T6")}
        else:
            a_ok = std["top_recovered"] >= th["top_strains"]
            b_ok = std["big_total"] > 0 and std["big_recovered"] >= th["big_fraction"] * std["big_total"]
            note = (f"{std['top_recovered']} of {std['top_total']} strains of the three highest tiers have an exact variant (needed: {th['top_strains']}); "
                    f"{std['big_recovered']} of {std['big_total']} expected variants of 1% or more recovered exactly (needed: {100 * th['big_fraction']:.0f}%)")
            g["T2"] = ("MET" if (a_ok and b_ok) else "NOT MET", note) if (std["top_total"] or std["big_total"]) else ("NOT DECIDED", "no strain or variant to judge")
            o = std["other_share"]
            g["T3"] = ("NOT DECIDED", "no final reads") if o is None else (("MET" if o <= th["other_max"] else "NOT MET"), f"{100 * o:.2f}% of the final reads are in 'other' ASVs (at most {100 * th['other_max']:.0f}%)")
            rho = std["rho"]
            g["T5"] = ("NOT DECIDED", "the correlation cannot be computed") if rho is None else (("MET" if rho >= th["rho_min"] else "NOT MET"), f"Spearman {rho:.2f} over {std['rho_strains']} strains (at least {th['rho_min']})")
            rule = rules.get(lib)
            if rule == 2:
                g["T6"] = ("MET", "the rule gives maxEE 2, the same condition as the standard")
            elif rule is None or f"ee{rule:g}" not in conds:
                g["T6"] = ("NOT DECIDED", "the condition of the rule was not run")
            else:
                r = conds[f"ee{rule:g}"]
                more = r["variants_recovered"] >= std["variants_recovered"]
                slack = (r["other_share"] is not None and std["other_share"] is not None and r["other_share"] <= std["other_share"] + th["rule_slack"])
                g["T6"] = ("MET" if (more and slack) else "NOT MET", f"the rule gives maxEE {rule}: {r['variants_recovered']} exact variants against {std['variants_recovered']} at maxEE 2; "
                           f"'other' share {100 * (r['other_share'] or 0):.2f}% against {100 * (std['other_share'] or 0):.2f}% (at most 0.5 points more)")
        out[lib] = g
    return out


def judge_refined(by_lib: dict, rules: dict, th: dict = None) -> dict:
    """The gates of Night 9, scored against the refined reference: T2 (a: strains with an exact or added ASV; b: the replication set), T3 (unexplained reads), T5 and T6."""
    th = th or THRESHOLDS_REFINED
    out = {}
    for lib, conds in by_lib.items():
        g, std = {}, conds.get("ee2")
        if std is None:
            g = {k: ("NOT DECIDED", "the condition ee2 was not run") for k in ("T2", "T3", "T5", "T6")}
        else:
            tot = std["replicate_total"]
            a_ok = std["top_recovered"] >= th["top_strains"]
            b_ok = tot > 0 and std["replicated"] >= th["replicate_fraction"] * tot
            note = (f"{std['top_recovered']} of {std['top_total']} strains of the three highest tiers have an exact or an added ASV (needed: {th['top_strains']}); "
                    f"{std['replicated']} of {tot} sequences of the replication set recovered (needed: {100 * th['replicate_fraction']:.0f}%)")
            g["T2"] = ("MET" if (a_ok and b_ok) else "NOT MET", note) if (std["top_total"] or tot) else ("NOT DECIDED", "no strain or sequence to judge")
            u = std["unexplained_share"]
            g["T3"] = (("NOT DECIDED", "no final reads") if u is None else
                       (("MET" if u <= th["unexplained_max"] else "NOT MET"), f"{100 * u:.2f}% of the final reads are in ASVs that are neither exact nor added (at most {100 * th['unexplained_max']:.0f}%)"))
            rho = std["rho"]
            g["T5"] = (("NOT DECIDED", "the correlation cannot be computed") if rho is None else
                       (("MET" if rho >= th["rho_min"] else "NOT MET"), f"Spearman {rho:.2f} over {std['rho_strains']} strains (at least {th['rho_min']})"))
            rule = rules.get(lib)
            if rule == 2:
                g["T6"] = ("MET", "the rule gives maxEE 2, the same condition as the standard")
            elif rule is None or f"ee{rule:g}" not in conds:
                g["T6"] = ("NOT DECIDED", "the condition of the rule was not run")
            else:
                r = conds[f"ee{rule:g}"]
                more = r["variants_recovered"] >= std["variants_recovered"]
                slack = (r["unexplained_share"] is not None and std["unexplained_share"] is not None and r["unexplained_share"] <= std["unexplained_share"] + th["rule_slack"])
                g["T6"] = ("MET" if (more and slack) else "NOT MET", f"the rule gives maxEE {rule}: {r['variants_recovered']} exact or added sequences against {std['variants_recovered']} at maxEE 2; "
                           f"unexplained share {100 * (r['unexplained_share'] or 0):.2f}% against {100 * (std['unexplained_share'] or 0):.2f}% (at most 0.5 points more)")
        out[lib] = g
    return out


def read_names(path) -> list:
    """One variant name per line (lines starting with # are ignored)."""
    return [ln.strip() for ln in open(path, encoding="utf-8") if ln.strip() and not ln.startswith("#")]


def fmt(x, digits: int = 2, pct: bool = False) -> str:
    return "-" if x is None else (f"{100 * x:.{digits}f}" if pct else f"{x:.{digits}f}")


def run(libraries: dict, expected_fasta, strains_table, primer_f: str, primer_r: str, out: Path, reads: int = 0, max_files: int = 0, grid=DEFAULT_GRID, band: int = 32, pool: str = "pseudo",
        threads: int = 0, error_rate: float = 0.15, only=None, keep: bool = False, thresholds: dict = None, log=print,
        refined_fasta=None, replicate_file=None, extras=("nowindow", "dada2primers"), errfun: str = None) -> dict:
    """With refined_fasta the ASVs are scored against it (the gates are those of Night 9) and, without a gate, against the original expected_fasta."""
    original = lc.read_fasta(expected_fasta)
    if not original:
        raise SystemExit(f"No expected variants in {expected_fasta}")
    oname, oseq = [n for n, _ in original], [s for _, s in original]
    variants = lc.read_fasta(refined_fasta) if refined_fasta else original
    if not variants:
        raise SystemExit(f"No variants in {refined_fasta}")
    names, seqs = [n for n, _ in variants], [s for _, s in variants]
    strains = read_strains(strains_table)
    vshare, ovshare = variant_shares(names, strains), variant_shares(oname, strains)
    replicate = read_names(replicate_file) if replicate_file else None
    work = out / "work"
    out.mkdir(parents=True, exist_ok=True)
    by_lib, rules, rows, strain_rows, libs = {}, {}, [], [], {}
    for lib, folder in libraries.items():
        info = prepare_library(lib, folder, work, primer_f, primer_r, reads, max_files, error_rate, log, errfun)
        libs[lib] = info
        rules[lib] = info["rule"]
        log(f"{lib}: {info['reads']:,} reads between the primers, median length {info['median_length']:.0f}, window {info['window'][0]} to {info['window'][1]}, "
            f"75th percentile of the expected errors {info['p75']:.2f}, so the rule gives maxEE {info['rule']}; highest quality score {info['max_q']}, "
            f"{len(info['quality_values'])} distinct values, error model {info['errfun']}")
        by_lib[lib] = {}
        for cond in build_conditions(grid, info["rule"], extras, binned=info["errfun"].startswith("binned")):
            if only and cond["tag"] not in only:
                continue
            t0 = time.time()
            files = info["trimmed"] if cond["primers"] == "cutadapt" else info["raw"]
            lo, hi = info["window"] if cond["window"] else (0, 0)
            used = info["errfun"] if cond.get("errfun", "auto") == "auto" else "PacBioErrfun"
            res = run_dada2(files, work / lib / cond["tag"], cond["max_ee"], lo, hi, band, pool, threads, (primer_f, primer_r) if cond["primers"] == "dada2" else None, used)
            seconds = time.time() - t0
            n_in, n_out = read_filter(res["filter"])
            asvs = read_asv(res["asv"])
            classified = classify(asvs, names, seqs)
            m = metrics(classified, names, strains, vshare, replicate)
            if refined_fasta:
                m["original"] = metrics(classify(asvs, oname, oseq), oname, strains, ovshare)
            m.update(reads_in=n_in, reads_out=n_out, seconds=seconds, errfun=used)
            by_lib[lib][cond["tag"]] = m
            rows.append((lib, cond, m))
            for s, i in strains.items():
                strain_rows.append((lib, cond["tag"], s, i["expected"], 100 * m["strain_share"][s], sum(1 for n in names if lc.strain_of(n) == s), m["strain_variants"][s]))
            write_asvs(out / f"truth_asvs_{lib}_{cond['tag']}.tsv", classified)
            log(f"{lib} {cond['tag']}: {n_out:,} of {n_in:,} reads kept, {m['asvs_final']} final ASVs ({m['asvs_exact']} exact, {m['asvs_added']} added, {m['asvs_near']} near, {m['asvs_other']} other), "
                f"{m['variants_recovered']} of {m['variants_total']} reference variants recovered, {seconds / 60:.1f} min")
    gates = judge_refined(by_lib, rules, thresholds) if refined_fasta else judge(by_lib, rules, thresholds)
    write_tables(rows, strain_rows, out)
    write_report(libs, rows, gates, out, primer_f, primer_r, reads, band, pool, bool(refined_fasta))
    if not keep:
        shutil.rmtree(work, ignore_errors=True)
    log(f"Saved: {out / 'TRUTH.md'}")
    for lib, g in gates.items():
        log(f"{lib}: " + ", ".join(f"{k} {s}" for k, (s, _) in g.items()))
    return {"by_lib": by_lib, "gates": gates, "rules": rules, "libraries": libs, "refined": bool(refined_fasta)}


def write_asvs(path: Path, classified: list) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["sequence", "reads", "chimera", "match", "nearest_variant", "distance", "reads_per_sample"])
        for a in sorted(classified, key=lambda a: -a["reads"]):
            w.writerow([a["sequence"], a["reads"], a["chimera"], a["match"], a["variant"], a["distance"], ";".join(f"{s}={n}" for s, n in a["counts"].items() if n)])


def write_tables(rows: list, strain_rows: list, out: Path) -> None:
    with open(out / "truth_conditions.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["library", "condition", "max_ee", "window", "primer_removal", "reads_in", "reads_out", "asvs_final", "asvs_exact", "asvs_near", "asvs_other", "asvs_chimeric", "reads_exact", "reads_near",
                    "reads_other", "other_share", "chimera_share", "exact_variants_flagged_chimeric", "variants_recovered", "variants_total", "top_strains_recovered", "top_strains_total",
                    "big_variants_recovered", "big_variants_total", "spearman", "seconds", "error_model", "asvs_added", "reads_added", "unexplained_share", "replicated", "replicate_total",
                    "original_variants_recovered", "original_variants_total", "original_other_share", "original_top_strains_recovered", "original_big_variants_recovered"])
        for lib, c, m in rows:
            o = m.get("original") or {}
            w.writerow([lib, c["tag"], f"{c['max_ee']:g}", "yes" if c["window"] else "no", c["primers"], m["reads_in"], m["reads_out"], m["asvs_final"], m["asvs_exact"], m["asvs_near"], m["asvs_other"],
                        m["asvs_chimeric"], m["reads_exact"], m["reads_near"], m["reads_other"], m["other_share"], m["chimera_share"], m["exact_flagged"], m["variants_recovered"], m["variants_total"],
                        m["top_recovered"], m["top_total"], m["big_recovered"], m["big_total"], m["rho"], round(m["seconds"], 1), m.get("errfun", ""), m["asvs_added"], m["reads_added"], m["unexplained_share"],
                        m["replicated"], m["replicate_total"], o.get("variants_recovered", ""), o.get("variants_total", ""), o.get("other_share", ""), o.get("top_recovered", ""), o.get("big_recovered", "")])
    with open(out / "truth_strains.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["library", "condition", "strain", "expected_read_share_percent", "observed_read_share_percent", "variants_expected", "variants_recovered"])
        w.writerows(strain_rows)


def write_report(libs: dict, rows: list, gates: dict, out: Path, primer_f: str, primer_r: str, reads: int, band: int, pool: str, refined: bool = False) -> None:
    lines = ["# Truth test: DADA2 on long reads against the known variants of a mock community", "",
             f"Primers {primer_f} and {primer_r}; " + (f"the first {reads:,} reads of each file" if reads else "all reads") + f"; DADA2 with the error model named for each library below, band size {band}, pool = {pool}; "
             "an ASV is exact when it equals an expected variant, " + ("added when it equals a variant added by the refinement rule, " if refined else "") +
             "near when it is within 2 edits of one, chimeric when DADA2 flags it, other otherwise." + (" The reference is the refined set; the original variants are scored in a second table, without a gate." if refined else ""), ""]
    for lib, g in gates.items():
        info = libs[lib]
        vals = info["quality_values"]
        lines += [f"## {lib}", "", f"{info['reads']:,} reads between the primers; median length {info['median_length']:.0f} nt, window {info['window'][0]} to {info['window'][1]} nt; the 75th percentile of the expected errors is "
                  f"{info['p75']:.2f}, so the package's rule gives **maxEE {info['rule']}**.", "",
                  f"Quality scores: highest {info['max_q']}, {len(vals)} distinct values" + (f" ({', '.join(str(v) for v in vals)})" if len(vals) <= MAX_BINNED_VALUES else "") + f"; error model: **{info['errfun']}**."
                  + (" The score 93 is absent, so PacBioErrfun falls back to standard fitting." if info["errfun"] == "PacBioErrfun" and info["max_q"] < 93 else ""), ""]
        for k, (status, note) in g.items():
            lines.append(f"**Gate ({k}): {status}.** {note}.")
        lines += ["", "| condition | maxEE | window | primers | error model | reads kept % | final ASVs | exact | added | near | other | chimeric ASVs | exact reads % | unexplained reads % | chimeric reads % | reference variants recovered | top strains | replicated | Spearman | min |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for l, c, m in rows:
            if l != lib:
                continue
            kept = (m["reads_out"] / m["reads_in"]) if m["reads_in"] else None
            ex = (m["reads_exact"] / m["reads_final"]) if m["reads_final"] else None
            rep = f"{m['replicated']} of {m['replicate_total']}" if m["replicate_total"] else "-"
            lines.append(f"| {c['tag']} | {c['max_ee']:g} | {'yes' if c['window'] else 'no'} | {c['primers']} | {m.get('errfun', '')} | {fmt(kept, 1, True)} | {m['asvs_final']} | {m['asvs_exact']} | {m['asvs_added']} | {m['asvs_near']} | "
                         f"{m['asvs_other']} | {m['asvs_chimeric']} | {fmt(ex, 1, True)} | {fmt(m['unexplained_share'], 2, True)} | {fmt(m['chimera_share'], 2, True)} | {m['variants_recovered']} of {m['variants_total']} | "
                         f"{m['top_recovered']} of {m['top_total']} | {rep} | {fmt(m['rho'])} | {m['seconds'] / 60:.1f} |")
        if refined:
            lines += ["", f"Scored against the original variants (no gate):", "", "| condition | variants recovered | 'other' reads % | top strains | big variants |", "|---|---|---|---|---|"]
            for l, c, m in rows:
                o = m.get("original")
                if l == lib and o:
                    lines.append(f"| {c['tag']} | {o['variants_recovered']} of {o['variants_total']} | {fmt(o['other_share'], 2, True)} | {o['top_recovered']} of {o['top_total']} | {o['big_recovered']} of {o['big_total']} |")
        lines.append("")
    lines += ["The tables of every strain and every ASV are in truth_strains.tsv and truth_asvs_*.tsv. 'Top strains' are those with a genomic share of 0.18% or more; 'unexplained' reads are those in ASVs that are neither exact "
              "nor added; 'replicated' counts the sequences of the replication set that were recovered.", ""]
    (out / "TRUTH.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_libraries(items: list) -> dict:
    libs = {}
    for it in items:
        if "=" not in it:
            raise SystemExit(f"--library needs NAME=FOLDER, not {it!r}")
        name, folder = it.split("=", 1)
        libs[name.strip()] = Path(folder.strip())
    return libs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--library", action="append", required=True, metavar="NAME=FOLDER")
    ap.add_argument("--expected", type=Path, required=True, help="expected_amplicons.fasta from genome_amplicons.py")
    ap.add_argument("--strains-table", type=Path, required=True, help="genome_amplicons.tsv from genome_amplicons.py")
    ap.add_argument("--primer-f", required=True)
    ap.add_argument("--primer-r", required=True)
    ap.add_argument("--out", type=Path, default=Path("truth"))
    ap.add_argument("--reads", type=int, default=0, help="the first N reads of each file (default: all)")
    ap.add_argument("--max-files", type=int, default=0, help="at most N files per library, spread evenly (default: all)")
    ap.add_argument("--grid", type=float, nargs="+", default=list(DEFAULT_GRID), help="maxEE values (default 1 2 3 5 10)")
    ap.add_argument("--band-size", type=int, default=32)
    ap.add_argument("--pool", default="pseudo", choices=["pseudo", "TRUE", "FALSE"])
    ap.add_argument("--threads", type=int, default=0, help="DADA2 threads: 1 = one, anything else = all cores (default)")
    ap.add_argument("--only", help="comma-separated conditions to run (for example ee2 for a pilot)")
    ap.add_argument("--error-rate", type=float, default=0.15)
    ap.add_argument("--refined", type=Path, help="the refined reference (msa1003_refined_variants.fasta): scored against it, with the gates of Night 9")
    ap.add_argument("--replicate-set", type=Path, help="the names of the sequences to be found again (msa1003_night8_asv_set.txt)")
    ap.add_argument("--errfun", help="PacBioErrfun or binned:<scores> (default: chosen from the quality scores of the reads)")
    ap.add_argument("--extras", default="nowindow,dada2primers", help="extra conditions at maxEE 2: nowindow, dada2primers, naive (default nowindow,dada2primers)")
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--sampling", choices=["spread", "first"], default="spread", help="which reads --reads keeps: spread evenly over each file (default) or the first N (the setting of the runs up to 15 October 2026)")
    a = ap.parse_args(argv)
    lf.SAMPLING = a.sampling
    lf.check_tools()
    run(parse_libraries(a.library), a.expected, a.strains_table, a.primer_f, a.primer_r, a.out, a.reads, a.max_files, tuple(a.grid), a.band_size, a.pool, a.threads, a.error_rate,
        [t.strip() for t in a.only.split(",")] if a.only else None, a.keep, refined_fasta=a.refined, replicate_file=a.replicate_set,
        extras=tuple(x.strip() for x in a.extras.split(",") if x.strip()), errfun=a.errfun)
    return 0


if __name__ == "__main__":
    sys.exit(main())
