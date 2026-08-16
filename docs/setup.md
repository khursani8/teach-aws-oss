---
layout: default
title: 1. Setup & the judge
---

# Chapter 1 — Task, data, and a judge that doesn't forgive

## The task

Teach `Qwen/Qwen3.5-2B` to answer AWS questions in Bahasa Malaysia, in the register of the
aws-malay-qa reference answers: tight factual paragraphs, no markdown walls.

## The data

**Train** — `khursanirevo/teach_aws`: 18,455 rows.
The structure matters more than the count: **2,811 unique answers** (clusters), each with
~6.6 *question paraphrases* (same intent, different phrasing) and one canonical answer.
This is a paraphrase-retrieval task wearing a QA costume.

**Eval** — `PixelSpaceAI/aws-malay-qa`, both splits = 2,661 questions. Never trained on.
Zero eval questions appear verbatim in training, so any accuracy must survive paraphrase.

## The judge (the most important design decision)

A small instruct model (Qwen3-4B) reads the question, the REFERENCE answer, and the
CANDIDATE, and outputs exactly one word — `TRUE` or `FALSE` — under these rules:

- TRUE only if the candidate is **completely correct**: every factual element of the
  reference present, nothing wrong, nothing hallucinated
- Partially correct = FALSE. No half credit.
- Style, wording, formatting ignored; facts only.

Output is structurally forced (guided decoding over `{TRUE, FALSE}`), temperature 0.

**Why strict-binary?** It matches the product requirement (an answer that's missing a
caveat about, say, MFA Delete is a wrong answer), and it makes progress measurable:
there's no partial credit to game. The cost appears in Chapter 4 — this judge
structurally punishes rephrasing — and we chose to keep it and characterize the frontier
rather than loosen the metric.

## How not to fool yourself (a lesson we paid for)

Our first eval pipeline had a silent bug: the LoRA merge loaded adapters onto a mismatched
model class, matched **0 of 48 modules**, and quietly saved the base weights. Every early
"finetuned" score was the base model in disguise — 4.5% vs 4.1% "improvement" was judge
noise on identical outputs. It was caught by md5: three different configs produced
byte-identical merged weights.

After that, every merge writes a provenance record and hard-fails unless the merged
weights *differ from base on a layer the adapter actually trained*. Trust nothing you
didn't verify at the tensor level.
