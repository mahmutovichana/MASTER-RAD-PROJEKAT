from __future__ import annotations

import argparse
import json

from docguard_hybrid.evaluator import DATA_DIR, REPORTS_DIR, evaluate_records, read_jsonl, write_report


def evaluate_command(args: argparse.Namespace) -> int:
    records = read_jsonl(DATA_DIR / f"{args.split}.jsonl")
    if args.limit:
        records = records[: args.limit]
    hf_predictions = None
    if args.decision_source == "hf_embedding":
        try:
            from docguard_hf_classifier.embedding_classifier import load_predictions_by_id
        except ModuleNotFoundError:
            print("HF classifier package is unavailable.")
            return 2
        hf_predictions = load_predictions_by_id(args.split, args.hf_input_mode)
        if not hf_predictions:
            print("HF embedding predictions are unavailable. Run `python -m docguard_hf_classifier.cli evaluate-embeddings --version v0_4 --split " + args.split + " --input-mode " + args.hf_input_mode + "` first.")
            return 2
    metrics, _predictions = evaluate_records(records, decision_source=args.decision_source, hf_predictions_by_id=hf_predictions)
    suffix = f"_{args.split}" if not args.limit else ""
    prefix = f"hybrid_hf_embedding_evaluation_v0_4_{args.hf_input_mode}" if args.decision_source == "hf_embedding" else "hybrid_evaluation_v0_4"
    write_report(REPORTS_DIR / f"{prefix}{suffix}.md", metrics)
    if args.limit:
        write_report(REPORTS_DIR / f"{prefix}.md", metrics)
    print(json.dumps(metrics, indent=2, ensure_ascii=False, default=dict))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="docguard_hybrid")
    sub = parser.add_subparsers(dest="command", required=True)
    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("--split", choices=["train", "validation", "test"], required=True)
    evaluate.add_argument("--version", default="v0_4")
    evaluate.add_argument("--limit", type=int)
    evaluate.add_argument("--decision-source", choices=["router", "hf_embedding"], default="router")
    evaluate.add_argument("--hf-input-mode", default="raw_diff_plus_docs")
    evaluate.set_defaults(func=evaluate_command)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
