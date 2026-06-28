from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from docguard.evaluator import evaluate_split
from docguard_hybrid.evaluator import DATA_DIR, evaluate_records, read_jsonl
from docguard_ml.evaluate import evaluate as evaluate_ml


REPORT = ROOT / "reports" / "ablation_v0_4.md"
REPORTS_DIR = ROOT / "reports"


def fmt(value) -> str:
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def row(name: str, metrics: dict) -> str:
    return (
        f"| {name} | {fmt(metrics.get('docs_update_required_precision', 0.0))} | "
        f"{fmt(metrics.get('docs_update_required_recall', 0.0))} | "
        f"{fmt(metrics.get('docs_update_required_f1', 0.0))} | "
        f"{fmt(metrics.get('positive_doc_category_accuracy', metrics.get('doc_category_accuracy', 0.0)))} | "
        f"{fmt(metrics.get('positive_target_doc_file_accuracy', metrics.get('target_doc_file_accuracy', 0.0)))} | "
        f"{fmt(metrics.get('positive_scenario_type_accuracy', metrics.get('scenario_type_accuracy', 0.0)))} | "
        f"{fmt(metrics.get('negative_classification_accuracy', 0.0))} | "
        f"{fmt(metrics.get('macro_scenario_f1', 0.0))} | "
        f"{fmt(metrics.get('macro_doc_category_f1', 0.0))} | "
        f"{fmt(metrics.get('average_latency_seconds', 0.0))} |"
    )


def read_metrics_report(path: Path) -> dict:
    metrics = {}
    if not path.exists():
        return metrics
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| `"):
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) >= 2:
                key = parts[0].strip("`")
                try:
                    metrics[key] = float(parts[1])
                except ValueError:
                    metrics[key] = parts[1]
    return metrics


def main() -> int:
    baseline, _ = evaluate_split("test")
    ml = evaluate_ml("test")
    test_records = read_jsonl(DATA_DIR / "test.jsonl")
    hybrid, _ = evaluate_records(test_records)
    hf_embedding = read_metrics_report(REPORTS_DIR / "hf_embedding_evaluation_v0_4_test.md")
    hf_sequence = read_metrics_report(REPORTS_DIR / "hf_sequence_evaluation_v0_4_scenario_type.md")
    hybrid_hf = read_metrics_report(REPORTS_DIR / "hybrid_hf_embedding_evaluation_v0_4_test.md")
    lines = [
        "# Ablation v0.4",
        "",
        "| System | Precision | Recall | F1 | Positive doc category acc. | Positive target file acc. | Positive scenario acc. | Negative acc. | Macro scenario F1 | Macro doc category F1 | Latency |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        row("rule baseline", baseline),
        row("ML-only", ml),
        row("HF embedding classifier", hf_embedding) if hf_embedding else "| HF embedding classifier | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run |",
        row("HF sequence classifier", hf_sequence) if hf_sequence else "| HF sequence classifier | optional | optional | optional | optional | optional | optional | optional | optional | optional | optional |",
        row("deterministic hybrid router", hybrid),
        row("hybrid + HF embedding classifier", hybrid_hf) if hybrid_hf else "| hybrid + HF embedding classifier | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run |",
        row("optional LLM-assisted hybrid", {"docs_update_required_precision": 0.0, "docs_update_required_recall": 0.0, "docs_update_required_f1": 0.0}),
        "",
        f"ML backend used for this ablation: `{ml.get('ml_backend', 'unknown')}`.",
        "",
        "The optional LLM-assisted hybrid is not run by default on the CPU-only machine. It should be evaluated only on small samples with `qwen2_5_coder_0_5b` or an optional GGUF/llama.cpp backend.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
