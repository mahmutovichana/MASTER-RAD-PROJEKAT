from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
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


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if value is None:
        return []
    return [str(value)]


def pred_value(row: dict[str, Any]) -> bool:
    if "swept_pred_docs_update_required" in row:
        return bool(row.get("swept_pred_docs_update_required"))
    return bool(row.get("pred_docs_update_required"))


def error_type(row: dict[str, Any]) -> str:
    gold = bool(row.get("gold_docs_update_required"))
    pred = pred_value(row)

    if gold and pred:
        return "TP"
    if not gold and pred:
        return "FP"
    if not gold and not pred:
        return "TN"
    return "FN"


def compact(value: Any, limit: int = 500) -> str:
    text = " ".join(str(value or "").split())
    return text[: limit - 3] + "..." if len(text) > limit else text


def by_key_counts(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(Counter(str(row.get(key) or "unknown") for row in rows))


def nested_error_counts(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, int]]:
    result: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        result[str(row.get(key) or "unknown")][error_type(row)] += 1
    return {group: dict(counts) for group, counts in sorted(result.items())}


def load_cases(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None:
        return {}
    return {
        str(row.get("case_id")): row
        for row in load_jsonl(path)
        if row.get("case_id")
    }


def merged_row(row: dict[str, Any], cases: dict[str, dict[str, Any]]) -> dict[str, Any]:
    case_id = str(row.get("case_id"))
    full = cases.get(case_id, {})
    merged = dict(full)
    merged.update(row)
    merged["error_type"] = error_type(row)
    merged["pred_docs_update_required_effective"] = pred_value(row)
    return merged


def write_error_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "case_id",
        "dataset_split",
        "error_type",
        "pred_probability",
        "swept_threshold",
        "gold_docs_update_required",
        "pred_docs_update_required_effective",
        "repository",
        "language",
        "candidate_type",
        "gold_doc_category",
        "label_confidence",
        "source_url",
        "pr_title",
        "code_changed_files",
        "docs_changed_files",
        "manual_label_notes",
        "code_diff_excerpt_preview",
        "docs_before_excerpt_preview",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()

        for row in rows:
            writer.writerow(
                {
                    "case_id": row.get("case_id"),
                    "dataset_split": row.get("dataset_split"),
                    "error_type": row.get("error_type"),
                    "pred_probability": row.get("pred_probability"),
                    "swept_threshold": row.get("swept_threshold"),
                    "gold_docs_update_required": row.get("gold_docs_update_required"),
                    "pred_docs_update_required_effective": row.get("pred_docs_update_required_effective"),
                    "repository": row.get("repository"),
                    "language": row.get("language"),
                    "candidate_type": row.get("candidate_type"),
                    "gold_doc_category": row.get("gold_doc_category"),
                    "label_confidence": row.get("label_confidence"),
                    "source_url": row.get("source_url"),
                    "pr_title": row.get("pr_title"),
                    "code_changed_files": "; ".join(safe_list(row.get("code_changed_files"))),
                    "docs_changed_files": "; ".join(safe_list(row.get("docs_changed_files"))),
                    "manual_label_notes": row.get("manual_label_notes"),
                    "code_diff_excerpt_preview": compact(row.get("code_diff_excerpt"), 800),
                    "docs_before_excerpt_preview": compact(row.get("docs_before_excerpt"), 800),
                }
            )


def write_md(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        "# Real PR Classifier Error Analysis",
        "",
        f"- Prediction file: `{summary['prediction_file']}`",
        f"- Cases file: `{summary.get('cases_file') or 'not provided'}`",
        f"- Total rows: `{summary['total_rows']}`",
        "",
        "## Error counts",
        "",
    ]

    for key, value in summary["error_counts"].items():
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(["", "## Error counts by split", ""])
    for split, counts in summary["error_counts_by_split"].items():
        lines.append(f"- `{split}`: `{counts}`")

    lines.extend(["", "## Error counts by language", ""])
    for language, counts in summary["error_counts_by_language"].items():
        lines.append(f"- `{language}`: `{counts}`")

    lines.extend(["", "## Error counts by candidate type", ""])
    for candidate_type, counts in summary["error_counts_by_candidate_type"].items():
        lines.append(f"- `{candidate_type}`: `{counts}`")

    lines.extend(["", "## Top repositories by false negatives", ""])
    for repo, count in summary["top_false_negative_repositories"]:
        lines.append(f"- `{repo}`: `{count}`")

    lines.extend(["", "## Top repositories by false positives", ""])
    for repo, count in summary["top_false_positive_repositories"]:
        lines.append(f"- `{repo}`: `{count}`")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    *,
    predictions_path: Path,
    cases_path: Path | None,
    output_json: Path,
    output_md: Path,
    output_csv: Path,
) -> dict[str, Any]:
    predictions = load_jsonl(predictions_path)
    cases = load_cases(cases_path)
    rows = [merged_row(row, cases) for row in predictions]

    error_counts = dict(Counter(row["error_type"] for row in rows))
    fn_rows = [row for row in rows if row["error_type"] == "FN"]
    fp_rows = [row for row in rows if row["error_type"] == "FP"]

    summary = {
        "status": "ok",
        "prediction_file": str(predictions_path),
        "cases_file": str(cases_path) if cases_path else None,
        "total_rows": len(rows),
        "error_counts": error_counts,
        "error_counts_by_split": nested_error_counts(rows, "dataset_split"),
        "error_counts_by_language": nested_error_counts(rows, "language"),
        "error_counts_by_candidate_type": nested_error_counts(rows, "candidate_type"),
        "repository_counts": by_key_counts(rows, "repository"),
        "top_false_negative_repositories": Counter(str(row.get("repository") or "unknown") for row in fn_rows).most_common(20),
        "top_false_positive_repositories": Counter(str(row.get("repository") or "unknown") for row in fp_rows).most_common(20),
        "top_false_negatives": sorted(
            fn_rows,
            key=lambda item: float(item.get("pred_probability") or 0.0),
            reverse=True,
        )[:30],
        "top_false_positives": sorted(
            fp_rows,
            key=lambda item: float(item.get("pred_probability") or 0.0),
            reverse=True,
        )[:30],
    }

    write_json(output_json, summary)
    write_md(output_md, summary)
    write_error_csv(output_csv, rows)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze false positives and false negatives for real PR classifier predictions.")
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--cases", required=False)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--output-csv", required=True)
    args = parser.parse_args()

    result = run(
        predictions_path=Path(args.predictions),
        cases_path=Path(args.cases) if args.cases else None,
        output_json=Path(args.output_json),
        output_md=Path(args.output_md),
        output_csv=Path(args.output_csv),
    )

    print(json.dumps({k: v for k, v in result.items() if k not in {"top_false_negatives", "top_false_positives"}}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())