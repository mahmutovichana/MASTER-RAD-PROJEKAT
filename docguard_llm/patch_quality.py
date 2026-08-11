from __future__ import annotations

import re
from typing import Any

from docguard_llm.fact_extractor import extract_allowed_facts


GENERIC_PATCH_TERMS = {
    "new_endpoint",
    "added_environment_variable",
    "changed_background_job_schedule",
    "changed_validation_min",
    "added_dto_model_field",
    "changed_default_config_value",
    "changed_test_command",
    "added_service_orchestration_flow",
    "changed_caching_or_rate_limit_flow",
    "patch",
}


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _positive_lines(patch_text: str | None) -> list[str]:
    if not patch_text:
        return []
    return [line for line in patch_text.splitlines() if line.startswith("+")]


def _is_generic_patch(patch_text: str | None, grounded_tokens: list[str]) -> bool:
    if not patch_text:
        return False
    text = patch_text.lower()
    content = " ".join(line.lstrip("+").strip() for line in _positive_lines(patch_text)).strip().lower()
    if content in GENERIC_PATCH_TERMS:
        return True
    if any(f"+{term}." in text or f"+{term}" == text.strip() for term in GENERIC_PATCH_TERMS):
        return True
    if not grounded_tokens and len(content.split()) <= 4:
        return True
    return False


def evaluate_patch_quality(
    *,
    patch_text: str | None,
    code_diff: str,
    docs_before: str,
    target_doc_file: str,
    doc_category: str,
    scenario_type: str,
    verifier_result: dict,
) -> dict[str, Any]:
    reasons: list[str] = []
    verifier_status = verifier_result.get("verifier_status", "fail")
    warnings = list(verifier_result.get("warnings") or [])
    grounded_tokens = list(verifier_result.get("grounded_tokens_found") or [])
    allowed = extract_allowed_facts(code_diff, docs_before, doc_category, scenario_type)
    allowed_tokens = list(allowed.get("allowed_tokens") or [])

    if not patch_text:
        if doc_category == "no_update" or scenario_type in {"unknown_change", "docs_already_updated"}:
            return {
                "groundedness_score": 1.0,
                "minimality_score": 1.0,
                "readability_score": 1.0,
                "usefulness_score": 1.0,
                "hallucination_risk": "low",
                "quality_label": "excellent",
                "quality_reasons": ["no patch generated for no-update style prediction"],
            }
        return {
            "groundedness_score": 0.0,
            "minimality_score": 1.0,
            "readability_score": 0.0,
            "usefulness_score": 0.0,
            "hallucination_risk": "high",
            "quality_label": "rejected",
            "quality_reasons": ["positive documentation update has no patch"],
        }

    line_count = len(_positive_lines(patch_text))
    word_count = len(re.findall(r"\b\w+\b", patch_text))
    generic = _is_generic_patch(patch_text, grounded_tokens)
    unsupported_warning_count = sum(1 for warning in warnings if "unsupported" in warning or "not visible" in warning)

    groundedness = 0.45
    if allowed_tokens:
        groundedness = len(set(token.lower() for token in grounded_tokens)) / max(1, len(set(token.lower() for token in allowed_tokens)))
        groundedness = max(groundedness, 0.35 if grounded_tokens else 0.0)
    elif grounded_tokens:
        groundedness = 0.75
    if verifier_status == "pass":
        groundedness = max(groundedness, 0.75)
    if verifier_status == "fail":
        groundedness = min(groundedness, 0.35)
    if unsupported_warning_count:
        groundedness = min(groundedness, 0.3)
        reasons.append("verifier found unsupported claims")

    minimality = 1.0
    if line_count > 6:
        minimality -= min(0.5, (line_count - 6) * 0.08)
        reasons.append("patch is longer than a minimal documentation update")
    if word_count > 120:
        minimality -= 0.25
        reasons.append("patch is verbose")
    if re.search(r"\|.+\|", patch_text):
        minimality -= 0.15
        reasons.append("patch uses table-like structure that may be too heavy for a minimal patch")

    readability = 0.7
    if patch_text.startswith("@@") and _positive_lines(patch_text):
        readability += 0.2
    if any(line.startswith("+### ") or line.startswith("+- ") or line.startswith("+ - ") for line in patch_text.splitlines()):
        readability += 0.1
    if "```" in patch_text:
        readability -= 0.25
        reasons.append("patch contains nested markdown fences")

    usefulness = (groundedness * 0.45) + (_clamp(minimality) * 0.2) + (_clamp(readability) * 0.2)
    if grounded_tokens:
        usefulness += 0.15
    if generic:
        usefulness = min(usefulness, 0.45)
        reasons.append("patch is technically safe but too generic")
    if verifier_status == "fail":
        usefulness = min(usefulness, 0.25)
    elif verifier_status == "warn":
        usefulness = min(usefulness, 0.75)

    hallucination_risk = "low"
    if verifier_status == "fail" or unsupported_warning_count:
        hallucination_risk = "high"
    elif verifier_status == "warn" or warnings:
        hallucination_risk = "medium"

    groundedness = _clamp(groundedness)
    minimality = _clamp(minimality)
    readability = _clamp(readability)
    usefulness = _clamp(usefulness)

    if verifier_status == "fail" or hallucination_risk == "high":
        label = "rejected"
    elif usefulness >= 0.85 and hallucination_risk == "low" and not generic:
        label = "excellent"
    elif usefulness >= 0.6 and hallucination_risk in {"low", "medium"}:
        label = "usable"
    else:
        label = "needs_review"

    if not reasons:
        reasons.append("patch is grounded, minimal, and readable under lightweight heuristic checks")
    return {
        "groundedness_score": round(groundedness, 4),
        "minimality_score": round(minimality, 4),
        "readability_score": round(readability, 4),
        "usefulness_score": round(usefulness, 4),
        "hallucination_risk": hallucination_risk,
        "quality_label": label,
        "quality_reasons": reasons,
    }
