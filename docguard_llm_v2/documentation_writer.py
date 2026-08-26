from __future__ import annotations

from typing import Any

from docguard_llm_v2.change_analyzer import parse_json
from docguard_llm_v2.generation_options import GenerationOptions, call_llm
from docguard_llm_v2.prompt_templates import writer_prompt
from docguard_llm_v2.schemas import WriterCandidate


def build_writer_candidate(data: dict[str, Any]) -> WriterCandidate:
    return WriterCandidate(
        target_document_path=str(data.get("target_document_path") or ""),
        target_section=str(data.get("target_section") or ""),
        patch_markdown=str(data.get("patch_markdown") or ""),
        writer_confidence=float(data.get("writer_confidence") or 0.0),
    )


def write_documentation(*, code_diff: str, predicted_category: str, analysis: dict[str, Any], retrieved_candidates: list[dict[str, Any]], llm: Any, model: str | None = None, generation_options: GenerationOptions | None = None) -> dict[str, Any]:
    raw = call_llm(llm, writer_prompt(code_diff=code_diff, predicted_category=predicted_category, analysis=analysis, candidates=retrieved_candidates), model=model, purpose="writer", options=generation_options)
    return {"raw": raw, "candidate": build_writer_candidate(parse_json(raw))}
