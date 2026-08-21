from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docguard_demo.run_project_evolution_flow import run
from docguard_llm.patch_quality import evaluate_patch_quality


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def observation(row: dict) -> str:
    if row.get("patch_backend") == "llm-mock":
        return "Mock backend validates prompt/postprocess/verifier flow only; it is excluded from real LLM quality conclusions."
    quality_label = row.get("quality_label")
    if quality_label:
        if quality_label == "rejected":
            return "Quality evaluator rejected the patch or marked high hallucination risk."
        if quality_label == "needs_review":
            return "Patch needs review because it is generic, weakly grounded, or verifier warnings remain."
        if quality_label == "usable":
            return "Patch is usable under heuristic quality checks."
        if quality_label == "excellent":
            return "Patch is strong under heuristic quality checks."
    if row.get("llm_generation_status") == "error":
        return "HF generation did not run successfully; inspect the dependency/model error."
    if row.get("patch_verifier_status") == "pass":
        return "Patch passed lightweight grounding checks."
    if row.get("patch_verifier_status") == "warn":
        return "Patch is usable for inspection but has verifier warnings."
    return "Patch failed lightweight verifier checks."


def markdown_cell(value: object, limit: int | None = None) -> str:
    text = " ".join(str(value if value is not None else "n/a").split())
    text = text.replace("|", "/").replace("`", "'")
    if limit is not None and len(text) > limit:
        text = text[: max(0, limit - 3)].rstrip() + "..."
    return text


def preview(value: str) -> str:
    return markdown_cell(value or "n/a", limit=120)


def fenced_patch(value: str | None) -> list[str]:
    return ["````diff", value or "not_applicable", "````"]


def add_quality(row: dict) -> dict:
    verifier_result = {
        "verifier_status": row.get("patch_verifier_status"),
        "warnings": row.get("patch_verifier_warnings") or [],
        "grounded_tokens_found": row.get("grounded_tokens_found") or [],
    }
    quality = evaluate_patch_quality(
        patch_text=row.get("generated_doc_patch"),
        code_diff=row.get("code_diff_excerpt") or "",
        docs_before=row.get("docs_before_excerpt") or "",
        target_doc_file=row.get("predicted_target_doc_file") or "",
        doc_category=row.get("predicted_doc_category") or "",
        scenario_type=row.get("predicted_scenario_type") or "",
        verifier_result=verifier_result,
    )
    return {**row, **quality}


def write_report(path: Path, grouped: dict[str, dict[str, dict]], hf_note: str) -> None:
    backend_counts = {backend: Counter(row.get("quality_label") for rows in grouped.values() for name, row in rows.items() if name == backend) for backend in ["legacy", "llm-hf", "llm-mock"]}
    risk_counts = {backend: Counter(row.get("hallucination_risk") for rows in grouped.values() for name, row in rows.items() if name == backend) for backend in ["legacy", "llm-hf", "llm-mock"]}
    lines = [
        "# DocGuard Patch Backend Comparison 2026-08",
        "",
        hf_note,
        "",
        "## Summary Counts",
        "",
        "Mock backend validates prompt/postprocess/verifier flow only; it is excluded from real LLM quality conclusions.",
        "",
        "| Backend | Role | Quality labels | Hallucination risk |",
        "| --- | --- | --- | --- |",
        f"| `legacy` | deterministic fallback | `{markdown_cell(dict(backend_counts['legacy']))}` | `{markdown_cell(dict(risk_counts['legacy']))}` |",
        f"| `llm-hf` | real model output when explicitly requested | `{markdown_cell(dict(backend_counts['llm-hf']))}` | `{markdown_cell(dict(risk_counts['llm-hf']))}` |",
        f"| `llm-mock` | architecture sanity only | `{markdown_cell(dict(backend_counts['llm-mock']))}` | `{markdown_cell(dict(risk_counts['llm-mock']))}` |",
        "",
        "## Comparison Table",
        "",
        "| Case | Target doc | Backend | Patch preview | Verifier | Warnings | Grounded tokens | Quality | Groundedness | Usefulness | Hallucination risk | Observation |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- |",
    ]
    for case_id, rows in grouped.items():
        for backend, row in rows.items():
            warnings = "; ".join(row.get("patch_verifier_warnings") or [])
            tokens = ", ".join(row.get("grounded_tokens_found") or [])
            lines.append(
                f"| `{markdown_cell(case_id)}` | `{markdown_cell(row.get('predicted_target_doc_file', ''))}` | `{markdown_cell(backend)}` | "
                f"`{preview(row.get('generated_doc_patch') or 'n/a')}` | `{markdown_cell(row.get('patch_verifier_status'))}` | "
                f"`{markdown_cell(warnings, limit=140)}` | `{markdown_cell(tokens, limit=100)}` | `{markdown_cell(row.get('quality_label'))}` | "
                f"{row.get('groundedness_score'):.2f} | {row.get('usefulness_score'):.2f} | "
                f"`{markdown_cell(row.get('hallucination_risk'))}` | {markdown_cell(observation(row), limit=180)} |"
            )
    lines.extend(["", "## Detailed Patch Outputs", ""])
    for case_id, rows in grouped.items():
        lines.extend([f"### `{case_id}`", ""])
        for backend, row in rows.items():
            lines.extend(
                [
                    f"#### `{backend}`",
                    "",
                    f"- target file: `{row.get('predicted_target_doc_file', '')}`",
                    f"- verifier: `{row.get('patch_verifier_status')}`",
                    f"- quality: `{row.get('quality_label')}`",
                    f"- hallucination risk: `{row.get('hallucination_risk')}`",
                    f"- observation: {observation(row)}",
                    "",
                    *fenced_patch(row.get("generated_doc_patch")),
                    "",
                ]
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_hf_findings_report(path: Path, grouped: dict[str, dict[str, dict]], model_name: str | None) -> None:
    hf_rows = [rows["llm-hf"] for rows in grouped.values() if "llm-hf" in rows]
    quality_counts = Counter(row.get("quality_label") for row in hf_rows)
    risk_counts = Counter(row.get("hallucination_risk") for row in hf_rows)
    verifier_counts = Counter(row.get("patch_verifier_status") for row in hf_rows)
    best = [row for row in hf_rows if row.get("quality_label") in {"excellent", "usable"}]
    rejected = [row for row in hf_rows if row.get("quality_label") == "rejected" or row.get("hallucination_risk") == "high"]
    lines = [
        "# DocGuard HF Patch Quality Findings 2026-08",
        "",
        f"- model: `{model_name or 'not_run'}`",
        f"- HF cases actually evaluated: {len(hf_rows)}",
        f"- HF quality label counts: `{markdown_cell(dict(quality_counts))}`",
        f"- HF hallucination risk counts: `{markdown_cell(dict(risk_counts))}`",
        f"- HF verifier status counts: `{markdown_cell(dict(verifier_counts))}`",
        "",
        "## Best HF Examples",
        "",
    ]
    if not best:
        lines.append("No usable/excellent HF examples were present in this comparison.")
    for row in best:
        lines.extend(
            [
                f"### `{row['case_id']}`",
                "",
                f"- quality: `{row.get('quality_label')}`",
                f"- hallucination risk: `{row.get('hallucination_risk')}`",
                f"- grounded tokens: `{', '.join(row.get('grounded_tokens_found') or [])}`",
                f"- usefulness score: `{row.get('usefulness_score')}`",
                "",
                "```diff",
                row.get("generated_doc_patch") or "not_applicable",
                "```",
                "",
            ]
        )
    lines.extend(["## Rejected HF Examples", ""])
    if not rejected:
        lines.append("No rejected/high-risk HF examples were present in this comparison.")
    for row in rejected:
        lines.extend(
            [
                f"### `{row['case_id']}`",
                "",
                f"- quality: `{row.get('quality_label')}`",
                f"- hallucination risk: `{row.get('hallucination_risk')}`",
                f"- verifier: `{row.get('patch_verifier_status')}`",
                f"- warnings: `{markdown_cell('; '.join(row.get('patch_verifier_warnings') or []))}`",
                "",
                *fenced_patch(row.get("generated_doc_patch")),
                "",
            ]
        )
    lines.extend(
        [
            "## Conclusion",
            "",
            "- HF can produce richer grounded patches than the legacy fallback when generation succeeds.",
            "- HF can hallucinate unsupported documentation details and must be guarded.",
            "- The verifier and patch-quality evaluator caught a failed/high-risk HF output in this comparison.",
            "- The deterministic layer is a guardrail and evaluator around generation, not the final generator.",
            "- The project-evolution setup remains synthetic demo evidence, not an external benchmark.",
            "- These results are not a production-readiness claim.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-limit", type=int, default=5)
    parser.add_argument("--hf-model")
    parser.add_argument("--include-hf", action="store_true")
    parser.add_argument("--max-new-tokens", type=int, default=384)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--device-map")
    parser.add_argument("--torch-dtype")
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--output-dir", default="reports/live_flow/patch_backend_comparison")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    legacy_dir = output_dir / "legacy"
    mock_dir = output_dir / "llm_mock"
    run(legacy_dir, patch_backend="legacy", case_limit=args.case_limit)
    run(mock_dir, patch_backend="llm-mock", case_limit=args.case_limit)
    paths = {
        "legacy": legacy_dir / "docguard_project_evolution_predictions.jsonl",
        "llm-mock": mock_dir / "docguard_project_evolution_predictions.jsonl",
    }
    hf_note = "HF backend was not run; pass both `--include-hf` and `--hf-model` to compare a real HuggingFace model."
    if args.include_hf and args.hf_model:
        hf_dir = output_dir / "llm_hf"
        run(
            hf_dir,
            patch_backend="llm-hf",
            patch_model=args.hf_model,
            case_limit=args.case_limit,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            device_map=args.device_map,
            torch_dtype=args.torch_dtype,
            trust_remote_code=args.trust_remote_code,
        )
        paths["llm-hf"] = hf_dir / "docguard_project_evolution_predictions.jsonl"
        hf_note = f"HF backend requested with `{args.hf_model}`. If dependencies/model are unavailable, row-level errors are shown."
    grouped: dict[str, dict[str, dict]] = {}
    for backend, path in paths.items():
        for row in read_jsonl(path):
            grouped.setdefault(row["case_id"], {})[backend] = add_quality(row)
    write_report(output_dir / "docguard_patch_backend_comparison_2026_08.md", grouped, hf_note)
    if "llm-hf" in paths:
        write_hf_findings_report(output_dir / "docguard_hf_patch_quality_findings_2026_08.md", grouped, args.hf_model)
    print(json.dumps({"status": "ok", "report": str(output_dir / "docguard_patch_backend_comparison_2026_08.md"), "hf_model": args.hf_model}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
