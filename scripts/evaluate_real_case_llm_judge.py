from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docguard_llm.llm_generator import generate_documentation_patch


ALLOWED_INPUT_FIELDS = {
    "case_id",
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
    "gold_doc_category",
    "gold_docs_update_required",
    "gold_patch_summary",
    "gold_target_doc_file",
    "gold_target_section",
    "label_confidence",
    "manual_label_notes",
    "source_url",
    "commit_or_pr",
    "allowed_model_input_fields",
    "audit_only_fields",
}

OUTPUT_STEM = "docguard_real_case_llm_judge_2026_08"


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


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if value is None:
        return []
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


def _truncate(text: Any, limit: int) -> str:
    value = str(text if text is not None else "")
    value = value.replace("\r\n", "\n").replace("\r", "\n").strip()
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def build_safe_case_input(case: dict[str, Any], *, max_diff_chars: int, max_docs_chars: int) -> dict[str, Any]:
    """
    This is the only payload allowed to enter the LLM prompt.

    Gold labels, docs-after, manual notes, source URL, docs-changed files, and
    manually assigned change type are intentionally excluded.
    """
    return {
        "case_id": str(case.get("case_id") or "unknown-real-case"),
        "language": str(case.get("language") or "unknown"),
        "code_changed_files": _safe_list(case.get("code_changed_files")),
        "code_diff_excerpt": _truncate(case.get("code_diff_excerpt") or "", max_diff_chars),
        "docs_before_excerpt": _truncate(case.get("docs_before_excerpt") or "", max_docs_chars),
    }


def assert_no_audit_key_leakage(payload: dict[str, Any]) -> None:
    leaked = sorted(key for key in AUDIT_ONLY_FIELDS if key in payload)
    if leaked:
        raise AssertionError(f"Audit-only keys leaked into LLM payload: {leaked}")


def assert_no_high_risk_audit_value_leakage(case: dict[str, Any], payload: dict[str, Any]) -> None:
    """
    Free-text audit fields must not leak into the prompt.

    We intentionally do not value-scan metadata such as source_url or target paths,
    because they may naturally appear inside allowed code/docs excerpts. The key-level
    exclusion check protects those fields.
    """
    high_risk_fields = {
        "docs_after_excerpt",
        "gold_patch_summary",
        "manual_label_notes",
        "change_type",
    }
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True)

    for key in high_risk_fields:
        value = case.get(key)
        if value is None:
            continue
        candidate = str(value).strip()
        if len(candidate) >= 12 and candidate in blob:
            raise AssertionError(f"High-risk audit value from `{key}` leaked into LLM payload.")


def build_llm_decision_prompt(safe_input: dict[str, Any]) -> str:
    """
    Neutral real-case LLM judge prompt.

    This is not a synthetic task and does not contain examples, gold labels, expected
    patch summaries, docs-after text, or manually assigned change types.
    """
    return f"""You are an independent software documentation consistency reviewer.

Decide whether the supplied code change likely requires a project documentation update.

Use only:
- language
- code_changed_files
- code_diff_excerpt
- docs_before_excerpt

Do not assume hidden files.
Do not use external knowledge.
Do not invent behavior not visible in the diff.
Do not rely on whether documentation files were changed in the original PR.
Do not produce a documentation patch.

A documentation update is likely required when the diff changes behavior or contracts that users, developers, integrators, operators, API clients, or maintainers would reasonably expect to find in project documentation.

A documentation update is likely not required when the diff is only an internal refactor, import reshuffle, test fixture, mock data, Storybook/example-only setup, comment-only change, or implementation detail without visible documented behavior impact.

Current documentation may be empty. Empty docs alone does not automatically mean an update is required; base the decision on the visible impact of the code diff.

Return only compact JSON with exactly these keys:
{{
  "docs_update_required": true or false,
  "confidence": number from 0 to 1,
  "documentation_area": short lowercase label such as api, data_model, configuration, testing, workflow, developer_setup, architecture, no_update, or uncertain,
  "rationale": one concise sentence grounded in the visible diff,
  "evidence": ["short visible evidence token 1", "short visible evidence token 2"]
}}

Safe input:
```json
{json.dumps(safe_input, ensure_ascii=False, indent=2)}
```
"""


def _strip_code_fences(text: str) -> str:
    stripped = text.strip()
    stripped = re.sub(r"^```(?:json)?\s*", "", stripped, flags=re.IGNORECASE)
    stripped = re.sub(r"\s*```$", "", stripped)
    return stripped.strip()


def parse_llm_json(text: str) -> dict[str, Any]:
    stripped = _strip_code_fences(text or "")
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", stripped, flags=re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def normalize_llm_decision(data: dict[str, Any]) -> dict[str, Any]:
    docs_required = _safe_bool(data.get("docs_update_required"))

    try:
        confidence = float(data.get("confidence", 0.5))
    except (TypeError, ValueError):
        confidence = 0.5
    confidence = max(0.0, min(1.0, confidence))

    area = str(data.get("documentation_area") or ("uncertain" if docs_required else "no_update"))
    area = re.sub(r"[^a-zA-Z0-9_/-]+", "_", area).strip("_").lower() or "uncertain"

    rationale = str(data.get("rationale") or "").strip()
    evidence = data.get("evidence") or []
    if not isinstance(evidence, list):
        evidence = [str(evidence)]
    evidence = [str(item).strip() for item in evidence if str(item).strip()][:8]

    return {
        "docs_update_required": docs_required,
        "confidence": confidence,
        "documentation_area": area,
        "rationale": rationale,
        "evidence": evidence,
    }


def generate_llm_decision(
    *,
    safe_input: dict[str, Any],
    backend: str,
    model_name: str | None,
    max_new_tokens: int,
    temperature: float,
) -> dict[str, Any]:
    prompt = build_llm_decision_prompt(safe_input)

    if backend == "mock":
        # Test-only backend. It is not real model evidence.
        raw = json.dumps(
            {
                "docs_update_required": False,
                "confidence": 0.5,
                "documentation_area": "no_update",
                "rationale": "Mock backend validates wiring only.",
                "evidence": [],
            }
        )
        parsed = parse_llm_json(raw)
        return {
            "decision_status": "ok",
            "raw_decision": raw,
            "prompt": prompt,
            **normalize_llm_decision(parsed),
        }

    generated = generate_documentation_patch(
        prompt,
        backend=backend,
        model_name=model_name,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
    )

    raw_text = str(generated.get("patch_text") or "")
    if generated.get("generation_status") != "ok":
        return {
            "decision_status": "error",
            "decision_error": generated.get("error_message") or "LLM decision generation failed.",
            "raw_decision": raw_text,
            "prompt": prompt,
            "docs_update_required": False,
            "confidence": 0.0,
            "documentation_area": "error",
            "rationale": "LLM generation failed.",
            "evidence": [],
        }

    try:
        parsed = parse_llm_json(raw_text)
        return {
            "decision_status": "ok",
            "decision_error": "",
            "raw_decision": raw_text,
            "prompt": prompt,
            **normalize_llm_decision(parsed),
        }
    except Exception as exc:
        return {
            "decision_status": "parse_error",
            "decision_error": f"Could not parse LLM JSON: {exc}",
            "raw_decision": raw_text,
            "prompt": prompt,
            "docs_update_required": False,
            "confidence": 0.0,
            "documentation_area": "parse_error",
            "rationale": "LLM returned invalid JSON.",
            "evidence": [],
        }


def predict_case_with_llm(
    *,
    case: dict[str, Any],
    backend: str,
    model_name: str | None,
    max_new_tokens: int,
    temperature: float,
    max_diff_chars: int,
    max_docs_chars: int,
) -> dict[str, Any]:
    safe_input = build_safe_case_input(case, max_diff_chars=max_diff_chars, max_docs_chars=max_docs_chars)
    assert_no_audit_key_leakage(safe_input)
    assert_no_high_risk_audit_value_leakage(case, safe_input)

    decision = generate_llm_decision(
        safe_input=safe_input,
        backend=backend,
        model_name=model_name,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
    )

    gold = _safe_bool(case.get("gold_docs_update_required"))
    status = str(decision.get("decision_status") or "unknown")
    abstained = status != "ok" or decision.get("documentation_area") in {"uncertain", "error", "parse_error"}

    pred = bool(decision.get("docs_update_required")) if not abstained else False

    return {
        "case_id": safe_input["case_id"],
        "language": safe_input["language"],
        "safe_code_changed_files": safe_input["code_changed_files"],
        "gold_docs_update_required": gold,
        "pred_docs_update_required": pred,
        "raw_pred_docs_update_required": bool(decision.get("docs_update_required")),
        "binary_correct": pred == gold,
        "decision_status": status,
        "abstained": abstained,
        "confidence": decision.get("confidence"),
        "documentation_area": decision.get("documentation_area"),
        "rationale": decision.get("rationale"),
        "evidence": decision.get("evidence") or [],
        "raw_decision": decision.get("raw_decision") or "",
        "decision_error": decision.get("decision_error") or "",
        "backend": backend,
        "model_name": model_name or "",
        "leakage_policy": {
            "allowed_input_fields": sorted(ALLOWED_INPUT_FIELDS),
            "audit_only_fields": sorted(AUDIT_ONLY_FIELDS),
        },
    }


def _safe_div(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def compute_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    tp = fp = tn = fn = 0
    for row in rows:
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

    precision = _safe_div(tp, tp + fp)
    recall = _safe_div(tp, tp + fn)
    f1 = _safe_div(2 * precision * recall, precision + recall)

    return {
        "total_cases": len(rows),
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "binary_accuracy": _safe_div(tp + tn, len(rows)),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "abstentions": sum(1 for row in rows if row.get("abstained")),
        "decision_status_counts": dict(Counter(str(row.get("decision_status")) for row in rows)),
        "documentation_area_counts": dict(Counter(str(row.get("documentation_area")) for row in rows)),
        "gold_distribution": dict(Counter(str(row.get("gold_docs_update_required")) for row in rows)),
        "pred_distribution": dict(Counter(str(row.get("pred_docs_update_required")) for row in rows)),
    }


def _pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def write_report(path: Path, rows: list[dict[str, Any]], metrics: dict[str, Any], input_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = [
        "# DocGuard Real Case LLM Judge Evaluation 2026-08",
        "",
        "This report evaluates an LLM decision layer on real public GitHub PR case-study records.",
        "The LLM receives only safe input fields and does not receive gold labels, docs-after text, manual notes, manually assigned change type, source URLs, or documentation-file presence from the original PR.",
        "",
        f"- Input: `{input_path}`",
        f"- Backend: `{rows[0]['backend'] if rows else 'none'}`",
        f"- Model: `{rows[0]['model_name'] if rows else 'none'}`",
        "",
        "## Input Leakage Policy",
        "",
        "Allowed LLM input fields:",
        "",
    ]

    for field in sorted(ALLOWED_INPUT_FIELDS):
        lines.append(f"- `{field}`")

    lines.extend(["", "Audit-only fields excluded from LLM input:", ""])

    for field in sorted(AUDIT_ONLY_FIELDS):
        lines.append(f"- `{field}`")

    lines.extend(
        [
            "",
            "## Metrics",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| total cases | {metrics['total_cases']} |",
            f"| true positives | {metrics['true_positives']} |",
            f"| false positives | {metrics['false_positives']} |",
            f"| true negatives | {metrics['true_negatives']} |",
            f"| false negatives | {metrics['false_negatives']} |",
            f"| binary accuracy | {_pct(metrics['binary_accuracy'])} |",
            f"| precision | {_pct(metrics['precision'])} |",
            f"| recall | {_pct(metrics['recall'])} |",
            f"| F1 | {_pct(metrics['f1'])} |",
            f"| abstentions | {metrics['abstentions']} |",
            "",
            "## Count Summaries",
            "",
            f"- Decision status counts: `{metrics['decision_status_counts']}`",
            f"- Documentation area counts: `{metrics['documentation_area_counts']}`",
            f"- Gold distribution: `{metrics['gold_distribution']}`",
            f"- Prediction distribution: `{metrics['pred_distribution']}`",
            "",
            "## Per-Case Table",
            "",
            "| Case | Gold | Pred | Correct | Status | Confidence | Area | Rationale | Evidence |",
            "| --- | ---: | ---: | ---: | --- | ---: | --- | --- | --- |",
        ]
    )

    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{_safe_cell(row['case_id'], 80)}`",
                    f"`{row['gold_docs_update_required']}`",
                    f"`{row['pred_docs_update_required']}`",
                    f"`{row['binary_correct']}`",
                    f"`{_safe_cell(row['decision_status'], 40)}`",
                    f"`{row['confidence']}`",
                    f"`{_safe_cell(row['documentation_area'], 60)}`",
                    _safe_cell(row["rationale"], 220),
                    _safe_cell(", ".join(row.get("evidence") or []), 140),
                ]
            )
            + " |"
        )

    lines.extend(["", "## Error Details", ""])

    for row in rows:
        if row["binary_correct"]:
            continue
        lines.extend(
            [
                f"### `{row['case_id']}`",
                "",
                f"- Gold docs update required: `{row['gold_docs_update_required']}`",
                f"- Predicted docs update required: `{row['pred_docs_update_required']}`",
                f"- Decision status: `{row['decision_status']}`",
                f"- Confidence: `{row['confidence']}`",
                f"- Documentation area: `{row['documentation_area']}`",
                f"- Rationale: {row['rationale']}",
                f"- Evidence: `{', '.join(row.get('evidence') or [])}`",
                "",
                "Raw decision:",
                "",
                "```json",
                str(row.get("raw_decision") or ""),
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## Interpretation Boundary",
            "",
            "- This is real public-PR case-study evidence, not synthetic project-evolution evidence.",
            "- The LLM judge is the decision layer; deterministic code here only handles safe input construction, JSON parsing, leakage protection, and metric calculation.",
            "- Gold labels are used only after prediction for evaluation.",
            "- Low-confidence negative cases should be interpreted carefully because absence of a documentation patch in a PR does not always prove that no documentation update was needed.",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    *,
    input_path: Path,
    output_dir: Path,
    backend: str,
    model_name: str | None,
    case_limit: int | None,
    max_new_tokens: int,
    temperature: float,
    max_diff_chars: int,
    max_docs_chars: int,
) -> dict[str, Any]:
    cases = load_jsonl(input_path)
    if case_limit is not None:
        cases = cases[:case_limit]

    rows = [
        predict_case_with_llm(
            case=case,
            backend=backend,
            model_name=model_name,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            max_diff_chars=max_diff_chars,
            max_docs_chars=max_docs_chars,
        )
        for case in cases
    ]

    metrics = compute_metrics(rows)

    output_dir.mkdir(parents=True, exist_ok=True)
    predictions_path = output_dir / f"{OUTPUT_STEM}_predictions.jsonl"
    report_path = output_dir / f"{OUTPUT_STEM}.md"

    write_jsonl(predictions_path, rows)
    write_report(report_path, rows, metrics, input_path)

    return {
        "status": "ok",
        "input": str(input_path),
        "output_dir": str(output_dir),
        "predictions": str(predictions_path),
        "report": str(report_path),
        "metrics": metrics,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate a real LLM documentation-update judge on DocGuard real cases.")
    parser.add_argument("--input", default="data/external/project_case_study/manual_cases.jsonl")
    parser.add_argument("--output-dir", default="reports/real_case_study_llm_judge")
    parser.add_argument("--backend", default="openai_compatible", choices=["openai_compatible", "hf", "ollama", "mock"])
    parser.add_argument("--model", default=None)
    parser.add_argument("--case-limit", type=int, default=None)
    parser.add_argument("--max-new-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-diff-chars", type=int, default=5000)
    parser.add_argument("--max-docs-chars", type=int, default=2500)
    args = parser.parse_args()

    result = run(
        input_path=Path(args.input),
        output_dir=Path(args.output_dir),
        backend=args.backend,
        model_name=args.model,
        case_limit=args.case_limit,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        max_diff_chars=args.max_diff_chars,
        max_docs_chars=args.max_docs_chars,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())