"""exp001 eval step 2: strict TRUE/FALSE judge via vLLM (run in .venv-vllm).

Judge: Qwen/Qwen3-4B-Instruct-2507, guided decoding choice:true,false.
TRUE only if candidate is COMPLETELY correct; partial => FALSE.

Usage:
  .venv-vllm/bin/python src/exp001/eval_judge.py --gen results/exp001/generations.jsonl --out results/exp001
"""

import argparse
import json
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

JUDGE_MODEL = "Qwen/Qwen3-4B-Instruct-2507"

JUDGE_SYSTEM = """You are a strict grader. Given a question, a REFERENCE answer, and a CANDIDATE answer, output exactly one word: TRUE or FALSE.

Rules:
- TRUE only if the candidate is COMPLETELY correct: every factual element of the reference is present and correct in the candidate, and the candidate contains no wrong or hallucinated information.
- FALSE if any element is missing, wrong, contradictory, or if the candidate adds incorrect information.
- Partially correct = FALSE. No half credit.
- Ignore differences in language style, wording, or formatting; judge factual content only.
- Output exactly: TRUE or FALSE"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen", required=True, help="generations.jsonl from eval_generate.py")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    from vllm import LLM, SamplingParams
    from vllm.sampling_params import StructuredOutputsParams

    verdicts_path = os.path.join(args.out, "verdicts.jsonl")
    judged: set[int] = set()
    if os.path.exists(verdicts_path):
        with open(verdicts_path) as f:
            for line in f:
                if line.strip():
                    judged.add(json.loads(line)["idx"])
        logger.info("Resuming: %d already judged", len(judged))

    with open(args.gen) as f:
        rows = [(i, json.loads(line)) for i, line in enumerate(f) if line.strip()]

    todo = [(i, d) for i, d in rows if i not in judged]
    if todo:
        llm = LLM(model=JUDGE_MODEL, max_model_len=8192, gpu_memory_utilization=0.85)
        tok = llm.get_tokenizer()
        prompts = [
            tok.apply_chat_template(
                [
                    {"role": "system", "content": JUDGE_SYSTEM},
                    {
                        "role": "user",
                        "content": (
                            f"Question: {d['question']}\n\n"
                            f"REFERENCE answer:\n{d['reference']}\n\n"
                            f"CANDIDATE answer:\n{d['candidate']}"
                        ),
                    },
                ],
                tokenize=False,
                add_generation_prompt=True,
            )
            for _, d in todo
        ]
        outs = llm.generate(
            prompts,
            SamplingParams(
                temperature=0.0,
                max_tokens=8,
                structured_outputs=StructuredOutputsParams(choice=["TRUE", "FALSE"]),
            ),
        )
        with open(verdicts_path, "a") as f:
            for (i, d), out in zip(todo, outs, strict=True):
                text = out.outputs[0].text.strip().upper()
                verdict = "TRUE" if text.startswith("TRUE") else "FALSE"
                f.write(
                    json.dumps(
                        {"idx": i, "verdict": verdict, "service": d.get("service")},
                        ensure_ascii=False,
                    )
                    + "\n"
                )
                f.flush()
    else:
        logger.info("All %d verdicts already present", len(rows))

    # Final tally (resume-safe)
    n_true = n_total = 0
    by_service: dict[str, list[int]] = {}
    with open(verdicts_path) as f:
        for line in f:
            if not line.strip():
                continue
            v = json.loads(line)
            n_total += 1
            n_true += v["verdict"] == "TRUE"
            key = v.get("service") or "?"
            by_service.setdefault(key, [0, 0])
            s = by_service[key]
            s[0] += v["verdict"] == "TRUE"
            s[1] += 1
    acc = n_true / n_total if n_total else 0.0
    logger.info("Strict accuracy: %d/%d = %.4f", n_true, n_total, acc)
    for svc, (t, n) in sorted(by_service.items()):
        logger.info("  %-12s %d/%d = %.3f", svc, t, n, t / n)

    with open(os.path.join(args.out, "summary.json"), "w") as f:
        json.dump(
            {
                "n_total": n_total,
                "n_true": n_true,
                "strict_accuracy": acc,
                "by_service": {k: {"true": v[0], "total": v[1]} for k, v in by_service.items()},
                "judge_model": JUDGE_MODEL,
            },
            f,
            indent=2,
        )


if __name__ == "__main__":
    main()
