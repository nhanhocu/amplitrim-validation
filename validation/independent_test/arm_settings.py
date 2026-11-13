#!/usr/bin/env python
"""AmpliTrim settings for each arm. Usage: arm_settings.py DRAW_A DRAW_B OUT_DIR"""
import json, sys, time
from pathlib import Path
import amplitrim
from amplitrim.api import recommend
from amplitrim.pipeline import Settings, run
a, b, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
res = {"amplitrim_version": amplitrim.__version__}
def row(rec, secs): return dict(truncF=rec.trim_f, truncR=rec.trim_r, maxEE=list(rec.ee) if hasattr(rec,"ee") else None, est_pass=rec.ee_pass_rate, est_yield=rec.yield_est, seconds=round(secs,1))
t=time.time(); r,_,s = recommend(a, out/"w_R", out/"report_R"); res["R"] = row(r.recommendation, time.time()-t)
res["R"]["maxEE"] = [s["recommended"]["maxEE_f"], s["recommended"]["maxEE_r"]]; res["R"]["relaxed"] = s["maxEE_rule"]["relaxed"]; res["R"]["pass_at_2_summary"]=s["maxEE_rule"]["pass_rate_at_maxEE_2"]; res["R"]["warnings"]=s.get("warnings"); res["R"]["data"]=s["data"]; res["R"]["longest_amplicon"]=s["longest_amplicon"]
for k, ee in (("D",(2.0,2.0)),("E",(2.0,5.0))):
    t=time.time(); x = run(Settings(input_dir=a, work_dir=out/f"w_{k}", max_ee=ee), say=lambda m: None); res[k]=row(x.recommendation, time.time()-t); res[k]["maxEE"]=list(ee)
t=time.time(); r,_,s = recommend(b, out/"w_Rb", out/"report_Rb"); res["Rb"]=row(r.recommendation, time.time()-t); res["Rb"]["maxEE"]=[s["recommended"]["maxEE_f"], s["recommended"]["maxEE_r"]]
json.dump(res, open(out/"settings.json","w"), indent=1); print(json.dumps({k:{j:v[j] for j in ("truncF","truncR","maxEE","est_pass","est_yield","seconds")} for k,v in res.items() if k!="amplitrim_version"}, indent=0))
