from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


FINAL_CATEGORIES = {
    "api_reference",
    "configuration",
    "developer_setup",
    "model_contract",
    "other_documentation",
    "no_update",
}

PUBLIC_PATTERNS = [
    ("api_reference", re.compile(r"\b(api|endpoint|route|controller|openapi|swagger|graphql|webhook|sdk|client)\b", re.I)),
    ("configuration", re.compile(r"\b(config|configuration|setting|settings|env|environment|option|flag|parameter)\b", re.I)),
    ("model_contract", re.compile(r"\b(schema|model|dto|interface|type|types|contract|entity|migration|database|sql)\b", re.I)),
    ("developer_setup", re.compile(r"\b(setup|install|dependency|build|local development|dev server|getting started)\b", re.I)),
]

NEGATIVE_RE = re.compile(r"\b(test|tests|fixture|mock|snapshot|format|lint|typo|refactor|dependabot|renovate|ci)\b", re.I)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"Row at {path}:{line_number} is not an object")
            rows.append(row)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)] if value else []


def text_blob(row: dict[str, Any]) -> str:
    return "\n".join(
        [
            str(row.get("language") or row.get("language_hint") or ""),
            " ".join(as_list(row.get("code_changed_files"))),
            str(row.get("code_diff_excerpt") or ""),
            str(row.get("docs_before_excerpt") or ""),
        ]
    )


def suggest(row: dict[str, Any]) -> tuple[bool, str, float, str]:
    blob = text_blob(row)
    if NEGATIVE_RE.search(blob):
        return False, "no_update", 0.7, "Prefill: safe pre-outcome code/docs-before terms suggest no documentation update."
    for category, pattern in PUBLIC_PATTERNS:
        if pattern.search(blob):
            return True, category, 0.58, f"Prefill: safe pre-outcome public documentation signal suggests {category}."
    return False, "no_update", 0.52, "Prefill: no strong safe pre-outcome documentation signal found."


def prefill_row(row: dict[str, Any]) -> dict[str, Any]:
    copied = {key: value for key, value in row.items() if not key.startswith("gold_")}
    docs_required, category, confidence, reason = suggest(copied)
    copied.update(
        {
            "suggested_docs_update_required": docs_required,
            "suggested_doc_category": category,
            "suggested_confidence": confidence,
            "suggested_reason": reason,
            "review_status": "",
            "human_docs_update_required": None,
            "human_doc_category": "",
            "human_label_notes": "",
        }
    )
    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description="Prefill a Final V2 human review JSONL sheet without writing gold labels.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = [prefill_row(row) for row in load_jsonl(Path(args.input))]
    for row in rows:
        forbidden = [key for key in row if key.startswith("gold_")]
        if forbidden:
            raise RuntimeError(f"Prefill attempted to emit forbidden gold fields: {forbidden}")
        if row["suggested_doc_category"] not in FINAL_CATEGORIES:
            raise RuntimeError(f"Unsupported suggested category: {row['suggested_doc_category']}")
    write_jsonl(Path(args.output), rows)
    print(json.dumps({"status": "ok", "rows": len(rows), "output": args.output}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
