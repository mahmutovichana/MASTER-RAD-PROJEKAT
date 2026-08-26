from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib

from docguard_ml_v2.data_contract import PRIMARY_STAGE2_LABELS, serialize_model_row


def _positive_probability(model: Any, row: dict[str, Any]) -> float:
    probabilities = model.predict_proba([row])[0]
    classes = list(model.named_steps["classifier"].classes_) if hasattr(model, "named_steps") else list(model.classes_)
    return float(probabilities[classes.index(1)])


def _category_probabilities(model: Any, row: dict[str, Any]) -> dict[str, float]:
    probabilities = model.predict_proba([row])[0]
    classes = list(model.named_steps["classifier"].classes_) if hasattr(model, "named_steps") else list(model.classes_)
    return {str(label): float(probabilities[index]) for index, label in enumerate(classes)}


class FinalV2Runtime:
    def __init__(self, *, binary_payload_path: str | Path, category_payload_path: str | Path) -> None:
        self.binary_payload = joblib.load(binary_payload_path)
        self.category_payload = joblib.load(category_payload_path)

    def predict(self, row: dict[str, Any]) -> dict[str, Any]:
        serialize_model_row(row)
        binary_model = self.binary_payload["model"]
        threshold = float(self.binary_payload["threshold"])
        probability = _positive_probability(binary_model, row)
        pred_positive = probability >= threshold
        if not pred_positive:
            return {
                "pred_docs_update_required": False,
                "binary_probability": probability,
                "binary_threshold": threshold,
                "pred_doc_category": "no_update",
                "category_probabilities": {},
                "category_confidence": 0.0,
            }
        category_model = self.category_payload["model"]
        probabilities = _category_probabilities(category_model, row)
        filtered = {label: probabilities.get(label, 0.0) for label in PRIMARY_STAGE2_LABELS if label in probabilities}
        pred_label = max(filtered, key=filtered.get) if filtered else str(category_model.predict([row])[0])
        return {
            "pred_docs_update_required": True,
            "binary_probability": probability,
            "binary_threshold": threshold,
            "pred_doc_category": pred_label,
            "category_probabilities": filtered,
            "category_confidence": float(filtered.get(pred_label, 0.0)),
        }
