from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib

from docguard_ml_v2.data_contract import binary_eligible_rows, binary_labels, load_jsonl, write_json, write_jsonl
from docguard_ml_v2.metrics import binary_metrics, bootstrap_ci, per_language_binary_metrics
from docguard_ml_v2.model_manifest import sha256_file, utc_now


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError("Freeze manifest is required before confirmation evaluation.")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_freeze(model: Path, freeze_manifest: Path) -> dict[str, Any]:
    manifest = load_manifest(freeze_manifest)
    if manifest.get("confirmation_accessed") is not False:
        raise ValueError("Freeze manifest must state confirmation_accessed=false.")
    expected = manifest.get("hashes", {}).get("model")
    actual = sha256_file(model)
    if expected and expected != actual:
        raise ValueError("Model hash does not match freeze manifest.")
    return manifest


def one_shot_guard(output_dir: Path, model_hash: str, confirmation_hash: str, *, enforce: bool, allow_repeat: bool) -> None:
    receipt = output_dir / "confirmation_evaluation_receipt.json"
    if not enforce or not receipt.exists():
        return
    existing = json.loads(receipt.read_text(encoding="utf-8"))
    same = existing.get("model_hash") == model_hash and existing.get("confirmation_dataset_sha256") == confirmation_hash
    if same and not allow_repeat:
        raise ValueError("Confirmation already evaluated for this model and dataset.")


def run(*, model_path: Path, confirmation: Path, freeze_manifest: Path, output_dir: Path, enforce_one_shot: bool = False, allow_repeat_for_reproducibility: bool = False) -> dict[str, Any]:
    manifest = validate_freeze(model_path, freeze_manifest)
    model_hash = sha256_file(model_path)
    confirmation_hash = sha256_file(confirmation)
    one_shot_guard(output_dir, model_hash, confirmation_hash, enforce=enforce_one_shot, allow_repeat=allow_repeat_for_reproducibility)
    payload = joblib.load(model_path)
    rows = binary_eligible_rows(load_jsonl(confirmation))
    y_true = binary_labels(rows)
    model = payload["model"]
    threshold = float(payload["threshold"])
    proba = model.predict_proba(rows)
    classes = list(model.named_steps["classifier"].classes_)
    scores = [float(item[classes.index(1)]) for item in proba]
    y_pred = [1 if score >= threshold else 0 for score in scores]
    metrics = binary_metrics(y_true, y_pred, scores)
    metrics["bootstrap_ci_95"] = {
        "f1": bootstrap_ci(lambda yt, yp: binary_metrics(yt, yp)["f1"], y_true, y_pred),
        "mcc": bootstrap_ci(lambda yt, yp: binary_metrics(yt, yp)["mcc"], y_true, y_pred),
        "accuracy": bootstrap_ci(lambda yt, yp: binary_metrics(yt, yp)["accuracy"], y_true, y_pred),
    }
    metrics["per_language"] = per_language_binary_metrics(rows, y_true, y_pred, scores)
    output_dir.mkdir(parents=True, exist_ok=True)
    predictions = [{"case_id": row.get("case_id"), "repository": row.get("repository"), "language": row.get("language"), "gold": int(gold), "prediction": int(pred), "probability": score} for row, gold, pred, score in zip(rows, y_true, y_pred, scores)]
    write_jsonl(output_dir / "confirmation_predictions.jsonl", predictions)
    write_json(output_dir / "confirmation_metrics.json", metrics)
    receipt = {"confirmation_evaluated": True, "evaluation_timestamp": utc_now(), "model_hash": model_hash, "confirmation_dataset_sha256": confirmation_hash, "freeze_manifest_hash": sha256_file(freeze_manifest), "repeat_for_reproducibility": bool(allow_repeat_for_reproducibility)}
    write_json(output_dir / "confirmation_evaluation_receipt.json", receipt)
    (output_dir / "confirmation_report.md").write_text(f"# Binary V4 Confirmation Evaluation\n\n- Frozen model: `{manifest.get('selected_model')}`\n- Threshold: `{threshold}`\n- F1: `{metrics['f1']:.4f}`\n- MCC: `{metrics['mcc']:.4f}`\n", encoding="utf-8")
    return {"status": "ok", "metrics": metrics, "receipt": receipt}


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate frozen Binary V4 on confirmation only.")
    parser.add_argument("--model", required=True)
    parser.add_argument("--confirmation", required=True)
    parser.add_argument("--freeze-manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--enforce-one-shot", action="store_true")
    parser.add_argument("--allow-repeat-for-reproducibility", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(model_path=Path(args.model), confirmation=Path(args.confirmation), freeze_manifest=Path(args.freeze_manifest), output_dir=Path(args.output_dir), enforce_one_shot=args.enforce_one_shot, allow_repeat_for_reproducibility=args.allow_repeat_for_reproducibility), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

