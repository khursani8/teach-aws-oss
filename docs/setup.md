---
layout: default
title: 1. Setup & the judge
next: sweep
---

# Chapter 1: Task, data, and a judge that doesn't forgive

## The task

Teach `Qwen/Qwen3.5-2B` to answer AWS questions in Bahasa Malaysia, in the register of the
aws-malay-qa reference answers: tight factual paragraphs, no markdown walls.

## The data

**Train:** `khursanirevo/teach_aws`, 18,455 rows.
The structure matters more than the count: **2,811 unique answers** (clusters), each with
~6.6 *question paraphrases* (same intent, different phrasing) and one canonical answer.
This is a paraphrase-retrieval task wearing a QA costume.

**Eval:** `PixelSpaceAI/aws-malay-qa`, both splits = 2,661 questions. Never trained on.
Zero eval questions appear verbatim in training, so any accuracy must survive paraphrase.

## The judge (the most important design decision)

A small instruct model (Qwen3-4B) reads the question, the REFERENCE answer, and the
CANDIDATE, and outputs exactly one word, `TRUE` or `FALSE`, under these rules:

- TRUE only if the candidate is **completely correct**: every factual element of the
  reference present, nothing wrong, nothing hallucinated
- Partially correct = FALSE. No half credit.
- Style, wording, formatting ignored; facts only.

Output is structurally forced (guided decoding over `{TRUE, FALSE}`), temperature 0.

**Why strict-binary?** It matches the product requirement (an answer that's missing a
caveat about, say, MFA Delete is a wrong answer), and it makes progress measurable:
there's no partial credit to game. The cost appears in Chapter 4: this judge
structurally punishes rephrasing. We kept it anyway and characterized the frontier
rather than loosening the metric.


## Why trust these numbers

Every headline on this site rests on four checks. Each failed at least once during the
project, which is how we know they bite.

**The eval is genuinely unseen.** Zero of the 2,661 eval questions appear verbatim in
training. The train set paraphrases the same facts, but no eval question does, so every
score reflects paraphrase generalization, not memorized prompts.

**The scores replicate.** Identical configs trained on different seeds land close
together: the 91% recipe scored 91.2% and 91.0%; the earlier 33% recipe scored
32.9/32.7/33.8 across three seeds. We also measured the noise floor directly by running
one config twice (4.7% vs 6.4% on the 343-question subset, so ±1.7pp). Deltas smaller
than that are treated as ties, which is why some near-identical sweep results were
never declared winners.

**The measurement instrument was cross-examined.** All verdicts come from a 4B judge,
so we re-judged a full generation set with a 30B judge: 97.4% agreement, net +2.1pp.
A judge 7x larger moves the headline less than the noise floor.

**Merges are tensor-verified.** The scariest bug of this project was a silent no-op
merge (adapters matched 0 modules, base weights shipped labeled as finetuned). Since
then every merge writes a provenance record and hard-fails unless the merged weights
differ from base on a layer the adapter actually trained. The shipped model's hub file
is md5-matched to the local merge.

Where the numbers are soft, the text says so: the gallery samples are n=1 per service
and labeled as such, and the 12% of strict-FALSE verdicts that a second judge
overturned are documented in Chapter 5 rather than rounded away.

## How not to fool yourself (a lesson we paid for)

Our first eval pipeline had a silent bug: the LoRA merge loaded adapters onto a mismatched
model class, matched **0 of 48 modules**, and quietly saved the base weights. Every early
"finetuned" score was the base model in disguise. The 4.5% vs 4.1% "improvement" was judge
noise on identical outputs. It was caught by md5: three different configs produced
byte-identical merged weights.

After that, every merge writes a provenance record and hard-fails unless the merged
weights differ from base on a layer the adapter trained. Trust nothing you
didn't verify at the tensor level.
