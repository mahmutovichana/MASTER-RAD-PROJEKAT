from __future__ import annotations

import argparse
import json

from docguard_llm.evaluator import DATA_DIR, REPORTS_DIR, evaluate_model, read_jsonl, split_path, write_comparison_report, write_jsonl, write_model_report
from docguard_llm.llm_agent import predict
from docguard_llm.model_registry import get_model_config, list_models
from docguard_llm.prompt_builder import select_few_shot_examples


def list_models_command(_args: argparse.Namespace) -> int:
    print(json.dumps(list_models(), indent=2, ensure_ascii=False))
    return 0


def evaluate_command(args: argparse.Namespace) -> int:
    metrics, predictions = evaluate_model(args.split, args.model, args.backend, args.limit)
    suffix = f"v0_3_{args.split}_{args.model}"
    write_jsonl(DATA_DIR / f"llm_predictions_{suffix}.jsonl", predictions)
    write_model_report(REPORTS_DIR / f"llm_evaluation_v0_3_{args.model}.md", args.model, args.split, args.backend, metrics)
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    return 0


def compare_command(args: argparse.Namespace) -> int:
    all_metrics = {}
    for model_key in list_models():
        metrics, predictions = evaluate_model(args.split, model_key, args.backend, args.limit)
        all_metrics[model_key] = metrics
        write_jsonl(DATA_DIR / f"llm_predictions_v0_3_{args.split}_{model_key}.jsonl", predictions)
        write_model_report(REPORTS_DIR / f"llm_evaluation_v0_3_{model_key}.md", model_key, args.split, args.backend, metrics)
    write_comparison_report(REPORTS_DIR / "llm_model_comparison_v0_3.md", args.split, all_metrics)
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
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

