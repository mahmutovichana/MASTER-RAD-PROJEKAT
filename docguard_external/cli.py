from __future__ import annotations

import argparse
import json
from pathlib import Path

from docguard_external.codocbench_adapter import inspect_codocbench, prepare_codocbench, validate_codocbench_sample
from docguard_external.comment_update_adapter import prepare_comment_update
from docguard_external.dataset_card import describe_candidate, list_candidates
from docguard_external.schema import validate_record


def emit(payload: object) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def list_command(_args: argparse.Namespace) -> int:
    emit(list_candidates())
    return 0


def describe_command(args: argparse.Namespace) -> int:
    try:
        emit(describe_candidate(args.dataset))
        return 0
    except KeyError as exc:
        emit({"status": "error", "message": str(exc)})
        return 2


def prepare_command(args: argparse.Namespace) -> int:
    output = Path(args.output)
    if args.dataset == "codocbench":
        result = prepare_codocbench(
            args.limit,
            output,
            split=args.split,
            exclude_whitespace_only=args.exclude_whitespace_only,
            max_per_project=args.max_per_project,
            seed=args.seed,
            shuffle=args.shuffle,
        )
        emit(result)
        return 0 if result.get("status") == "ok" else 2
    if args.dataset == "comment_update":
        emit(prepare_comment_update(args.limit, output))
        return 2
    if args.dataset == "docchecker":
        from docguard_external.docchecker_adapter import prepare_docchecker

        result = prepare_docchecker(data_dir=Path(args.data_dir) if args.data_dir else None, limit=args.limit, output=output)
        emit(result)
        return 0 if result.get("status") == "ok" else 2
    emit({"status": "error", "message": f"prepare is not implemented for {args.dataset}"})
    return 2


def inspect_command(args: argparse.Namespace) -> int:
    if args.dataset == "codocbench":
        result = inspect_codocbench(args.limit)
        emit(result)
        return 0 if result.get("status") in {"ok", "fallback"} else 2
    if args.dataset == "docchecker":
        from docguard_external.docchecker_adapter import inspect_docchecker

        result = inspect_docchecker(Path(args.data_dir) if args.data_dir else None, args.limit)
        emit(result)
        return 0 if result.get("status") in {"needs_local_data", "local_files_inspected"} else 2
    if args.dataset == "panthaplackel_comment_update":
        from docguard_external.panthaplackel_adapter import inspect_panthaplackel

        result = inspect_panthaplackel(Path(args.data_dir) if args.data_dir else None, args.limit)
        emit(result)
        return 0 if result.get("status") in {"needs_local_data", "local_files_inspected"} else 2
    emit({"status": "error", "message": f"inspect is not implemented for {args.dataset}"})
    return 2


def validate_command(args: argparse.Namespace) -> int:
    path = Path(args.input)
    if "codocbench" in path.name:
        result = validate_codocbench_sample(path)
        emit(result)
        return 0 if result.get("status") == "ok" else 1
    if "docchecker" in path.name or "deep_jit" in path.name:
        from docguard_external.docchecker_adapter import validate_docchecker_binary_sample

        result = validate_docchecker_binary_sample(path)
        emit(result)
        return 0 if result.get("status") == "ok" else 1
    if not path.exists():
        emit({"status": "error", "message": f"input not found: {path}"})
        return 2
    errors = []
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        row_errors = validate_record(row)
        if row_errors:
            errors.append({"line": index, "errors": row_errors})
    emit({"status": "ok" if not errors else "error", "records_checked": index if "index" in locals() else 0, "errors": errors[:50]})
    return 0 if not errors else 1


def evaluate_existing_command(args: argparse.Namespace) -> int:
    from docguard_external.evaluate_existing_docguard import evaluate_existing_docguard

    result = evaluate_existing_docguard(Path(args.input), Path(args.output), external_input_mode=args.external_input_mode)
    emit(result)
    return 0 if result.get("status") == "ok" else 2


def evaluate_synthetic_negatives_command(args: argparse.Namespace) -> int:
    from docguard_external.synthetic_negative_control import evaluate_synthetic_negatives

    result = evaluate_synthetic_negatives(args.limit, args.external_input_mode, Path(args.output))
    emit(result)
    return 0 if result.get("status") == "ok" else 2


def evaluate_existing_binary_command(args: argparse.Namespace) -> int:
    from docguard_external.evaluate_binary import evaluate_existing_binary

    result = evaluate_existing_binary(Path(args.input), Path(args.output))
    emit(result)
    return 0 if result.get("status") == "ok" else 2


def deep_jit_split_audit_command(args: argparse.Namespace) -> int:
    from docguard_external.deep_jit_binary import split_audit

    result = split_audit(Path(args.data_dir))
    emit(result)
    return 0 if result.get("status") == "ok" else 2


def export_deep_jit_binary_command(args: argparse.Namespace) -> int:
    from docguard_external.deep_jit_binary import export_normalized

    result = export_normalized(Path(args.data_dir), Path(args.output_dir))
    emit(result)
    return 0 if result.get("status") == "ok" else 2


def train_binary_command(args: argparse.Namespace) -> int:
    from docguard_external.train_binary_classifier import train_and_evaluate

    result = train_and_evaluate(
        Path(args.train),
        Path(args.validation),
        Path(args.test),
        Path(args.model_output),
        Path(args.report),
        include_sentence_embeddings=args.include_sentence_embeddings,
    )
    emit(result)
    return 0 if result.get("status") == "ok" else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="docguard_external")
    sub = parser.add_subparsers(dest="command", required=True)
    list_parser = sub.add_parser("list-candidates")
    list_parser.set_defaults(func=list_command)
    describe = sub.add_parser("describe")
    describe.add_argument("--dataset", required=True)
    describe.set_defaults(func=describe_command)
    inspect = sub.add_parser("inspect")
    inspect.add_argument("--dataset", required=True)
    inspect.add_argument("--limit", type=int, default=5)
    inspect.add_argument("--data-dir")
    inspect.set_defaults(func=inspect_command)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("--dataset", required=True)
    prepare.add_argument("--limit", type=int, default=100)
    prepare.add_argument("--output", required=True)
    prepare.add_argument("--data-dir")
    prepare.add_argument("--exclude-whitespace-only", action="store_true")
    prepare.add_argument("--max-per-project", type=int)
    prepare.add_argument("--split", default="train")
    prepare.add_argument("--seed", type=int, default=42)
    prepare.add_argument("--shuffle", action="store_true")
    prepare.set_defaults(func=prepare_command)
    validate = sub.add_parser("validate")
    validate.add_argument("--input", required=True)
    validate.set_defaults(func=validate_command)
    evaluate_existing = sub.add_parser("evaluate-existing")
    evaluate_existing.add_argument("--input", required=True)
    evaluate_existing.add_argument("--output", required=True)
    evaluate_existing.add_argument("--diagnostics", action="store_true", help="Accepted for compatibility; diagnostics are always written.")
    evaluate_existing.add_argument(
        "--external-input-mode",
        choices=["code_diff_only", "code_diff_plus_doc_before", "code_diff_plus_doc_diff_upper_bound"],
        default="code_diff_plus_doc_before",
    )
    evaluate_existing.set_defaults(func=evaluate_existing_command)
    evaluate_negatives = sub.add_parser("evaluate-synthetic-negatives")
    evaluate_negatives.add_argument("--limit", type=int, default=500)
    evaluate_negatives.add_argument("--external-input-mode", choices=["code_diff_only", "code_diff_plus_doc_before"], default="code_diff_only")
    evaluate_negatives.add_argument("--output", required=True)
    evaluate_negatives.set_defaults(func=evaluate_synthetic_negatives_command)
    evaluate_binary = sub.add_parser("evaluate-existing-binary")
    evaluate_binary.add_argument("--input", required=True)
    evaluate_binary.add_argument("--output", required=True)
    evaluate_binary.set_defaults(func=evaluate_existing_binary_command)
    split_audit = sub.add_parser("deep-jit-split-audit")
    split_audit.add_argument("--data-dir", required=True)
    split_audit.set_defaults(func=deep_jit_split_audit_command)
    export_deep_jit = sub.add_parser("export-deep-jit-binary")
    export_deep_jit.add_argument("--data-dir", required=True)
    export_deep_jit.add_argument("--output-dir", required=True)
    export_deep_jit.set_defaults(func=export_deep_jit_binary_command)
    train_binary = sub.add_parser("train-binary")
    train_binary.add_argument("--train", required=True)
    train_binary.add_argument("--validation", required=True)
    train_binary.add_argument("--test", required=True)
    train_binary.add_argument("--model-output", required=True)
    train_binary.add_argument("--report", required=True)
    train_binary.add_argument("--include-sentence-embeddings", action="store_true")
    train_binary.set_defaults(func=train_binary_command)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
