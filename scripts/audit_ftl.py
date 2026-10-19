#!/usr/bin/env python3
"""Audit First-Token Latency (FTL) from Retell call logs.

Usage:
  python audit_ftl.py calls/*.json                 # local JSON files
  RETELL_API_KEY=... python audit_ftl.py --ids call_1 call_2   # fetch via API
"""
import argparse, json, os, statistics, sys, urllib.request

THRESHOLD_MS = 1200


def fetch(call_id):
    req = urllib.request.Request(
        f"https://api.retellai.com/get-call/{call_id}",
        headers={"Authorization": f"Bearer {os.environ['RETELL_API_KEY']}"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def extract(call):
    """Return list of FTL values (ms) from a call log."""
    vals = []
    lm = call.get("latency_metrics", {})
    for src in (call, lm):
        v = src.get("first_token_latency_ms")
        if isinstance(v, (int, float)):
            vals.append(v)
    # fallback: Retell native latency block (per-turn values)
    for key in ("e2e", "llm"):
        block = call.get("latency", {}).get(key, {})
        if isinstance(block.get("values"), list) and not vals:
            vals.extend(block["values"])
    return vals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--ids", nargs="*", default=[])
    a = ap.parse_args()

    calls = []
    for f in a.files:
        with open(f) as fh:
            calls.append((f, json.load(fh)))
    for cid in a.ids:
        calls.append((cid, fetch(cid)))
    if not calls:
        sys.exit("No input. Pass JSON files or --ids.")

    all_vals = []
    for name, c in calls:
        v = extract(c)
        all_vals += v
        print(f"{name}: {len(v)} value(s), avg={statistics.mean(v):.0f} ms" if v else f"{name}: no FTL found")

    if not all_vals:
        sys.exit("No FTL values found.")
    avg = statistics.mean(all_vals)
    print(f"\nTurns: {len(all_vals)} | Avg FTL: {avg:.0f} ms | Max: {max(all_vals):.0f} ms")
    if avg < THRESHOLD_MS:
        print(f"PASS: average below {THRESHOLD_MS} ms")
    else:
        print(f"FLAG: average >= {THRESHOLD_MS} ms - optimise routing/model/prompt and re-audit")
        sys.exit(1)


if __name__ == "__main__":
    main()
