#!/usr/bin/env python
"""Per 100 input pairs, where DADA2 loses pairs at one setting, next to AmpliTrim's two estimates for that setting.
Usage: breakdown_summary.py OUT_PREFIX LABEL:ARM:BREAKDOWN_TSV:SETTINGS_JSON [...]

BREAKDOWN_TSV is written by merge_breakdown.R; SETTINGS_JSON is the settings.json of the dataset (AmpliTrim's est_pass and est_yield per arm).
Refused pairs: 'close overlap' = an overlap of 12 nt or more with 1 to 10% mismatches between the two denoised sequences; 'poor or no overlap' = no overlap
of 12 nt or more with at most 10% mismatches. est_merge_allowance is est_pass minus est_yield, the pairs AmpliTrim already expects not to merge.
Writes OUT_PREFIX.tsv and OUT_PREFIX.md."""
import json, sys
import pandas as pd

rows = []
for spec in sys.argv[2:]:
    label, arm, tsv, settings = spec.split(":")
    t = pd.read_csv(tsv, sep="\t")
    s = t[["input", "passed_filter", "paired_after_denoise", "merged", "refused_short_overlap", "refused_mismatch", "refused_other",
           "refused_with_1mismatch", "refused_with_2to3"]].sum()
    st = json.load(open(settings))[arm]
    per = lambda x: round(100 * x / s["input"], 1)
    refused = s["paired_after_denoise"] - s["merged"]
    rows.append({
        "dataset": label, "arm": arm, "cut": f"{st['truncF']}/{st['truncR']}", "maxEE": ",".join(f"{x:g}" for x in st["maxEE"]), "samples": len(t),
        "est_pass": round(100 * st["est_pass"], 1), "est_yield": round(100 * st["est_yield"], 1),
        "fail_filter": per(s["input"] - s["passed_filter"]), "lost_denoising": per(s["passed_filter"] - s["paired_after_denoise"]),
        "refused_at_merge": per(refused), "refused_close_overlap": per(s["refused_mismatch"]), "of_which_1_mismatch": per(s["refused_with_1mismatch"]),
        "of_which_2to3": per(s["refused_with_2to3"]), "refused_poor_or_no_overlap": per(s["refused_short_overlap"]), "refused_other": per(s["refused_other"]),
        "merged": per(s["merged"]),
        "est_yield_minus_merged": round(100 * st["est_yield"] - 100 * s["merged"] / s["input"], 1),
        "est_merge_allowance": round(100 * (st["est_pass"] - st["est_yield"]), 1),
        "median_overlap_merged": float(t["median_overlap_merged"].median()),
    })
out = pd.DataFrame(rows)
out.to_csv(sys.argv[1] + ".tsv", sep="\t", index=False)
cols = ["dataset", "arm", "cut", "maxEE", "est_pass", "fail_filter", "lost_denoising", "refused_close_overlap", "of_which_1_mismatch",
        "refused_poor_or_no_overlap", "merged", "est_merge_allowance", "est_yield", "est_yield_minus_merged"]
md = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)] + ["| " + " | ".join(str(r[c]) for c in cols) + " |" for r in rows]
open(sys.argv[1] + ".md", "w").write("\n".join(md) + "\n")
print("\n".join(md))
