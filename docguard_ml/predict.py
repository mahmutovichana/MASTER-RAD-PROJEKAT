from __future__ import annotations

import pickle
from pathlib import Path

from docguard_hybrid.doc_router import route
from docguard_ml.features import text_for_record

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models" / "v0_4"


def load_model() -> dict:
    sklearn_path = MODELS_DIR / "sklearn_model.joblib"
    if sklearn_path.exists():
        try:
            import joblib
            return joblib.load(sklearn_path)
        except ModuleNotFoundError:
            pass
    with (MODELS_DIR / "fallback_model.pkl").open("rb") as handle:
        return pickle.load(handle)


def most_common(counter, default: str) -> str:
    return counter.most_common(1)[0][0] if counter else default


def combine_votes(model: dict, table: str, signals: list[str], prior: str):
    votes = model["label_priors"][prior].copy()
    for signal in signals:
        votes.update(model[table].get(signal, {}))
    return votes


def predict(record: dict, model: dict | None = None) -> dict:
    model = model or load_model()
    if model.get("backend") == "sklearn":
        text = [text_for_record(record)]
        docs = bool(model["docs_update_required"].predict(text)[0])
        if not docs:
            return {"docs_update_required": False, "doc_category": "no_update", "target_doc_file": "", "scenario_type": str(model["scenario_type"].predict(text)[0]), "ml_backend": "sklearn"}
        return {
            "docs_update_required": True,
            "doc_category": str(model["doc_category"].predict(text)[0]),
            "target_doc_file": str(model["target_doc_file"].predict(text)[0]),
            "scenario_type": str(model["scenario_type"].predict(text)[0]),
            "ml_backend": "sklearn",
        }

    routed = route(record)
    if not routed["docs_update_required"]:
        return {"docs_update_required": False, "doc_category": "no_update", "target_doc_file": "", "scenario_type": (routed["candidate_scenario_types"] or ["unknown_change"])[0], "ml_backend": "fallback"}
    signals = routed["signals"] or ["no_signal"]
    scenario_votes = combine_votes(model, "scenario_by_signal", signals, "scenario_type")
    category_votes = combine_votes(model, "category_by_signal", signals, "doc_category")
    target_votes = combine_votes(model, "target_by_signal", signals, "target_doc_file")
    category = most_common(category_votes, routed["candidate_doc_categories"][0])
    if category == "no_update":
        category = routed["candidate_doc_categories"][0]
    return {
        "docs_update_required": True,
        "doc_category": category,
        "target_doc_file": most_common(target_votes, routed["candidate_target_doc_files"][0]),
        "scenario_type": most_common(scenario_votes, routed["candidate_scenario_types"][0]),
        "ml_backend": "fallback",
    }
