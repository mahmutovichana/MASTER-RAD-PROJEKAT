from __future__ import annotations

from docguard.diff_analyzer import DiffFacts, analyze_record


POSITIVE_SCENARIOS = {
    "new_endpoint",
    "changed_validation_min",
    "changed_auth_requirement",
    "added_response_field",
}


def classify_facts(facts: DiffFacts) -> dict[str, object]:
    for scenario_type in [
        "changed_auth_requirement",
        "changed_validation_min",
        "added_response_field",
        "new_endpoint",
        "internal_refactor",
    ]:
        if scenario_type in facts.scenario_signals:
            return {
                "docs_update_required": scenario_type in POSITIVE_SCENARIOS,
                "scenario_type": scenario_type,
                "target_doc_file": facts.target_doc_file,
            }

    if "unsupported_positive" in facts.scenario_signals:
        return {
            "docs_update_required": True,
            "scenario_type": "unknown_change",
            "target_doc_file": facts.target_doc_file,
        }

    if "unsupported_negative" in facts.scenario_signals:
        return {
            "docs_update_required": False,
            "scenario_type": "unknown_change",
            "target_doc_file": facts.target_doc_file,
        }

    return {
        "docs_update_required": False,
        "scenario_type": "unknown_change",
        "target_doc_file": facts.target_doc_file,
    }


def classify_record(record: dict) -> dict[str, object]:
    return classify_facts(analyze_record(record))
