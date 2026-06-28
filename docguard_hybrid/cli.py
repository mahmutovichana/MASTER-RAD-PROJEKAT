from __future__ import annotations

import argparse
import json

from docguard_hybrid.evaluator import DATA_DIR, REPORTS_DIR, evaluate_records, read_jsonl, write_report


def evaluate_command(args: argparse.Namespace) -> int:
    records = read_jsonl(DATA_DIR / f"{args.split}.jsonl")
    if args.limit:
        records = records[: args.limit]
    metrics, _predictions = evaluate_records(records)
    write_report(REPORTS_DIR / "hybrid_evaluation_v0_4.md", metrics)
    print(json.dumps(metrics, indent=2, ensure_ascii=False, default=dict))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="docguard_hybrid")
    sub = parser.add_subparsers(dest="command", required=True)
    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("--split", choices=["train", "validation", "test"], required=True)
    evaluate.add_argument("--version", default="v0_4")
    evaluate.add_argument("--limit", type=int)
    evaluate.set_defaults(func=evaluate_command)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
