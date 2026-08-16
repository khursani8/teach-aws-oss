---
layout: default
title: 4. The flexibility frontier
---

# Chapter 4 — Verbatim collapse and the flexibility frontier

## What 2 epochs actually learns

C/H3's outputs are correct (86–89%) and **83% of them reproduce the reference at >99%
similarity**. Median similarity: 1.000. The model maps any question paraphrase to the
canonical answer text — genuinely *generalized* across phrasings (recall: 0/2,661 eval
questions appear in training), but with zero rephrasing on the answer side.

Why: the canonical answer appears ~7× per cluster (once per question paraphrase), each
synthetic variant 1×. Majority surface wins; the second epoch hardens it.

## Mapping the frontier (similarity-banded eval)

We added flexibility metrics: candidate/reference similarity distribution, and accuracy
*per similarity band*. The frontier, all on the same judge:

| Model | Acc | Median sim | %verbatim | Mechanism |
|---|---|---|---|---|
| H3 (2ep, comp-only) | 89.2% | 1.000 | 84% | recall |
| C + softening prompt | 81.9% | 1.000 | 78% | prompt can't unlock it |
| D (1ep, comp-only, K5) | 38.8% | 0.372 | 29% | half-remembered rephrase |
| G2 (D-data + balanced answers) | 32.1% | 0.241 | 19% | balanced mixture |
| G1 (canonical ×2) | 31.8% | 0.262 | 19% | half-balanced |
| F1a/F1b (fully balanced) | 16.6–17.5% | ~0.15 | 5% | full diversity |

The frontier is **monotone and steep**: every step toward diversity costs accuracy under
a strict judge, because a rephrased answer must retain *every* fact to score TRUE.

## What didn't work

- **Inference-time softening** (system prompt "answer in your own words"): changed the
  wording, walked back to canonical anyway — cost 4pp, bought no flexibility. The
  verbatim lock survives prompting.
- **Balancing variant frequency** (each answer surface seen equally): succeeded wildly at
  diversity (median sim 0.15) and collapsed accuracy to 17%. The judge fails nearly every
  free rephrase.
- **NEFTune from epoch 2** (noise on embeddings in the second epoch only): our first wave
  ran with the noise silently inactive — caught by missing activation markers, re-run with
  verified markers. (Results in `results/exp003/N*/` when complete.)

## The structural insight

Strict binary judging and free rephrasing are nearly incompatible *by construction*: the
reference is the fact list, and paraphrase-model outputs usually drop something the judge
checks for. If your product needs flexible phrasing, either the judge must become a
fact-coverage rubric (extract the reference's facts, check each in the candidate), or you
rephrase *after* retrieval with a bigger model. We chose to ship accuracy and guard the
failure mode (Chapter 5).

*Artifacts: `results/exp003/{F1*,G*,H*,C_softprompt}/`*
