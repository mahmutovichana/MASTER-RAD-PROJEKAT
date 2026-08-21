from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docguard_runtime.workspace_analyzer import analyze_workspace


DEFAULT_MODELS = [
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "Qwen/Qwen2.5-Coder-7B-Instruct",
    "meta-llama/Llama-3.1-8B-Instruct",
]

REPORT_STEM = "vscode_llm_patch_model_comparison_2026_08"


def _truncate(text: str, limit: int = 900) -> str:
    normalized = "\n".join(line.rstrip() for line in (text or "").splitlines()).strip()
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."


def _table_cell(value: Any, limit: int = 180) -> str:
    text = str(value or "").replace("\n", " ").replace("`", "\\`").replace("|", "\\|")
    text = " ".join(text.split())
    if len(text) > limit:
        text = text[: limit - 3].rstrip() + "..."
    return text


def _patch_summary(result: dict[str, Any]) -> dict[str, Any]:
    patch = result.get("patch") or {}
    fallback = patch.get("fallback_patch") or {}
    return {
        "model": patch.get("model_name") or "",
        "status": result.get("status"),
        "docs_update_required": result.get("docs_update_required"),
        "target_doc_file": result.get("target_doc_file"),
        "target_section": result.get("target_section"),
        "scenario_type": result.get("scenario_type"),
        "doc_category": result.get("doc_category"),
        "confidence": result.get("confidence"),
        "generation_status": patch.get("generation_status") or "",
        "postprocess_status": patch.get("postprocess_status") or "",
        "verifier_status": patch.get("verifier_status") or "",
        "quality_label": patch.get("quality_label") or "",
        "hallucination_risk": patch.get("hallucination_risk") or "",
        "grounded_tokens_found": patch.get("grounded_tokens_found") or [],
        "warnings": patch.get("warnings") or [],
        "patch_preview": _truncate(patch.get("preview") or patch.get("text") or ""),
        "raw_patch_preview": _truncate(patch.get("raw_patch") or ""),
        "fallback_preview": _truncate(fallback.get("preview") or fallback.get("text") or ""),
        "runtime_ms": (result.get("diagnostics") or {}).get("runtime_ms"),
        "error_message": result.get("error_message") or "",
    }


def _score(summary: dict[str, Any]) -> tuple[int, int, int]:
    quality_rank = {
        "excellent": 4,
        "usable": 3,
        "partial": 2,
        "rejected": 0,
    }.get(str(summary.get("quality_label") or ""), 1)
    verifier_rank = 2 if summary.get("verifier_status") == "pass" else 1 if summary.get("verifier_status") == "warn" else 0
    risk_rank = 2 if summary.get("hallucination_risk") == "low" else 1 if summary.get("hallucination_risk") == "medium" else 0
    return quality_rank, verifier_rank, risk_rank


def _openai_compatible_preflight(model: str, timeout_seconds: int) -> dict[str, Any]:
    base_url = os.getenv("DOCGUARD_LLM_BASE_URL", "").rstrip("/")
    api_key = os.getenv("DOCGUARD_LLM_API_KEY", "")
    if not base_url:
        return {"ok": False, "status": None, "error": "DOCGUARD_LLM_BASE_URL is not set."}
    if not api_key:
        return {"ok": False, "status": None, "error": "DOCGUARD_LLM_API_KEY is not set."}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Return only OK."},
            {"role": "user", "content": "Reply with OK."},
        ],
        "max_tokens": 8,
        "temperature": 0,
    }
    request = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            return {"ok": True, "status": response.status, "error": ""}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        safe_body = body.replace(api_key, "<redacted>") if api_key else body
        return {"ok": False, "status": exc.code, "error": safe_body[:500]}
    except Exception as exc:
        return {"ok": False, "status": None, "error": str(exc)}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    rows = payload["results"]
    best = payload.get("recommended_model") or "None"
    lines = [
        "# VS Code LLM Patch Model Comparison",
        "",
        "This report compares live DocGuard documentation patch generation on the current VS Code demo workspace.",
        "The deterministic patch composer is used only as a safe fallback and grounding aid; model quality is judged from the LLM patch output.",
        "",
        f"- Workspace: `{payload['workspace']}`",
        f"- Backend: `{payload['patch_backend']}`",
        f"- Recommended model from this run: `{best}`",
        "",
        "## Connection Check",
        "",
        "| Model | Preflight | Status | Error |",
        "|---|---:|---:|---|",
    ]
    for check in payload.get("preflight", []):
        lines.append(
            "| "
            + " | ".join(
                [
                    _table_cell(check.get("model"), 70),
                    _table_cell("ok" if check.get("ok") else "failed", 20),
                    _table_cell(check.get("status"), 20),
                    _table_cell(check.get("error"), 180),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
        "## Summary",
        "",
        "| Model | Generation | Verifier | Quality | Hallucination risk | Target | Patch preview | Runtime ms |",
        "|---|---:|---:|---:|---:|---|---|---:|",
        ]
    )
    for row in rows:
        target = f"{row.get('target_doc_file') or ''}#{row.get('target_section') or ''}".rstrip("#")
        lines.append(
            "| "
            + " | ".join(
                [
                    _table_cell(row.get("model"), 70),
                    _table_cell(row.get("generation_status"), 20),
                    _table_cell(row.get("verifier_status"), 20),
                    _table_cell(row.get("quality_label"), 20),
                    _table_cell(row.get("hallucination_risk"), 20),
                    _table_cell(target, 70),
                    _table_cell(row.get("patch_preview"), 220),
                    _table_cell(row.get("runtime_ms"), 20),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Detailed Patch Outputs",
            "",
        ]
    )
    for row in rows:
        lines.extend(
            [
                f"### {row.get('model')}",
                "",
                f"- Generation: `{row.get('generation_status')}`",
                f"- Postprocess: `{row.get('postprocess_status')}`",
                f"- Verifier: `{row.get('verifier_status')}`",
                f"- Quality: `{row.get('quality_label')}`",
                f"- Hallucination risk: `{row.get('hallucination_risk')}`",
                f"- Grounded tokens: `{', '.join(row.get('grounded_tokens_found') or [])}`",
                "",
                "Patch preview:",
                "",
                "```markdown",
                row.get("patch_preview") or "",
                "```",
                "",
            ]
        )
        if row.get("warnings"):
            lines.extend(["Warnings:", ""])
            for warning in row["warnings"][:12]:
                lines.append(f"- {warning}")
            lines.append("")
        if row.get("fallback_preview"):
            lines.extend(
                [
                    "Safe fallback patch:",
                    "",
                    "```markdown",
                    row["fallback_preview"],
                    "```",
                    "",
                ]
            )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare live LLM patch models on the DocGuard VS Code demo workspace.")
    parser.add_argument("--workspace", default="examples/vscode_demo")
    parser.add_argument("--models", nargs="*", default=DEFAULT_MODELS)
    parser.add_argument("--backend", default="llm-openai-compatible", choices=["llm-openai-compatible", "llm-ollama", "llm-hf", "llm-mock"])
    parser.add_argument("--max-new-tokens", type=int, default=384)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--output-dir", default="reports/live_flow")
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--skip-preflight", action="store_true")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    preflight = []
    if args.backend == "llm-openai-compatible" and not args.skip_preflight:
        for model in args.models:
            check = {"model": model, **_openai_compatible_preflight(model, args.timeout_seconds)}
            preflight.append(check)

    results = []
    for model in args.models:
        check = next((item for item in preflight if item.get("model") == model), None)
        if check and not check.get("ok"):
            results.append(
                {
                    "model": model,
                    "status": "preflight_error",
                    "generation_status": "not_run",
                    "postprocess_status": "not_run",
                    "verifier_status": "not_run",
                    "quality_label": "not_scored",
                    "hallucination_risk": "not_scored",
                    "warnings": [f"Preflight failed before DocGuard patch generation: {check.get('error') or 'unknown error'}"],
                    "patch_preview": "",
                    "raw_patch_preview": "",
                    "fallback_preview": "",
                    "runtime_ms": None,
                    "error_message": check.get("error") or "",
                }
            )
            continue
        try:
            result = analyze_workspace(
                workspace,
                patch_backend=args.backend,
                patch_model=model,
                patch_max_new_tokens=args.max_new_tokens,
                patch_temperature=args.temperature,
            )
            summary = _patch_summary(result)
        except Exception as exc:
            summary = {
                "model": model,
                "status": "error",
                "generation_status": "error",
                "postprocess_status": "fail",
                "verifier_status": "fail",
                "quality_label": "rejected",
                "hallucination_risk": "high",
                "warnings": [str(exc)],
                "patch_preview": "",
                "raw_patch_preview": "",
                "fallback_preview": "",
                "runtime_ms": None,
                "error_message": str(exc),
            }
        results.append(summary)

    usable = [row for row in results if row.get("generation_status") == "ok" and row.get("quality_label") in {"excellent", "usable"}]
    recommended = max(usable, key=_score).get("model") if usable else ""
    payload = {
        "status": "ok" if results else "empty",
        "workspace": str(workspace),
        "patch_backend": args.backend,
        "models": args.models,
        "preflight": preflight,
        "recommended_model": recommended,
        "results": results,
    }

    json_path = output_dir / f"{REPORT_STEM}.json"
    md_path = output_dir / f"{REPORT_STEM}.md"
    _write_json(json_path, payload)
    _write_markdown(md_path, payload)

    print(json.dumps({"status": payload["status"], "recommended_model": recommended, "json": str(json_path), "report": str(md_path)}, indent=2))
    return 0 if results else 1


if __name__ == "__main__":
    raise SystemExit(main())
