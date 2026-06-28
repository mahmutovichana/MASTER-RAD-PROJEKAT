from __future__ import annotations

import argparse
import json

from docguard_hf_classifier.dataset_export import export
from docguard_hf_classifier.text_builder import DEFAULT_INPUT_MODE, INPUT_MODES


def print_json(payload: dict) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def export_command(args: argparse.Namespace) -> int:
    print_json(export(args.version, args.input_mode))
    return 0


def train_embeddings_command(args: argparse.Namespace) -> int:
    from docguard_hf_classifier.embedding_classifier import train
    try:
        print_json(train(args.version, args.model, args.backend, args.input_mode))
    except RuntimeError as exc:
        print(str(exc))
        return 2
    return 0


def evaluate_embeddings_command(args: argparse.Namespace) -> int:
    from docguard_hf_classifier.embedding_classifier import evaluate
    from docguard_hf_classifier.evaluator import write_error_analysis
    try:
        metrics, _predictions = evaluate(args.split, args.input_mode)
        if args.split == "validation":
            write_error_analysis(args.split, args.input_mode)
        print_json(metrics)
    except RuntimeError as exc:
        print(str(exc))
        return 2
    return 0


def zero_shot_command(args: argparse.Namespace) -> int:
    from docguard_hf_classifier.zero_shot import evaluate_zero_shot
    try:
        print_json(evaluate_zero_shot(args.version, args.split, args.limit, args.model))
    except RuntimeError as exc:
        print(str(exc))
        return 2
    return 0


def train_sequence_command(args: argparse.Namespace) -> int:
    from docguard_hf_classifier.sequence_classifier import train_sequence
    try:
        print_json(train_sequence(args.task, args.base_model, args.epochs, args.limit_train, args.limit_eval))
    except RuntimeError as exc:
        print(str(exc))
        return 2
    return 0


def evaluate_sequence_command(args: argparse.Namespace) -> int:
    from docguard_hf_classifier.sequence_classifier import evaluate_sequence
    try:
        print_json(evaluate_sequence(args.task, args.split))
    except RuntimeError as exc:
        print(str(exc))
        return 2
    return 0


def ablate_inputs_command(args: argparse.Namespace) -> int:
    from docguard_hf_classifier.evaluator import ablate_inputs, write_leakage_risk_report, write_split_leakage_check
    try:
        results = ablate_inputs(args.version, args.model)
        write_leakage_risk_report()
        write_split_leakage_check(DEFAULT_INPUT_MODE)
        print_json({"version": args.version, "input_modes": list(results)})
    except RuntimeError as exc:
        print(str(exc))
        return 2
    return 0


def stress_test_command(args: argparse.Namespace) -> int:
    from docguard_hf_classifier.evaluator import stress_test
    try:
        print_json(stress_test(args.version, args.input_mode))
    except RuntimeError as exc:
        print(str(exc))
        return 2
    return 0


def leakage_report_command(args: argparse.Namespace) -> int:
    from docguard_hf_classifier.evaluator import write_leakage_risk_report, write_split_leakage_check
    write_leakage_risk_report()
    print_json(write_split_leakage_check(args.input_mode))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="docguard_hf_classifier")
    sub = parser.add_subparsers(dest="command", required=True)
    export_parser = sub.add_parser("export")
    export_parser.add_argument("--version", default="v0_4")
    export_parser.add_argument("--input-mode", choices=INPUT_MODES, default=DEFAULT_INPUT_MODE)
    export_parser.set_defaults(func=export_command)

    train_embeddings = sub.add_parser("train-embeddings")
    train_embeddings.add_argument("--version", default="v0_4")
    train_embeddings.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    train_embeddings.add_argument("--backend", choices=["sentence_transformers", "transformers"], default="sentence_transformers")
    train_embeddings.add_argument("--input-mode", choices=INPUT_MODES, default=DEFAULT_INPUT_MODE)
    train_embeddings.set_defaults(func=train_embeddings_command)

    evaluate_embeddings = sub.add_parser("evaluate-embeddings")
    evaluate_embeddings.add_argument("--version", default="v0_4")
    evaluate_embeddings.add_argument("--split", choices=["train", "validation", "test"], required=True)
    evaluate_embeddings.add_argument("--input-mode", choices=INPUT_MODES, default=DEFAULT_INPUT_MODE)
    evaluate_embeddings.set_defaults(func=evaluate_embeddings_command)

    zero_shot = sub.add_parser("evaluate-zero-shot")
    zero_shot.add_argument("--version", default="v0_4")
    zero_shot.add_argument("--split", choices=["train", "validation", "test"], required=True)
    zero_shot.add_argument("--limit", type=int, default=20)
    zero_shot.add_argument("--model", default="facebook/bart-large-mnli")
    zero_shot.set_defaults(func=zero_shot_command)

    train_sequence = sub.add_parser("train-sequence")
    train_sequence.add_argument("--version", default="v0_4")
    train_sequence.add_argument("--task", choices=["docs_update_required", "doc_category", "target_doc_file", "scenario_type"], required=True)
    train_sequence.add_argument("--base-model", default="distilroberta-base")
    train_sequence.add_argument("--epochs", type=int, default=1)
    train_sequence.add_argument("--limit-train", type=int)
    train_sequence.add_argument("--limit-eval", type=int)
    train_sequence.set_defaults(func=train_sequence_command)

    evaluate_sequence = sub.add_parser("evaluate-sequence")
    evaluate_sequence.add_argument("--version", default="v0_4")
    evaluate_sequence.add_argument("--task", choices=["docs_update_required", "doc_category", "target_doc_file", "scenario_type"], required=True)
    evaluate_sequence.add_argument("--split", choices=["train", "validation", "test"], required=True)
    evaluate_sequence.set_defaults(func=evaluate_sequence_command)

    ablate = sub.add_parser("ablate-inputs")
    ablate.add_argument("--version", default="v0_4")
    ablate.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    ablate.set_defaults(func=ablate_inputs_command)

    stress = sub.add_parser("stress-test")
    stress.add_argument("--version", default="v0_4")
    stress.add_argument("--input-mode", choices=INPUT_MODES, default=DEFAULT_INPUT_MODE)
    stress.set_defaults(func=stress_test_command)

    leakage = sub.add_parser("leakage-check")
    leakage.add_argument("--version", default="v0_4")
    leakage.add_argument("--input-mode", choices=INPUT_MODES, default=DEFAULT_INPUT_MODE)
    leakage.set_defaults(func=leakage_report_command)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
