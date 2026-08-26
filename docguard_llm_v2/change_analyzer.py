from __future__ import annotations

import json
import re
from typing import Any

from docguard_llm_v2.prompt_templates import analysis_prompt
from docguard_llm_v2.schemas import ChangeAnalysis, SupportedInference, asdict_shallow


def normalize_text(text: str) -> str:
    return " ".join(str(text or "").split())


def parse_json(text: str) -> dict[str, Any]:
    stripped = str(text or "").strip()
    stripped = re.sub(r"^```(?:json)?\s*", "", stripped, flags=re.I)
    stripped = re.sub(r"\s*```$", "", stripped)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", stripped, flags=re.S)
        if not match:
            raise
        return json.loads(match.group(0))


def evidence_is_valid(quote: str, source: str) -> bool:
    return bool(normalize_text(quote)) and normalize_text(quote).lower() in normalize_text(source).lower()


def build_analysis(data: dict[str, Any], *, code_diff: str, docs_before: str) -> tuple[ChangeAnalysis, list[SupportedInference], list[SupportedInference]]:
    valid: list[SupportedInference] = []
    invalid: list[SupportedInference] = []
    inferences = []
    for item in data.get("supported_inferences") or []:
        source_name = str(item.get("evidence_source") or "")
        source_text = code_diff if source_name == "code_diff" else docs_before if source_name == "docs_before" else ""
        inference = SupportedInference(
            claim=str(item.get("claim") or ""),
            evidence_source=source_name,
            evidence_quote=str(item.get("evidence_quote") or ""),
            evidence_valid=evidence_is_valid(str(item.get("evidence_quote") or ""), source_text),
        )
        (valid if inference.evidence_valid else invalid).append(inference)
        inferences.append(inference)
    analysis = ChangeAnalysis(
        change_summary=str(data.get("change_summary") or ""),
        behavior_before=str(data.get("behavior_before") or ""),
        behavior_after=str(data.get("behavior_after") or ""),
        developer_or_user_impact=str(data.get("developer_or_user_impact") or ""),
        documentation_impact=str(data.get("documentation_impact") or ""),
        supported_inferences=inferences,
        uncertainties=[str(item) for item in data.get("uncertainties") or []],
    )
    return analysis, valid, invalid


def analyze_change(*, code_diff: str, predicted_category: str, docs_before: str, llm: Any, model: str | None = None) -> dict[str, Any]:
    raw = llm.generate(analysis_prompt(code_diff=code_diff, predicted_category=predicted_category, docs_before=docs_before), model=model, purpose="analysis")
    parsed = parse_json(raw)
    analysis, valid, invalid = build_analysis(parsed, code_diff=code_diff, docs_before=docs_before)
    return {
        "raw": raw,
        "analysis": analysis,
        "validated_inferences": valid,
        "invalid_inferences": invalid,
        "analysis_dict": asdict_shallow(analysis),
    }

