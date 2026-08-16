---
layout: default
title: 3. Data vs hyperparams
---

# Chapter 3: It's the data (until it's the schedule)

## Synthetic answer paraphrases

The original dataset has ~6 paraphrased *questions* per answer but one canonical *answer*, so
the model learns "this fact has exactly one phrasing". To break that, we generated
K paraphrased answers per cluster with a teacher (Qwen3.5-35B-A3B, thinking disabled,
register constraints: plain Malay prose, ±30% length, keep every fact).
8,433 verified generations: 0 prompt leaks, 0 markdown, 511-char mean.

## The K-grid (scoped to 3 services for speed: 8 conditions, ~12 min each)

| | 7 question paraphrases | 2 question paraphrases |
|---|---|---|
| K0 (no synth) | 1.5% | 0.5% |
| K1 | 3.0% | 1.0% |
| K3 | 3.0% | 5.1% |
| K5 | 4.5% | **6.6%** |

Answer diversity helped monotonically; fewer question surfaces *helped once K≥3*.
At a weak config, data composition moved 1.5%→6.6%, dwarfing any single hyperparameter.

## Then the schedule kicked the door in

The exp002 grid crossed epochs × loss-mask × data:

| Run | Config | Subset acc | Train loss |
|---|---|---|---|
| A1/A2 | K5, 1ep, full-seq | 33.2 / 34.1% | 1.235 |
| D | K5, 1ep, **completion-only** | **38.8%** | 1.149 |
| E | K3, 1ep (4th seed) | 33.8% | 1.248 |
| C | K3, **2ep**, full-seq | **86.0%** | 0.929 |
| H3 | K3, **2ep, completion-only** | **89.2%** | 0.822 |

Two findings:
1. **Completion-only loss** (mask the question tokens, train on the answer only) helps at
   every epoch count: +5pp at 1ep, +3pp at 2ep.
2. **The second epoch is worth +50pp.** Train loss still descending at 1ep (1.15 → 0.93)
   was the tell: the recall simply wasn't finished.

Look at the next chapter before celebrating: that second epoch buys accuracy by
*collapsing the output distribution*.

*Artifacts: `results/kaxis/`, `results/exp002/`*
