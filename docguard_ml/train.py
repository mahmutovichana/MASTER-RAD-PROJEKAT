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


def train(version: str = "v0_4") -> dict:
    records = read_jsonl(DATA_DIR / "train.jsonl")
    model = {
        "version": version,
        "backend": "signal_fallback_no_sklearn",
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
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    with (MODELS_DIR / "fallback_model.pkl").open("wb") as handle:
        pickle.dump(model, handle)
    return {"records": len(records), "model_path": str(MODELS_DIR / "fallback_model.pkl"), "feature_example": text_for_record(records[0])[:120]}


if __name__ == "__main__":
    print(json.dumps(train(), indent=2))
