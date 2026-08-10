from __future__ import annotations

import time
from pathlib import Path

from docguard_hybrid.doc_router import route
from docguard_runtime.doc_context import docs_before_excerpt
from docguard_runtime.git_diff import changed_files, workspace_diff
from docguard_runtime.patch_composer import compose_patch
from docguard_runtime.schemas import DOC_FILES, SECTIONS, ok_response


def record_for_workspace(workspace: Path, diff_text: str | None = None, files: list[str] | None = None) -> dict:
    return {
        "id": "workspace-current",
        "project_id": workspace.name,
        "split": "runtime",
        "changed_files": files or changed_files(workspace),
        "code_diff": diff_text if diff_text is not None else workspace_diff(workspace),
        "docs_before_excerpt": docs_before_excerpt(workspace),
        "change_summary": "",
        "docs_update_required": False,
        "doc_category": "no_update",
        "target_doc_file": "",
        "scenario_type": "runtime_unknown",
    }


def hf_predict(record: dict, input_mode: str, architecture: str) -> tuple[dict | None, str]:
    try:
        from docguard_hf_classifier.embedding_classifier import load_model, predict_rows
        from docguard_hf_classifier.dataset_export import export_row

        model = load_model(input_mode, architecture)
        row = export_row(record, input_mode=input_mode)
        predictions, _latency = predict_rows([row], model)
        return predictions[0], "hf_embedding"
    except Exception:
        return None, "hybrid_router"


def analyze_workspace(workspace: Path, diff_text: str | None = None, input_mode: str = "raw_diff_plus_docs", architecture: str = "staged") -> dict:
    started = time.perf_counter()
    record = record_for_workspace(workspace, diff_text=diff_text)
    routed = route(record)
    hf_prediction, model_used = hf_predict(record, input_mode, architecture)
    if hf_prediction:
        docs_required = bool(hf_prediction["docs_update_required"])
        doc_category = hf_prediction["doc_category"]
        target_file = hf_prediction["target_doc_file"] or DOC_FILES.get(doc_category, "")
        scenario = hf_prediction["scenario_type"]
        confidence = float(hf_prediction.get("confidence") or 0.0)
        reason = "HF embedding classifier prediction with router guardrail."
    else:
        docs_required = bool(routed["docs_update_required"])
        doc_category = routed["candidate_doc_categories"][0]
        target_file = (routed["candidate_target_doc_files"] or [""])[0]
        scenario = (routed["candidate_scenario_types"] or ["unknown_change"])[0]
        confidence = float(routed.get("router_confidence") or 0.0)
        reason = routed.get("router_reason", "Hybrid router prediction.")
    if not docs_required:
        patch = None
        target_file = None
    else:
        if not target_file:
            target_file = DOC_FILES.get(doc_category, "docs/api.md")
        patch = compose_patch(workspace, target_file, scenario, doc_category, record["code_diff"], SECTIONS.get(target_file, "Documentation"))
    diagnostics = {
        "changed_files": record["changed_files"],
        "model_used": model_used,
        "classifier_architecture": architecture if model_used == "hf_embedding" else "router_fallback",
        "input_mode": input_mode,
        "runtime_ms": round((time.perf_counter() - started) * 1000, 2),
    }
    return ok_response(docs_required, doc_category, target_file, scenario, confidence, reason, patch, diagnostics, patch.get("section") if patch else None)

