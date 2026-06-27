from __future__ import annotations

import argparse
import json
from pathlib import Path

from docguard_llm.evaluator import DATA_DIR, MOCK_WARNING, REPORTS_DIR, evaluate_model, read_jsonl, write_comparison_report, write_jsonl, write_model_report
from docguard_llm.llm_agent import predict
from docguard_llm.model_registry import get_model_config, list_models
from docguard_llm.prompt_builder import select_few_shot_examples


def backend_tag(backend: str) -> str:
    return "mock" if backend == "mock" else backend


def prediction_path(split: str, model_key: str, backend: str) -> Path:
    return DATA_DIR / f"llm_predictions_v0_3_{split}_{backend_tag(backend)}_{model_key}.jsonl"


def model_report_path(model_key: str, backend: str) -> Path:
    return REPORTS_DIR / f"llm_evaluation_v0_3_{backend_tag(backend)}_{model_key}.md"


def comparison_report_path(backend: str) -> Path:
    return REPORTS_DIR / f"llm_model_comparison_v0_3_{backend_tag(backend)}.md"


def write_mock_compatibility_files(split: str, model_key: str, predictions: list[dict], metrics: dict) -> None:
    write_jsonl(DATA_DIR / f"llm_predictions_v0_3_{split}_{model_key}.jsonl", predictions)
    write_model_report(REPORTS_DIR / f"llm_evaluation_v0_3_{model_key}.md", model_key, split, "mock", metrics)


def list_models_command(_args: argparse.Namespace) -> int:
    print(json.dumps(list_models(), indent=2, ensure_ascii=False))
    return 0


def evaluate_command(args: argparse.Namespace) -> int:
    metrics, predictions = evaluate_model(args.split, args.model, args.backend, args.limit)
    write_jsonl(prediction_path(args.split, args.model, args.backend), predictions)
    write_model_report(model_report_path(args.model, args.backend), args.model, args.split, args.backend, metrics)
    if args.backend == "mock":
        write_mock_compatibility_files(args.split, args.model, predictions, metrics)
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    return 0


def compare_command(args: argparse.Namespace) -> int:
    all_metrics = {}
    for model_key in list_models():
        metrics, predictions = evaluate_model(args.split, model_key, args.backend, args.limit)
        all_metrics[model_key] = metrics
        write_jsonl(prediction_path(args.split, model_key, args.backend), predictions)
        write_model_report(model_report_path(model_key, args.backend), model_key, args.split, args.backend, metrics)
        if args.backend == "mock":
            write_mock_compatibility_files(args.split, model_key, predictions, metrics)
    write_comparison_report(comparison_report_path(args.backend), args.split, all_metrics, args.backend)
    if args.backend == "mock":
        write_comparison_report(REPORTS_DIR / "llm_model_comparison_v0_3.md", args.split, all_metrics, args.backend)
    print(json.dumps(all_metrics, indent=2, ensure_ascii=False))
    return 0


def predict_command(args: argparse.Namespace) -> int:
    records = read_jsonl(DATA_DIR / "docguard_dataset.jsonl")
    record = next((r for r in records if r["id"] == args.record_id), None)
    if not record:
        raise SystemExit(f"Record not found: {args.record_id}")
    prediction = predict(record, args.model, args.backend, select_few_shot_examples())
    print(json.dumps(prediction, indent=2, ensure_ascii=False))
    return 0


def smoke_test_command(args: argparse.Namespace) -> int:
    record = read_jsonl(DATA_DIR / "validation.jsonl")[0]
    report_path = REPORTS_DIR / f"real_llm_smoke_test_{args.model}.md"
    try:
        prediction = predict(record, args.model, args.backend, select_few_shot_examples())
    except Exception as exc:
        message = str(exc) or exc.__class__.__name__
        lines = [
            f"# Real LLM Smoke Test: {args.model}",
            "",
            f"- backend: {args.backend}",
            "- status: failed",
            "",
            "The selected backend could not complete one validation prediction.",
            "",
            f"Clear message: {message}",
            "",
            "For local Transformers runs, install optional dependencies with:",
            "",
            "```bash",
            "pip install transformers accelerate torch sentencepiece",
            "```",
            "",
            "If hardware is the issue, try `qwen2_5_coder_3b` first or use a local vLLM/TGI OpenAI-compatible server.",
        ]
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(json.dumps({"status": "failed", "model": args.model, "backend": args.backend, "message": message, "report": str(report_path)}, indent=2))
        return 1
    lines = [
        f"# Real LLM Smoke Test: {args.model}",
        "",
        f"- backend: {args.backend}",
        "- status: succeeded",
        f"- record_id: {record['id']}",
        "",
        "## Structured Prediction",
        "",
        "```json",
        json.dumps(prediction, indent=2, ensure_ascii=False),
        "```",
    ]
    if args.backend == "mock":
        lines[1:1] = ["", f"> {MOCK_WARNING}"]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(prediction, indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="docguard_llm")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list-models").set_defaults(func=list_models_command)
    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("--split", choices=["train", "validation", "test"], required=True)
    evaluate.add_argument("--model", choices=list(list_models()), required=True)
    evaluate.add_argument("--backend", choices=["mock", "transformers_local", "text_generation_inference"], default="mock")
    evaluate.add_argument("--limit", type=int)
    evaluate.set_defaults(func=evaluate_command)
    compare = sub.add_parser("compare")
    compare.add_argument("--split", choices=["train", "validation", "test"], required=True)
    compare.add_argument("--backend", choices=["mock", "transformers_local", "text_generation_inference"], default="mock")
    compare.add_argument("--limit", type=int)
    compare.set_defaults(func=compare_command)
    predict_parser = sub.add_parser("predict")
    predict_parser.add_argument("--record-id", required=True)
    predict_parser.add_argument("--model", choices=list(list_models()), required=True)
    predict_parser.add_argument("--backend", choices=["mock", "transformers_local", "text_generation_inference"], default="mock")
    predict_parser.set_defaults(func=predict_command)
    smoke = sub.add_parser("smoke-test")
    smoke.add_argument("--model", choices=list(list_models()), required=True)
    smoke.add_argument("--backend", choices=["mock", "transformers_local", "text_generation_inference"], default="transformers_local")
    smoke.set_defaults(func=smoke_test_command)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
