---
layout: default
title: 6. What we shipped
---

# Chapter 6 — The shipped recipe and its honest limits

## Final model

**H3** — 87.3% strict accuracy on the full 2,661-question unseen eval (base: 4.1%).

| Ingredient | Value |
|---|---|
| Base | unsloth/Qwen3.5-2B (text-only) |
| LoRA | full MLP (gate/up/gate_up/down), ALL layers, r=16, α=2r=32, dropout 0 |
| LR | 4e-4 linear, 5 warmup steps, batch 2×4, adamw_8bit |
| Schedule | **2 epochs**, **completion-only loss** |
| Data | teach_aws + K3 synthetic answer paraphrases (26,888 rows) |

Weights: Hugging Face (see notebook for the repo id). Training code: private.

## How it compares (same strict judge, same unseen eval)

| Model | Strict acc |
|---|---|
| **teach-aws Qwen3.5-2B (ours)** | **87.3%** (n=2,661) |
| PixelSpaceAI Malaysian-Qwen2.5-7B-AWS-Malay-LoRA | 15.0% (n=60) |
| mesolitica Malaysian-Qwen2.5-7B-Instruct (their base) | 8.3% (n=60) |
| base Qwen3.5-2B (our base) | 4.1% (n=2,661) |

The 7B community adapter nearly doubles its base on facts and reads beautifully in Malay —
but it's a register/style LoRA (~2.5k pairs, card recommends RAG for factual accuracy), so a
fact-complete judge keeps only 15%. Style and facts are different axes; the notebook lets you
run all three yourself.

## Use it

The [Colab notebook](../notebook/teach_aws_inference.ipynb) shows loading with vLLM,
asking questions, the real failure example, and the guardrail in action.

## What it can do

- Answer paraphrased AWS questions it has never seen, at doc-quality register, 87% strict-correct
- Short questions get short answers; long ones get complete reference-grade paragraphs
- Malay AWS terminology consistent with the reference corpus

## What it cannot do (and what we do about it)

| Limitation | Evidence | Mitigation |
|---|---|---|
| Invented features on thin-coverage topics | "Memory and Cache Behavior" example | grounding guardrail (59% catch, 0.3% overblock) |
| ~13% overall failure rate | 2,324/2,661 TRUE | surface confidence UX; verify-on-flag |
| Rigid phrasing (83% verbatim) | median sim 1.000 | accepted by design; rephrase post-retrieval if needed |
| No knowledge outside the corpus | canary tests | retrieval-augmented deployment |

## What we'd try next

1. Judge redesign: fact-coverage rubric (element extraction + per-fact check) — makes
   flexible answers scorable, unlocking the training-side diversity work
2. Hard-service synthetic mining (vpc/amplify/appsync FALSE-rates → targeted data)
3. Teacher-rewrite chain: tiny accurate retriever + 35B rewriter, if flexible phrasing
   becomes a requirement

## Reproduction & record

Everything on this site is backed by artifacts in `results/`: every sweep trial's config
and verdict, the 24-layer ablation map, the K-grid, the flexibility frontier runs, the
guardrail benchmark, and the full-set finals. The experiment log (in experiment order,
including the invalidated results and why) is the source of this walkthrough.
