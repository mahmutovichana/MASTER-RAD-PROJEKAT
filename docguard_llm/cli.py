from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
import traceback
from pathlib import Path

from docguard_llm.evaluator import DATA_DIR, MOCK_WARNING, REPORTS_DIR, evaluate_model, read_jsonl, write_comparison_report, write_jsonl, write_model_report
from docguard_llm.hf_client import HFClient
from docguard_llm.json_parser import FALLBACK_PREDICTION, extract_json_object, parse_model_output
from docguard_llm.label_normalizer import add_normalized_fields
from docguard_llm.llm_agent import predict
from docguard_llm.model_registry import get_model_config, list_models
from docguard_llm.prompt_builder import build_compact_prompt, build_prompt, build_sanity_prompt, select_few_shot_examples


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


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def fallback_prediction(record: dict, model_key: str, backend: str, error_message: str) -> dict:
    config = get_model_config(model_key)
    row = {
        "record_id": record["id"],
        "model_key": model_key,
        "model_id": config["model_id"],
        "backend": backend,
        **dict(FALLBACK_PREDICTION),
        "raw_model_output": "",
        "parse_error": True,
        "parse_error_type": "runtime_error",
        "latency_seconds": None,
        "error_message": error_message,
    }
    return add_normalized_fields(row, record)


def retry_prediction_on_parse_error(record: dict, args: argparse.Namespace, examples: list[dict], prediction: dict) -> dict:
    if args.backend == "mock" or not args.retry_on_parse_error:
        return prediction
    if not prediction.get("parse_error") or prediction.get("parse_error_type") != "truncated_json":
        return prediction
    original_tokens = os.getenv("DOCGUARD_MAX_NEW_TOKENS")
    current_tokens = int(original_tokens or "150")
    os.environ["DOCGUARD_MAX_NEW_TOKENS"] = str(current_tokens + 100)
    print(f"retry-on-parse-error: retrying {record['id']} with max_new_tokens={current_tokens + 100}", flush=True)
    try:
        original_raw_output = prediction.get("raw_model_output", "")
        original_parse_error_type = prediction.get("parse_error_type", "")
        retry = predict(record, args.model, args.backend, examples, compact_prompt=args.compact_prompt)
        retry["retry_attempted"] = True
        retry["retry_success"] = not retry.get("parse_error")
        retry["original_raw_output"] = original_raw_output
        retry["original_parse_error_type"] = original_parse_error_type
        retry["retry_raw_output"] = retry.get("raw_model_output", "")
        return retry
    except Exception as exc:
        prediction["retry_attempted"] = True
        prediction["retry_success"] = False
        prediction["retry_error_message"] = traceback.format_exc() if args.debug else (str(exc) or exc.__class__.__name__)
        return prediction
    finally:
        if original_tokens is None:
            os.environ.pop("DOCGUARD_MAX_NEW_TOKENS", None)
        else:
            os.environ["DOCGUARD_MAX_NEW_TOKENS"] = original_tokens


def list_models_command(_args: argparse.Namespace) -> int:
    print(json.dumps(list_models(), indent=2, ensure_ascii=False))
    return 0


def evaluate_command(args: argparse.Namespace) -> int:
    output_path = prediction_path(args.split, args.model, args.backend)
    if args.backend == "mock":
        metrics, predictions = evaluate_model(args.split, args.model, args.backend, args.limit, compact_prompt=args.compact_prompt)
        write_jsonl(output_path, predictions)
        write_model_report(model_report_path(args.model, args.backend), args.model, args.split, args.backend, metrics)
        write_mock_compatibility_files(args.split, args.model, predictions, metrics)
        print(json.dumps(metrics, indent=2, ensure_ascii=False))
        return 0

    records = read_jsonl(DATA_DIR / f"{args.split}.jsonl")
    if args.limit:
        records = records[: args.limit]
    if output_path.exists():
        output_path.unlink()
    predictions = []
    examples = select_few_shot_examples()
    total = len(records)
    for index, record in enumerate(records, start=1):
        print(f"record {index}/{total}: {record['id']}", flush=True)
        print(f"model key: {args.model}", flush=True)
        print(f"prompt mode: {'compact' if args.compact_prompt else 'full'}", flush=True)
        try:
            print("generation started", flush=True)
            prediction = predict(record, args.model, args.backend, examples, compact_prompt=args.compact_prompt)
            prediction = retry_prediction_on_parse_error(record, args, examples, prediction)
            print("generation finished", flush=True)
            print(f"latency: {prediction.get('latency_seconds')}", flush=True)
            print(f"parse success: {not prediction.get('parse_error')}", flush=True)
            print(f"parse error type: {prediction.get('parse_error_type', '')}", flush=True)
        except Exception as exc:
            message = traceback.format_exc() if args.debug else (str(exc) or exc.__class__.__name__)
            print(f"generation failed: {message}", flush=True)
            prediction = fallback_prediction(record, args.model, args.backend, message)
            if not args.continue_on_error:
                append_jsonl(output_path, prediction)
                print(f"output file append status: wrote fallback to {output_path}", flush=True)
                raise SystemExit(1)
        append_jsonl(output_path, prediction)
        print(f"output file append status: wrote {output_path}", flush=True)
        predictions.append(prediction)
    from docguard_llm.evaluator import evaluate_predictions
    metrics = evaluate_predictions(records, predictions)
    write_model_report(model_report_path(args.model, args.backend), args.model, args.split, args.backend, metrics)
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
    prediction = predict(record, args.model, args.backend, select_few_shot_examples(), compact_prompt=args.compact_prompt)
    print(json.dumps(prediction, indent=2, ensure_ascii=False))
    return 0


def smoke_test_command(args: argparse.Namespace) -> int:
    config = get_model_config(args.model)
    report_path = REPORTS_DIR / f"real_llm_smoke_test_{args.model}.md"
    record = None
    record_id = args.record_id or "first validation record"
    prompt_messages: list[dict] = []
    prompt_text = ""
    raw_output = ""
    parsed_prediction: dict = {}
    parse_error = True
    latency = None
    error_message = ""
    state = {
        "last_completed_step": "initialized",
        "generation_started_at": "",
        "generation_finished_at": "",
    }

    def progress(label: str, value: object = None) -> None:
        if value is None:
            print(label, flush=True)
        else:
            print(f"{label}: {value}", flush=True)

    def write_smoke_report(status: str, usable: bool) -> None:
        lines = [
            f"# Real LLM Smoke Test: {args.model}",
            "",
            f"- command: `python -m docguard_llm.cli smoke-test --model {args.model} --backend {args.backend}`",
            f"- backend: {args.backend}",
            f"- model_key: {args.model}",
            f"- model_id: {config['model_id']}",
            f"- selected_record_id: {record.get('id') if record else record_id}",
            f"- compact_prompt: {args.compact_prompt}",
            f"- sanity_only: {args.sanity_only}",
            f"- prompt_length_characters: {len(prompt_text)}",
            f"- parse_success: {not parse_error}",
            f"- latency_seconds: {latency if latency is not None else 'n/a'}",
            f"- last_completed_step: {state['last_completed_step']}",
            f"- generation_started_at: {state['generation_started_at'] or 'n/a'}",
            f"- generation_finished_at: {state['generation_finished_at'] or 'n/a'}",
            f"- raw_output_length: {len(raw_output) if raw_output else 'n/a'}",
            f"- status: {status}",
            f"- output_usable: {usable}",
            "",
        ]
        if args.backend == "mock":
            lines.extend([f"> {MOCK_WARNING}", ""])
        if error_message:
            lines.extend(["## Error Message", "", error_message, ""])
        lines.extend([
            "## Prompt Preview",
            "",
            "```text",
            prompt_text[:2000],
            "```",
            "",
            "## Raw Model Output",
            "",
            "```text",
            raw_output,
            "```",
            "",
            "## Parsed Prediction",
            "",
            "```json",
            json.dumps(parsed_prediction, indent=2, ensure_ascii=False) if parsed_prediction else "{}",
            "```",
        ])
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    try:
        progress("selected model key", args.model)
        progress("model id", config["model_id"])
        progress("backend", args.backend)
        progress("max_new_tokens", os.getenv("DOCGUARD_MAX_NEW_TOKENS", "150" if args.backend == "transformers_local" else "800"))
        progress("compact_prompt", args.compact_prompt)
        progress("sanity_only", args.sanity_only)
        progress("output report path", report_path)
        write_smoke_report("started", False)

        if args.sanity_only:
            record_id = "sanity-only"
            progress("selected record id", record_id)
            progress("record loaded successfully", "skipped")
            prompt_messages = build_sanity_prompt()
        else:
            records = read_jsonl(DATA_DIR / "validation.jsonl")
            if args.record_id:
                record = next((r for r in records if r["id"] == args.record_id), None)
                if record is None:
                    raise ValueError(f"Record not found in validation split: {args.record_id}")
            else:
                record = records[0]
            record_id = record["id"]
            progress("selected record id", record_id)
            progress("record loaded successfully", True)
            prompt_messages = build_compact_prompt(record) if args.compact_prompt else build_prompt(record, select_few_shot_examples())
        state["last_completed_step"] = "record_loaded"
        write_smoke_report("record_loaded", False)

        prompt_text = "\n\n".join(f"{message['role']}: {message['content']}" for message in prompt_messages)
        progress("prompt built successfully", True)
        progress("prompt length in characters", len(prompt_text))
        progress("first 500 characters of prompt", prompt_text[:500])
        state["last_completed_step"] = "prompt_built"
        write_smoke_report("prompt_built", False)

        client = HFClient(model_key=args.model, backend=args.backend)
        progress("generation started")
        state["generation_started_at"] = utc_now()
        state["last_completed_step"] = "generation_started"
        write_smoke_report("generation_started", False)
        raw_output, latency = client.generate(prompt_messages)
        progress("generation finished")
        state["generation_finished_at"] = utc_now()
        state["last_completed_step"] = "generation_finished"
        write_smoke_report("generation_finished", False)
        progress("latency seconds", latency)
        progress("raw output length", len(raw_output))
        progress("first 1000 characters of raw output", raw_output[:1000])

        if args.sanity_only:
            try:
                extracted = extract_json_object(raw_output)
                parsed_prediction = json.loads(extracted) if extracted else {"raw_json_parse_error": True}
                parse_error = parsed_prediction != {"ok": True}
            except json.JSONDecodeError:
                parsed_prediction = {"raw_json_parse_error": True}
                parse_error = True
        else:
            parsed_prediction, parse_error = parse_model_output(raw_output)

        progress("parse success", not parse_error)
        progress("structured prediction JSON", json.dumps(parsed_prediction, indent=2, ensure_ascii=False))
        state["last_completed_step"] = "parsed"
        write_smoke_report("succeeded", not parse_error)
        return 0 if not parse_error else 1
    except Exception as exc:
        error_message = str(exc) or exc.__class__.__name__
        if args.debug:
            error_message = traceback.format_exc()
        write_smoke_report("failed", False)
        print(json.dumps({"status": "failed", "model": args.model, "backend": args.backend, "message": error_message, "report": str(report_path)}, indent=2))
        if args.debug:
            traceback.print_exc()
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="docguard_llm")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list-models").set_defaults(func=list_models_command)
    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("--split", choices=["train", "validation", "test"], required=True)
    evaluate.add_argument("--model", choices=list(list_models()), required=True)
    evaluate.add_argument("--backend", choices=["mock", "transformers_local", "text_generation_inference"], default="mock")
    evaluate.add_argument("--limit", type=int)
    evaluate.add_argument("--compact-prompt", action="store_true")
    evaluate.add_argument("--continue-on-error", action="store_true")
    evaluate.add_argument("--retry-on-parse-error", action="store_true")
    evaluate.add_argument("--debug", action="store_true")
    evaluate.add_argument("--timeout-seconds", type=int, help="Documentary option for CPU-only runs; no hard Windows timeout is enforced.")
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
    predict_parser.add_argument("--compact-prompt", action="store_true")
    predict_parser.set_defaults(func=predict_command)
    smoke = sub.add_parser("smoke-test")
    smoke.add_argument("--model", choices=list(list_models()), required=True)
    smoke.add_argument("--backend", choices=["mock", "transformers_local", "text_generation_inference"], default="transformers_local")
    smoke.add_argument("--record-id")
    smoke.add_argument("--compact-prompt", action="store_true")
    smoke.add_argument("--sanity-only", action="store_true")
    smoke.add_argument("--debug", action="store_true")
    smoke.set_defaults(func=smoke_test_command)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
