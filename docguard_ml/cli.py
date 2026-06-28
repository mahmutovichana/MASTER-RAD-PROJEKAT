from __future__ import annotations

import argparse
import json

from docguard_ml.evaluate import evaluate, write_reports
from docguard_ml.train import train


def train_command(args: argparse.Namespace) -> int:
    print(json.dumps(train(args.version), indent=2, ensure_ascii=False))
    return 0


def evaluate_command(args: argparse.Namespace) -> int:
    metrics = evaluate(args.split)
    write_reports(metrics)
    print(json.dumps(metrics, indent=2, ensure_ascii=False, default=dict))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="docguard_ml")
    sub = parser.add_subparsers(dest="command", required=True)
    train_parser = sub.add_parser("train")
    train_parser.add_argument("--version", default="v0_4")
    train_parser.set_defaults(func=train_command)
    evaluate_parser = sub.add_parser("evaluate")
    evaluate_parser.add_argument("--version", default="v0_4")
    evaluate_parser.add_argument("--split", choices=["train", "validation", "test"], required=True)
    evaluate_parser.set_defaults(func=evaluate_command)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
