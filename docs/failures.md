---
layout: default
title: 5. Failures & the guardrail
---

# Chapter 5: The failures that matter

## Quantifying the risk on the shipped model (H3, 89.2%)

- 37/343 answers judged FALSE (10.8%)
- 76% of those failures are fluent, confident-length text; users cannot self-detect them
- Concentrated in thin-coverage services: vpc 40% FALSE, amplify/appsync 30%

## The canonical failure: invented features

> **Q:** Bolehkah saya menyimpan data saya apabila stack dipadamkan?
>
> **Model:** "Ya, anda boleh menggunakan ciri **Memory and Cache Behavior** dalam AWS
> CloudFormation untuk mengekalkan data semasa stack dipadamkan…"
>
> **Reference:** CloudFormation deletion policies (snapshots for EBS volumes / RDS instances).

"Memory and Cache Behavior" does not exist. This is wrong-cluster recall wearing the
reference register: the model found *a* feature-shaped answer, not *this question's*
answer. The verbatim polish makes it *more* convincing, not less.

## The grounding guardrail

Inference-only, no retraining: extract named entities from the candidate, compare against
the reference (in production: your retrieved ground-truth passage), flag novel ones.

```python
novel = entities(answer) - entities(reference)
if novel:  # mention of something the source never said
    warn_or_fallback()
```

Benchmark on H3's eval (n=343):

| | value |
|---|---|
| Catches wrong answers | **22/37 (59%)** |
| False-flags correct answers | 1/306 (0.3%) |

The guardrail turns confident-wrong into honest-unsure, which is what
prevents user complaints. The remaining 41% of failures (wrong numbers, omissions,
same-entity different-claims) need retrieval-side coverage, not generation-side patching:
the vpc/amplify/appsync FALSE-rates track training coverage directly.

## Is the judge itself reliable?

Every number on this site comes from a 4B judge. We re-judged H3's
identical generations with a 30B-A3B judge: **89.2% vs 91.3%, 97.4% agreement**
(9/343 verdicts flipped, net +2.1pp, within the subset noise floor). The strict-judge
foundation holds; the small judge is not the source of our results. (`results/exp003/H3/judge_ab.json`)

## What we did about the data side

Error analysis at every stage (bucketed FALSE reasons → truncation fix → register fix →
service coverage) is in `results/*/false_reasons.json`; the pattern that survived to the
end is knowledge gaps, not style. The fix is more/better data on the weak services, which
is exactly what the training pipeline is for.

*Artifacts: `results/exp003/guardrail/`, `results/exp003/H3/`*
