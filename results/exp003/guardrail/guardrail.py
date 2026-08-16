"""Grounding guardrail: flag answers whose entity claims don't appear in the
reference/retrieved ground truth. Turns confident-wrong into honest-unsure.

Usage (library):
    from guardrail import GroundingGuard
    guard = GroundingGuard()
    ok, novel_entities = guard.check(answer, reference)
"""

import re

# AWS-ish entity pattern: service/feature names, acronyms
ENT_RE = re.compile(
    r"\b(?:Amazon\s+[A-Z][a-zA-Z0-9]+|AWS\s+[A-Z][a-zA-Z0-9]+(?:\s+[A-Z][a-zA-Z0-9]+){0,2}"
    r"|[A-Z][a-zA-Z0-9]*(?:Flow|Front|Watch|Maker|Bridge|Formation|Sync|Lake|Base|Glue|Grid)"
    r"|[A-Z][a-zA-Z0-9]+\s(?:and\s)?[A-Z][a-zA-Z0-9]+(?:\s[A-Z][a-zA-Z0-9]+)*"  # TitleCase phrases (feature names)
    r"|S3|EC2|EBS|Lambda|IAM|VPC|KMS|SSE|TLS|SSL|HTTP|DNS|SQL|API|SDK|CLI|MFA|HSM|WAF"
    r"|Route\s?53|Step\sFunctions|CloudFormation|CloudFront|CloudWatch|Direct\sConnect)\b"
)


def entities(text: str) -> set[str]:
    return {
        m.group(0).lower().replace("amazon ", "").replace("aws ", "")
        for m in ENT_RE.finditer(text)
    }


class GroundingGuard:
    """Flags candidate answers containing named entities absent from the
    ground-truth (reference/retrieved) text. Intended deployment: retrieve the
    canonical answer for the user's question, generate freely, then verify the
    generation only uses entities present in ground truth."""

    def __init__(self, max_novel: int = 0):
        self.max_novel = max_novel

    def check(self, answer: str, reference: str) -> tuple[bool, set[str]]:
        novel = entities(answer) - entities(reference)
        return (len(novel) <= self.max_novel), novel

    def guard_answer(self, answer: str, reference: str) -> str:
        ok, novel = self.check(answer, reference)
        if ok:
            return answer
        missing = ", ".join(sorted(novel))
        return (
            f"{answer}\n\n---\n⚠️ Amaran: jawapan ini menyebut entiti yang tidak "
            f"disahkan dalam rujukan ({missing}). Sila semak dokumentasi AWS."
        )
