"""Judge A/B: 4B vs 8B judge on the same frozen generations (H3 subset).

Agreement rate + which model wins under each judge. De-risks the 4B-verdict
foundation of every number we've published.

Usage: .venv-vllm/bin/python src/exp001/judge_ab.py --res results/exp003/H3 --gpu-mem 0.55
"""
import argparse, json, logging, os
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

JUDGES = ["Qwen/Qwen3-4B-Instruct-2507", "Qwen/Qwen3-30B-A3B-Instruct-2507"]
JSYS = ("You are a strict grader. Given a question, a REFERENCE answer, and a CANDIDATE answer, "
        "output exactly one word: TRUE or FALSE.\nTRUE only if the candidate is COMPLETELY correct: "
        "every factual element of the reference is present and correct, and nothing wrong or "
        "hallucinated is added. Partially correct = FALSE. Ignore style/wording/formatting; "
        "judge factual content only.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--res", required=True)
    ap.add_argument("--gpu-mem", type=float, default=0.55)
    args = ap.parse_args()

    gens = [json.loads(l) for l in open(f"{args.res}/generations.jsonl") if l.strip()]
    out = {"n": len(gens)}
    verdict_sets = {}
    from vllm import LLM, SamplingParams
    from vllm.sampling_params import StructuredOutputsParams
    import gc, torch
    for judge in JUDGES:
        jl = LLM(model=judge, max_model_len=8192, gpu_memory_utilization=args.gpu_mem,
                 max_num_seqs=256, enforce_eager=True)
        jt = jl.get_tokenizer()
        jp = [jt.apply_chat_template(
            [{"role": "system", "content": JSYS},
             {"role": "user", "content": f"Question: {g['question']}\n\nREFERENCE answer:\n{g['reference']}\n\nCANDIDATE answer:\n{g['candidate']}"}],
            tokenize=False, add_generation_prompt=True) for g in gens]
        jo = jl.generate(jp, SamplingParams(temperature=0.0, max_tokens=8,
                       structured_outputs=StructuredOutputsParams(choice=["TRUE", "FALSE"])))
        verdict_sets[judge] = [o.outputs[0].text.strip().upper().startswith("TRUE") for o in jo]
        del jl; gc.collect(); torch.cuda.empty_cache()
        acc = sum(verdict_sets[judge]) / len(gens)
        out[judge] = acc
        logger.info("%s: %.4f", judge, acc)

    a, b = verdict_sets[JUDGES[0]], verdict_sets[JUDGES[1]]
    agree = sum(x == y for x, y in zip(a, b)) / len(a)
    out["agreement"] = agree
    out["disagree_idx"] = [i for i, (x, y) in enumerate(zip(a, b)) if x != y][:20]
    json.dump(out, open(f"{args.res}/judge_ab.json", "w"), indent=2)
    logger.info("agreement: %.4f (%d disagreements)", agree, len(out["disagree_idx"]))

if __name__ == "__main__":
    main()
