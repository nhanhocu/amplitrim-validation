# Night 1 report (2026-10-09 07:59)

Problems: 0


### d6300_V3-V4  (mock_V3-V4_zymoD6300_PRJNA1261676)
- 10 runs of reads in raw
- primers: already removed from the reads (used as they are)
- share of reads with the conserved V3 start (GGGAAT in the first 30 bases): 99%
- prepared: 10 samples in C:\data\mock_V3-V4_zymoD6300_PRJNA1261676\prepared\all\ready
- expected sequences: C:\data\mock_V3-V4_zymoD6300_PRJNA1261676\reference\d6300_V3-V4_expected_sequences.fasta

### d6300_V4-V5  (mock_V4-V5_zymoD6300_miseq)
- 3 runs of reads in raw
- primers: 515F/926R
- prepared: 3 samples in C:\data\mock_V4-V5_zymoD6300_miseq\prepared\all\ready
- expected sequences: C:\data\mock_V4-V5_zymoD6300_miseq\reference\d6300_V4-V5_expected_sequences.fasta

### wastewater_V3-V4  (real_V3-V4_wastewater_PRJEB75155)
- 9 runs of reads in raw
- primers: 341F/805R
- some pairs are sequenced in the reverse orientation: --mixed-orientation
- prepared: 9 samples in C:\data\real_V3-V4_wastewater_PRJEB75155\prepared\all\ready

### spikein_V3-V4  (real_V3-V4_spikein_PRJNA1243306)
- 12 runs of reads in raw
- primers: 341F/805R
- prepared: 12 samples in C:\data\real_V3-V4_spikein_PRJNA1243306\prepared\all\ready

### swabs_V3-V4  (real_V3-V4_swabs_PRJNA1261676)
- 392 runs in the project; 21 left out as mock or control by their labels; 371 eligible; 36 taken (evenly spaced over the sorted accessions)
- 36 runs of reads in raw
- primers: already removed from the reads (used as they are)
- share of reads with the conserved V3 start (GGGAAT in the first 30 bases): 97%
- prepared: 36 samples in C:\data\real_V3-V4_swabs_PRJNA1261676\prepared\all\ready
- registered in amplitrim_paths.json (copy kept as .bak_before_night1): d6300_V3-V4, d6300_V4-V5, wastewater_V3-V4, spikein_V3-V4, swabs_V3-V4
- the battery ended with code 0; results in C:\data\runs\night1_2026-10-09

#### battery
- battery (the standard battery on the original datasets): ok in 35.6 min
    met      battery_mockA_high: AmpliTrim equals FIGARO at FIGARO's maxEE (3,4): -0.0 points (95% interval -0.3 to +0.3); margin +/-1.0
    met      battery_v1v2: AmpliTrim equals FIGARO at FIGARO's maxEE (2,1): +0.4 points (95% interval -0.1 to +0.8); margin +/-1.0

#### extra_datasets
- extra_datasets (the standard battery on new datasets): ok in 177.0 min
    met      battery_v4: AmpliTrim equals FIGARO at FIGARO's maxEE (1): +0.0 points (95% interval +0.0 to +0.0); margin +/-1.0
    met      battery_mcm_v12: AmpliTrim equals FIGARO at FIGARO's maxEE (1): -0.0 points (95% interval -0.0 to +0.0); margin +/-1.0
    NOT MET  battery_mockB: AmpliTrim equals FIGARO at FIGARO's maxEE (6,9): +2.6 points (95% interval +0.3 to +5.2); margin +/-1.0
    info     battery_mcm_v46: paired comparison with FIGARO: no paired per-sample comparison was printed (it needs at least 6 samples)
    met      battery_d6300_V3-V4: AmpliTrim equals FIGARO at FIGARO's maxEE (1): +0.0 points (95% interval +0.0 to +0.0); margin +/-1.0
    NOT MET  battery_d6300_V4-V5: FIGARO ran: no FIGARO row in the comparison table (FIGARO may have refused these reads)
    NOT MET  battery_wastewater_V3-V4: AmpliTrim equals FIGARO at FIGARO's maxEE (5): -1.0 points (95% interval -1.4 to -0.7); margin +/-1.0
    NOT MET  battery_spikein_V3-V4: AmpliTrim equals FIGARO at FIGARO's maxEE (2,1): +1.3 points (95% interval +0.4 to +2.5); margin +/-1.0
    met      battery_swabs_V3-V4: AmpliTrim equals FIGARO at FIGARO's maxEE (1): +0.0 points (95% interval +0.0 to +0.0); margin +/-1.0

Next: send this file and OVERNIGHT_SUMMARY.md from the same folder.
