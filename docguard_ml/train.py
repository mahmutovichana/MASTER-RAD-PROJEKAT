from __future__ import annotations

import json
import pickle
from collections import Counter, defaultdict
from pathlib import Path

from docguard_hybrid.doc_router import route
from docguard_ml.features import text_for_record

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
MODELS_DIR = ROOT / "models" / "v0_4"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def train_sklearn(records: list[dict], version: str) -> dict | None:
    try:
        import joblib
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
    except ModuleNotFoundError:
        return None
    texts = [text_for_record(record) for record in records]
    positives = [record for record in records if record["docs_update_required"]]
    positive_texts = [text_for_record(record) for record in positives]

    def pipeline():
        return Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=20000)),
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ])

    model = {
        "version": version,
        "backend": "sklearn",
        "docs_update_required": pipeline().fit(texts, [record["docs_update_required"] for record in records]),
        "doc_category": pipeline().fit(texts, [record["doc_category"] for record in records]),
        "scenario_type": pipeline().fit(texts, [record["scenario_type"] for record in records]),
        "target_doc_file": pipeline().fit(positive_texts, [record["target_doc_file"] for record in positives]),
    }
    path = MODELS_DIR / "sklearn_model.joblib"
    joblib.dump(model, path)
    return {"records": len(records), "backend": "sklearn", "model_path": str(path)}


def train_fallback(records: list[dict], version: str) -> dict:
    model = {
        "version": version,
        "backend": "fallback",
        "label_priors": {
            "docs_update_required": Counter(str(r["docs_update_required"]) for r in records),
            "doc_category": Counter(r["doc_category"] for r in records),
            "target_doc_file": Counter(r["target_doc_file"] for r in records if r["docs_update_required"]),
            "scenario_type": Counter(r["scenario_type"] for r in records),
        },
        "scenario_by_signal": defaultdict(Counter),
        "category_by_signal": defaultdict(Counter),
        "target_by_signal": defaultdict(Counter),
    }
    for record in records:
        routed = route(record)
        for signal in routed["signals"] or ["no_signal"]:
            model["scenario_by_signal"][signal][record["scenario_type"]] += 1
            model["category_by_signal"][signal][record["doc_category"]] += 1
            if record["docs_update_required"]:
                model["target_by_signal"][signal][record["target_doc_file"]] += 1
    path = MODELS_DIR / "fallback_model.pkl"
    with path.open("wb") as handle:
        pickle.dump(model, handle)
    return {"records": len(records), "backend": "fallback", "model_path": str(path), "feature_example": text_for_record(records[0])[:120]}


def train(version: str = "v0_4") -> dict:
    records = read_jsonl(DATA_DIR / "train.jsonl")
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    result = train_sklearn(records, version)
    if result is not None:
        return result
    return train_fallback(records, version)


if __name__ == "__main__":
    print(json.dumps(train(), indent=2))
