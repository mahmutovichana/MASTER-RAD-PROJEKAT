from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docguard_demo.run_project_evolution_flow import run


def write_hf_smoke_report(path: Path, predictions: list[dict], model: str) -> None:
    status_counts: dict[str, int] = {}
    for row in predictions:
        status = row.get("llm_generation_status") or "not_applicable"
        status_counts[status] = status_counts.get(status, 0) + 1
    lines = [
        "# DocGuard HuggingFace Patch Generation Smoke Report 2026-08",
        "",
        f"- model: `{model}`",
        f"- cases: {len(predictions)}",
        f"- generation status counts: `{json.dumps(status_counts, sort_keys=True)}`",
        "",
        "This smoke report is produced only when the user explicitly runs the HF command. It may download the requested model through HuggingFace.",
        "",
    ]
    for row in predictions:
        lines.extend(
            [
                f"## `{row['case_id']}`",
                "",
                f"- target doc: `{row['predicted_target_doc_file']}`",
                f"- generation status: `{row.get('llm_generation_status')}`",
                f"- verifier status: `{row.get('patch_verifier_status')}`",
                f"- grounded tokens: `{', '.join(row.get('grounded_tokens_found') or [])}`",
                f"- error: `{row.get('llm_error_message') or ''}`",
                "",
                "Patch:",
                "",
                "```diff",
                row.get("generated_doc_patch") or "not_applicable",
                "```",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--case-limit", type=int, default=3)
    parser.add_argument("--max-new-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--device-map")
    parser.add_argument("--torch-dtype")
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--output-dir", default="reports/live_flow/hf_smoke")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    result = run(
        output_dir,
        patch_backend="llm-hf",
        patch_model=args.model,
        case_limit=args.case_limit,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        device_map=args.device_map,
        torch_dtype=args.torch_dtype,
        trust_remote_code=args.trust_remote_code,
        save_prompts=True,
    )
    predictions_path = output_dir / "docguard_project_evolution_predictions.jsonl"
    predictions = [json.loads(line) for line in predictions_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    smoke_predictions = output_dir / "docguard_hf_smoke_predictions.jsonl"
    smoke_predictions.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in predictions) + "\n", encoding="utf-8")
    write_hf_smoke_report(output_dir / "docguard_hf_smoke_report_2026_08.md", predictions, args.model)
    print(json.dumps({"status": "ok", "result": result, "smoke_predictions": str(smoke_predictions)}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
