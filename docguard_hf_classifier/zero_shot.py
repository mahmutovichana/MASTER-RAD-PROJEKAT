from __future__ import annotations

from docguard_hf_classifier.dataset_export import HF_DATA_DIR, read_jsonl
from docguard_hf_classifier.label_maps import load_label_maps


def evaluate_zero_shot(version: str = "v0_4", split: str = "validation", limit: int = 20, model: str = "facebook/bart-large-mnli") -> dict:
    try:
        from transformers import pipeline
    except ModuleNotFoundError as exc:
        raise RuntimeError(f"Missing zero-shot dependency `{exc.name}`. Install with: python -m pip install transformers torch") from exc
    rows = read_jsonl(HF_DATA_DIR / f"{split}.jsonl")[:limit]
    labels = load_label_maps()["doc_category"]["labels"]
    classifier = pipeline("zero-shot-classification", model=model)
    correct = 0
    for row in rows:
        result = classifier(row["input_text"], candidate_labels=labels)
        correct += int(result["labels"][0] == row["doc_category_label"])
    return {"version": version, "split": split, "limit": len(rows), "model": model, "doc_category_accuracy": correct / len(rows) if rows else 0.0}

