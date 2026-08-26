from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_eval_v2.reference_evaluation import HUMAN_DIMENSIONS, bootstrap_mean_ci, read_jsonl, sha256_file, write_json
from docguard_ml_v2.model_manifest import utc_now


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def receipt_guard(output_dir: Path, *, frozen_hash: str, confirmation_hash: str, enforce: bool, allow_repeat: bool) -> None:
    receipt = output_dir / "stage3_confirmation_evaluation_receipt.json"
    if not enforce or not receipt.exists():
        return
    old = load_json(receipt)
    if old.get("frozen_generator_hash") == frozen_hash and old.get("confirmation_dataset_hash") == confirmation_hash and not allow_repeat:
        raise ValueError("Stage 3 confirmation evaluation already has a receipt for this frozen generator and confirmation dataset.")


def run(*, safety: Path, reference: Path, human_reviews: Path, freeze_manifest: Path, confirmation_dataset: Path, sample_manifest: Path, output_dir: Path, enforce_one_shot: bool = False, allow_repeat_for_reproducibility: bool = False) -> dict:
    frozen_hash = sha256_file(freeze_manifest)
    confirmation_hash = sha256_file(confirmation_dataset)
    receipt_guard(output_dir, frozen_hash=frozen_hash, confirmation_hash=confirmation_hash, enforce=enforce_one_shot, allow_repeat=allow_repeat_for_reproducibility)
    human_rows = read_jsonl(human_reviews)
    human_summary = load_json(human_reviews.with_name("human_review_summary.json")) if human_reviews.with_name("human_review_summary.json").exists() else {}
    ci = {
        "accept_as_is_rate": bootstrap_mean_ci([1.0 if str(row.get("human_accept_as_is")).lower() == "yes" else 0.0 for row in human_rows]),
        "mean_factual_correctness": bootstrap_mean_ci([float(row["human_factual_correctness"]) for row in human_rows]),
        "mean_semantic_completeness": bootstrap_mean_ci([float(row["human_semantic_completeness"]) for row in human_rows]),
        "mean_developer_usefulness": bootstrap_mean_ci([float(row["human_developer_usefulness"]) for row in human_rows]),
    }
    result = {
        "safety_provenance": load_json(safety),
        "reference_metrics_supporting_only": load_json(reference),
        "human_quality_primary": human_summary,
        "human_confidence_intervals_95": ci,
        "separation_policy": "Safety, reference similarity, and human quality remain separate; no opaque combined accuracy percentage is computed.",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "stage3_final_evaluation_summary.json", result)
    receipt = {
        "stage3_confirmation_evaluation_receipt": True,
        "stage3_config_hash": load_json(freeze_manifest).get("config_sha256"),
        "source_code_hashes": load_json(freeze_manifest).get("source_file_sha256"),
        "frozen_generator_hash": frozen_hash,
        "confirmation_dataset_hash": confirmation_hash,
        "sample_manifest_hash": sha256_file(sample_manifest),
        "evaluation_timestamp": utc_now(),
        "repeat_for_reproducibility": bool(allow_repeat_for_reproducibility),
    }
    write_json(output_dir / "stage3_confirmation_evaluation_receipt.json", receipt)
    (output_dir / "stage3_final_evaluation_report.md").write_text("# Stage 3 V2 Final Evaluation\n\nHuman quality, safety/provenance, and reference metrics are reported separately.\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate completed Stage 3 V2 evaluation artifacts.")
    parser.add_argument("--safety", required=True)
    parser.add_argument("--reference", required=True)
    parser.add_argument("--human-reviews", required=True)
    parser.add_argument("--freeze-manifest", required=True)
    parser.add_argument("--confirmation-dataset", required=True)
    parser.add_argument("--sample-manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--enforce-one-shot", action="store_true")
    parser.add_argument("--allow-repeat-for-reproducibility", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(safety=Path(args.safety), reference=Path(args.reference), human_reviews=Path(args.human_reviews), freeze_manifest=Path(args.freeze_manifest), confirmation_dataset=Path(args.confirmation_dataset), sample_manifest=Path(args.sample_manifest), output_dir=Path(args.output_dir), enforce_one_shot=args.enforce_one_shot, allow_repeat_for_reproducibility=args.allow_repeat_for_reproducibility), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
