from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

from docguard_llm_v2.change_analyzer import analyze_change
from docguard_llm_v2.document_retriever import retrieve_documents
from docguard_llm_v2.documentation_writer import write_documentation
from docguard_llm_v2.provenance_verifier import verify_candidate
from docguard_llm_v2.repair import repair_documentation
from docguard_llm_v2.schemas import asdict_shallow


FORBIDDEN_CONTEXT_KEYS = {"docs_after_excerpt", "docs_diff_excerpt", "gold_docs_update_required", "gold_doc_category", "human_label_notes", "manual_label_notes"}


def load_config(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def config_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def candidate_dicts(candidates: list[Any]) -> list[dict[str, Any]]:
    return [asdict_shallow(item) for item in candidates]


def generate_semantic_documentation_patch(
    *,
    docs_update_required: bool,
    predicted_category: str,
    code_diff: str,
    docs_before: str,
    documentation_context_candidates: list[dict[str, Any]],
    llm_backend: Any,
    llm_model: str | None = None,
    config: dict[str, Any] | None = None,
    forbidden_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    started = time.perf_counter()
    llm_call_count = 0
    cfg = config or {}
    if not docs_update_required:
        return {
            "final_status": "no_update",
            "final_source": "none",
            "final_patch": None,
            "llm_call_count": 0,
            "latencies": {"total_seconds": time.perf_counter() - started},
        }
    forbidden = {key: value for key, value in (forbidden_context or {}).items() if key in FORBIDDEN_CONTEXT_KEYS and value}
    analysis_result = analyze_change(code_diff=code_diff, predicted_category=predicted_category, docs_before=docs_before, llm=llm_backend, model=cfg.get("analysis_model") or llm_model)
    llm_call_count += 1
    analysis_dict = analysis_result["analysis_dict"]
    analysis_dict["supported_inferences"] = [asdict_shallow(item) for item in analysis_result["validated_inferences"]]
    retrieval = retrieve_documents(
        predicted_category=predicted_category,
        analysis=analysis_dict,
        code_diff=code_diff,
        documentation_context_candidates=documentation_context_candidates,
        top_k=int(cfg.get("top_k_documents") or 3),
    )
    retrieved = candidate_dicts(retrieval["top_k"])
    writer = write_documentation(code_diff=code_diff, predicted_category=predicted_category, analysis=analysis_dict, retrieved_candidates=retrieved, llm=llm_backend, model=cfg.get("writer_model") or llm_model)
    llm_call_count += 1
    retrieved_paths = [item["path"] for item in retrieved]
    first_verifier = verify_candidate(
        candidate=writer["candidate"],
        retrieved_paths=retrieved_paths,
        code_diff=code_diff,
        docs_before=docs_before,
        validated_inferences=[asdict_shallow(item) for item in analysis_result["validated_inferences"]],
        forbidden_inputs=forbidden,
    )
    repair_attempted = False
    repair_result = None
    repair_verifier = None
    if first_verifier.safety_status == "pass":
        final_status = "accepted_first_pass"
        final_source = "llm"
        final_patch = asdict_shallow(writer["candidate"])
    else:
        final_status = "human_review_required"
        final_source = "none"
        final_patch = None
        if int(cfg.get("max_repair_attempts", 1)) > 0:
            repair_attempted = True
            repair_result = repair_documentation(original_candidate=writer["candidate"], verifier_result=first_verifier, analysis=analysis_dict, code_diff=code_diff, retrieved_candidates=retrieved, llm=llm_backend, model=cfg.get("repair_model") or llm_model)
            llm_call_count += 1
            repair_verifier = verify_candidate(
                candidate=repair_result["candidate"],
                retrieved_paths=retrieved_paths,
                code_diff=code_diff,
                docs_before=docs_before,
                validated_inferences=[asdict_shallow(item) for item in analysis_result["validated_inferences"]],
                forbidden_inputs=forbidden,
            )
            if repair_verifier.safety_status == "pass":
                final_status = "accepted_after_repair"
                final_source = "llm_repair"
                final_patch = asdict_shallow(repair_result["candidate"])
    return {
        "analysis": analysis_result["analysis_dict"],
        "validated_inferences": [asdict_shallow(item) for item in analysis_result["validated_inferences"]],
        "invalid_inferences": [asdict_shallow(item) for item in analysis_result["invalid_inferences"]],
        "retrieval": {**retrieval, "top_k": retrieved},
        "selected_document": writer["candidate"].target_document_path,
        "writer_raw": writer["raw"],
        "writer_candidate": asdict_shallow(writer["candidate"]),
        "first_pass_verifier": asdict_shallow(first_verifier),
        "repair_attempted": repair_attempted,
        "repair_raw": None if repair_result is None else repair_result["raw"],
        "repair_candidate": None if repair_result is None else asdict_shallow(repair_result["candidate"]),
        "repair_verifier": None if repair_verifier is None else asdict_shallow(repair_verifier),
        "final_status": final_status,
        "final_source": final_source,
        "final_patch": final_patch,
        "llm_call_count": llm_call_count,
        "latencies": {"total_seconds": time.perf_counter() - started},
        "model_configuration": cfg,
    }
