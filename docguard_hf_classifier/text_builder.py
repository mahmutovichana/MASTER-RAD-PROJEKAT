from __future__ import annotations

from docguard_hybrid.signal_extractor import extract_signals, signal_names


MAX_DIFF_CHARS = 5000


def truncate_text(text: str, max_chars: int = MAX_DIFF_CHARS) -> str:
    if len(text) <= max_chars:
        return text
    head = text[: max_chars // 2]
    tail = text[-max_chars // 2 :]
    return f"{head}\n...[truncated]...\n{tail}"


def build_input_text(record: dict, max_diff_chars: int = MAX_DIFF_CHARS) -> str:
    signals = signal_names(extract_signals(record))
    parts = [
        "changed_files: " + ", ".join(record.get("changed_files", [])),
        "change_summary: " + str(record.get("change_summary") or record.get("change_intent_summary") or ""),
        "signals: " + ", ".join(signals),
        "docs_before_excerpt: " + str(record.get("docs_before_excerpt") or ""),
        "code_diff: " + truncate_text(str(record.get("code_diff") or ""), max_diff_chars),
    ]
    return "\n".join(part for part in parts if part.strip())

