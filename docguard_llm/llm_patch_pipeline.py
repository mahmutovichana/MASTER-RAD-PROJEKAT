from __future__ import annotations

from typing import Any

from docguard_llm.grounded_patch_generator import generate_grounded_patch
from docguard_llm.llm_generator import generate_documentation_patch
from docguard_llm.patch_postprocessor import postprocess_patch
from docguard_llm.patch_quality import evaluate_patch_quality
from docguard_llm.patch_verifier import verify_patch
from docguard_llm.prompt_builder import build_patch_prompt


def _empty_no_update_result() -> dict[str, Any]:
    verifier = {
        "verifier_status": "pass",
        "warnings": [],
        "grounded_tokens_found": [],
    }
    quality = {
        "groundedness_score": 1.0,
        "minimality_score": 1.0,
        "readability_score": 1.0,
        "usefulness_score": 1.0,
        "hallucination_risk": "low",
        "quality_label": "excellent",
        "quality_reasons": ["no patch generated for no-update prediction"],
    }

    return {
        "final_patch_text": None,
        "final_patch_source": "no_update",
        "final_generation_status": "not_applicable",
        "final_error_message": "",
        "llm_prompt": "",
        "llm_patch_raw": "",
        "llm_generation_status": "not_applicable",
        "llm_error_message": "",
        "llm_latency_seconds": None,
        "grounded_patch_text": None,
        "grounded_patch_status": "not_applicable",
        "postprocess_status": "not_applicable",
        "postprocess_warnings": [],
        "verifier": verifier,
        "quality": quality,
        "allowed_facts": {},
        "grounding_tokens": [],
        "patch_pipeline_warnings": [],
    }


def _verify_and_score(
    *,
    patch_text: str | None,
    docs_update_required: bool,
    target_doc_file: str,
    code_diff: str,
    docs_before: str,
    doc_category: str,
    scenario_type: str,
    allowed_facts: dict[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    verifier = verify_patch(
        patch_text,
        docs_update_required,
        target_doc_file,
        code_diff,
        docs_before,
        doc_category,
        scenario_type,
        allowed_facts,
    )

    quality = evaluate_patch_quality(
        patch_text=patch_text,
        code_diff=code_diff,
        docs_before=docs_before,
        target_doc_file=target_doc_file,
        doc_category=doc_category,
        scenario_type=scenario_type,
        verifier_result=verifier,
    )

    return verifier, quality


def _is_acceptable(verifier: dict[str, Any], quality: dict[str, Any]) -> bool:
    verifier_status = str(verifier.get("verifier_status") or "fail")
    quality_label = str(quality.get("quality_label") or "rejected")
    risk = str(quality.get("hallucination_risk") or "high")

    if verifier_status not in {"pass", "warn"}:
        return False

    if quality_label in {"rejected"}:
        return False

    if risk == "high":
        return False

    return True


def generate_llm_patch_candidate(
    *,
    docs_update_required: bool,
    code_diff: str,
    docs_before: str,
    doc_category: str,
    target_doc_file: str,
    target_section: str,
    scenario_type: str,
    project_id: str,
    patch_backend: str,
    patch_model: str | None = None,
    max_new_tokens: int = 512,
    temperature: float = 0.1,
    save_prompt: bool = False,
) -> dict[str, Any]:
    """
    Generate a documentation patch with an LLM, but keep classification separate.

    The LLM does NOT decide:
    - whether documentation is needed
    - which category should be used
    - which target file should be used

    The LLM only rewrites/synthesizes a patch from:
    - safe code diff
    - docs-before excerpt
    - ML-predicted category
    - ML-derived target document
    - extracted allowed facts
    - grounded deterministic draft

    If the LLM patch fails verifier/quality checks, the pipeline falls back to the
    grounded deterministic patch when that fallback is acceptable.
    """
    if not docs_update_required:
        return _empty_no_update_result()

    pipeline_warnings: list[str] = []

    grounded = generate_grounded_patch(
        docs_update_required=True,
        code_diff=code_diff,
        docs_before=docs_before,
        doc_category=doc_category,
        target_doc_file=target_doc_file,
        target_section=target_section,
        scenario_type=scenario_type,
    )

    grounded_patch_text = grounded.get("patch_text")
    allowed_facts = grounded.get("allowed_facts") or {}
    grounding_tokens = list(grounded.get("grounding_tokens") or [])

    grounded_postprocessed = postprocess_patch(
        grounded_patch_text,
        target_doc_file,
        target_section,
    )

    grounded_final_patch = grounded_postprocessed.get("patch_text")

    grounded_verifier, grounded_quality = _verify_and_score(
        patch_text=grounded_final_patch,
        docs_update_required=True,
        target_doc_file=target_doc_file,
        code_diff=code_diff,
        docs_before=docs_before,
        doc_category=doc_category,
        scenario_type=scenario_type,
        allowed_facts=allowed_facts,
    )

    prompt, prompt_metadata = build_patch_prompt(
        code_diff=code_diff,
        docs_before=docs_before,
        target_doc_file=target_doc_file,
        doc_category=doc_category,
        scenario_type=scenario_type,
        signals=[],
        router_reason=(
            "ML cascade selected the documentation category and target file. "
            "The LLM may only synthesize a grounded documentation patch."
        ),
        project_id=project_id,
        target_section=target_section,
        grounded_draft=grounded_final_patch or grounded_patch_text,
    )

    generated = generate_documentation_patch(
        prompt,
        backend=patch_backend,
        model_name=patch_model,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
    )

    llm_raw = generated.get("patch_text") or ""
    llm_status = str(generated.get("generation_status") or "unknown")
    llm_error = str(generated.get("error_message") or "")

    if llm_status == "ok":
        llm_postprocessed = postprocess_patch(
            llm_raw,
            target_doc_file,
            target_section,
        )
    else:
        llm_postprocessed = {
            "patch_text": None,
            "postprocess_status": "fail",
            "warnings": [llm_error or "LLM generation failed"],
        }

    llm_patch_text = llm_postprocessed.get("patch_text")

    llm_verifier, llm_quality = _verify_and_score(
        patch_text=llm_patch_text,
        docs_update_required=True,
        target_doc_file=target_doc_file,
        code_diff=code_diff,
        docs_before=docs_before,
        doc_category=doc_category,
        scenario_type=scenario_type,
        allowed_facts=allowed_facts,
    )

    llm_ok = _is_acceptable(llm_verifier, llm_quality)
    grounded_ok = _is_acceptable(grounded_verifier, grounded_quality)

    if llm_ok:
        final_patch = llm_patch_text
        final_source = "llm"
        final_verifier = llm_verifier
        final_quality = llm_quality
        final_postprocess_status = llm_postprocessed.get("postprocess_status")
        final_postprocess_warnings = list(llm_postprocessed.get("warnings") or [])
    elif grounded_ok:
        final_patch = grounded_final_patch
        final_source = "grounded_fallback"
        final_verifier = grounded_verifier
        final_quality = grounded_quality
        final_postprocess_status = grounded_postprocessed.get("postprocess_status")
        final_postprocess_warnings = list(grounded_postprocessed.get("warnings") or [])
        pipeline_warnings.append("llm_patch_rejected_grounded_fallback_used")
    else:
        final_patch = llm_patch_text or grounded_final_patch
        final_source = "llm_rejected_no_acceptable_fallback" if llm_patch_text else "grounded_rejected_no_acceptable_llm"
        final_verifier = llm_verifier if llm_patch_text else grounded_verifier
        final_quality = llm_quality if llm_patch_text else grounded_quality
        final_postprocess_status = llm_postprocessed.get("postprocess_status") if llm_patch_text else grounded_postprocessed.get("postprocess_status")
        final_postprocess_warnings = list(llm_postprocessed.get("warnings") or grounded_postprocessed.get("warnings") or [])
        pipeline_warnings.append("no_acceptable_patch_candidate")

    return {
        "final_patch_text": final_patch,
        "final_patch_source": final_source,
        "final_generation_status": llm_status,
        "final_error_message": llm_error,
        "llm_prompt": prompt if save_prompt else "",
        "llm_prompt_metadata": prompt_metadata if save_prompt else {},
        "llm_patch_raw": llm_raw,
        "llm_generation_status": llm_status,
        "llm_error_message": llm_error,
        "llm_latency_seconds": generated.get("latency_seconds"),
        "llm_postprocess_status": llm_postprocessed.get("postprocess_status"),
        "llm_postprocess_warnings": list(llm_postprocessed.get("warnings") or []),
        "llm_verifier": llm_verifier,
        "llm_quality": llm_quality,
        "grounded_patch_text": grounded_final_patch,
        "grounded_patch_status": grounded.get("patch_status"),
        "grounded_postprocess_status": grounded_postprocessed.get("postprocess_status"),
        "grounded_postprocess_warnings": list(grounded_postprocessed.get("warnings") or []),
        "grounded_verifier": grounded_verifier,
        "grounded_quality": grounded_quality,
        "postprocess_status": final_postprocess_status,
        "postprocess_warnings": final_postprocess_warnings,
        "verifier": final_verifier,
        "quality": final_quality,
        "allowed_facts": allowed_facts,
        "grounding_tokens": grounding_tokens,
        "patch_pipeline_warnings": pipeline_warnings,
    }