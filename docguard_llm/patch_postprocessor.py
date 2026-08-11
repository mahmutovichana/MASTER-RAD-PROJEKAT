from __future__ import annotations

import re
from typing import Any

from docguard_llm.config import PATCH_TARGET_FILES


ROLE_PREFIX_RE = re.compile(r"^(assistant|user|system)\s*:\s*", re.IGNORECASE)
NOISY_HEADING_RE = re.compile(r"^\s*(?:patch|documentation patch|markdown patch)\s*:?\s*$", re.IGNORECASE)
TARGET_LABEL_RE = re.compile(r"^\s*(?:docs/[A-Za-z0-9_.-]+\.md|CHANGELOG\.md|README\.md)\s*:?\s*$")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")


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
    cleaned_lines: list[str] = []
    previous_heading = ""
    for raw_line in text.splitlines():
        line = ROLE_PREFIX_RE.sub("", raw_line).rstrip()
        stripped = line.strip()
        if not stripped:
            if cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("")
            continue
        if NOISY_HEADING_RE.match(stripped) or TARGET_LABEL_RE.match(stripped) or TABLE_SEPARATOR_RE.match(stripped):
            warnings.append("removed noisy model output line")
            continue
        if stripped.startswith("###") and stripped == previous_heading:
            warnings.append("removed duplicated heading")
            continue
        if stripped.startswith("###"):
            previous_heading = stripped
        cleaned_lines.append(line)
    text = "\n".join(cleaned_lines).strip()
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
        content_lines = []
        for line in text.splitlines():
            if not line.strip():
                continue
            if line.lstrip().startswith("|"):
                warnings.append("converted table-like row into bullet")
                content_lines.append("+ - " + " ".join(part.strip() for part in line.strip("| ").split("|") if part.strip()))
                continue
            content_lines.append(line if line.startswith("+") else f"+{line}")
        content = "\n".join(content_lines)
        text = f"@@ {section}\n{content}"
        warnings.append("normalized patch into lightweight diff form")
    else:
        lines = text.splitlines()
        normalized = [lines[0]]
        for line in lines[1:]:
            if not line.strip():
                continue
            if line.lstrip().startswith("|"):
                warnings.append("converted table-like row into bullet")
                normalized.append("+ - " + " ".join(part.strip() for part in line.strip("| ").split("|") if part.strip()))
            elif line.startswith(("+", "-")):
                normalized.append(line)
            else:
                normalized.append(f"+{line}")
        text = "\n".join(normalized)
    return {"patch_text": text.strip(), "postprocess_status": "ok", "warnings": warnings}
