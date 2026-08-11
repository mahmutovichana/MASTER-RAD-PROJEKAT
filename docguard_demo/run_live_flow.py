from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from docguard_hybrid.hybrid_agent import predict

from docguard_demo.live_flow_scenarios import generate_live_flow_cases


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def evaluate(records: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    predictions = []
    false_positives = false_negatives = unknown = patch_positive = positive_total = 0
    binary_correct = category_correct = target_correct = scenario_correct = 0
    for record in records:
        pred = predict(record)
        router = pred.get("router_output") or {}
        gold_required = bool(record["docs_update_required"])
        predicted_required = bool(pred["docs_update_required"])
        if gold_required:
            positive_total += 1
            if pred.get("generated_doc_patch"):
                patch_positive += 1
        if not gold_required and predicted_required:
            false_positives += 1
        if gold_required and not predicted_required:
            false_negatives += 1
        if pred.get("scenario_type") == "unknown_change":
            unknown += 1
        row = {
            "case_id": record["id"],
            "gold_docs_update_required": gold_required,
            "predicted_docs_update_required": predicted_required,
            "gold_doc_category": record["doc_category"],
            "predicted_doc_category": pred["doc_category"],
            "gold_scenario_type": record["scenario_type"],
            "predicted_scenario_type": pred["scenario_type"],
            "gold_target_doc_file": record["target_doc_file"],
            "predicted_target_doc_file": pred["target_doc_file"],
            "generated_doc_patch": pred.get("generated_doc_patch"),
            "router_reason": router.get("router_reason"),
            "signals_detected": router.get("signals") or [],
            "binary_pass": gold_required == predicted_required,
            "category_pass": record["doc_category"] == pred["doc_category"],
            "target_file_pass": record["target_doc_file"] == pred["target_doc_file"],
            "scenario_pass": record["scenario_type"] == pred["scenario_type"],
        }
        binary_correct += int(row["binary_pass"])
        category_correct += int(row["category_pass"])
        target_correct += int(row["target_file_pass"])
        scenario_correct += int(row["scenario_pass"])
        predictions.append(row)
    total = len(records)
    metrics = {
        "total_cases": total,
        "binary_accuracy": binary_correct / total if total else 0.0,
        "category_accuracy": category_correct / total if total else 0.0,
        "target_file_accuracy": target_correct / total if total else 0.0,
        "scenario_accuracy": scenario_correct / total if total else 0.0,
        "patch_non_empty_rate_for_positive_cases": patch_positive / positive_total if positive_total else 0.0,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "unknown_scenario_count": unknown,
    }
    return metrics, predictions


def write_predictions(path: Path, predictions: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in predictions) + "\n", encoding="utf-8")


def write_report(path: Path, metrics: dict[str, Any], predictions: list[dict[str, Any]]) -> None:
    lines = [
        "# DocGuard Live Flow Evaluation 2026-08",
        "",
        "This is an invented synthetic live-flow playground for implementation sanity/demo purposes. It is not a benchmark and does not replace the leakage-hardened real project case study or external Deep-JIT proxy evidence.",
        "",
        "## Summary Metrics",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]
    for key, value in metrics.items():
        lines.append(f"| `{key}` | {pct(value) if isinstance(value, float) else value} |")
    lines.extend(
        [
            "",
            "## Per-Case Results",
            "",
            "| Case | Binary | Category | Target | Scenario | Gold category | Pred category | Gold target | Pred target | Signals |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in predictions:
        lines.append(
            f"| `{item['case_id']}` | `{item['binary_pass']}` | `{item['category_pass']}` | `{item['target_file_pass']}` | `{item['scenario_pass']}` | "
            f"`{item['gold_doc_category']}` | `{item['predicted_doc_category']}` | `{item['gold_target_doc_file']}` | `{item['predicted_target_doc_file']}` | `{', '.join(item['signals_detected'])}` |"
        )
    lines.extend(["", "## Generated Patches", ""])
    for item in predictions:
        lines.extend(
            [
                f"### `{item['case_id']}`",
                "",
                f"- Router reason: {item['router_reason']}",
                f"- Generated patch:",
                "",
                "```diff",
                item["generated_doc_patch"] or "not_applicable",
                "```",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_failure_analysis(path: Path, predictions: list[dict[str, Any]]) -> None:
    failures = [
        item
        for item in predictions
        if not (item["binary_pass"] and item["category_pass"] and item["target_file_pass"] and item["scenario_pass"])
    ]
    if not failures:
        if path.exists():
            path.unlink()
        return
    lines = [
        "# DocGuard Live Flow Failure Analysis 2026-08",
        "",
        "The live-flow runner keeps failures visible. Gold labels were not changed to improve the result.",
        "",
        "## Failed Cases",
        "",
    ]
    for item in failures:
        reasons = []
        if not item["binary_pass"]:
            reasons.append("binary update-required decision")
        if not item["category_pass"]:
            reasons.append("category routing")
        if not item["target_file_pass"]:
            reasons.append("target file routing")
        if not item["scenario_pass"]:
            reasons.append("scenario routing")
        lines.extend(
            [
                f"### `{item['case_id']}`",
                "",
                f"- Failed dimensions: {', '.join(reasons)}",
                f"- Gold category/target/scenario: `{item['gold_doc_category']}` / `{item['gold_target_doc_file']}` / `{item['gold_scenario_type']}`",
                f"- Pred category/target/scenario: `{item['predicted_doc_category']}` / `{item['predicted_target_doc_file']}` / `{item['predicted_scenario_type']}`",
                f"- Signals: `{', '.join(item['signals_detected'])}`",
                f"- Router reason: {item['router_reason']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Likely Causes",
            "",
            "- Signal extractor coverage is deterministic and pattern-based.",
            "- Router priority can choose the first matching signal when multiple signals are present.",
            "- Patch generation is intentionally generic and uses the first expected fact.",
            "- The synthetic live records include gold `scenario_type` because the current hybrid synthetic-evaluation path expects it; this is a demo limitation, not a clean real-world runner design.",
            "",
            "## Needed Improvements",
            "",
            "- Add a clean real-case adapter that does not rely on gold scenario fields.",
            "- Improve conflict handling when multiple signals fire.",
            "- Expand patch generation beyond one-line expected-fact patches.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(output_dir: Path) -> dict[str, Any]:
    records = generate_live_flow_cases()
    metrics, predictions = evaluate(records)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_predictions(output_dir / "docguard_live_flow_predictions.jsonl", predictions)
    write_report(output_dir / "docguard_live_flow_evaluation_2026_08.md", metrics, predictions)
    write_failure_analysis(output_dir / "docguard_live_flow_failure_analysis_2026_08.md", predictions)
    return {"status": "ok", **metrics, "output_dir": str(output_dir)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="reports/live_flow")
    args = parser.parse_args()
    print(json.dumps(run(Path(args.output_dir)), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
