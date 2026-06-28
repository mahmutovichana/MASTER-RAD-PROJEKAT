from __future__ import annotations

from docguard_hybrid.signal_extractor import extract_signals, signal_names


MAX_DIFF_CHARS = 5000
INPUT_MODES = [
    "raw_diff_only",
    "raw_diff_plus_docs",
    "raw_diff_plus_signals",
    "raw_diff_plus_summary",
    "full_current",
]
DEFAULT_INPUT_MODE = "raw_diff_plus_docs"


def truncate_text(text: str, max_chars: int = MAX_DIFF_CHARS) -> str:
    if len(text) <= max_chars:
        return text
    head = text[: max_chars // 2]
    tail = text[-max_chars // 2 :]
    return f"{head}\n...[truncated]...\n{tail}"


def build_input_text(record: dict, max_diff_chars: int = MAX_DIFF_CHARS, input_mode: str = DEFAULT_INPUT_MODE) -> str:
    if input_mode not in INPUT_MODES:
        raise ValueError(f"Unsupported input mode: {input_mode}")
    signals = signal_names(extract_signals(record))
    parts = ["changed_files: " + ", ".join(record.get("changed_files", []))]
    if input_mode in {"raw_diff_plus_summary", "full_current"}:
        parts.append("change_summary: " + str(record.get("change_summary") or record.get("change_intent_summary") or ""))
    if input_mode in {"raw_diff_plus_signals", "full_current"}:
        parts.append("signals: " + ", ".join(signals))
    if input_mode in {"raw_diff_plus_docs", "raw_diff_plus_signals", "raw_diff_plus_summary", "full_current"}:
        parts.append("docs_before_excerpt: " + str(record.get("docs_before_excerpt") or ""))
    parts.append("code_diff: " + truncate_text(str(record.get("code_diff") or ""), max_diff_chars))
    return "\n".join(part for part in parts if part.strip())
