# teach-aws-oss: Experiment Results

Open experiment record: unsloth LoRA finetuning of Qwen3.5-2B for Malay AWS QA,
evaluated with a strict completely-correct LLM judge on unseen questions.

**What's here:** verdicts, generations (samples), flexibility metrics, ablation
summaries, sweep trial configs/results, grounding guardrail, Colab notebook.
**What's NOT here:** training code and model weights (weights at [khursanirevo/teach-aws-qwen3.5-2b](https://huggingface.co/khursanirevo/teach-aws-qwen3.5-2b); training code stays private).

## Headline results (full 2,661-row unseen eval)

| Model | Strict acc | Output style |
|---|---|---|
| Base Qwen3.5-2B | 4.1% | — |
| D (1ep, completion-only, K5) | 35.7% | flexible rephrasing |
| C (2ep, full-seq, K3) | 86.8% | verbatim reference recall |
| **H3 (2ep, completion-only, K3)** | **87.3%** (2,324/2,661) | verbatim reference recall |

## Repo layout
- `results/exp001/`: 24-trial hyperparameter sweep, layer leave-one-out ablation, K-grid (data diversity)
- `results/exp002/`: epochs × completion-only × K5 grid
- `results/exp003/`: flexibility frontier (balanced mixtures), NEFTune attempts, full-set finals, grounding guardrail benchmark
- `notebook/`: Colab: how to use the final model + guardrail
- `docs/`: GitHub Pages walkthrough (in progress)

## The story (short version)
1ep + completion-only learns facts with flexible phrasing but scores 38.8% under
a strict judge; 2ep collapses to verbatim recall at 87%. Balancing answer-variant
frequency trades accuracy for diversity along a steep frontier. The judge itself
punishes rephrasing (a rephrased answer must keep EVERY fact to pass). We ship
the accurate model + a grounding guardrail that flags invented entities
(59% hallucination catch at 0.3% overblocking) and document honest limitations
with real examples (see notebook).

Full walkthrough: `docs/` (GitHub Pages). Colab: `notebook/`.

## Learn LoRA finetuning

New to LoRA finetuning? This video walks through the fundamentals that this
project builds on: [How to finetune LLMs with LoRA](https://www.youtube.com/watch?v=zQi0kqQNDrU)

## Reproducing the eval

`tools/` ships the evaluation stack (inference-side only, no training code):
- `eval_flex.py`: similarity-banded flexibility metrics for any generations.jsonl
- `judge_ab.py`: 4B vs 30B judge agreement check
- `service_delta.py`: per-service FALSE-rate comparison between runs
- `eval_judge.py`: the strict judge itself (Qwen3-4B, guided TRUE/FALSE)
