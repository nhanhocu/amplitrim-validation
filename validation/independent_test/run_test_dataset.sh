#!/bin/bash
# Usage: run_test_dataset.sh LABEL RAW_DIR WORK_DIR N_PAIRS
set -eo pipefail
L=$1; RAW=$2; W=$3; N=$4; P=$(dirname "$(readlink -f "$0")"); mkdir -p "$W"
[ -f "$W/prepare.json" ] || python "$P/prepare.py" "$L" "$RAW" "$W" "$N"
[ -f "$W/.gate_ok" ] || { [ -n "$PREPARE_ONLY" ] && exit 0; }
[ -f "$W/settings.json" ] || python "$P/arm_settings.py" "$W/a" "$W/b" "$W"
A=$(python -c "import json;s=json.load(open('$W/settings.json'));[print(k,s[k]['truncF'],s[k]['truncR'],s[k]['maxEE'][0],s[k]['maxEE'][1]) for k in ('R','D','E')]")
while read k f r e1 e2; do [ -f "$W/${k}_seqtab.tsv" ] || Rscript "$P/dada2_arm.R" "$W/a" $f $r $e1 $e2 "$W/$k"; done <<< "$A"
read _ f r e1 e2 < <(echo "$A" | grep '^D ')
[ -f "$W/Db_seqtab.tsv" ] || Rscript "$P/dada2_arm.R" "$W/b" $f $r $e1 $e2 "$W/Db"
python - "$W" <<'PY'
import sys,json,csv
W=sys.argv[1]; seen={}
csv.field_size_limit(10**9)
for a in ("R","D","E","Db"):
    h=open(f"{W}/{a}_seqtab.tsv").readline().rstrip("\n").split("\t")
    for s in h:
        if s and s not in seen: seen[s]=f"ASV{len(seen)+1}"
json.dump(seen,open(f"{W}/asv_ids.json","w"))
open(f"{W}/asvs.fa","w").write("".join(f">{i}\n{s}\n" for s,i in seen.items())); print(len(seen),"ASVs in union")
PY
rdp_classifier -Xmx3g classify -f fixrank -c 0.8 -o "$W/rdp.tsv" "$W/asvs.fa" 2>&1 | tail -1
python "$P/analyze.py" "$L" "$W" "$W/rdp.tsv" > "$W/analyze.log"; tail -3 "$W/analyze.log"
