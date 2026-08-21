from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from docguard_hybrid.doc_router import route
from docguard_llm.analysis_decision import generate_analysis_decision
from docguard_llm.llm_generator import generate_documentation_patch
from docguard_llm.patch_postprocessor import postprocess_patch
from docguard_llm.patch_quality import evaluate_patch_quality
from docguard_llm.patch_verifier import verify_patch
from docguard_llm.prompt_builder import build_patch_prompt
from docguard_runtime.doc_context import docs_before_excerpt
from docguard_runtime.git_diff import changed_files, workspace_diff
from docguard_runtime.patch_composer import compose_patch
from docguard_runtime.schemas import DOC_FILES, SECTIONS, ok_response


def record_for_workspace(workspace: Path, diff_text: str | None = None, files: list[str] | None = None) -> dict:
    docs_excerpt = docs_before_excerpt(workspace)
    return {
        "id": "workspace-current",
        "project_id": workspace.name,
        "split": "runtime",
        "changed_files": files or changed_files(workspace),
        "code_diff": diff_text if diff_text is not None else workspace_diff(workspace),
        "docs_before": docs_excerpt,
        "docs_before_excerpt": docs_excerpt,
        "change_summary": "",
        "docs_update_required": False,
        "doc_category": "no_update",
        "target_doc_file": "",
        "scenario_type": "runtime_unknown",
    }


def hf_predict(record: dict, input_mode: str, architecture: str) -> tuple[dict | None, str]:
    if architecture in {"hybrid_router", "router_fallback", "router"}:
        return None, "hybrid_router"
    try:
        from docguard_hf_classifier.embedding_classifier import load_model, predict_rows
        from docguard_hf_classifier.dataset_export import export_row

        model = load_model(input_mode, architecture)
        row = export_row(record, input_mode=input_mode)
        predictions, _latency = predict_rows([row], model)
        return predictions[0], "hf_embedding"
    except Exception:
        return None, "hybrid_router"


def _deterministic_patch(workspace: Path, target_file: str, scenario: str, doc_category: str, code_diff: str) -> dict[str, Any]:
    patch = compose_patch(workspace, target_file, scenario, doc_category, code_diff, SECTIONS.get(target_file, "Documentation"))
    patch["backend"] = "deterministic"
    patch["generation_status"] = "ok"
    patch["verifier_status"] = "not_run"
    patch["quality_label"] = "not_scored"
    patch["hallucination_risk"] = "not_scored"
    patch["warnings"] = []
    return patch


def _llm_patch(
    *,
    workspace: Path,
    record: dict,
    target_file: str,
    scenario: str,
    doc_category: str,
    router_reason: str,
    signals: list[str],
    backend: str,
    model_name: str | None,
    max_new_tokens: int,
    temperature: float,
) -> dict[str, Any]:
    target_section = SECTIONS.get(target_file, "Documentation")
    fallback_patch = _deterministic_patch(workspace, target_file, scenario, doc_category, record["code_diff"])
    prompt, _metadata = build_patch_prompt(
        code_diff=record["code_diff"],
        docs_before=record["docs_before"],
        target_doc_file=target_file,
        doc_category=doc_category,
        scenario_type=scenario,
        signals=signals,
        router_reason=router_reason,
        project_id=record["project_id"],
        target_section=target_section,
        grounded_draft=fallback_patch.get("preview") or fallback_patch.get("text") or "",
    )
    backend_map = {
        "llm-mock": "mock",
        "llm-hf": "hf",
        "llm-openai-compatible": "openai_compatible",
        "llm-ollama": "ollama",
    }
    generated = generate_documentation_patch(
        prompt,
        backend=backend_map[backend],
        model_name=model_name,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
    )
    postprocessed = postprocess_patch(generated.get("patch_text"), target_file, target_section)
    patch_text = postprocessed.get("patch_text")
    verifier = verify_patch(
        patch_text,
        True,
        target_file,
        record["code_diff"],
        record["docs_before"],
        doc_category,
        scenario,
    )
    quality = evaluate_patch_quality(
        patch_text=patch_text,
        code_diff=record["code_diff"],
        docs_before=record["docs_before"],
        target_doc_file=target_file,
        doc_category=doc_category,
        scenario_type=scenario,
        verifier_result=verifier,
    )
    warnings = [
        *list(postprocessed.get("warnings") or []),
        *list(verifier.get("warnings") or []),
        *list(quality.get("quality_reasons") or []),
    ]
    if generated.get("generation_status") != "ok":
        warnings.append(generated.get("error_message") or "LLM generation failed")
    if postprocessed.get("postprocess_status") != "ok":
        warnings.append("LLM patch postprocessing failed")
    preview = (patch_text or "").replace("@@ " + target_section, f"## {target_section}", 1)
    preview = "\n".join(line[1:] if line.startswith("+") else line for line in preview.splitlines()).strip()
    return {
        "file": target_file,
        "mode": "append_to_section",
        "section": target_section,
        "text": "\n".join(line[1:] for line in (patch_text or "").splitlines() if line.startswith("+")),
        "preview": preview + ("\n" if preview else ""),
        "backend": backend,
        "model_name": model_name or "",
        "generation_status": generated.get("generation_status"),
        "generation_error": generated.get("error_message") or "",
        "raw_patch": generated.get("patch_text") or "",
        "postprocess_status": postprocessed.get("postprocess_status"),
        "verifier_status": verifier.get("verifier_status"),
        "quality_label": quality.get("quality_label"),
        "hallucination_risk": quality.get("hallucination_risk"),
        "grounded_tokens_found": verifier.get("grounded_tokens_found", []),
        "warnings": warnings,
        "fallback_patch": fallback_patch if generated.get("generation_status") != "ok" or postprocessed.get("postprocess_status") != "ok" or verifier.get("verifier_status") == "fail" else None,
    }


def analyze_workspace(
    workspace: Path,
    diff_text: str | None = None,
    input_mode: str = "raw_diff_plus_docs",
    architecture: str = "hybrid_router",
    analysis_backend: str = "hybrid",
    analysis_model: str | None = None,
    analysis_max_new_tokens: int = 256,
    analysis_temperature: float = 0.0,
    patch_backend: str = "deterministic",
    patch_model: str | None = None,
    patch_max_new_tokens: int = 192,
    patch_temperature: float = 0.1,
) -> dict:
    started = time.perf_counter()
    record = record_for_workspace(workspace, diff_text=diff_text)
    routed = route(record)
    hf_prediction, model_used = hf_predict(record, input_mode, architecture)
    llm_decision: dict[str, Any] | None = None
    if analysis_backend in {"llm-openai-compatible", "llm-ollama", "llm-hf", "llm-mock"}:
        llm_decision = generate_analysis_decision(
            changed_files=list(record["changed_files"]),
            code_diff=record["code_diff"],
            docs_before=record["docs_before"],
            backend=analysis_backend,
            model_name=analysis_model or patch_model,
            max_new_tokens=analysis_max_new_tokens,
            temperature=analysis_temperature,
        )
        model_used = f"{analysis_backend}_analysis"
        docs_required = bool(llm_decision["docs_update_required"])
        doc_category = str(llm_decision["doc_category"])
        target_file = str(llm_decision["target_doc_file"] or "")
        scenario = str(llm_decision["scenario_type"])
        confidence = float(llm_decision["confidence"])
        reason = "LLM analysis decision: " + str(llm_decision["reason"])
        if llm_decision.get("decision_status") != "ok":
            reason = "LLM analysis failed; no documentation update was selected. " + str(llm_decision.get("decision_error") or "")
    elif hf_prediction:
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
        if patch_backend in {"llm-hf", "llm-mock", "llm-openai-compatible", "llm-ollama"}:
            patch = _llm_patch(
                workspace=workspace,
                record=record,
                target_file=target_file,
                scenario=scenario,
                doc_category=doc_category,
                router_reason=reason,
                signals=list(routed.get("signals") or []),
                backend=patch_backend,
                model_name=patch_model,
                max_new_tokens=patch_max_new_tokens,
                temperature=patch_temperature,
            )
        else:
            patch = _deterministic_patch(workspace, target_file, scenario, doc_category, record["code_diff"])
    diagnostics = {
        "changed_files": record["changed_files"],
        "model_used": model_used,
        "classifier_architecture": architecture if model_used == "hf_embedding" else "router_fallback",
        "input_mode": input_mode,
        "patch_backend": patch_backend,
        "patch_model": patch_model or "",
        "analysis_backend": analysis_backend,
        "analysis_model": analysis_model or "",
        "runtime_ms": round((time.perf_counter() - started) * 1000, 2),
    }
    if llm_decision:
        diagnostics["analysis_status"] = llm_decision.get("decision_status", "")
        diagnostics["analysis_error"] = llm_decision.get("decision_error", "")
        diagnostics["analysis_raw_decision"] = llm_decision.get("raw_decision", "")
    return ok_response(docs_required, doc_category, target_file, scenario, confidence, reason, patch, diagnostics, patch.get("section") if patch else None)
