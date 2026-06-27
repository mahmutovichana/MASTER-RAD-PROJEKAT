from __future__ import annotations

import json
import re


REQUIRED_FIELDS = {
    "docs_update_required",
    "scenario_type",
    "doc_category",
    "target_doc_file",
    "target_section",
    "generated_doc_patch",
    "change_intent_summary",
    "primary_documentation_reason",
    "expected_facts_covered",
    "confidence",
}

FALLBACK_PREDICTION = {
    "docs_update_required": False,
    "scenario_type": "parse_error",
    "doc_category": "unknown",
    "target_doc_file": "",
    "target_section": "",
    "generated_doc_patch": None,
    "change_intent_summary": "",
    "primary_documentation_reason": "Model output could not be parsed as JSON.",
    "expected_facts_covered": [],
    "confidence": 0.0,
}


def extract_json_object(text: str) -> str | None:
    text = text.strip()
    if text.startswith("{") and text.endswith("}"):
        return text
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None


def normalize_prediction(value: dict) -> dict:
    prediction = dict(FALLBACK_PREDICTION)
    for key in REQUIRED_FIELDS:
        if key in value:
            prediction[key] = value[key]
    prediction["docs_update_required"] = bool(prediction["docs_update_required"])
    if prediction["generated_doc_patch"] in ("", "null"):
        prediction["generated_doc_patch"] = None
    if not isinstance(prediction["expected_facts_covered"], list):
        prediction["expected_facts_covered"] = []
    try:
        prediction["confidence"] = max(0.0, min(1.0, float(prediction["confidence"])))
    except (TypeError, ValueError):
        prediction["confidence"] = 0.0
    for key in ["scenario_type", "doc_category", "target_doc_file", "target_section", "change_intent_summary", "primary_documentation_reason"]:
        prediction[key] = "" if prediction[key] is None else str(prediction[key])
    return prediction


def parse_model_output(text: str) -> tuple[dict, bool]:
    candidate = extract_json_object(text)
    if not candidate:
        return dict(FALLBACK_PREDICTION), True
    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError:
        return dict(FALLBACK_PREDICTION), True
    if not isinstance(parsed, dict):
        return dict(FALLBACK_PREDICTION), True
    missing = REQUIRED_FIELDS - set(parsed)
    prediction = normalize_prediction(parsed)
    return prediction, bool(missing)

