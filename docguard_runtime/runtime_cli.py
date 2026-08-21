from __future__ import annotations

import argparse
import json
from pathlib import Path

from docguard_runtime.patch_composer import apply_patch
from docguard_runtime.schemas import error_response
from docguard_runtime.workspace_analyzer import analyze_workspace


def emit(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def analyze_workspace_command(args: argparse.Namespace) -> int:
    try:
        emit(
            analyze_workspace(
                Path(args.workspace).resolve(),
                input_mode=args.input_mode,
                architecture=args.classifier_architecture,
                analysis_backend=args.analysis_backend,
                analysis_model=args.analysis_model,
                analysis_max_new_tokens=args.analysis_max_new_tokens,
                analysis_temperature=args.analysis_temperature,
                patch_backend=args.patch_backend,
                patch_model=args.patch_model,
                patch_max_new_tokens=args.patch_max_new_tokens,
                patch_temperature=args.patch_temperature,
            )
        )
        return 0
    except Exception as exc:
        emit(error_response(str(exc)))
        return 1


def analyze_diff_command(args: argparse.Namespace) -> int:
    try:
        diff = Path(args.diff_file).read_text(encoding="utf-8", errors="ignore")
        emit(
            analyze_workspace(
                Path(args.workspace).resolve(),
                diff_text=diff,
                input_mode=args.input_mode,
                architecture=args.classifier_architecture,
                analysis_backend=args.analysis_backend,
                analysis_model=args.analysis_model,
                analysis_max_new_tokens=args.analysis_max_new_tokens,
                analysis_temperature=args.analysis_temperature,
                patch_backend=args.patch_backend,
                patch_model=args.patch_model,
                patch_max_new_tokens=args.patch_max_new_tokens,
                patch_temperature=args.patch_temperature,
            )
        )
        return 0
    except Exception as exc:
        emit(error_response(str(exc)))
        return 1


def apply_patch_command(args: argparse.Namespace) -> int:
    try:
        patch = json.loads(Path(args.patch_file).read_text(encoding="utf-8"))
        path = apply_patch(Path(args.workspace).resolve(), patch)
        emit({"status": "ok", "applied_file": str(path), "error_message": None})
        return 0
    except Exception as exc:
        emit(error_response(str(exc)))
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="docguard_runtime")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze = sub.add_parser("analyze-workspace")
    analyze.add_argument("--workspace", required=True)
    analyze.add_argument("--format", choices=["json"], default="json")
    analyze.add_argument("--input-mode", default="raw_diff_plus_docs")
    analyze.add_argument("--classifier-architecture", default="hybrid_router")
    analyze.add_argument("--analysis-backend", choices=["hybrid", "llm-mock", "llm-hf", "llm-openai-compatible", "llm-ollama"], default="hybrid")
    analyze.add_argument("--analysis-model")
    analyze.add_argument("--analysis-max-new-tokens", type=int, default=256)
    analyze.add_argument("--analysis-temperature", type=float, default=0.0)
    analyze.add_argument("--patch-backend", choices=["deterministic", "llm-mock", "llm-hf", "llm-openai-compatible", "llm-ollama"], default="deterministic")
    analyze.add_argument("--patch-model")
    analyze.add_argument("--patch-max-new-tokens", type=int, default=192)
    analyze.add_argument("--patch-temperature", type=float, default=0.1)
    analyze.set_defaults(func=analyze_workspace_command)
    diff = sub.add_parser("analyze-diff")
    diff.add_argument("--workspace", required=True)
    diff.add_argument("--diff-file", required=True)
    diff.add_argument("--format", choices=["json"], default="json")
    diff.add_argument("--input-mode", default="raw_diff_plus_docs")
    diff.add_argument("--classifier-architecture", default="hybrid_router")
    diff.add_argument("--analysis-backend", choices=["hybrid", "llm-mock", "llm-hf", "llm-openai-compatible", "llm-ollama"], default="hybrid")
    diff.add_argument("--analysis-model")
    diff.add_argument("--analysis-max-new-tokens", type=int, default=256)
    diff.add_argument("--analysis-temperature", type=float, default=0.0)
    diff.add_argument("--patch-backend", choices=["deterministic", "llm-mock", "llm-hf", "llm-openai-compatible", "llm-ollama"], default="deterministic")
    diff.add_argument("--patch-model")
    diff.add_argument("--patch-max-new-tokens", type=int, default=192)
    diff.add_argument("--patch-temperature", type=float, default=0.1)
    diff.set_defaults(func=analyze_diff_command)
    apply = sub.add_parser("apply-patch")
    apply.add_argument("--workspace", required=True)
    apply.add_argument("--patch-file", required=True)
    apply.set_defaults(func=apply_patch_command)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
