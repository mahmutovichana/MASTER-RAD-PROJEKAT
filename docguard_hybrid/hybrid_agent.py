from __future__ import annotations

from docguard_hybrid.doc_router import route
from docguard_hybrid.scenario_router import choose_scenario

DOC_FILES = {"docs/api.md", "docs/architecture.md", "docs/models.md", "docs/developer-setup.md", "docs/testing.md", "docs/configuration.md", "docs/workflows.md", "CHANGELOG.md"}


def compose_patch(record: dict, category: str, target_file: str, scenario: str) -> str | None:
    if not target_file:
        return None
    section = record.get("target_section") or "Documentation"
    fact = (record.get("expected_facts") or [record.get("change_summary", scenario)])[0]
    return f"@@ {section}\n+{fact}."


def predict(record: dict, ml_prediction: dict | None = None, llm_prediction: dict | None = None) -> dict:
    routed = route(record)
    docs_required = bool(routed["docs_update_required"])
    if ml_prediction and ml_prediction.get("docs_update_required") is not None:
        docs_required = bool(ml_prediction["docs_update_required"]) if routed["router_confidence"] < 0.9 else docs_required
    if not docs_required:
        return {
            "record_id": record["id"],
            "docs_update_required": False,
            "scenario_type": (routed.get("candidate_scenario_types") or ["unknown_change"])[0],
            "doc_category": "no_update",
            "target_doc_file": "",
            "generated_doc_patch": None,
            "router_output": routed,
            "router_ml_agree": ml_prediction is None or ml_prediction.get("docs_update_required") is False,
            "router_llm_agree": llm_prediction is None,
            "deterministic_patch_used": False,
            "llm_patch_rewrite_used": False,
            "corrected_target_doc_file": False,
            "invalid_source_file_target": False,
            "latency_seconds": 0.0,
        }
    category = (ml_prediction or {}).get("doc_category") or routed["candidate_doc_categories"][0]
    if category == "no_update":
        category = routed["candidate_doc_categories"][0]
    target = (ml_prediction or {}).get("target_doc_file") or routed["candidate_target_doc_files"][0]
    corrected = target not in DOC_FILES
    if corrected:
        target = routed["candidate_target_doc_files"][0]
    scenario = (ml_prediction or {}).get("scenario_type") or choose_scenario(record, routed)
    return {
        "record_id": record["id"],
        "docs_update_required": True,
        "scenario_type": scenario,
        "doc_category": category,
        "target_doc_file": target,
        "generated_doc_patch": compose_patch(record, category, target, scenario),
        "router_output": routed,
        "router_ml_agree": ml_prediction is None or ml_prediction.get("doc_category") == category,
        "router_llm_agree": llm_prediction is None,
        "deterministic_patch_used": True,
        "llm_patch_rewrite_used": False,
        "corrected_target_doc_file": corrected,
        "invalid_source_file_target": target not in DOC_FILES,
        "latency_seconds": 0.0,
    }
