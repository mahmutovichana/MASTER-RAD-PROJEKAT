from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


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


def pr_key(row: dict[str, Any]) -> str:
    repo = str(row.get("repository") or row.get("repo") or "").strip().lower()
    pr = row.get("pr_number")
    return f"pr:{repo}#{int(pr)}" if repo and pr is not None else ""


def keys(row: dict[str, Any]) -> list[str]:
    return [key for key in [pr_key(row), f"url:{row.get('source_url') or row.get('url') or ''}", f"case:{row.get('case_id') or row.get('id') or ''}"] if not key.endswith(":") and key not in {"url:", "case:"}]


def human_label(row: dict[str, Any]) -> tuple[Any, Any]:
    return (row.get("human_docs_update_required"), row.get("human_doc_category"))


def merge_sources(paths: list[Path]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    index: dict[str, dict[str, Any]] = {}
    for path in paths:
        for row in load_jsonl(path):
            matched = next((index[key] for key in keys(row) if key in index), None)
            if matched is None:
                merged.append(row)
                for key in keys(row):
                    index[key] = row
                continue
            if human_label(matched) != human_label(row):
                conflicts.append({"conflict_reason": "duplicate_pr_with_conflicting_human_labels", "existing": matched, "incoming": row})
                continue
            for key in keys(row):
                index[key] = matched
    manifest = {
        "input_files": [str(path) for path in paths],
        "merged_rows": len(merged),
        "conflicts": len(conflicts),
        "human_label_counts": dict(Counter(str(human_label(row)) for row in merged)),
    }
    return merged, conflicts, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge Final V2 human review sources with strict duplicate conflict handling.")
    parser.add_argument("--input", action="append", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    merged, conflicts, manifest = merge_sources([Path(path) for path in args.input])
    write_jsonl(out_dir / "merged_human_review.jsonl", merged)
    write_jsonl(out_dir / "merge_conflicts.jsonl", conflicts)
    (out_dir / "merge_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"status": "conflicts" if conflicts else "ok", **manifest}, indent=2))
    return 1 if conflicts else 0


if __name__ == "__main__":
    raise SystemExit(main())
