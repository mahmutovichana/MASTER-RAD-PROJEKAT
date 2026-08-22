from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"JSONL row must be an object at {path}:{line_number}")
            rows.append(row)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def build_retry_set(
    *,
    original_input: Path,
    predictions: Path,
    output: Path,
    retry_statuses: set[str],
) -> dict[str, Any]:
    original_rows = load_jsonl(original_input)
    prediction_rows = load_jsonl(predictions)

    retry_case_ids = {
        str(row.get("case_id"))
        for row in prediction_rows
        if str(row.get("decision_status")) in retry_statuses
    }

    retry_rows = [
        row
        for row in original_rows
        if str(row.get("case_id")) in retry_case_ids
    ]

    write_jsonl(output, retry_rows)

    return {
        "status": "ok",
        "original_input": str(original_input),
        "predictions": str(predictions),
        "output": str(output),
        "retry_statuses": sorted(retry_statuses),
        "retry_case_ids": len(retry_case_ids),
        "retry_rows": len(retry_rows),
        "missing_from_original": sorted(retry_case_ids - {str(row.get("case_id")) for row in original_rows}),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build retry input JSONL for failed LLM judge cases.")
    parser.add_argument("--original-input", required=True)
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--retry-statuses", default="error,parse_error")
    args = parser.parse_args()

    retry_statuses = {
        item.strip()
        for item in args.retry_statuses.split(",")
        if item.strip()
    }

    result = build_retry_set(
        original_input=Path(args.original_input),
        predictions=Path(args.predictions),
        output=Path(args.output),
        retry_statuses=retry_statuses,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())