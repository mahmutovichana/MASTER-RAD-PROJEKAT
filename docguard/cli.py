from __future__ import annotations

import argparse
import json
from pathlib import Path

from docguard.evaluator import (
    DATA_DIR,
    ROOT,
    evaluate_split,
    predict_record,
    read_jsonl,
    split_path,
    write_predictions,
    write_report,
)


def evaluate_command(args: argparse.Namespace) -> int:
    metrics, predictions = evaluate_split(args.split)
    if args.split == "test":
        write_predictions(ROOT / "data" / "predictions_test.jsonl", predictions)
        write_report(ROOT / "reports" / "baseline_evaluation.md", args.split, metrics)

    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    return 0


def find_record(record_id: str) -> dict:
    for path in [
        DATA_DIR / "docguard_dataset.jsonl",
        split_path("train"),
        split_path("validation"),
        split_path("test"),
    ]:
        if not path.exists():
            continue
        for record in read_jsonl(path):
            if record["id"] == record_id:
                return record
    raise ValueError(f"Record not found: {record_id}")


def predict_command(args: argparse.Namespace) -> int:
    record = find_record(args.record_id)
    prediction = predict_record(record)
    output = {
        "record_id": record["id"],
        "predicted_docs_update_required": prediction["docs_update_required"],
        "predicted_scenario_type": prediction["scenario_type"],
        "predicted_target_doc_file": prediction["target_doc_file"],
        "generated_doc_patch": prediction["generated_doc_patch"],
        "gold_scenario_type": record["scenario_type"],
        "gold_docs_update_required": record["docs_update_required"],
        "expected_facts": record["expected_facts"],
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="docguard")
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate_parser = subparsers.add_parser("evaluate")
    evaluate_parser.add_argument("--split", choices=["train", "validation", "test"], required=True)
    evaluate_parser.set_defaults(func=evaluate_command)

    predict_parser = subparsers.add_parser("predict")
    predict_parser.add_argument("--record-id", required=True)
    predict_parser.set_defaults(func=predict_command)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
