# Night 1 protocol (written 2026-10-09 01:20, before any analysis)

Build: AmpliTrim 0.1.0 build 6b0c25b6e3

Purpose: a FRESH, COMPLETE head-to-head run: prepare the new datasets, then run the standard battery (criteria fixed in TEST_REGISTER.md, section 3) on EVERY dataset, old and new, in one build, one output folder and one default setting (--allow-unmergeable 0.2%), replacing the mixed numbers of earlier runs. No criterion was added or changed for this run, and no result has been looked at.

Arms (the standard battery's comparisons, run through DADA2 on the same reads): AmpliTrim's recommendation at maxEE 2 (and 1 and 5), AmpliTrim at FIGARO's own maxEE, FIGARO as shipped, and no truncation; paired per-sample differences with intervals. FIGARO cannot be run on ITS. Not in this run: the median-Q30 baseline and the skin dataset (no run table yet).

| dataset | kind | role |
| --- | --- | --- |
| mockA_high | mock | development |
| mockA_all | mock | development |
| v4 (soil V4) | real | development |
| mockB | mock | held out |
| mcm_v12 (inter-lab V1-V2) | mock | held out |
| mcm_v46 (inter-lab V4-V6) | mock | held out |
| v1v2 | real | held out |
| its | real | case study (no FIGARO) |
| d6300_V3-V4 | mock | held out (not used to design anything) |
| d6300_V4-V5 | mock | held out (not used to design anything) |
| wastewater_V3-V4 | real | held out (not used to design anything) |
| spikein_V3-V4 | real | held out (not used to design anything) |
| swabs_V3-V4 | real | held out (not used to design anything) |

Swab selection rule (fixed here): paired NovaSeq runs of PRJNA1261676, leaving out runs whose own labels match the mock/control pattern `zymo|d6300|mock|\bmoc\s*\d|negative control|\bneg(ative)?\b|\bntc\b|blank|positive control|water control|pcr control|extraction control|standard`, with at least 20,000 reads; 36 runs evenly spaced over the sorted accessions. Samples under 5,000 read pairs are dropped at preparation.
Primers and orientation are chosen from what describe_reads.py finds in the reads of each dataset, as written in night1.py.
Expected sequences for the D6300 mocks: the Zymo reference file, cut between the primers.
