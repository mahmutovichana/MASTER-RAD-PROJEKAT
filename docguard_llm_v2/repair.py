from __future__ import annotations

from typing import Any

from docguard_llm_v2.change_analyzer import parse_json
from docguard_llm_v2.documentation_writer import build_writer_candidate
from docguard_llm_v2.generation_options import GenerationOptions, call_llm
from docguard_llm_v2.prompt_templates import repair_prompt
from docguard_llm_v2.schemas import SafetyResult, WriterCandidate, asdict_shallow


def repair_documentation(*, original_candidate: WriterCandidate, verifier_result: SafetyResult, analysis: dict[str, Any], code_diff: str, retrieved_candidates: list[dict[str, Any]], llm: Any, model: str | None = None, generation_options: GenerationOptions | None = None) -> dict[str, Any]:
    raw = call_llm(
        llm,
        repair_prompt(
            original_patch=original_candidate.patch_markdown,
            violations=[asdict_shallow(item) for item in verifier_result.violations],
            analysis=analysis,
            code_diff=code_diff,
            candidates=retrieved_candidates,
        ),
        model=model,
        purpose="repair",
        options=generation_options,
    )
    return {"raw": raw, "candidate": build_writer_candidate(parse_json(raw))}
