from __future__ import annotations

from docguard_hybrid.signal_extractor import extract_signals, signal_names


def text_for_record(record: dict) -> str:
    signals = signal_names(extract_signals(record))
    return " ".join([
        " ".join(record.get("changed_files", [])),
        record.get("code_diff", ""),
        record.get("docs_before_excerpt", ""),
        " ".join(signals),
    ])
