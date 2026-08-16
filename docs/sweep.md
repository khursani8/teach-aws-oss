---
layout: default
title: 2. The sweep
---

# Chapter 2: Where the knowledge lives

## The grid

24 trials over the axes that matter for LoRA on a 2B:

- **Module families**: MLP subsets (gate/up/gateup/down), attention (qkv/o), mixed
- **Layer ranges**: full, halves, quarters, middle band (0.25–0.75)
- **Rank** r ∈ {8,16,32}, **alpha** ∈ {1r, 2r}, **LR** log-uniform 5e-5…4e-4

Optuna, 8 parallel trials (packed 2–3/GPU on 4×H200), judged on a fixed stratified
343-question subset.

## Single axes looked flat; the interaction wasn't

Read one axis at a time and nothing mattered: rank within ±0.2pp, layer ranges within ~1pp,
families within noise. The winner hid in a **combination**:

| Trial | Config | Subset acc |
|---|---|---|
| t021 | full MLP, **all layers**, r16, **α=2r**, **lr 4e-4** | **32.9%** |
| next 20 trials | various partial configs | 4.7–7.9% |

Partial-layer trials at lr 2e-4 plateaued; full-layer at lr 5e-5 also plateaued. Full
coverage × high LR is what trains. Capacity that isn't pushed doesn't move.
t021 replicated across seeds (32.9 / 32.7 / 33.8 / one 25.4 outlier).

## Leave-one-out: every layer matters, the middle matters most

From t021's full-layer adapter we zeroed each layer's LoRA-B in turn: 24 merges, 24 evals,
no retraining:

| Band | Accuracy drop when removed |
|---|---|
| L9–L16 (core) | 13–17pp each |
| L17–L19 | 11–13pp |
| early L0–L4 | 6–9pp |
| L5–L7, L20–L23 | 5–9pp |

Removing *any single layer* costs ≥5pp; the hump peaks at L11/L12. That's why every
partial-range config lost: there is no cheap window; the knowledge spreads across the
whole stack with a middle-weighted profile.

*Artifacts: `results/exp001/sweep/`, `results/ablate/LOO_L00…23/`*
