"""Per-service FALSE-rate comparison between two runs (e.g. H4 vs H3).

Usage: PYTHONPATH=src/exp001 uv run python src/exp001/service_delta.py \
         --a results/exp003/H3 --b results/exp004/H4a [--label "H4a vs H3"]
"""
import argparse, json, logging
from collections import Counter
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def rates(res):
    vers = [json.loads(l) for l in open(f"{res}/verdicts.jsonl") if l.strip()]
    tot, false = Counter(), Counter()
    for v in vers:
        tot[v["service"]] += 1
        false[v["service"]] += v["verdict"] == "FALSE"
    return {s: (false[s], tot[s]) for s in tot}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True, help="baseline run (H3)")
    ap.add_argument("--b", required=True, help="candidate run (H4)")
    ap.add_argument("--label", default=None)
    args = ap.parse_args()
    ra, rb = rates(args.a), rates(args.b)
    print(f"{'service':16s} {'A_false':>8s} {'B_false':>8s} {'delta':>7s}")
    worse = better = 0
    for s in sorted(set(ra) | set(rb), key=lambda s: -(ra.get(s, (0, 1))[0] / max(ra.get(s, (0, 1))[1], 1))):
        fa, ta = ra.get(s, (0, 0)); fb, tb = rb.get(s, (0, 0))
        if ta < 3 and tb < 3:
            continue
        pa = fa / max(ta, 1); pb = fb / max(tb, 1)
        d = pb - pa
        mark = "<<" if d <= -0.10 else (">>" if d >= 0.10 else "")
        if d <= -0.10: better += 1
        if d >= 0.10: worse += 1
        print(f"{s:16s} {fa}/{ta:>3d}={pa:5.0%} {fb}/{tb:>3d}={pb:5.0%} {d:+7.0%} {mark}")
    oa = sum(f for f, _ in ra.values()); ob = sum(f for f, _ in rb.values())
    nt = sum(t for _, t in ra.values())
    print(f"\noverall: A {oa}/{nt} = {oa/nt:.1%} | B {ob}/{nt} = {ob/nt:.1%} | services improved>=10pp: {better}, worsened>=10pp: {worse}")

if __name__ == "__main__":
    main()
