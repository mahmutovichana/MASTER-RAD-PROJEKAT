from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from docguard_external.real_case_detector import predict_real_case_runtime
from docguard_llm.patch_quality import evaluate_patch_quality
from docguard_llm.patch_verifier import verify_patch


ALLOWED_MODEL_INPUT_FIELDS = {
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
}

AUDIT_ONLY_FIELDS = {
    "change_type",
    "changed_files",
    "docs_after_excerpt",
    "docs_changed_files",
    "gold_docs_update_required",
    "gold_doc_category",
    "gold_target_doc_file",
    "gold_target_section",
    "gold_patch_summary",
    "manual_label_notes",
    "label_confidence",
    "allowed_model_input_fields",
    "audit_only_fields",
    "source_url",
    "commit_or_pr",
}

# `changed_files` is audit-only in the source real-case record because it may
# reveal documentation-file edits. However, the existing DocGuard runtime expects
# a field named `changed_files`. In the adapter, runtime `changed_files` is
# allowed only when derived from safe `code_changed_files`.
RUNTIME_DERIVED_SAFE_FIELDS = {"changed_files"}

STRICT_AUDIT_ONLY_FIELDS = AUDIT_ONLY_FIELDS - RUNTIME_DERIVED_SAFE_FIELDS

# Only these audit-only text fields are value-scanned for accidental leakage.
# Other audit metadata such as source_url, commit_or_pr, gold category names, or
# target file paths may legitimately appear inside allowed code/docs excerpts, so
# they are protected by key-level exclusion rather than brittle substring scans.
VALUE_LEAKAGE_CHECK_FIELDS = {
    "docs_after_excerpt",
    "gold_patch_summary",
    "manual_label_notes",
    "change_type",
}

# This is only used for evaluation reporting, not as model input.
# It lets us compare real-case coarse categories to DocGuard internal categories.
REAL_TO_DOCGUARD_CATEGORY = {
    "api": "api_reference",
    "api_endpoint": "api_reference",
    "api_endpoint_change": "api_reference",
    "request_response_schema_change": "model_contract",
    "data_model": "model_contract",
    "model": "model_contract",
    "testing": "testing_instructions",
    "testing_command_change": "testing_instructions",
    "configuration": "configuration",
    "configuration_change": "configuration",
    "workflow": "workflow_documentation",
    "workflow_change": "workflow_documentation",
    "architecture": "architecture_flow",
    "developer_setup": "developer_setup",
    "changelog": "changelog",
    "internal_refactor_no_docs_needed": "no_update",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
    return records


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _safe_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return [str(value)]


def _safe_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    return bool(value)


def _safe_cell(value: Any, limit: int = 160) -> str:
    text = str(value if value is not None else "")
    text = text.replace("\n", " ").replace("|", "\\|").replace("`", "\\`")
    text = " ".join(text.split())
    if len(text) > limit:
        return text[: limit - 3].rstrip() + "..."
    return text


def _safe_div(numerator: int | float, denominator: int | float) -> float:
    return float(numerator) / float(denominator) if denominator else 0.0


def normalize_gold_category(raw: Any) -> str:
    key = str(raw or "").strip().lower()
    return REAL_TO_DOCGUARD_CATEGORY.get(key, key or "not_available")


def build_runtime_record(case: dict[str, Any]) -> dict[str, Any]:
    """
    Build the exact object that DocGuard may inspect.

    Critical leakage rule:
    This function must only use ALLOWED_MODEL_INPUT_FIELDS plus a neutral case id.
    Gold labels, docs_after, docs_changed_files, manual notes, and change_type are not copied.
    """
    case_id = str(case.get("case_id") or case.get("id") or "real-case-unknown")
    code_changed_files = _safe_list(case.get("code_changed_files"))
    code_diff = str(case.get("code_diff_excerpt") or "")
    docs_before = str(case.get("docs_before_excerpt") or "")
    language = str(case.get("language") or "unknown")

    runtime_record = {
        "id": case_id,
        "project_id": "real_case_study",
        "split": "real_case_study",
        "language": language,
        "changed_files": code_changed_files,
        "code_changed_files": code_changed_files,
        "code_diff": code_diff,
        "docs_before": docs_before,
        "docs_before_excerpt": docs_before,
        "change_summary": "",
        "docs_update_required": False,
        "doc_category": "no_update",
        "target_doc_file": "",
        "target_section": "Documentation",
        "scenario_type": "runtime_unknown",
    }

    assert_no_audit_fields(runtime_record)
    return runtime_record


def assert_no_audit_fields(runtime_record: dict[str, Any]) -> None:
    leaked_keys = sorted(key for key in STRICT_AUDIT_ONLY_FIELDS if key in runtime_record)
    if leaked_keys:
        raise AssertionError(f"Audit-only fields leaked into runtime record: {leaked_keys}")


def assert_no_audit_values(case: dict[str, Any], runtime_record: dict[str, Any]) -> None:
    """
    Defensive leakage check.

    Special rule:
    Source `changed_files` is audit-only because it may reveal documentation-file
    edits. Runtime `changed_files` is still required by the existing DocGuard
    runtime, but it is safe only when derived from `code_changed_files`.

    Value-level leakage checks are intentionally limited to high-risk free-text
    audit fields. Metadata such as source_url, commit_or_pr, gold category names,
    and target doc paths may naturally appear inside the allowed code/docs
    excerpts, so checking them as raw substrings would create false positives.
    """
    runtime_changed_files = _safe_list(runtime_record.get("changed_files"))
    safe_code_files = _safe_list(case.get("code_changed_files"))

    if runtime_changed_files != safe_code_files:
        raise AssertionError("Runtime `changed_files` must be derived only from safe `code_changed_files`.")

    runtime_blob = json.dumps(runtime_record, ensure_ascii=False, sort_keys=True)

    for key in VALUE_LEAKAGE_CHECK_FIELDS:
        value = case.get(key)
        if value is None:
            continue

        if isinstance(value, (dict, list)):
            candidate = json.dumps(value, ensure_ascii=False, sort_keys=True)
        else:
            candidate = str(value)

        candidate = candidate.strip()

        # Avoid noisy false positives for tiny/common values.
        if len(candidate) >= 12 and candidate in runtime_blob:
            raise AssertionError(f"Audit-only value from `{key}` leaked into runtime payload.")
def predict_real_case(case: dict[str, Any]) -> dict[str, Any]:
    runtime_record = build_runtime_record(case)
    assert_no_audit_values(case, runtime_record)

    prediction = predict_real_case_runtime(runtime_record)

    docs_required = bool(prediction.get("docs_update_required"))
    doc_category = str(prediction.get("doc_category") or "no_update")
    scenario_type = str(prediction.get("scenario_type") or "unknown_change")
    target_doc_file = str(prediction.get("target_doc_file") or "")
    generated_patch = prediction.get("generated_doc_patch")

    router_output = prediction.get("router_output") or {}
    router_reason = str(router_output.get("router_reason") or "")
    signals = list(router_output.get("signals") or [])

    verifier_result = verify_patch(
        generated_patch,
        docs_required,
        target_doc_file,
        runtime_record["code_diff"],
        runtime_record["docs_before"],
        doc_category,
        scenario_type,
    )

    quality_result = evaluate_patch_quality(
        patch_text=generated_patch,
        code_diff=runtime_record["code_diff"],
        docs_before=runtime_record["docs_before"],
        target_doc_file=target_doc_file,
        doc_category=doc_category,
        scenario_type=scenario_type,
        verifier_result=verifier_result,
    )

    gold_docs_required = _safe_bool(case.get("gold_docs_update_required"))
    gold_category_raw = str(case.get("gold_doc_category") or "")
    gold_category_normalized = normalize_gold_category(gold_category_raw)
    gold_target_doc_file = str(case.get("gold_target_doc_file") or "")

    return {
        "case_id": str(case.get("case_id") or runtime_record["id"]),
        "language": runtime_record["language"],

        # Gold fields are copied only into the evaluation output, after prediction.
        # They are never passed into build_runtime_record() or predict().
        "gold_docs_update_required": gold_docs_required,
        "gold_doc_category_raw": gold_category_raw,
        "gold_doc_category_normalized": gold_category_normalized,
        "gold_target_doc_file": gold_target_doc_file,

        "pred_docs_update_required": docs_required,
        "pred_doc_category": doc_category,
        "pred_target_doc_file": target_doc_file,
        "pred_scenario_type": scenario_type,
        "pred_generated_doc_patch": generated_patch,

        "binary_correct": docs_required == gold_docs_required,
        "category_correct_supported": (
            gold_docs_required
            and gold_category_normalized != "not_available"
            and doc_category == gold_category_normalized
        ),
        "category_evaluated": bool(gold_docs_required and gold_category_normalized != "not_available"),
        "target_exact_correct_diagnostic": bool(
            gold_docs_required and gold_target_doc_file and target_doc_file == gold_target_doc_file
        ),
        "target_exact_evaluated_diagnostic": bool(gold_docs_required and gold_target_doc_file),

        "router_reason": router_reason,
        "signals": signals,
        "verifier_status": verifier_result.get("verifier_status"),
        "verifier_warnings": verifier_result.get("warnings") or [],
        "grounded_tokens_found": verifier_result.get("grounded_tokens_found") or [],
        "quality_label": quality_result.get("quality_label"),
        "hallucination_risk": quality_result.get("hallucination_risk"),
        "groundedness_score": quality_result.get("groundedness_score"),
        "usefulness_score": quality_result.get("usefulness_score"),
        "quality_reasons": quality_result.get("quality_reasons") or [],
        "decision_source": prediction.get("decision_source") or "hybrid_router",
        "leakage_policy": {
            "allowed_model_input_fields": sorted(ALLOWED_MODEL_INPUT_FIELDS),
            "audit_only_fields": sorted(AUDIT_ONLY_FIELDS),
        },
    }


def compute_metrics(predictions: list[dict[str, Any]]) -> dict[str, Any]:
    tp = fp = tn = fn = 0

    for row in predictions:
        gold = bool(row["gold_docs_update_required"])
        pred = bool(row["pred_docs_update_required"])
        if gold and pred:
            tp += 1
        elif not gold and pred:
            fp += 1
        elif not gold and not pred:
            tn += 1
        elif gold and not pred:
            fn += 1

    total = len(predictions)
    precision = _safe_div(tp, tp + fp)
    recall = _safe_div(tp, tp + fn)
    f1 = _safe_div(2 * precision * recall, precision + recall)
    accuracy = _safe_div(tp + tn, total)

    category_rows = [row for row in predictions if row.get("category_evaluated")]
    category_correct = sum(1 for row in category_rows if row.get("category_correct_supported"))

    target_rows = [row for row in predictions if row.get("target_exact_evaluated_diagnostic")]
    target_correct = sum(1 for row in target_rows if row.get("target_exact_correct_diagnostic"))

    return {
        "total_cases": total,
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "binary_accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "category_supported_total": len(category_rows),
        "category_supported_correct": category_correct,
        "category_supported_accuracy": _safe_div(category_correct, len(category_rows)),
        "target_exact_total_diagnostic": len(target_rows),
        "target_exact_correct_diagnostic": target_correct,
        "target_exact_accuracy_diagnostic": _safe_div(target_correct, len(target_rows)),
        "gold_distribution": dict(Counter(str(row["gold_docs_update_required"]) for row in predictions)),
        "pred_distribution": dict(Counter(str(row["pred_docs_update_required"]) for row in predictions)),
        "quality_label_counts": dict(Counter(str(row.get("quality_label")) for row in predictions)),
        "hallucination_risk_counts": dict(Counter(str(row.get("hallucination_risk")) for row in predictions)),
        "verifier_status_counts": dict(Counter(str(row.get("verifier_status")) for row in predictions)),
        "pred_category_counts": dict(Counter(str(row.get("pred_doc_category")) for row in predictions)),
        "gold_category_counts": dict(Counter(str(row.get("gold_doc_category_normalized")) for row in predictions)),
    }


def _percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def write_markdown_report(path: Path, metrics: dict[str, Any], predictions: list[dict[str, Any]], input_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = [
        "# DocGuard Real Project Case Study Evaluation 2026-08",
        "",
        "This report evaluates DocGuard on manually validated public GitHub PR cases.",
        "Gold labels are used only after prediction for scoring. They are not passed into the runtime record.",
        "",
        f"- Input: `{input_path}`",
        "- Prediction mode: `hybrid_router` through the real-case adapter",
        "- Patch backend: `deterministic`",
        "",
        "## Leakage Policy",
        "",
        "Allowed runtime/model input fields:",
        "",
    ]

    for field in sorted(ALLOWED_MODEL_INPUT_FIELDS):
        lines.append(f"- `{field}`")

    lines.extend(["", "Audit-only fields excluded from runtime/model input:", ""])

    for field in sorted(AUDIT_ONLY_FIELDS):
        lines.append(f"- `{field}`")

    lines.extend(
        [
            "",
            "## Binary Metrics",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| total cases | {metrics['total_cases']} |",
            f"| true positives | {metrics['true_positives']} |",
            f"| false positives | {metrics['false_positives']} |",
            f"| true negatives | {metrics['true_negatives']} |",
            f"| false negatives | {metrics['false_negatives']} |",
            f"| binary accuracy | {_percent(metrics['binary_accuracy'])} |",
            f"| precision | {_percent(metrics['precision'])} |",
            f"| recall | {_percent(metrics['recall'])} |",
            f"| F1 | {_percent(metrics['f1'])} |",
            "",
            "## Category And Target Diagnostics",
            "",
            "Category accuracy is reported only for real-case labels that can be normalized to a DocGuard internal category.",
            "Target-file exact accuracy is diagnostic only because real repositories have project-specific documentation paths.",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| category supported total | {metrics['category_supported_total']} |",
            f"| category supported correct | {metrics['category_supported_correct']} |",
            f"| category supported accuracy | {_percent(metrics['category_supported_accuracy'])} |",
            f"| target exact total diagnostic | {metrics['target_exact_total_diagnostic']} |",
            f"| target exact correct diagnostic | {metrics['target_exact_correct_diagnostic']} |",
            f"| target exact accuracy diagnostic | {_percent(metrics['target_exact_accuracy_diagnostic'])} |",
            "",
            "## Quality And Guardrail Counts",
            "",
            f"- Quality labels: `{metrics['quality_label_counts']}`",
            f"- Hallucination risk: `{metrics['hallucination_risk_counts']}`",
            f"- Verifier status: `{metrics['verifier_status_counts']}`",
            f"- Gold distribution: `{metrics['gold_distribution']}`",
            f"- Prediction distribution: `{metrics['pred_distribution']}`",
            "",
            "## Per-Case Results",
            "",
            "| Case | Gold | Pred | Binary | Gold category | Pred category | Pred target | Verifier | Quality | Risk | Signals |",
            "| --- | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )

    for row in predictions:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{_safe_cell(row['case_id'], 80)}`",
                    f"`{row['gold_docs_update_required']}`",
                    f"`{row['pred_docs_update_required']}`",
                    f"`{row['binary_correct']}`",
                    f"`{_safe_cell(row['gold_doc_category_normalized'], 60)}`",
                    f"`{_safe_cell(row['pred_doc_category'], 60)}`",
                    f"`{_safe_cell(row['pred_target_doc_file'], 80)}`",
                    f"`{_safe_cell(row['verifier_status'], 40)}`",
                    f"`{_safe_cell(row['quality_label'], 40)}`",
                    f"`{_safe_cell(row['hallucination_risk'], 40)}`",
                    f"`{_safe_cell(', '.join(row.get('signals') or []), 120)}`",
                ]
            )
            + " |"
        )

    lines.extend(["", "## Case Details", ""])

    for row in predictions:
        lines.extend(
            [
                f"### `{row['case_id']}`",
                "",
                f"- Gold docs update required: `{row['gold_docs_update_required']}`",
                f"- Predicted docs update required: `{row['pred_docs_update_required']}`",
                f"- Predicted category: `{row['pred_doc_category']}`",
                f"- Predicted target: `{row['pred_target_doc_file']}`",
                f"- Predicted scenario: `{row['pred_scenario_type']}`",
                f"- Router reason: {_safe_cell(row.get('router_reason'), 500)}",
                f"- Signals: `{', '.join(row.get('signals') or [])}`",
                f"- Verifier: `{row['verifier_status']}`",
                f"- Quality: `{row['quality_label']}`",
                f"- Hallucination risk: `{row['hallucination_risk']}`",
                "",
                "Generated patch:",
                "",
                "```diff",
                str(row.get("pred_generated_doc_patch") or "not_applicable"),
                "```",
                "",
            ]
        )
        warnings = row.get("verifier_warnings") or []
        quality_reasons = row.get("quality_reasons") or []
        if warnings or quality_reasons:
            lines.append("Warnings / quality reasons:")
            lines.append("")
            for warning in warnings[:10]:
                lines.append(f"- {warning}")
            for reason in quality_reasons[:10]:
                lines.append(f"- {reason}")
            lines.append("")

    lines.extend(
        [
            "## Interpretation Boundary",
            "",
            "- This is the first automatic real-case adapter run.",
            "- Metrics may be weaker than synthetic project-evolution metrics; that is expected and methodologically useful.",
            "- Synthetic project-evolution remains demo evidence.",
            "- This real-case study is the thesis-critical workflow evidence stream.",
            "- Deterministic patches are fallback-quality suggestions, not final proof of human-quality documentation.",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def run_evaluation(
    *,
    input_path: Path,
    output_dir: Path,
    case_limit: int | None = None,
    patch_backend: str = "deterministic",
) -> dict[str, Any]:
    if patch_backend != "deterministic":
        raise ValueError("First real-case runner step supports only --patch-backend deterministic.")

    records = load_jsonl(input_path)
    if case_limit is not None:
        records = records[:case_limit]

    predictions = [predict_real_case(record) for record in records]
    metrics = compute_metrics(predictions)

    output_dir.mkdir(parents=True, exist_ok=True)
    predictions_path = output_dir / "docguard_real_case_study_predictions.jsonl"
    report_path = output_dir / "docguard_real_case_study_evaluation_2026_08.md"

    write_jsonl(predictions_path, predictions)
    write_markdown_report(report_path, metrics, predictions, input_path)

    return {
        "status": "ok",
        "input": str(input_path),
        "output_dir": str(output_dir),
        "predictions": str(predictions_path),
        "report": str(report_path),
        "metrics": metrics,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run DocGuard on validated real project case-study records.")
    parser.add_argument("--input", default="data/external/project_case_study/manual_cases.jsonl")
    parser.add_argument("--output-dir", default="reports/real_case_study")
    parser.add_argument("--case-limit", type=int, default=None)
    parser.add_argument("--patch-backend", default="deterministic", choices=["deterministic"])
    args = parser.parse_args()

    result = run_evaluation(
        input_path=Path(args.input),
        output_dir=Path(args.output_dir),
        case_limit=args.case_limit,
        patch_backend=args.patch_backend,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())