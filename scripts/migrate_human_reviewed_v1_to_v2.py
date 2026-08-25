from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PRIMARY_STAGE2 = {"api_reference", "configuration", "developer_setup", "model_contract"}
LABEL_SOURCE = "human_reviewed_final_v2"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def as_bool(value: Any, row_id: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.lower() in {"true", "false"}:
        return value.lower() == "true"
    raise ValueError(f"{row_id}: existing human decision is not boolean")


def normalize_category(category: Any, positive: bool) -> str:
    if not positive:
        return "no_update"
    text = str(category or "").strip()
    return text if text in PRIMARY_STAGE2 else "other_documentation"


def migrate_row(row: dict[str, Any], index: int) -> dict[str, Any]:
    row_id = str(row.get("case_id") or row.get("id") or f"row_{index}")
    existing_decision = row.get("gold_docs_update_required", row.get("human_docs_update_required"))
    docs_required = as_bool(existing_decision, row_id)
    original_category = str(row.get("gold_doc_category") or row.get("human_doc_category") or "").strip()
    human_category = normalize_category(original_category, docs_required)
    copied = dict(row)
    copied["review_status"] = "approved"
    copied["human_docs_update_required"] = docs_required
    copied["original_human_doc_category"] = original_category or ("no_update" if not docs_required else "")
    copied["human_doc_category"] = human_category
    copied["human_label_notes"] = str(row.get("human_label_notes") or row.get("manual_label_notes") or "")
    copied["label_source"] = LABEL_SOURCE
    copied["human_review_complete"] = True
    copied["migrated_from_human_reviewed_v1"] = True
    copied["historical_label_source_audit"] = row.get("label_source")
    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate fully human-reviewed V1/4k rows into Final V2 review format.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--attest-all-rows-human-reviewed", action="store_true")
    args = parser.parse_args()
    if not args.attest_all_rows_human_reviewed:
        raise SystemExit("Refusing migration without --attest-all-rows-human-reviewed")
    rows = [migrate_row(row, index) for index, row in enumerate(load_jsonl(Path(args.input)), 1)]
    write_jsonl(Path(args.output), rows)
    print(json.dumps({"status": "ok", "rows": len(rows), "output": args.output}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
