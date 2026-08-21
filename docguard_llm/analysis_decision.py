from __future__ import annotations

import json
import re
from typing import Any

from docguard_llm.llm_generator import generate_documentation_patch


ALLOWED_TARGETS = {
    "docs/configuration.md": ("configuration", "Environment Variables"),
    "docs/api.md": ("api_reference", "API Reference"),
    "docs/developer-setup.md": ("developer_setup", "Local Development"),
    "docs/workflows.md": ("workflow_documentation", "Workflows"),
    "docs/architecture.md": ("architecture_flow", "Architecture"),
    "docs/models.md": ("model_contract", "Data Models"),
    "docs/testing.md": ("testing_instructions", "Testing"),
    "CHANGELOG.md": ("changelog", "Unreleased"),
}


def _extract_json(text: str) -> dict[str, Any]:
    stripped = (text or "").strip()
    stripped = re.sub(r"^```(?:json)?\s*", "", stripped, flags=re.IGNORECASE)
    stripped = re.sub(r"\s*```$", "", stripped)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", stripped, flags=re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def _normalize_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1", "update_required"}
    return bool(value)


def _normalize_decision(data: dict[str, Any]) -> dict[str, Any]:
    docs_required = _normalize_bool(data.get("docs_update_required"))
    target = str(data.get("target_doc_file") or "").strip()
    if target not in ALLOWED_TARGETS:
        target = ""
        docs_required = False
    category, section = ALLOWED_TARGETS.get(target, ("no_update", "Documentation"))
    if not docs_required:
        target = ""
        category = "no_update"
        section = "Documentation"
    raw_confidence = data.get("confidence", 0.75 if docs_required else 0.65)
    try:
        confidence = float(raw_confidence)
    except (TypeError, ValueError):
        confidence = 0.75 if docs_required else 0.65
    confidence = max(0.0, min(1.0, confidence))
    scenario = str(data.get("scenario_type") or ("llm_detected_documentation_change" if docs_required else "llm_no_update")).strip()
    scenario = re.sub(r"[^a-zA-Z0-9_]+", "_", scenario).strip("_").lower() or "llm_detected_documentation_change"
    reason = str(data.get("reason") or "LLM analysis decision based on the live code diff and current documentation.").strip()
    return {
        "docs_update_required": docs_required,
        "doc_category": category,
        "target_doc_file": target,
        "target_section": section,
        "scenario_type": scenario,
        "confidence": confidence,
        "reason": reason,
    }


def build_analysis_prompt(*, changed_files: list[str], code_diff: str, docs_before: str) -> str:
    targets = "\n".join(f"- {path}: {category}, section {section}" for path, (category, section) in ALLOWED_TARGETS.items())
    return f"""You are DocGuard, a careful software documentation reviewer.

Decide whether the current code diff requires a documentation update.

Use only the supplied changed files, code diff, and current documentation text.
Do not assume hidden behavior. Do not invent fields, routes, defaults, auth, or status codes.
If documentation already describes the exact changed behavior and exact default values, return docs_update_required=false.
If documentation mentions a setting but has the wrong value from the code diff, return docs_update_required=true.

Allowed target files:
{targets}

Return only compact JSON with these keys:
docs_update_required: boolean
target_doc_file: one allowed target path, or empty string
scenario_type: short snake_case label
confidence: number from 0 to 1
reason: one short sentence grounded in the diff

Changed files:
{json.dumps(changed_files, ensure_ascii=False)}

Code diff:
```diff
{code_diff[:6000]}
```

Current documentation:
```markdown
{docs_before[:6000]}
```
"""


def generate_analysis_decision(
    *,
    changed_files: list[str],
    code_diff: str,
    docs_before: str,
    backend: str,
    model_name: str | None,
    max_new_tokens: int = 256,
    temperature: float = 0.0,
) -> dict[str, Any]:
    backend_map = {
        "llm-mock": "mock",
        "llm-hf": "hf",
        "llm-openai-compatible": "openai_compatible",
        "llm-ollama": "ollama",
    }
    if backend == "llm-mock":
        return {
            "decision_status": "ok",
            "raw_decision": "{}",
            **_normalize_decision(
                {
                    "docs_update_required": False,
                    "target_doc_file": "",
                    "scenario_type": "llm_mock_no_update",
                    "confidence": 0.5,
                    "reason": "Mock analysis backend validates wiring only.",
                }
            ),
        }
    generated = generate_documentation_patch(
        build_analysis_prompt(changed_files=changed_files, code_diff=code_diff, docs_before=docs_before),
        backend=backend_map[backend],
        model_name=model_name,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
    )
    if generated.get("generation_status") != "ok":
        return {
            "decision_status": "error",
            "decision_error": generated.get("error_message") or "LLM analysis generation failed.",
            "raw_decision": generated.get("patch_text") or "",
            **_normalize_decision({"docs_update_required": False}),
        }
    try:
        parsed = _extract_json(str(generated.get("patch_text") or ""))
        return {
            "decision_status": "ok",
            "decision_error": "",
            "raw_decision": generated.get("patch_text") or "",
            **_normalize_decision(parsed),
        }
    except Exception as exc:
        return {
            "decision_status": "error",
            "decision_error": f"Could not parse LLM analysis JSON: {exc}",
            "raw_decision": generated.get("patch_text") or "",
            **_normalize_decision({"docs_update_required": False}),
        }
