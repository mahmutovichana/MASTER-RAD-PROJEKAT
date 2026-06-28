from __future__ import annotations

from pathlib import Path

from docguard_hf_classifier.dataset_export import HF_DATA_DIR, read_jsonl
from docguard_hf_classifier.label_maps import label_for_record, load_label_maps

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models" / "hf_v0_4"
REPORTS_DIR = ROOT / "reports"


def train_sequence(task: str, base_model: str, epochs: int = 1, limit_train: int | None = None, limit_eval: int | None = None) -> dict:
    try:
        from datasets import Dataset
        from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
    except ModuleNotFoundError as exc:
        raise RuntimeError(f"Missing fine-tuning dependency `{exc.name}`. Install with: python -m pip install transformers datasets torch scikit-learn") from exc
    label_maps = load_label_maps()[task]
    train_rows = read_jsonl(HF_DATA_DIR / "train.jsonl")[:limit_train]
    eval_rows = read_jsonl(HF_DATA_DIR / "validation.jsonl")[:limit_eval]
    tokenizer = AutoTokenizer.from_pretrained(base_model)

    def to_examples(rows: list[dict]) -> dict:
        return {"text": [row["input_text"] for row in rows], "label": [label_maps["label2id"][row[f"{task}_label"]] for row in rows]}

    def tokenize(batch: dict) -> dict:
        return tokenizer(batch["text"], truncation=True, max_length=256)

    train_ds = Dataset.from_dict(to_examples(train_rows)).map(tokenize, batched=True)
    eval_ds = Dataset.from_dict(to_examples(eval_rows)).map(tokenize, batched=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        base_model,
        num_labels=len(label_maps["labels"]),
        id2label={int(k): v for k, v in label_maps["id2label"].items()},
        label2id=label_maps["label2id"],
    )
    output_dir = MODELS_DIR / f"sequence_{task}"
    args = TrainingArguments(output_dir=str(output_dir), num_train_epochs=epochs, per_device_train_batch_size=4, per_device_eval_batch_size=4, report_to=[])
    trainer = Trainer(model=model, args=args, train_dataset=train_ds, eval_dataset=eval_ds)
    trainer.train()
    trainer.save_model(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))
    return {"task": task, "base_model": base_model, "output_dir": str(output_dir), "train_records": len(train_rows), "eval_records": len(eval_rows)}


def evaluate_sequence(task: str, split: str = "validation") -> dict:
    raise RuntimeError("Sequence evaluation requires a trained Hugging Face sequence model and is intentionally optional for CPU runs.")

