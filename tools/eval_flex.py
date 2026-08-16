"""Similarity-banded flexibility metrics for any generations.jsonl.

Appends {sim_mean, sim_median, frac_gt_099, frac_gt_095, bands:{<0.7, 0.7-0.9,
0.9-0.99, >0.99: {n, n_true, acc}}} to the results dir as flex.json.
Bands tell us WHERE the model earns its accuracy: low-sim bands = flexible
correctness; >0.99 = verbatim recall.

Usage: PYTHONPATH=src/exp001 uv run python src/exp001/eval_flex.py \
         --res results/exp003/F1
"""

import argparse
import difflib
import json
import logging
import statistics

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BANDS = [(0.0, 0.7), (0.7, 0.9), (0.9, 0.99), (0.99, 1.01)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--res", required=True, help="results dir with generations.jsonl + verdicts.jsonl")
    args = ap.parse_args()

    gens = [json.loads(l) for l in open(f"{args.res}/generations.jsonl") if l.strip()]
    vers = [json.loads(l) for l in open(f"{args.res}/verdicts.jsonl") if l.strip()]
    assert len(gens) == len(vers)

    sims = [
        difflib.SequenceMatcher(None, g["candidate"], g["reference"]).ratio()
        for g in gens
    ]
    out = {
        "n": len(gens),
        "sim_mean": round(statistics.mean(sims), 3),
        "sim_median": round(statistics.median(sims), 3),
        "frac_gt_099": round(sum(s > 0.99 for s in sims) / len(sims), 3),
        "frac_gt_095": round(sum(s > 0.95 for s in sims) / len(sims), 3),
        "bands": {},
    }
    for lo, hi in BANDS:
        idx = [i for i, s in enumerate(sims) if lo <= s < hi]
        n_true = sum(vers[i]["verdict"] == "TRUE" for i in idx)
        out["bands"][f"{lo}-{min(hi,1.0)}"] = {
            "n": len(idx),
            "n_true": n_true,
            "acc": round(n_true / len(idx), 3) if idx else None,
        }

    with open(f"{args.res}/flex.json", "w") as f:
        json.dump(out, f, indent=2)
    logger.info("%s: median_sim=%.3f frac>0.99=%.3f", args.res, out["sim_median"], out["frac_gt_099"])
    for b, v in out["bands"].items():
        logger.info("  band %s: n=%d acc=%s", b, v["n"], v["acc"])


if __name__ == "__main__":
    main()
