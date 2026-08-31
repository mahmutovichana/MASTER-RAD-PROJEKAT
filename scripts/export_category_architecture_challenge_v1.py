"""Export the bounded Stage-2 CodeBERT architecture challenge artifacts.

This script does not train a model.  It materializes only the natural,
independently reviewed, primary-four rows needed by the Colab GPU notebook and
writes a self-contained notebook for the CodeBERT joint classifier experiment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


LABELS = ["api_reference", "configuration", "developer_setup", "model_contract"]
LABEL_SET = set(LABELS)
SEED = 42
FROZEN_VALIDATION_CASE_IDS_SHA256 = "aac3384de6d482abefb4201091bf828d6d8c1c91c1ddbdad40a4ec7273051e3e"
FROZEN_BENCHMARK = {
    "model": "hybrid__natural_only__multinomial_logreg__natural_diversity_expansion_v1",
    "support": 322,
    "macro_f1": 0.45628987455472775,
    "balanced_accuracy": 0.478023538961039,
    "per_class_f1": {
        "api_reference": 0.5340314136125655,
        "configuration": 0.6824324324324325,
        "developer_setup": 0.0,
        "model_contract": 0.6086956521739131,
    },
}
SAFE_EXPORT_FIELDS = [
    "case_id",
    "repository",
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
    "gold_doc_category",
    "partition",
]
FORBIDDEN_EXPORT_FIELDS = {
    "docs_after",
    "docs_after_excerpt",
    "docs_diff",
    "docs_diff_excerpt",
    "suggested_docs_update_required",
    "suggested_doc_category",
    "suggested_notes",
    "human_label_notes",
    "label_source",
    "supervision_source",
    "provenance_tier",
    "controlled_design_supervision",
    "controlled_design_label",
    "repository_full_name_for_model",
}


def stable_json_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def reject_confirmation_path(path: Path) -> None:
    text = str(path).replace("\\", "/").lower()
    if "confirmation" in text:
        raise ValueError(f"Confirmation path is forbidden: {path}")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    reject_confirmation_path(path)
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: row is not an object")
            if str(row.get("partition") or "").lower() == "confirmation":
                raise ValueError(f"{path}:{line_number}: confirmation row is forbidden")
            rows.append(row)
    return rows


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def list_value(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        text = value.strip()
        if text.startswith("["):
            try:
                parsed = json.loads(text)
                if isinstance(parsed, list):
                    return [str(item) for item in parsed]
            except json.JSONDecodeError:
                pass
        return [text] if text else []
    return []


def sanitize_repository_identity(text: str, repository: str) -> str:
    repo = repository.strip().strip("/")
    if not repo or "/" not in repo:
        return str(text)
    owner, name = repo.split("/", 1)
    patterns = [
        re.escape(repo),
        re.escape(f"github.com/{repo}"),
        re.escape(f"https://github.com/{repo}"),
        re.escape(f"http://github.com/{repo}"),
        re.escape(f"git@github.com:{repo}"),
    ]
    sanitized = str(text)
    for pattern in patterns:
        sanitized = re.sub(pattern, "[REPOSITORY]", sanitized, flags=re.IGNORECASE)
    return re.sub(
        rf"github\.com/{re.escape(owner)}/{re.escape(name)}(?:\.git)?",
        "[REPOSITORY]",
        sanitized,
        flags=re.IGNORECASE,
    )


def reject_forbidden_row(row: dict[str, Any], *, source: str) -> None:
    case_id = str(row.get("case_id") or "<missing-case-id>")
    partition = str(row.get("partition") or "").lower()
    if partition == "confirmation":
        raise ValueError(f"{source}:{case_id}: confirmation row is forbidden")
    if row.get("controlled_design_supervision") is True:
        raise ValueError(f"{source}:{case_id}: controlled row is forbidden")
    for field in ("label_source", "supervision_source", "provenance_tier"):
        if "controlled" in str(row.get(field) or "").lower():
            raise ValueError(f"{source}:{case_id}: controlled provenance is forbidden")


def is_primary_positive(row: dict[str, Any]) -> bool:
    return row.get("gold_docs_update_required") is True and str(row.get("gold_doc_category")) in LABEL_SET


def is_natural_reviewed(row: dict[str, Any]) -> bool:
    return row.get("independent_human_reviewed") is True and not (
        row.get("controlled_design_supervision") is True
        or "controlled" in str(row.get("label_source") or "").lower()
        or "controlled" in str(row.get("supervision_source") or "").lower()
    )


def build_code_text(row: dict[str, Any]) -> str:
    text = "\n".join(
        [
            f"language: {str(row.get('language') or 'unknown').lower()}",
            "changed files:",
            "\n".join(list_value(row.get("code_changed_files"))),
            "code change:",
            str(row.get("code_diff_excerpt") or ""),
        ]
    )
    return sanitize_repository_identity(text, str(row.get("repository") or ""))


def build_docs_text(row: dict[str, Any]) -> str:
    return sanitize_repository_identity(str(row.get("docs_before_excerpt") or ""), str(row.get("repository") or ""))


def export_row(row: dict[str, Any], *, partition: str) -> dict[str, Any]:
    if partition == "development_train" and row.get("partition") not in {"development_train", None, ""}:
        raise ValueError(f"{row.get('case_id')}: non-train row entered training export")
    if partition == "development_validation" and row.get("partition") != "development_validation":
        raise ValueError(f"{row.get('case_id')}: validation membership changed")
    if partition == "refresh_validation":
        raise ValueError("refresh validation is forbidden for this training export")
    exported = {
        "case_id": str(row["case_id"]),
        "repository": str(row["repository"]),
        "language": str(row.get("language") or "unknown").lower(),
        "code_changed_files": list_value(row.get("code_changed_files")),
        "code_diff_excerpt": str(row.get("code_diff_excerpt") or ""),
        "docs_before_excerpt": str(row.get("docs_before_excerpt") or ""),
        "gold_doc_category": str(row["gold_doc_category"]),
        "partition": partition,
    }
    return exported


def select_old_train(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = [
        export_row(row, partition="development_train")
        for row in rows
        if is_primary_positive(row) and is_natural_reviewed(row) and row.get("partition") == "development_train"
    ]
    return selected


def select_expansion_train(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = [
        export_row(row, partition="development_train")
        for row in rows
        if is_primary_positive(row) and is_natural_reviewed(row) and row.get("partition") == "development_train"
    ]
    return selected


def select_validation(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = [
        export_row(row, partition="development_validation")
        for row in rows
        if is_primary_positive(row) and row.get("partition") == "development_validation"
    ]
    return selected


def distribution(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_label = Counter(str(row["gold_doc_category"]) for row in rows)
    by_language = Counter(str(row["language"]) for row in rows)
    return {
        "row_count": len(rows),
        "category_counts": {label: by_label.get(label, 0) for label in LABELS},
        "language_counts": dict(sorted(by_language.items())),
        "distinct_repository_count": len({str(row["repository"]).lower() for row in rows}),
    }


def audit_export_rows(train: list[dict[str, Any]], validation: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    for collection_name, rows in (("train", train), ("validation", validation)):
        ids = [str(row["case_id"]) for row in rows]
        if len(ids) != len(set(ids)):
            errors.append(f"{collection_name}: duplicate case IDs")
        for row in rows:
            keys = set(row)
            forbidden = sorted(keys & FORBIDDEN_EXPORT_FIELDS)
            if forbidden:
                errors.append(f"{collection_name}:{row['case_id']}: forbidden export keys {forbidden}")
            if row["gold_doc_category"] not in LABEL_SET:
                errors.append(f"{collection_name}:{row['case_id']}: invalid category")
            if "confirmation" in str(row.get("partition") or "").lower():
                errors.append(f"{collection_name}:{row['case_id']}: confirmation row")
            code_text = build_code_text(row)
            docs_text = build_docs_text(row)
            combined = f"{code_text}\n{docs_text}"
            if str(row["repository"]) in combined:
                errors.append(f"{collection_name}:{row['case_id']}: repository identity serialized into model text")
            for forbidden_text in ("docs_after", "docs_diff", "label_source", "supervision_source", "provenance_tier"):
                if forbidden_text in combined:
                    errors.append(f"{collection_name}:{row['case_id']}: forbidden provenance/post-change token")
    validation_hash = stable_json_hash([row["case_id"] for row in validation])
    if validation_hash != FROZEN_VALIDATION_CASE_IDS_SHA256:
        errors.append(
            "validation membership hash changed: "
            f"{validation_hash} != {FROZEN_VALIDATION_CASE_IDS_SHA256}"
        )
    train_repos = {str(row["repository"]).lower() for row in train}
    validation_repos = {str(row["repository"]).lower() for row in validation}
    return {
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "validation_case_ids_sha256": validation_hash,
        "frozen_validation_case_ids_sha256": FROZEN_VALIDATION_CASE_IDS_SHA256,
        "train_validation_repository_overlap": sorted(train_repos & validation_repos),
        "repository_identity_excluded_from_model_text": True,
        "forbidden_fields_excluded_from_export": True,
        "confirmation_accessed": False,
        "controlled_rows_used": False,
        "refresh_validation_used_for_training": False,
    }


def make_notebook() -> dict[str, Any]:
    cells: list[dict[str, Any]] = []

    def markdown(text: str) -> None:
        cells.append({"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)})

    def code(text: str) -> None:
        cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": text.splitlines(keepends=True)})

    markdown(
        """# Stage-2 Architecture Challenge V1: CodeBERT Joint Classifier

This notebook trains exactly one architecture: `microsoft/codebert-base` as a
joint code/docs cross-encoder for the four primary Stage-2 categories.  It uses
only natural, independently reviewed development-train positives and evaluates
once on the frozen 322-row natural development validation."""
    )
    code(
        """%pip install -q \\
  transformers==4.44.2 \\
  accelerate==0.33.0 \\
  scikit-learn==1.5.1 \\
  matplotlib==3.9.2 \\
  huggingface_hub==0.24.6 \\
  safetensors==0.4.4"""
    )
    code(
        """from __future__ import annotations

import hashlib
import json
import platform
import random
import re
import time
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from huggingface_hub import HfApi
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)
from sklearn.model_selection import GroupShuffleSplit
from torch.utils.data import Dataset
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    set_seed,
)

SEED = 42
LABELS = ["api_reference", "configuration", "developer_setup", "model_contract"]
LABEL_TO_ID = {label: index for index, label in enumerate(LABELS)}
ID_TO_LABEL = {index: label for label, index in LABEL_TO_ID.items()}
MODEL_NAME = "microsoft/codebert-base"
MODEL_REVISION_ALIAS = "main"
FROZEN_VALIDATION_CASE_IDS_SHA256 = "aac3384de6d482abefb4201091bf828d6d8c1c91c1ddbdad40a4ec7273051e3e"
FROZEN_BENCHMARK = {
    "model": "hybrid__natural_only__multinomial_logreg__natural_diversity_expansion_v1",
    "macro_f1": 0.45628987455472775,
    "balanced_accuracy": 0.478023538961039,
}
EXPORT_DIR = Path("data/final_v2/architecture_challenge_v1")
TRAIN_PATH = EXPORT_DIR / "natural_train_primary_four.jsonl"
VALIDATION_PATH = EXPORT_DIR / "natural_validation_primary_four.jsonl"
MANIFEST_PATH = EXPORT_DIR / "export_manifest.json"
OUTPUT_DIR = Path("experiments/category_architecture_challenge_v1/codebert_joint")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
set_seed(SEED)

print("CUDA available:", torch.cuda.is_available())
if not torch.cuda.is_available():
    raise RuntimeError("This experiment is intended for a Colab GPU runtime. Enable Runtime > Change runtime type > GPU.")
print("CUDA device:", torch.cuda.get_device_name(0))"""
    )
    code(
        """def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_json_hash(value) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    if "confirmation" in str(path).lower():
        raise ValueError(f"Confirmation path is forbidden: {path}")
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                row = json.loads(line)
                if str(row.get("partition", "")).lower() == "confirmation":
                    raise ValueError(f"Confirmation row is forbidden: {row.get('case_id')}")
                rows.append(row)
    return rows


def ensure_inputs_present() -> None:
    missing = [path for path in (TRAIN_PATH, VALIDATION_PATH, MANIFEST_PATH) if not path.exists()]
    if not missing:
        return
    try:
        from google.colab import files
    except Exception as exc:
        raise FileNotFoundError(f"Missing export files: {missing}") from exc
    print("Upload natural_train_primary_four.jsonl, natural_validation_primary_four.jsonl, and export_manifest.json")
    uploaded = files.upload()
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    for name, data in uploaded.items():
        target = EXPORT_DIR / Path(name).name
        target.write_bytes(data)
    missing = [path for path in (TRAIN_PATH, VALIDATION_PATH, MANIFEST_PATH) if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Still missing export files after upload: {missing}")


ensure_inputs_present()
train_rows = read_jsonl(TRAIN_PATH)
validation_rows = read_jsonl(VALIDATION_PATH)
manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

assert sha256_file(TRAIN_PATH) == manifest["artifacts"]["natural_train_primary_four.jsonl"]["sha256"]
assert sha256_file(VALIDATION_PATH) == manifest["artifacts"]["natural_validation_primary_four.jsonl"]["sha256"]
validation_case_hash = stable_json_hash([row["case_id"] for row in validation_rows])
assert validation_case_hash == FROZEN_VALIDATION_CASE_IDS_SHA256
assert len(validation_rows) == 322
assert all(row["partition"] == "development_train" for row in train_rows)
assert all(row["partition"] == "development_validation" for row in validation_rows)
assert not any("confirmation" in str(row.get("partition", "")).lower() for row in train_rows + validation_rows)
assert not any(field in row for row in train_rows + validation_rows for field in ["controlled_design_supervision", "controlled_design_label", "docs_after_excerpt", "docs_diff_excerpt", "suggested_notes", "human_label_notes"])

print("Train rows:", len(train_rows), Counter(row["gold_doc_category"] for row in train_rows))
print("Validation rows:", len(validation_rows), Counter(row["gold_doc_category"] for row in validation_rows))"""
    )
    code(
        """api = HfApi()
model_info = api.model_info(MODEL_NAME, revision=MODEL_REVISION_ALIAS)
CODEBERT_REVISION_SHA = model_info.sha
print("Resolved CodeBERT revision:", CODEBERT_REVISION_SHA)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, revision=CODEBERT_REVISION_SHA, use_fast=True)


def sanitize_repository_identity(text: str, repository: str) -> str:
    repo = repository.strip().strip("/")
    if not repo or "/" not in repo:
        return str(text)
    owner, name = repo.split("/", 1)
    patterns = [
        re.escape(repo),
        re.escape(f"github.com/{repo}"),
        re.escape(f"https://github.com/{repo}"),
        re.escape(f"http://github.com/{repo}"),
        re.escape(f"git@github.com:{repo}"),
    ]
    sanitized = str(text)
    for pattern in patterns:
        sanitized = re.sub(pattern, "[REPOSITORY]", sanitized, flags=re.IGNORECASE)
    return re.sub(
        rf"github\\.com/{re.escape(owner)}/{re.escape(name)}(?:\\.git)?",
        "[REPOSITORY]",
        sanitized,
        flags=re.IGNORECASE,
    )


def code_text(row: dict) -> str:
    text = "\\n".join([
        f"language: {str(row.get('language') or 'unknown').lower()}",
        "changed files:",
        "\\n".join(str(item) for item in row.get("code_changed_files", [])),
        "code change:",
        str(row.get("code_diff_excerpt") or ""),
    ])
    return sanitize_repository_identity(text, str(row.get("repository") or ""))


def docs_text(row: dict) -> str:
    return sanitize_repository_identity(str(row.get("docs_before_excerpt") or ""), str(row.get("repository") or ""))


def head_tail(ids: list[int], budget: int) -> list[int]:
    if budget <= 0:
        return []
    if len(ids) <= budget:
        return list(ids)
    head = max(1, budget // 2)
    tail = budget - head
    return list(ids[:head]) + list(ids[-tail:])


def balanced_pair(row: dict, *, max_length: int = 512, code_ratio: float = 0.58) -> tuple[dict, dict]:
    repo = str(row.get("repository") or "")
    prefix = sanitize_repository_identity("\\n".join([
        f"language: {str(row.get('language') or 'unknown').lower()}",
        "changed files:",
        "\\n".join(str(item) for item in row.get("code_changed_files", [])),
        "code change:",
    ]), repo)
    diff = sanitize_repository_identity(str(row.get("code_diff_excerpt") or ""), repo)
    docs = docs_text(row)
    prefix_ids = tokenizer.encode(prefix, add_special_tokens=False)
    diff_ids = tokenizer.encode(diff, add_special_tokens=False)
    docs_ids = tokenizer.encode(docs, add_special_tokens=False)
    special = tokenizer.num_special_tokens_to_add(pair=True)
    available = max_length - special
    code_budget = max(8, int(available * code_ratio))
    docs_budget = max(1, available - code_budget)
    if len(docs_ids) > 0 and docs_budget < 1:
        docs_budget = 1
        code_budget = available - docs_budget
    prefix_budget_cap = max(1, int(code_budget * 0.23))
    if len(diff_ids) > 0:
        prefix_budget = min(len(prefix_ids), prefix_budget_cap)
        diff_budget = max(1, code_budget - prefix_budget)
    else:
        prefix_budget = min(len(prefix_ids), code_budget)
        diff_budget = 0
    kept_prefix = head_tail(prefix_ids, prefix_budget)
    kept_diff = head_tail(diff_ids, diff_budget)
    kept_code = kept_prefix + kept_diff
    kept_docs = head_tail(docs_ids, docs_budget)
    prepared = tokenizer.prepare_for_model(
        kept_code,
        kept_docs,
        max_length=max_length,
        padding="max_length",
        truncation=False,
        return_attention_mask=True,
    )
    stats = {
        "original_code_tokens": len(prefix_ids) + len(diff_ids),
        "original_prefix_tokens": len(prefix_ids),
        "original_diff_tokens": len(diff_ids),
        "original_docs_tokens": len(docs_ids),
        "retained_code_tokens": len(kept_code),
        "retained_prefix_tokens": len(kept_prefix),
        "retained_diff_tokens": len(kept_diff),
        "retained_docs_tokens": len(kept_docs),
        "code_truncated": len(prefix_ids) + len(diff_ids) > len(kept_code),
        "prefix_truncated": len(prefix_ids) > len(kept_prefix),
        "diff_truncated": len(diff_ids) > len(kept_diff),
        "diff_became_empty": len(diff_ids) > 0 and len(kept_diff) == 0,
        "docs_truncated": len(docs_ids) > len(kept_docs),
        "docs_became_empty": len(docs_ids) > 0 and len(kept_docs) == 0,
    }
    return prepared, stats


def assert_repository_not_in_model_text(rows: list[dict]) -> None:
    for row in rows:
        combined = code_text(row) + "\\n" + docs_text(row)
        if str(row["repository"]) in combined:
            raise ValueError(f"Repository identity serialized into model text: {row['case_id']}")


assert_repository_not_in_model_text(train_rows + validation_rows)"""
    )
    code(
        """def summarize_truncation(rows: list[dict]) -> dict:
    stats = [balanced_pair(row)[1] for row in rows]
    rows_with_diff = [item for item in stats if item["original_diff_tokens"] > 0]
    original_diff_tokens = sum(item["original_diff_tokens"] for item in rows_with_diff)
    retained_diff_tokens = sum(item["retained_diff_tokens"] for item in rows_with_diff)
    return {
        "rows": len(stats),
        "percent_rows_truncated": 100.0 * sum(item["code_truncated"] or item["docs_truncated"] for item in stats) / len(stats),
        "average_original_code_tokens": float(np.mean([item["original_code_tokens"] for item in stats])),
        "average_original_diff_tokens": float(np.mean([item["original_diff_tokens"] for item in stats])),
        "average_original_docs_tokens": float(np.mean([item["original_docs_tokens"] for item in stats])),
        "average_retained_code_tokens": float(np.mean([item["retained_code_tokens"] for item in stats])),
        "average_retained_diff_tokens": float(np.mean([item["retained_diff_tokens"] for item in stats])),
        "average_retained_docs_tokens": float(np.mean([item["retained_docs_tokens"] for item in stats])),
        "rows_with_nonempty_original_diff": len(rows_with_diff),
        "rows_with_zero_retained_diff": int(sum(item["diff_became_empty"] for item in stats)),
        "percent_diff_tokens_retained": 100.0 * retained_diff_tokens / original_diff_tokens if original_diff_tokens else 100.0,
        "docs_became_empty": int(sum(item["docs_became_empty"] for item in stats)),
    }


truncation_stats = {
    "train": summarize_truncation(train_rows),
    "validation": summarize_truncation(validation_rows),
    "policy": "Manual pair construction with about 58% non-special tokens for code side and 42% for docs side; within code-side budget, language/changed-files prefix is capped near 23% and non-empty code diffs reserve the remaining majority; docs use deterministic head/tail truncation.",
}
assert truncation_stats["train"]["docs_became_empty"] == 0
assert truncation_stats["validation"]["docs_became_empty"] == 0
assert truncation_stats["train"]["rows_with_zero_retained_diff"] == 0
assert truncation_stats["validation"]["rows_with_zero_retained_diff"] == 0
truncation_stats"""
    )
    code(
        """groups = np.array([row["repository"].lower() for row in train_rows])
y = np.array([LABEL_TO_ID[row["gold_doc_category"]] for row in train_rows])
indices = np.arange(len(train_rows))

splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEED)
for internal_train_idx, internal_eval_idx in splitter.split(indices, y, groups):
    pass

if set(y[internal_train_idx]) != set(range(len(LABELS))) or set(y[internal_eval_idx]) != set(range(len(LABELS))):
    raise RuntimeError("Internal repository-grouped split missed at least one class; do not tune on external validation.")

print("Internal train:", len(internal_train_idx), Counter(y[internal_train_idx]))
print("Internal eval:", len(internal_eval_idx), Counter(y[internal_eval_idx]))
print("Repository overlap:", set(groups[internal_train_idx]) & set(groups[internal_eval_idx]))"""
    )
    code(
        """class PairDataset(Dataset):
    def __init__(self, rows: list[dict]):
        self.rows = rows

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int) -> dict:
        row = self.rows[index]
        encoded, _stats = balanced_pair(row)
        encoded = {key: torch.tensor(value) for key, value in encoded.items()}
        encoded["labels"] = torch.tensor(LABEL_TO_ID[row["gold_doc_category"]], dtype=torch.long)
        return encoded


internal_train_rows = [train_rows[index] for index in internal_train_idx]
internal_eval_rows = [train_rows[index] for index in internal_eval_idx]
train_ds = PairDataset(internal_train_rows)
eval_ds = PairDataset(internal_eval_rows)
validation_ds = PairDataset(validation_rows)"""
    )
    code(
        """def compute_metrics(eval_pred) -> dict:
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "macro_f1": f1_score(labels, preds, average="macro", labels=list(range(len(LABELS))), zero_division=0),
        "weighted_f1": f1_score(labels, preds, average="weighted", labels=list(range(len(LABELS))), zero_division=0),
        "balanced_accuracy": balanced_accuracy_score(labels, preds),
    }


model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    revision=CODEBERT_REVISION_SHA,
    num_labels=len(LABELS),
    id2label=ID_TO_LABEL,
    label2id=LABEL_TO_ID,
)

training_args = TrainingArguments(
    output_dir=str(OUTPUT_DIR / "checkpoints"),
    seed=SEED,
    data_seed=SEED,
    learning_rate=2e-5,
    num_train_epochs=3,
    weight_decay=0.01,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    gradient_accumulation_steps=2,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    save_total_limit=2,
    load_best_model_at_end=True,
    metric_for_best_model="eval_macro_f1",
    greater_is_better=True,
    fp16=torch.cuda.is_available(),
    logging_steps=25,
    report_to=[],
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=eval_ds,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

started = time.perf_counter()
train_result = trainer.train()
training_seconds = time.perf_counter() - started"""
    )
    code(
        """prediction_output = trainer.predict(validation_ds)
logits = prediction_output.predictions
gold_ids = prediction_output.label_ids
pred_ids = np.argmax(logits, axis=1)
probs = torch.softmax(torch.tensor(logits), dim=1).numpy()
gold_labels = [ID_TO_LABEL[int(item)] for item in gold_ids]
pred_labels = [ID_TO_LABEL[int(item)] for item in pred_ids]

precision, recall, f1, support = precision_recall_fscore_support(
    gold_labels, pred_labels, labels=LABELS, zero_division=0
)
cm = confusion_matrix(gold_labels, pred_labels, labels=LABELS)
cm_norm = cm.astype(float) / np.maximum(cm.sum(axis=1, keepdims=True), 1)

metrics = {
    "model": "codebert_joint_classifier",
    "benchmark": FROZEN_BENCHMARK,
    "accuracy": float(accuracy_score(gold_labels, pred_labels)),
    "macro_f1": float(f1_score(gold_labels, pred_labels, labels=LABELS, average="macro", zero_division=0)),
    "weighted_f1": float(f1_score(gold_labels, pred_labels, labels=LABELS, average="weighted", zero_division=0)),
    "balanced_accuracy": float(balanced_accuracy_score(gold_labels, pred_labels)),
    "delta_vs_frozen_hybrid": {},
    "per_class": {
        label: {
            "precision": float(precision[index]),
            "recall": float(recall[index]),
            "f1": float(f1[index]),
            "support": int(support[index]),
        }
        for index, label in enumerate(LABELS)
    },
    "confusion_matrix": cm.tolist(),
    "normalized_confusion_matrix": cm_norm.tolist(),
    "predicted_class_counts": dict(sorted(Counter(pred_labels).items())),
}
metrics["delta_vs_frozen_hybrid"] = {
    "macro_f1": metrics["macro_f1"] - FROZEN_BENCHMARK["macro_f1"],
    "balanced_accuracy": metrics["balanced_accuracy"] - FROZEN_BENCHMARK["balanced_accuracy"],
}

setup_rows = []
api_false_positive_counts = {
    "configuration_to_api_reference": 0,
    "model_contract_to_api_reference": 0,
    "developer_setup_to_api_reference": 0,
    "total_api_reference_false_positives": 0,
}
predictions = []
for row, gold, pred, scores in zip(validation_rows, gold_labels, pred_labels, probs):
    ranking = sorted(
        [{"label": label, "probability": float(scores[index])} for index, label in enumerate(LABELS)],
        key=lambda item: item["probability"],
        reverse=True,
    )
    item = {
        "case_id": row["case_id"],
        "gold": gold,
        "prediction": pred,
        "correct": gold == pred,
        "probabilities": {label: float(scores[index]) for index, label in enumerate(LABELS)},
        "top2": ranking[:2],
    }
    predictions.append(item)
    if gold == "developer_setup":
        setup_rows.append(item)
    if pred == "api_reference" and gold != "api_reference":
        key = f"{gold}_to_api_reference"
        if key in api_false_positive_counts:
            api_false_positive_counts[key] += 1
        api_false_positive_counts["total_api_reference_false_positives"] += 1

developer_setup_payload = {
    "support": len(setup_rows),
    "correct": sum(item["correct"] for item in setup_rows),
    "precision": metrics["per_class"]["developer_setup"]["precision"],
    "recall": metrics["per_class"]["developer_setup"]["recall"],
    "f1": metrics["per_class"]["developer_setup"]["f1"],
    "top2_predictions": setup_rows,
}
metrics["developer_setup_diagnostics"] = {
    key: developer_setup_payload[key]
    for key in ("support", "correct", "precision", "recall", "f1")
}
metrics["api_catch_all_diagnostics"] = api_false_positive_counts
metrics"""
    )
    code(
        """def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\\n")


def plot_matrix(matrix, path: Path, title: str, normalized: bool) -> None:
    plt.figure(figsize=(7.5, 6.5))
    plt.imshow(matrix, cmap="Blues")
    plt.colorbar(label="Proportion" if normalized else "Count")
    plt.xticks(range(len(LABELS)), LABELS, rotation=25, ha="right")
    plt.yticks(range(len(LABELS)), LABELS)
    for i in range(len(LABELS)):
        for j in range(len(LABELS)):
            text = f"{matrix[i][j]:.2f}" if normalized else str(int(matrix[i][j]))
            plt.text(j, i, text, ha="center", va="center", color="white" if matrix[i][j] > matrix.max() / 2 else "black")
    plt.xlabel("Predicted")
    plt.ylabel("Gold")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


plot_matrix(cm, OUTPUT_DIR / "confusion_matrix.png", "CodeBERT joint classifier", normalized=False)
plot_matrix(cm_norm, OUTPUT_DIR / "normalized_confusion_matrix.png", "CodeBERT joint classifier normalized", normalized=True)

plt.figure(figsize=(9, 5))
plt.bar(LABELS, [metrics["per_class"][label]["f1"] for label in LABELS])
plt.ylim(0, 1)
plt.ylabel("F1")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "per_class_f1.png", dpi=180)
plt.close()

history = trainer.state.log_history
epochs = [item["epoch"] for item in history if "eval_macro_f1" in item]
macro = [item["eval_macro_f1"] for item in history if "eval_macro_f1" in item]
loss = [item.get("eval_loss") for item in history if "eval_macro_f1" in item]
plt.figure(figsize=(8, 5))
plt.plot(epochs, macro, marker="o", label="Internal eval Macro-F1")
if any(value is not None for value in loss):
    plt.plot(epochs, loss, marker="o", label="Internal eval loss")
plt.xlabel("Epoch")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "training_history.png", dpi=180)
plt.close()

model_dir = OUTPUT_DIR / "model"
trainer.save_model(str(model_dir))
tokenizer.save_pretrained(str(model_dir))
model_file = model_dir / "model.safetensors"
if not model_file.exists():
    model_file = model_dir / "pytorch_model.bin"

training_manifest = {
    "schema": "category_architecture_challenge_v1_codebert_joint_training",
    "model_name": MODEL_NAME,
    "model_revision_sha": CODEBERT_REVISION_SHA,
    "tokenizer_revision_sha": CODEBERT_REVISION_SHA,
    "seed": SEED,
    "cuda_device": torch.cuda.get_device_name(0),
    "python": platform.python_version(),
    "platform": platform.platform(),
    "torch_version": torch.__version__,
    "transformers_version": __import__("transformers").__version__,
    "training_seconds": training_seconds,
    "train_result": train_result.metrics,
    "internal_split": {
        "method": "GroupShuffleSplit by repository",
        "train_rows": len(internal_train_rows),
        "eval_rows": len(internal_eval_rows),
        "repository_overlap": sorted(set(row["repository"].lower() for row in internal_train_rows) & set(row["repository"].lower() for row in internal_eval_rows)),
    },
    "truncation": truncation_stats,
    "input_fields": {
        "code_side": ["language", "code_changed_files", "code_diff_excerpt"],
        "docs_side": ["docs_before_excerpt"],
        "repository_used_only_for_grouping": True,
    },
    "model_sha256": sha256_file(model_file),
    "confirmation_accessed": False,
    "controlled_data_used": False,
    "refresh_validation_used_for_training": False,
}

write_json(OUTPUT_DIR / "metrics.json", metrics)
write_json(OUTPUT_DIR / "training_manifest.json", training_manifest)
write_jsonl(OUTPUT_DIR / "validation_predictions.jsonl", predictions)
write_json(OUTPUT_DIR / "developer_setup_predictions.json", developer_setup_payload)

report = [
    "# CodeBERT Joint Architecture Challenge V1",
    "",
    f"- Model: `{MODEL_NAME}` at `{CODEBERT_REVISION_SHA}`",
    f"- Natural validation Macro-F1: **{metrics['macro_f1']:.4f}**",
    f"- Frozen hybrid Macro-F1: **{FROZEN_BENCHMARK['macro_f1']:.4f}**",
    f"- Delta Macro-F1: **{metrics['delta_vs_frozen_hybrid']['macro_f1']:+.4f}**",
    f"- Balanced accuracy: **{metrics['balanced_accuracy']:.4f}**",
    f"- Delta balanced accuracy: **{metrics['delta_vs_frozen_hybrid']['balanced_accuracy']:+.4f}**",
    f"- developer_setup correct: **{developer_setup_payload['correct']} / {developer_setup_payload['support']}**",
    f"- API false positives: **{api_false_positive_counts['total_api_reference_false_positives']}**",
    "- Confirmation accessed: **no**",
    "- Controlled/synthetic data used: **no**",
]
(OUTPUT_DIR / "RESULTS.md").write_text("\\n".join(report) + "\\n", encoding="utf-8")
print("Wrote outputs to", OUTPUT_DIR)"""
    )
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write_notebook(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(make_notebook(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(args: argparse.Namespace) -> dict[str, Any]:
    for path in (args.old_train, args.old_validation, args.expansion_train):
        reject_confirmation_path(path)
    old_train_rows = read_jsonl(args.old_train)
    old_validation_rows = read_jsonl(args.old_validation)
    expansion_train_rows = read_jsonl(args.expansion_train)

    train = select_old_train(old_train_rows) + select_expansion_train(expansion_train_rows)
    validation = select_validation(old_validation_rows)
    audit = audit_export_rows(train, validation)
    if audit["errors"]:
        raise ValueError("Architecture challenge export audit failed: " + "; ".join(audit["errors"][:20]))

    expected_train_counts = {"api_reference": 412, "configuration": 277, "developer_setup": 88, "model_contract": 261}
    expected_validation_counts = {"api_reference": 85, "configuration": 154, "developer_setup": 19, "model_contract": 64}
    train_counts = distribution(train)["category_counts"]
    validation_counts = distribution(validation)["category_counts"]
    if train_counts != expected_train_counts:
        raise ValueError(f"Unexpected training support: {train_counts}")
    if validation_counts != expected_validation_counts:
        raise ValueError(f"Unexpected validation support: {validation_counts}")

    train_path = args.export_dir / "natural_train_primary_four.jsonl"
    validation_path = args.export_dir / "natural_validation_primary_four.jsonl"
    write_jsonl(train_path, train)
    write_jsonl(validation_path, validation)

    manifest = {
        "schema": "category_architecture_challenge_v1_export",
        "created_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "purpose": "bounded CodeBERT joint classifier architecture challenge",
        "labels": LABELS,
        "seed": SEED,
        "frozen_benchmark": FROZEN_BENCHMARK,
        "train": distribution(train),
        "validation": distribution(validation),
        "audit": audit,
        "safe_export_fields": SAFE_EXPORT_FIELDS,
        "forbidden_export_fields": sorted(FORBIDDEN_EXPORT_FIELDS),
        "model_input_policy": {
            "code_side": ["language", "code_changed_files", "code_diff_excerpt"],
            "docs_side": ["docs_before_excerpt"],
            "repository": "grouping/audit only, never tokenizer input",
        },
        "source_hashes": {
            str(args.old_train): sha256_file(args.old_train),
            str(args.old_validation): sha256_file(args.old_validation),
            str(args.expansion_train): sha256_file(args.expansion_train),
        },
        "artifacts": {
            "natural_train_primary_four.jsonl": {
                "path": str(train_path),
                "sha256": sha256_file(train_path),
                "bytes": train_path.stat().st_size,
            },
            "natural_validation_primary_four.jsonl": {
                "path": str(validation_path),
                "sha256": sha256_file(validation_path),
                "bytes": validation_path.stat().st_size,
            },
        },
        "colab_notebook": str(args.notebook),
        "expected_output_dir": str(args.experiment_dir),
        "confirmation_accessed": False,
        "controlled_or_synthetic_rows_used": False,
        "refresh_validation_used_for_training": False,
    }
    write_json(args.export_dir / "export_manifest.json", manifest)
    write_notebook(args.notebook)
    report = [
        "# Category Architecture Challenge V1 Export",
        "",
        "Prepared artifacts for the CodeBERT joint cross-encoder experiment. No local fine-tuning was run.",
        "",
        f"- Train rows: **{len(train)}** `{train_counts}`",
        f"- Validation rows: **{len(validation)}** `{validation_counts}`",
        f"- Validation case hash: `{audit['validation_case_ids_sha256']}`",
        f"- Train/validation repository overlap: **{len(audit['train_validation_repository_overlap'])}**",
        f"- Train artifact size: **{train_path.stat().st_size:,} bytes**",
        f"- Validation artifact size: **{validation_path.stat().st_size:,} bytes**",
        "- Confirmation accessed: **no**",
        "- Controlled/synthetic rows used: **no**",
        "- Refresh validation used for training: **no**",
    ]
    (args.export_dir / "EXPORT_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old-train", type=Path, default=Path("experiments/consolidated_enriched_training_v2/gold/train.jsonl"))
    parser.add_argument("--old-validation", type=Path, default=Path("experiments/consolidated_enriched_training_v2/gold/validation.jsonl"))
    parser.add_argument(
        "--expansion-train",
        type=Path,
        default=Path("data/final_v2/natural_diversity_expansion_v1/human_review/finalized/natural_expansion_train_gold.jsonl"),
    )
    parser.add_argument("--export-dir", type=Path, default=Path("data/final_v2/architecture_challenge_v1"))
    parser.add_argument("--notebook", type=Path, default=Path("notebooks/category_codebert_architecture_challenge_v1.ipynb"))
    parser.add_argument("--experiment-dir", type=Path, default=Path("experiments/category_architecture_challenge_v1/codebert_joint"))
    args = parser.parse_args()
    manifest = run(args)
    print(json.dumps({
        "status": "ok",
        "train": manifest["train"],
        "validation": manifest["validation"],
        "notebook": manifest["colab_notebook"],
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
