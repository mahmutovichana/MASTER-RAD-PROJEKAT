from __future__ import annotations

import argparse
import csv
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


def safe_str(value: Any, limit: int | None = None) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if limit is not None and len(text) > limit:
        return text[: limit - 3].rstrip() + "..."
    return text


def compact(value: Any, limit: int = 400) -> str:
    text = safe_str(value)
    text = " ".join(text.split())
    if len(text) > limit:
        return text[: limit - 3].rstrip() + "..."
    return text


def load_by_case_id(path: Path) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("case_id")): row
        for row in load_jsonl(path)
    }


def get_nested(row: dict[str, Any], *keys: str) -> Any:
    current: Any = row
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def build_review_rows(
    *,
    locked_test_path: Path,
    full_labeling_pack_path: Path,
    classifier_predictions_path: Path,
    llm_predictions_path: Path | None,
) -> list[dict[str, Any]]:
    locked_rows = load_jsonl(locked_test_path)
    full_pack = load_by_case_id(full_labeling_pack_path)

    classifier_rows = [
        row
        for row in load_jsonl(classifier_predictions_path)
        if str(row.get("dataset_split")) == "locked_test"
    ]
    classifier_by_case = {
        str(row.get("case_id")): row
        for row in classifier_rows
    }

    llm_by_case: dict[str, dict[str, Any]] = {}
    if llm_predictions_path is not None and llm_predictions_path.exists():
        llm_by_case = load_by_case_id(llm_predictions_path)

    review_rows: list[dict[str, Any]] = []

    for locked in locked_rows:
        case_id = str(locked.get("case_id"))
        full = full_pack.get(case_id, {})
        classifier = classifier_by_case.get(case_id, {})
        llm = llm_by_case.get(case_id, {})

        gold = bool(locked.get("gold_docs_update_required"))
        cls_pred = bool(classifier.get("swept_pred_docs_update_required", classifier.get("pred_docs_update_required", False)))
        llm_pred = llm.get("pred_docs_update_required")

        if gold and not cls_pred:
            cls_error_type = "FN"
        elif not gold and cls_pred:
            cls_error_type = "FP"
        else:
            cls_error_type = "correct"

        audit = full.get("audit_labeling_context") if isinstance(full.get("audit_labeling_context"), dict) else {}
        model_input = full.get("model_input") if isinstance(full.get("model_input"), dict) else {}

        review_rows.append(
            {
                "case_id": case_id,
                "repository": locked.get("repository"),
                "source_url": locked.get("source_url"),
                "language": locked.get("language"),
                "candidate_type": locked.get("candidate_type"),
                "gold_docs_update_required": gold,
                "gold_doc_category": locked.get("gold_doc_category"),
                "label_confidence": locked.get("label_confidence"),
                "classifier_probability": classifier.get("pred_probability"),
                "classifier_pred_thresholded": cls_pred,
                "classifier_error_type": cls_error_type,
                "llm_status": llm.get("decision_status", ""),
                "llm_pred": llm_pred if llm else "",
                "llm_area": llm.get("documentation_area", ""),
                "llm_rationale": compact(llm.get("rationale", ""), 300),
                "pr_title": compact(locked.get("pr_title"), 250),
                "code_changed_files": compact(model_input.get("code_changed_files") or locked.get("code_changed_files"), 500),
                "docs_changed_files": compact(audit.get("docs_changed_files"), 500),
                "code_diff_excerpt": compact(model_input.get("code_diff_excerpt") or locked.get("code_diff_excerpt"), 1200),
                "docs_before_excerpt": compact(model_input.get("docs_before_excerpt") or locked.get("docs_before_excerpt"), 800),
                "docs_after_excerpt": compact(audit.get("docs_after_excerpt"), 800),
                "review_gold_docs_update_required": "",
                "review_label_confidence": "",
                "review_notes": "",
            }
        )

    review_rows.sort(
        key=lambda row: (
            0 if row["classifier_error_type"] != "correct" else 1,
            str(row["classifier_error_type"]),
            str(row["case_id"]),
        )
    )

    return review_rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fieldnames = list(rows[0].keys())

    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    fp = sum(1 for row in rows if row["classifier_error_type"] == "FP")
    fn = sum(1 for row in rows if row["classifier_error_type"] == "FN")
    correct = sum(1 for row in rows if row["classifier_error_type"] == "correct")

    lines = [
        "# DocGuard Locked-Test Review Pack",
        "",
        f"- Total locked-test cases: `{len(rows)}`",
        f"- Classifier false positives: `{fp}`",
        f"- Classifier false negatives: `{fn}`",
        f"- Classifier correct: `{correct}`",
        "",
        "Review priority: FP/FN first, then correct cases.",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"## {row['case_id']} — {row['classifier_error_type']}",
                "",
                f"- Repository: `{row['repository']}`",
                f"- Source: `{row['source_url']}`",
                f"- Gold: `{row['gold_docs_update_required']}` / `{row['gold_doc_category']}` / `{row['label_confidence']}`",
                f"- Classifier probability: `{row['classifier_probability']}`",
                f"- Classifier prediction: `{row['classifier_pred_thresholded']}`",
                f"- LLM status/prediction: `{row['llm_status']}` / `{row['llm_pred']}`",
                f"- LLM rationale: {row['llm_rationale']}",
                "",
                "**Changed code files:**",
                "",
                f"`{row['code_changed_files']}`",
                "",
                "**Docs changed files:**",
                "",
                f"`{row['docs_changed_files']}`",
                "",
                "**Code diff excerpt:**",
                "",
                "```text",
                safe_str(row["code_diff_excerpt"], 1800),
                "```",
                "",
                "**Docs before excerpt:**",
                "",
                "```text",
                safe_str(row["docs_before_excerpt"], 1200),
                "```",
                "",
                "**Docs after excerpt / audit context:**",
                "",
                "```text",
                safe_str(row["docs_after_excerpt"], 1200),
                "```",
                "",
                "---",
                "",
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build locked-test review pack combining gold labels, classifier predictions and LLM predictions.")
    parser.add_argument("--locked-test", required=True)
    parser.add_argument("--full-labeling-pack", required=True)
    parser.add_argument("--classifier-predictions", required=True)
    parser.add_argument("--llm-predictions", default=None)
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    rows = build_review_rows(
        locked_test_path=Path(args.locked_test),
        full_labeling_pack_path=Path(args.full_labeling_pack),
        classifier_predictions_path=Path(args.classifier_predictions),
        llm_predictions_path=Path(args.llm_predictions) if args.llm_predictions else None,
    )

    write_csv(Path(args.output_csv), rows)
    write_markdown(Path(args.output_md), rows)

    result = {
        "status": "ok",
        "records": len(rows),
        "false_positives": sum(1 for row in rows if row["classifier_error_type"] == "FP"),
        "false_negatives": sum(1 for row in rows if row["classifier_error_type"] == "FN"),
        "correct": sum(1 for row in rows if row["classifier_error_type"] == "correct"),
        "output_csv": args.output_csv,
        "output_md": args.output_md,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())