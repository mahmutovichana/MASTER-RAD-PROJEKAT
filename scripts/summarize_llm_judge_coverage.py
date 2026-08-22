from __future__ import annotations

import argparse
import json
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
                row = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"JSONL row must be an object at {path}:{line_number}")
            rows.append(row)
    return rows


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def safe_div(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def compute_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    tp = fp = tn = fn = 0

    for row in rows:
        gold = bool(row.get("gold_docs_update_required"))
        pred = bool(row.get("pred_docs_update_required"))

        if gold and pred:
            tp += 1
        elif not gold and pred:
            fp += 1
        elif not gold and not pred:
            tn += 1
        elif gold and not pred:
            fn += 1

    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    f1 = safe_div(2 * precision * recall, precision + recall)
    specificity = safe_div(tn, tn + fp)

    return {
        "total_cases": len(rows),
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "accuracy": safe_div(tp + tn, len(rows)),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "specificity": specificity,
        "false_positive_rate": safe_div(fp, fp + tn),
        "gold_distribution": dict(Counter(str(bool(row.get("gold_docs_update_required"))) for row in rows)),
        "pred_distribution": dict(Counter(str(bool(row.get("pred_docs_update_required"))) for row in rows)),
    }


def classify_failure_reason(message: str) -> str:
    lowered = message.lower()

    if "402" in lowered or "depleted your monthly included credits" in lowered or "pre-paid credits" in lowered:
        return "quota_or_credits_depleted"
    if "401" in lowered or "unauthorized" in lowered or "authentication" in lowered:
        return "auth_error"
    if "429" in lowered or "rate limit" in lowered:
        return "rate_limit"
    if "timeout" in lowered or "timed out" in lowered:
        return "timeout"
    if "parse" in lowered or "json" in lowered:
        return "parse_or_json_error"
    if not message.strip():
        return "unknown_error"

    return "other_error"


def summarize(rows: list[dict[str, Any]], *, input_path: Path) -> dict[str, Any]:
    completed = [row for row in rows if row.get("decision_status") == "ok"]
    failed = [row for row in rows if row.get("decision_status") != "ok"]

    failure_reasons = Counter(
        classify_failure_reason(str(row.get("decision_error") or ""))
        for row in failed
    )

    return {
        "status": "ok",
        "input": str(input_path),
        "total_cases": len(rows),
        "completed_cases": len(completed),
        "failed_or_abstained_cases": len(failed),
        "coverage": safe_div(len(completed), len(rows)),
        "decision_status_counts": dict(Counter(str(row.get("decision_status")) for row in rows)),
        "failure_reason_counts": dict(failure_reasons),
        "all_cases_conservative_metrics": compute_metrics(rows),
        "completed_only_metrics": compute_metrics(completed),
        "documentation_area_counts_all": dict(Counter(str(row.get("documentation_area")) for row in rows)),
        "documentation_area_counts_completed": dict(Counter(str(row.get("documentation_area")) for row in completed)),
        "interpretation": {
            "all_cases_conservative": "Counts failed/error/abstained cases using the evaluator's conservative prediction, usually False.",
            "completed_only": "Evaluates only successful LLM decisions. Use with coverage reporting, not alone.",
            "warning": "Completed-only metrics are not final if coverage is low.",
        },
    }


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def write_markdown(path: Path, summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    all_m = summary["all_cases_conservative_metrics"]
    ok_m = summary["completed_only_metrics"]

    lines = [
        "# DocGuard LLM Judge Coverage Summary",
        "",
        f"- Input: `{summary['input']}`",
        f"- Total cases: `{summary['total_cases']}`",
        f"- Completed cases: `{summary['completed_cases']}`",
        f"- Failed/abstained cases: `{summary['failed_or_abstained_cases']}`",
        f"- Coverage: `{pct(summary['coverage'])}`",
        "",
        "## Failure Reasons",
        "",
        f"`{summary['failure_reason_counts']}`",
        "",
        "## Metrics",
        "",
        "| Scope | Cases | Accuracy | Precision | Recall | F1 | Specificity | FPR | TP | FP | TN | FN |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        (
            f"| all cases conservative | {all_m['total_cases']} | {pct(all_m['accuracy'])} | "
            f"{pct(all_m['precision'])} | {pct(all_m['recall'])} | {pct(all_m['f1'])} | "
            f"{pct(all_m['specificity'])} | {pct(all_m['false_positive_rate'])} | "
            f"{all_m['true_positives']} | {all_m['false_positives']} | {all_m['true_negatives']} | {all_m['false_negatives']} |"
        ),
        (
            f"| completed only | {ok_m['total_cases']} | {pct(ok_m['accuracy'])} | "
            f"{pct(ok_m['precision'])} | {pct(ok_m['recall'])} | {pct(ok_m['f1'])} | "
            f"{pct(ok_m['specificity'])} | {pct(ok_m['false_positive_rate'])} | "
            f"{ok_m['true_positives']} | {ok_m['false_positives']} | {ok_m['true_negatives']} | {ok_m['false_negatives']} |"
        ),
        "",
        "## Interpretation Boundary",
        "",
        "- All-cases conservative metrics are useful for operational robustness.",
        "- Completed-only metrics are useful for model behavior, but only together with coverage.",
        "- If coverage is low due to provider quota, the result should be reported as partial.",
        "- Failed provider calls must not be hidden or silently removed.",
    ]

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize coverage-aware LLM judge results.")
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    predictions_path = Path(args.predictions)
    rows = load_jsonl(predictions_path)
    summary = summarize(rows, input_path=predictions_path)

    write_json(Path(args.output_json), summary)
    write_markdown(Path(args.report), summary)

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())