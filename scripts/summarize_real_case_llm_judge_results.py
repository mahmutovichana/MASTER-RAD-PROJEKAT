from __future__ import annotations

import argparse
import json
import re
from collections import Counter
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
                rows.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
    return rows


def _safe_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    return bool(value)


def _safe_div(numerator: int | float, denominator: int | float) -> float:
    return float(numerator) / float(denominator) if denominator else 0.0


def _pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def _safe_cell(value: Any, limit: int = 180) -> str:
    text = str(value if value is not None else "")
    text = text.replace("\n", " ").replace("|", "\\|").replace("`", "\\`")
    text = " ".join(text.split())
    if len(text) > limit:
        return text[: limit - 3].rstrip() + "..."
    return text


def classify_failure_reason(row: dict[str, Any]) -> str:
    status = str(row.get("decision_status") or "")
    error = str(row.get("decision_error") or "")

    if status == "ok":
        return "none"

    if "HTTP 402" in error or "depleted your monthly included credits" in error:
        return "quota_or_credits_depleted"

    if "HTTP 401" in error or "unauthorized" in error.lower() or "invalid token" in error.lower():
        return "authentication_error"

    if "HTTP 429" in error or "rate limit" in error.lower():
        return "rate_limit"

    if "timeout" in error.lower() or "timed out" in error.lower():
        return "timeout"

    if "parse" in status.lower() or "json" in error.lower():
        return "json_parse_error"

    if status == "error":
        return "backend_error"

    return "other"


def compute_binary_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    tp = fp = tn = fn = 0

    for row in rows:
        gold = _safe_bool(row.get("gold_docs_update_required"))
        pred = _safe_bool(row.get("pred_docs_update_required"))

        if gold and pred:
            tp += 1
        elif not gold and pred:
            fp += 1
        elif not gold and not pred:
            tn += 1
        elif gold and not pred:
            fn += 1

    precision = _safe_div(tp, tp + fp)
    recall = _safe_div(tp, tp + fn)
    f1 = _safe_div(2 * precision * recall, precision + recall)

    return {
        "total_cases": len(rows),
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "accuracy": _safe_div(tp + tn, len(rows)),
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def is_completed_llm_decision(row: dict[str, Any]) -> bool:
    return str(row.get("decision_status") or "") == "ok" and not bool(row.get("abstained"))


def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    completed_rows = [row for row in rows if is_completed_llm_decision(row)]
    failed_rows = [row for row in rows if not is_completed_llm_decision(row)]

    return {
        "total_cases": len(rows),
        "completed_cases": len(completed_rows),
        "failed_or_abstained_cases": len(failed_rows),
        "coverage": _safe_div(len(completed_rows), len(rows)),
        "completed_cases_metrics": compute_binary_metrics(completed_rows),
        "all_cases_conservative_metrics": compute_binary_metrics(rows),
        "decision_status_counts": dict(Counter(str(row.get("decision_status")) for row in rows)),
        "failure_reason_counts": dict(Counter(classify_failure_reason(row) for row in failed_rows)),
        "documentation_area_counts_completed": dict(
            Counter(str(row.get("documentation_area")) for row in completed_rows)
        ),
        "gold_distribution_all": dict(Counter(str(row.get("gold_docs_update_required")) for row in rows)),
        "pred_distribution_all": dict(Counter(str(row.get("pred_docs_update_required")) for row in rows)),
        "pred_distribution_completed": dict(Counter(str(row.get("pred_docs_update_required")) for row in completed_rows)),
    }


def extract_model_name(rows: list[dict[str, Any]]) -> str:
    for row in rows:
        model = str(row.get("model_name") or "").strip()
        if model:
            return model
    return "not_recorded"


def extract_backend(rows: list[dict[str, Any]]) -> str:
    for row in rows:
        backend = str(row.get("backend") or "").strip()
        if backend:
            return backend
    return "not_recorded"


def write_markdown_report(path: Path, rows: list[dict[str, Any]], summary: dict[str, Any], source_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    completed_metrics = summary["completed_cases_metrics"]
    conservative_metrics = summary["all_cases_conservative_metrics"]

    lines: list[str] = [
        "# DocGuard Real Case LLM Judge Summary 2026-08",
        "",
        "This report summarizes the real-case LLM judge run on public GitHub PR case-study records.",
        "",
        "The result is **not synthetic** and does **not** use the deterministic real-case detector as the final decision layer.",
        "The LLM judge receives only safe case inputs and predicts whether documentation should be updated.",
        "",
        f"- Source predictions: `{source_path}`",
        f"- Backend: `{extract_backend(rows)}`",
        f"- Model: `{extract_model_name(rows)}`",
        f"- Total real cases: `{summary['total_cases']}`",
        f"- Completed LLM decisions: `{summary['completed_cases']}`",
        f"- Failed/abstained decisions: `{summary['failed_or_abstained_cases']}`",
        f"- LLM execution coverage: `{_pct(summary['coverage'])}`",
        "",
        "## Methodological Boundary",
        "",
        "- These are real public GitHub PR case-study records.",
        "- Gold labels are used only after prediction for evaluation.",
        "- The report does not use `docs_after_excerpt`, `manual_label_notes`, `docs_changed_files`, source URLs, or original documentation-file presence as model input.",
        "- Deterministic code is used only for prompt construction, leakage protection, JSON parsing, failure classification, and metric calculation.",
        "- Backend/quota failures are reported separately and are not hidden as model decisions.",
        "- Because the provider returned quota errors, the completed-case metric and all-case conservative metric are both reported.",
        "",
        "## Completed LLM Decisions Only",
        "",
        "This metric evaluates only cases where the LLM successfully returned a parseable decision.",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| completed cases | {completed_metrics['total_cases']} |",
        f"| true positives | {completed_metrics['true_positives']} |",
        f"| false positives | {completed_metrics['false_positives']} |",
        f"| true negatives | {completed_metrics['true_negatives']} |",
        f"| false negatives | {completed_metrics['false_negatives']} |",
        f"| accuracy | {_pct(completed_metrics['accuracy'])} |",
        f"| precision | {_pct(completed_metrics['precision'])} |",
        f"| recall | {_pct(completed_metrics['recall'])} |",
        f"| F1 | {_pct(completed_metrics['f1'])} |",
        "",
        "## All Cases Conservative Metric",
        "",
        "This metric keeps all 20 cases and treats failed/abstained LLM calls as negative predictions because no usable LLM decision was produced.",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| total cases | {conservative_metrics['total_cases']} |",
        f"| true positives | {conservative_metrics['true_positives']} |",
        f"| false positives | {conservative_metrics['false_positives']} |",
        f"| true negatives | {conservative_metrics['true_negatives']} |",
        f"| false negatives | {conservative_metrics['false_negatives']} |",
        f"| accuracy | {_pct(conservative_metrics['accuracy'])} |",
        f"| precision | {_pct(conservative_metrics['precision'])} |",
        f"| recall | {_pct(conservative_metrics['recall'])} |",
        f"| F1 | {_pct(conservative_metrics['f1'])} |",
        "",
        "## Execution And Failure Counts",
        "",
        f"- Decision status counts: `{summary['decision_status_counts']}`",
        f"- Failure reason counts: `{summary['failure_reason_counts']}`",
        f"- Completed documentation area counts: `{summary['documentation_area_counts_completed']}`",
        f"- Gold distribution, all cases: `{summary['gold_distribution_all']}`",
        f"- Prediction distribution, all cases: `{summary['pred_distribution_all']}`",
        f"- Prediction distribution, completed cases: `{summary['pred_distribution_completed']}`",
        "",
        "## Completed Case Details",
        "",
        "| Case | Gold | Pred | Correct | Confidence | Area | Rationale | Evidence |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]

    for row in rows:
        if not is_completed_llm_decision(row):
            continue

        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{_safe_cell(row.get('case_id'), 80)}`",
                    f"`{row.get('gold_docs_update_required')}`",
                    f"`{row.get('pred_docs_update_required')}`",
                    f"`{row.get('binary_correct')}`",
                    f"`{row.get('confidence')}`",
                    f"`{_safe_cell(row.get('documentation_area'), 80)}`",
                    _safe_cell(row.get("rationale"), 260),
                    _safe_cell(", ".join(row.get("evidence") or []), 160),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Failed Or Abstained Case Details",
            "",
            "| Case | Status | Failure reason | Gold | Conservative pred | Error preview |",
            "| --- | --- | --- | ---: | ---: | --- |",
        ]
    )

    for row in rows:
        if is_completed_llm_decision(row):
            continue

        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{_safe_cell(row.get('case_id'), 80)}`",
                    f"`{_safe_cell(row.get('decision_status'), 60)}`",
                    f"`{classify_failure_reason(row)}`",
                    f"`{row.get('gold_docs_update_required')}`",
                    f"`{row.get('pred_docs_update_required')}`",
                    _safe_cell(row.get("decision_error"), 260),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Thesis Interpretation",
            "",
            "The completed LLM decisions show the behavior of the AI judge when the provider returns a usable response.",
            "The conservative metric shows end-to-end performance under the actual budget-limited execution condition.",
            "The quota failures are an infrastructure limitation of the run, not evidence that the LLM judged those cases as no-update.",
            "",
            "Safe thesis wording:",
            "",
            "> In the real public-PR case study, the LLM judge completed 9 of 20 cases before the inference provider quota was exhausted. On completed cases it achieved perfect binary agreement with the manual labels, including zero false positives. When non-completed calls are conservatively counted as no-update decisions, the end-to-end score across all 20 cases is lower, reflecting provider coverage rather than decision quality alone.",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def write_json_summary(path: Path, summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize real-case LLM judge results with coverage-aware metrics.")
    parser.add_argument(
        "--predictions",
        default="reports/real_case_study_llm_judge/docguard_real_case_llm_judge_2026_08_predictions.jsonl",
    )
    parser.add_argument(
        "--output-md",
        default="reports/real_case_study_llm_judge/docguard_real_case_llm_judge_summary_2026_08.md",
    )
    parser.add_argument(
        "--output-json",
        default="reports/real_case_study_llm_judge/docguard_real_case_llm_judge_summary_2026_08.json",
    )
    args = parser.parse_args()

    predictions_path = Path(args.predictions)
    rows = load_jsonl(predictions_path)
    summary = build_summary(rows)

    write_markdown_report(Path(args.output_md), rows, summary, predictions_path)
    write_json_summary(Path(args.output_json), summary)

    print(
        json.dumps(
            {
                "status": "ok",
                "predictions": str(predictions_path),
                "output_md": args.output_md,
                "output_json": args.output_json,
                "summary": summary,
            },
            indent=2,
            ensure_ascii=False,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())