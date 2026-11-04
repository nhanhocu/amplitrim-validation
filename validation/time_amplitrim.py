"""Time a command and record its peak memory, with the machine details a paper needs.

    pip install psutil
    python time_amplitrim.py -- amplitrim --input-dir reads --work-dir work --out-dir report
    python time_amplitrim.py --label "mock B" -- amplitrim --input-dir reads --work-dir work --out-dir report

It runs the command (everything after the "--"), polls the memory of the command and of every program it starts
(vsearch, for example) twice a second, and prints one summary. It also appends the summary to timing.jsonl, so that
several runs can be put into one table. It changes nothing else.
"""
import argparse
import json
import platform
import re
import subprocess
import sys
import time

try:
    import psutil
except ImportError:
    sys.exit("This script needs psutil: pip install psutil")


def version_of(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        text = ((out.stdout or "") + "\n" + (out.stderr or "")).strip().splitlines()
        for line in text:                                   # vsearch prints a banner such as "vsearch v2.32.0_win_x86_64, ..."
            if re.match(r"vsearch v\d", line):
                return line.strip()
        return text[0] if text else "unknown"
    except Exception:
        return "not found"


def tree_rss(proc):
    """Resident memory of a process and all of its children, in bytes."""
    total = 0
    try:
        procs = [proc] + proc.children(recursive=True)
    except psutil.Error:
        return 0
    for p in procs:
        try:
            total += p.memory_info().rss
        except psutil.Error:
            pass
    return total


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--label", default="", help="a name for this run, for example the dataset")
    ap.add_argument("--log", default="timing.jsonl", help="file that the summary is appended to")
    ap.add_argument("command", nargs=argparse.REMAINDER, help="after --: the command to run")
    args = ap.parse_args(argv)
    cmd = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not cmd:
        ap.error("give the command after --")
    start = time.perf_counter()
    child = subprocess.Popen(cmd)
    watch = psutil.Process(child.pid)
    peak = 0
    while child.poll() is None:
        peak = max(peak, tree_rss(watch))
        time.sleep(0.5)
    wall = time.perf_counter() - start
    summary = {
        "label": args.label, "command": " ".join(cmd), "exit_code": child.returncode,
        "wall_seconds": round(wall, 1), "wall_minutes": round(wall / 60, 2), "peak_memory_mb": round(peak / 1e6),
        "cpu_cores": psutil.cpu_count(logical=True), "ram_gb": round(psutil.virtual_memory().total / 1e9, 1),
        "os": platform.platform(), "python": platform.python_version(), "cpu": platform.processor() or "unknown",
        "vsearch": version_of(["vsearch", "--version"]), "amplitrim": version_of(["amplitrim", "--version"]),
    }
    print("\n" + json.dumps(summary, indent=2))
    with open(args.log, "a", encoding="utf-8") as f:
        f.write(json.dumps(summary) + "\n")
    return child.returncode


if __name__ == "__main__":
    sys.exit(main())
