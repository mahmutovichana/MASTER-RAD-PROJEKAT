from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from docguard_hybrid.hybrid_agent import predict
from docguard_llm.evaluation import write_llm_mock_patch_report
from docguard_llm.llm_generator import generate_documentation_patch
from docguard_llm.patch_postprocessor import postprocess_patch
from docguard_llm.patch_verifier import verify_patch
from docguard_llm.prompt_builder import build_patch_prompt

from docguard_demo.project_evolution_scenarios import BASE_DIR, generate_project_evolution_cases


@dataclass
class PatchBackendOptions:
    backend: str = "legacy"
    model_name: str | None = None
    max_new_tokens: int = 512
    temperature: float = 0.2
    device_map: str | None = None
    torch_dtype: str | None = None
    trust_remote_code: bool = False
    save_prompts: bool = True


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def prediction_input(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": record["case_id"],
        "project_id": record["project_id"],
        "changed_files": record["code_changed_files"],
        "code_diff": record["code_diff"],
        "docs_before": record["docs_before"],
    }


def generate_patch_with_backend(record: dict[str, Any], pred: dict[str, Any], options: PatchBackendOptions) -> dict[str, Any]:
    if options.backend == "legacy":
        verifier = verify_patch(
            pred.get("generated_doc_patch"),
            bool(pred["docs_update_required"]),
            pred.get("target_doc_file") or "",
            record["code_diff"],
            record["docs_before"],
            pred.get("doc_category"),
            pred.get("scenario_type"),
        )
        return {
            "patch_backend": "legacy",
            "patch_model": "",
            "llm_prompt": "",
            "llm_patch_raw": "",
            "llm_generation_status": "not_applicable",
            "llm_error_message": "",
            "llm_latency_seconds": None,
            "generated_doc_patch": pred.get("generated_doc_patch"),
            "patch_verifier_status": verifier["verifier_status"],
            "patch_verifier_warnings": verifier["warnings"],
            "grounded_tokens_found": verifier["grounded_tokens_found"],
        }
    if options.backend not in {"llm-mock", "llm-hf"}:
        raise ValueError(f"Unsupported patch backend: {options.backend}")
    if options.backend == "llm-hf" and not options.model_name:
        raise ValueError("--patch-model is required when --patch-backend llm-hf")
    if not pred["docs_update_required"]:
        verifier = verify_patch(None, False, "", record["code_diff"], record["docs_before"], pred.get("doc_category"), pred.get("scenario_type"))
        return {
            "patch_backend": options.backend,
            "patch_model": options.model_name or "",
            "llm_prompt": "",
            "llm_patch_raw": "",
            "llm_generation_status": "not_applicable",
            "llm_error_message": "",
            "llm_latency_seconds": None,
            "generated_doc_patch": None,
            "patch_verifier_status": verifier["verifier_status"],
            "patch_verifier_warnings": verifier["warnings"],
            "grounded_tokens_found": verifier["grounded_tokens_found"],
        }
    router = pred.get("router_output") or {}
    prompt, _metadata = build_patch_prompt(
        code_diff=record["code_diff"],
        docs_before=record["docs_before"],
        target_doc_file=pred["target_doc_file"],
        doc_category=pred["doc_category"],
        scenario_type=pred["scenario_type"],
        signals=router.get("signals") or [],
        router_reason=router.get("router_reason") or "",
        project_id=record["project_id"],
        target_section=None,
    )
    generated = generate_documentation_patch(
        prompt,
        backend="mock" if options.backend == "llm-mock" else "hf",
        model_name=options.model_name,
        max_new_tokens=options.max_new_tokens,
        temperature=options.temperature,
        device_map=options.device_map,
        torch_dtype=options.torch_dtype,
        trust_remote_code=options.trust_remote_code,
    )
    postprocessed = postprocess_patch(generated.get("patch_text"), pred["target_doc_file"], None)
    patch_text = postprocessed.get("patch_text")
    verifier = verify_patch(patch_text, True, pred["target_doc_file"], record["code_diff"], record["docs_before"], pred.get("doc_category"), pred.get("scenario_type"))
    warnings = list(postprocessed.get("warnings") or []) + list(verifier.get("warnings") or [])
    return {
        "patch_backend": options.backend,
        "patch_model": options.model_name or "",
        "llm_prompt": prompt if options.save_prompts else "",
        "llm_patch_raw": generated.get("patch_text") or "",
        "llm_generation_status": generated.get("generation_status") or "unknown",
        "llm_error_message": generated.get("error_message") or "",
        "llm_latency_seconds": generated.get("latency_seconds"),
        "generated_doc_patch": patch_text,
        "patch_verifier_status": verifier["verifier_status"] if postprocessed["postprocess_status"] == "ok" else "fail",
        "patch_verifier_warnings": warnings,
        "grounded_tokens_found": verifier["grounded_tokens_found"],
    }


def evaluate(records: list[dict[str, Any]], patch_options: PatchBackendOptions | None = None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    options = patch_options or PatchBackendOptions()
    rows = []
    by_project: dict[str, Counter] = defaultdict(Counter)
    by_category: dict[str, Counter] = defaultdict(Counter)
    by_difficulty: dict[str, Counter] = defaultdict(Counter)
    tp = fp = tn = fn = 0
    patch_positive = positive_total = unknown = 0
    for record in records:
        pred = predict(prediction_input(record))
        patch_result = generate_patch_with_backend(record, pred, options)
        pred["generated_doc_patch"] = patch_result["generated_doc_patch"]
        router = pred.get("router_output") or {}
        gold_required = bool(record["gold_docs_update_required"])
        predicted_required = bool(pred["docs_update_required"])
        binary_pass = gold_required == predicted_required
        category_pass = record["gold_doc_category"] == pred["doc_category"]
        target_pass = record["gold_target_doc_file"] == pred["target_doc_file"]
        scenario_pass = record["scenario_type"] == pred["scenario_type"]
        if gold_required and predicted_required:
            tp += 1
        elif gold_required and not predicted_required:
            fn += 1
        elif not gold_required and predicted_required:
            fp += 1
        else:
            tn += 1
        if gold_required:
            positive_total += 1
            patch_positive += int(bool(pred.get("generated_doc_patch")))
        unknown += int(pred["scenario_type"] == "unknown_change")
        for bucket in [by_project[record["project_id"]], by_category[record["gold_doc_category"]], by_difficulty[record["difficulty"]]]:
            bucket["total"] += 1
            bucket["binary"] += int(binary_pass)
            bucket["category"] += int(category_pass)
            bucket["target"] += int(target_pass)
            bucket["scenario"] += int(scenario_pass)
        rows.append(
            {
                "case_id": record["case_id"],
                "project_id": record["project_id"],
                "pr_title": record["pr_title"],
                "difficulty": record["difficulty"],
                "code_diff_excerpt": record["code_diff"],
                "docs_before_excerpt": record["docs_before"],
                "gold_docs_update_required": gold_required,
                "predicted_docs_update_required": predicted_required,
                "gold_doc_category": record["gold_doc_category"],
                "predicted_doc_category": pred["doc_category"],
                "gold_scenario_type": record["scenario_type"],
                "predicted_scenario_type": pred["scenario_type"],
                "gold_target_doc_file": record["gold_target_doc_file"],
                "predicted_target_doc_file": pred["target_doc_file"],
                "generated_doc_patch": pred.get("generated_doc_patch"),
                "patch_backend": patch_result["patch_backend"],
                "patch_model": patch_result["patch_model"],
                "llm_prompt": patch_result["llm_prompt"],
                "llm_patch_raw": patch_result["llm_patch_raw"],
                "llm_generation_status": patch_result["llm_generation_status"],
                "llm_error_message": patch_result["llm_error_message"],
                "llm_latency_seconds": patch_result["llm_latency_seconds"],
                "patch_verifier_status": patch_result["patch_verifier_status"],
                "patch_verifier_warnings": patch_result["patch_verifier_warnings"],
                "grounded_tokens_found": patch_result["grounded_tokens_found"],
                "expected_patch_summary": record["expected_patch_summary"],
                "router_reason": router.get("router_reason"),
                "signals_detected": router.get("signals") or [],
                "binary_pass": binary_pass,
                "category_pass": category_pass,
                "target_file_pass": target_pass,
                "scenario_pass": scenario_pass,
                "realism_notes": record["realism_notes"],
            }
        )
    total = len(records)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    metrics = {
        "total_cases": total,
        "binary_accuracy": (tp + tn) / total if total else 0.0,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "category_accuracy": sum(row["category_pass"] for row in rows) / total if total else 0.0,
        "target_file_accuracy": sum(row["target_file_pass"] for row in rows) / total if total else 0.0,
        "scenario_accuracy": sum(row["scenario_pass"] for row in rows) / total if total else 0.0,
        "patch_non_empty_rate_for_positive_cases": patch_positive / positive_total if positive_total else 0.0,
        "false_positives": fp,
        "false_negatives": fn,
        "unknown_scenarios": unknown,
        "by_project": summarize_buckets(by_project),
        "by_category": summarize_buckets(by_category),
        "by_difficulty": summarize_buckets(by_difficulty),
    }
    return metrics, rows


def summarize_buckets(buckets: dict[str, Counter]) -> dict[str, dict[str, float | int]]:
    result = {}
    for name, values in sorted(buckets.items()):
        total = values["total"]
        result[name] = {
            "total": total,
            "binary_accuracy": values["binary"] / total if total else 0.0,
            "category_accuracy": values["category"] / total if total else 0.0,
            "target_accuracy": values["target"] / total if total else 0.0,
            "scenario_accuracy": values["scenario"] / total if total else 0.0,
        }
    return result


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def table(lines: list[str], title: str, rows: dict[str, dict[str, Any]]) -> None:
    lines.extend(["", f"## {title}", "", "| Name | Total | Binary | Category | Target | Scenario |", "| --- | ---: | ---: | ---: | ---: | ---: |"])
    for name, values in rows.items():
        lines.append(
            f"| `{name}` | {values['total']} | {pct(values['binary_accuracy'])} | {pct(values['category_accuracy'])} | "
            f"{pct(values['target_accuracy'])} | {pct(values['scenario_accuracy'])} |"
        )


def write_report(path: Path, metrics: dict[str, Any], predictions: list[dict[str, Any]], patch_backend: str) -> None:
    lines = [
        "# DocGuard Project Evolution Evaluation 2026-08",
        "",
        "This is a synthetic project-evolution live demo. It simulates multiple PR-like changes across invented projects and runs `docguard_hybrid.predict()` with sanitized input only: code-side changed files, code diff, docs-before excerpt, project id, and case id.",
        "",
        f"- Patch backend: `{patch_backend}`",
        "",
        "## Summary Metrics",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]
    for key in ["total_cases", "binary_accuracy", "precision", "recall", "f1", "category_accuracy", "target_file_accuracy", "scenario_accuracy", "patch_non_empty_rate_for_positive_cases", "false_positives", "false_negatives", "unknown_scenarios"]:
        value = metrics[key]
        lines.append(f"| `{key}` | {pct(value) if isinstance(value, float) else value} |")
    table(lines, "By Project", metrics["by_project"])
    table(lines, "By Category", metrics["by_category"])
    table(lines, "By Difficulty", metrics["by_difficulty"])
    lines.extend(
        [
            "",
            "## Per-Case Walkthrough Table",
            "",
            "| Case | Project | Difficulty | Binary | Category | Target | Scenario | Gold target | Pred target | Signals |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in predictions:
        lines.append(
            f"| `{item['case_id']}` | `{item['project_id']}` | `{item['difficulty']}` | `{item['binary_pass']}` | `{item['category_pass']}` | "
            f"`{item['target_file_pass']}` | `{item['scenario_pass']}` | `{item['gold_target_doc_file']}` | `{item['predicted_target_doc_file']}` | `{', '.join(item['signals_detected'])}` |"
        )
    lines.extend(["", "## Case Details", ""])
    for item in predictions:
        lines.extend(case_markdown(item))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def case_markdown(item: dict[str, Any]) -> list[str]:
    interpretation = "DocGuard matched the intended route." if all([item["binary_pass"], item["category_pass"], item["target_file_pass"], item["scenario_pass"]]) else "DocGuard missed at least one expected dimension; inspect router reason and signals."
    return [
        f"### `{item['case_id']}` {item['pr_title']}",
        "",
        f"- Project: `{item['project_id']}`",
        f"- Difficulty: `{item['difficulty']}`",
        f"- Gold/pred docs update: `{item['gold_docs_update_required']}` / `{item['predicted_docs_update_required']}`",
        f"- Gold/pred category: `{item['gold_doc_category']}` / `{item['predicted_doc_category']}`",
        f"- Gold/pred scenario: `{item['gold_scenario_type']}` / `{item['predicted_scenario_type']}`",
        f"- Gold/pred target: `{item['gold_target_doc_file']}` / `{item['predicted_target_doc_file']}`",
        f"- Expected patch summary: {item['expected_patch_summary']}",
        f"- Router reason: {item['router_reason']}",
        f"- Signals: `{', '.join(item['signals_detected'])}`",
        f"- Patch backend/verifier: `{item['patch_backend']}` / `{item['patch_verifier_status']}`",
        f"- Patch model/generation: `{item['patch_model'] or 'none'}` / `{item['llm_generation_status']}`",
        f"- LLM error: `{item['llm_error_message']}`",
        f"- Grounded tokens found: `{', '.join(item['grounded_tokens_found'])}`",
        f"- Patch verifier warnings: `{'; '.join(item['patch_verifier_warnings'])}`",
        f"- Interpretation: {interpretation}",
        "",
        "Code diff:",
        "",
        "```diff",
        item["code_diff_excerpt"].strip(),
        "```",
        "",
        "Docs before:",
        "",
        "```md",
        item["docs_before_excerpt"].strip(),
        "```",
        "",
        "Generated patch:",
        "",
        "```diff",
        item["generated_doc_patch"] or "not_applicable",
        "```",
        "",
    ]


def write_failure_analysis(path: Path, predictions: list[dict[str, Any]]) -> None:
    failures = [item for item in predictions if not all([item["binary_pass"], item["category_pass"], item["target_file_pass"], item["scenario_pass"]])]
    if not failures:
        if path.exists():
            path.unlink()
        return
    lines = ["# DocGuard Project Evolution Failure Analysis 2026-08", "", "Failures are kept visible; gold labels were not changed.", ""]
    for item in failures:
        if "docs_already_updated" in item["signals_detected"] and item["predicted_docs_update_required"]:
            likely_cause = "router priority issue: a no-update docs-already-aligned signal was present, but the positive route signal won."
        elif item["predicted_scenario_type"] == "unknown_change":
            likely_cause = "signal extractor gap: no specific documentation-impact signal was detected."
        elif item["binary_pass"] and not item["scenario_pass"]:
            likely_cause = "router mapping or gold-scenario strictness: the update decision was correct but the scenario label differed."
        else:
            likely_cause = "signal extractor gap, router mapping issue, generic patching, case ambiguity, or strict gold scenario."
        lines.extend(
            [
                f"## `{item['case_id']}` {item['pr_title']}",
                "",
                f"- Project: `{item['project_id']}`",
                f"- Failed binary/category/target/scenario: `{not item['binary_pass']}` / `{not item['category_pass']}` / `{not item['target_file_pass']}` / `{not item['scenario_pass']}`",
                f"- Router reason: {item['router_reason']}",
                f"- Signals: `{', '.join(item['signals_detected'])}`",
                f"- Likely cause: {likely_cause}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_walkthrough(path: Path, predictions: list[dict[str, Any]]) -> None:
    selected_categories = ["api_reference", "configuration", "workflow_documentation", "model_contract", "no_update"]
    selected = []
    for category in selected_categories:
        item = next((item for item in predictions if item["gold_doc_category"] == category), None)
        if item is not None:
            selected.append(item)
    lines = [
        "# DocGuard Project Evolution Walkthrough 2026-08",
        "",
        "This narrative report is for human inspection and thesis/demo screenshots. It shows what changed, what the documentation said before, what DocGuard detected, where it routed, and what patch it proposed.",
        "",
    ]
    for item in selected:
        useful = "useful as a concise starting patch" if item["generated_doc_patch"] else "not applicable because DocGuard predicted no update"
        lines.extend(
            [
                f"## `{item['case_id']}` {item['pr_title']}",
                "",
                f"Simulated developer change: {item['expected_patch_summary']}",
                "",
                "Relevant code diff:",
                "",
                "```diff",
                item["code_diff_excerpt"].strip(),
                "```",
                "",
                "Documentation before:",
                "",
                "```md",
                item["docs_before_excerpt"].strip(),
                "```",
                "",
                f"What DocGuard understood: docs update `{item['predicted_docs_update_required']}`, category `{item['predicted_doc_category']}`, scenario `{item['predicted_scenario_type']}`.",
                "",
                f"DocGuard detected signals: `{', '.join(item['signals_detected'])}`.",
                "",
                f"Where DocGuard wanted to write: `{item['predicted_target_doc_file'] or 'none'}`.",
                "",
                f"Why DocGuard decided that: {item['router_reason']}",
                "",
                "Generated patch:",
                "",
                "```diff",
                item["generated_doc_patch"] or "not_applicable",
                "```",
                "",
                f"Patch usefulness: {useful}. The patch is intentionally generic and should be reviewed by a developer before applying.",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def update_evolution_logs(predictions: list[dict[str, Any]]) -> None:
    by_project: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in predictions:
        by_project[item["project_id"]].append(item)
    for project_id, items in by_project.items():
        path = BASE_DIR / project_id / "evolution_log.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = text.replace("- DocGuard prediction: pending runner execution", "- DocGuard prediction: see generated results below")
        lines = [text.rstrip(), "", "## DocGuard Runner Results", ""]
        for item in items:
            lines.append(
                f"- `{item['case_id']}`: docs `{item['predicted_docs_update_required']}`, category `{item['predicted_doc_category']}`, target `{item['predicted_target_doc_file'] or 'none'}`."
            )
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    output_dir: Path,
    patch_backend: str = "legacy",
    patch_model: str | None = None,
    case_limit: int | None = None,
    max_new_tokens: int = 512,
    temperature: float = 0.2,
    device_map: str | None = None,
    torch_dtype: str | None = None,
    trust_remote_code: bool = False,
    save_prompts: bool = True,
) -> dict[str, Any]:
    records = generate_project_evolution_cases()
    if case_limit is not None:
        records = records[:case_limit]
    patch_options = PatchBackendOptions(
        backend=patch_backend,
        model_name=patch_model,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        device_map=device_map,
        torch_dtype=torch_dtype,
        trust_remote_code=trust_remote_code,
        save_prompts=save_prompts,
    )
    metrics, predictions = evaluate(records, patch_options=patch_options)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_dir / "docguard_project_evolution_predictions.jsonl", predictions)
    write_report(output_dir / "docguard_project_evolution_evaluation_2026_08.md", metrics, predictions, patch_backend)
    write_failure_analysis(output_dir / "docguard_project_evolution_failure_analysis_2026_08.md", predictions)
    write_walkthrough(output_dir / "docguard_project_evolution_walkthrough_2026_08.md", predictions)
    if patch_backend == "llm-mock":
        write_llm_mock_patch_report(output_dir / "docguard_llm_mock_patch_generation_report_2026_08.md", predictions, len(records))
    update_evolution_logs(predictions)
    return {"status": "ok", "output_dir": str(output_dir), "patch_backend": patch_backend, "patch_model": patch_model, **{k: v for k, v in metrics.items() if not k.startswith("by_")}}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="reports/live_flow/project_evolution")
    parser.add_argument("--patch-backend", choices=["legacy", "llm-mock", "llm-hf"], default="legacy")
    parser.add_argument("--patch-model")
    parser.add_argument("--case-limit", type=int)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--device-map")
    parser.add_argument("--torch-dtype")
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--save-prompts", action=argparse.BooleanOptionalAction, default=True)
    args = parser.parse_args()
    print(json.dumps(run(
        Path(args.output_dir),
        patch_backend=args.patch_backend,
        patch_model=args.patch_model,
        case_limit=args.case_limit,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        device_map=args.device_map,
        torch_dtype=args.torch_dtype,
        trust_remote_code=args.trust_remote_code,
        save_prompts=args.save_prompts,
    ), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
