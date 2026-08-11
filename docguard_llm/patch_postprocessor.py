from __future__ import annotations

import re
from typing import Any

from docguard_llm.config import PATCH_TARGET_FILES


ROLE_PREFIX_RE = re.compile(r"^(assistant|user|system)\s*:\s*", re.IGNORECASE)


def _strip_markdown_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:diff|markdown|md)?\s*", "", stripped, flags=re.IGNORECASE)
        stripped = re.sub(r"\s*```$", "", stripped)
    return stripped.strip()


def postprocess_patch(
    raw_patch: str | None,
    target_doc_file: str,
    target_section: str | None = None,
    allowed_target_files: set[str] | None = None,
) -> dict[str, Any]:
    warnings: list[str] = []
    allowed = allowed_target_files or PATCH_TARGET_FILES
    if target_doc_file and target_doc_file not in allowed:
        return {"patch_text": None, "postprocess_status": "fail", "warnings": [f"unsupported target file: {target_doc_file}"]}
    text = _strip_markdown_fences(raw_patch or "")
    text = "\n".join(ROLE_PREFIX_RE.sub("", line).rstrip() for line in text.splitlines()).strip()
    if not text:
        return {"patch_text": None, "postprocess_status": "fail", "warnings": ["empty patch"]}
    mentioned_files = {match for match in re.findall(r"(?:docs/[A-Za-z0-9_.-]+\.md|CHANGELOG\.md|README\.md)", text)}
    unsupported = sorted(path for path in mentioned_files if path != target_doc_file)
    if unsupported:
        return {
            "patch_text": None,
            "postprocess_status": "fail",
            "warnings": [f"patch mentions unsupported target filename: {', '.join(unsupported)}"],
        }
    if not text.startswith("@@"):
        section = target_section or target_doc_file or "Documentation"
        content = "\n".join(line if line.startswith("+") else f"+{line}" for line in text.splitlines() if line.strip())
        text = f"@@ {section}\n{content}"
        warnings.append("normalized patch into lightweight diff form")
    return {"patch_text": text.strip(), "postprocess_status": "ok", "warnings": warnings}
