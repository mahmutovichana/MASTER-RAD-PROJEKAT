from __future__ import annotations

import argparse
import json
from pathlib import Path

from docguard_external.codocbench_adapter import prepare_codocbench
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
        emit(prepare_codocbench(args.limit, output))
        return 2
    if args.dataset == "comment_update":
        emit(prepare_comment_update(args.limit, output))
        return 2
    emit({"status": "error", "message": f"prepare is not implemented for {args.dataset}"})
    return 2


def validate_command(args: argparse.Namespace) -> int:
    path = Path(args.input)
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="docguard_external")
    sub = parser.add_subparsers(dest="command", required=True)
    list_parser = sub.add_parser("list-candidates")
    list_parser.set_defaults(func=list_command)
    describe = sub.add_parser("describe")
    describe.add_argument("--dataset", required=True)
    describe.set_defaults(func=describe_command)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("--dataset", required=True)
    prepare.add_argument("--limit", type=int, default=100)
    prepare.add_argument("--output", required=True)
    prepare.set_defaults(func=prepare_command)
    validate = sub.add_parser("validate")
    validate.add_argument("--input", required=True)
    validate.set_defaults(func=validate_command)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
