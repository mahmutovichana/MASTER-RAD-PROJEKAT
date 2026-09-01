"""Prepare the bounded Stage-2 ModernBERT architecture challenge notebook.

This script does not train a model. It validates the frozen Architecture
Challenge V1 natural export and writes the Colab notebook plus lightweight
methodology notes for the ModernBERT long-context joint classifier experiment.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LABELS = ["api_reference", "configuration", "developer_setup", "model_contract"]
LABEL_SET = set(LABELS)
SEED = 42
MODEL_NAME = "answerdotai/ModernBERT-base"

EXPORT_DIR = ROOT / "data" / "final_v2" / "architecture_challenge_v1"
TRAIN_PATH = EXPORT_DIR / "natural_train_primary_four.jsonl"
VALIDATION_PATH = EXPORT_DIR / "natural_validation_primary_four.jsonl"
MANIFEST_PATH = EXPORT_DIR / "export_manifest.json"

NOTEBOOK_PATH = ROOT / "notebooks" / "category_modernbert_architecture_challenge_v2.ipynb"
EXPERIMENT_DIR = ROOT / "experiments" / "category_architecture_challenge_v2"
OUTPUT_DIR = EXPERIMENT_DIR / "modernbert_long_context"

FROZEN_VALIDATION_CASE_IDS_SHA256 = "aac3384de6d482abefb4201091bf828d6d8c1c91c1ddbdad40a4ec7273051e3e"
FROZEN_TRAIN_SHA256 = "9dc1136f1cf695eb69c70b763ad051898aa5fae351fcf028eed97116c8891f99"
FROZEN_VALIDATION_SHA256 = "1865d6803ac7e57cf38e315789732ee6592ddb6890373afa7fd1f988eb45ba2e"
FROZEN_TRAIN_COUNT = 1038
FROZEN_VALIDATION_COUNT = 322
FROZEN_TRAIN_CATEGORY_COUNTS = {
    "api_reference": 412,
    "configuration": 277,
    "developer_setup": 88,
    "model_contract": 261,
}
FROZEN_VALIDATION_CATEGORY_COUNTS = {
    "api_reference": 85,
    "configuration": 154,
    "developer_setup": 19,
    "model_contract": 64,
}
SAFE_EXPORT_FIELDS = {
    "case_id",
    "repository",
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
    "gold_doc_category",
    "partition",
}
FORBIDDEN_EXPORT_FIELDS = {
    "controlled_design_label",
    "controlled_design_supervision",
    "docs_after",
    "docs_after_excerpt",
    "docs_diff",
    "docs_diff_excerpt",
    "human_label_notes",
    "label_source",
    "provenance_tier",
    "repository_full_name_for_model",
    "suggested_doc_category",
    "suggested_docs_update_required",
    "suggested_notes",
    "supervision_source",
}

FROZEN_BASELINES = {
    "tfidf_category_v8": {
        "model": "TF-IDF Category V8",
        "macro_f1": 0.3817290905323643,
        "balanced_accuracy": 0.41814481474407944,
        "developer_setup_f1": 0.0,
    },
    "hybrid_natural_only": {
        "model": "hybrid__natural_only__multinomial_logreg__natural_diversity_expansion_v1",
        "macro_f1": 0.45628987455472775,
        "balanced_accuracy": 0.478023538961039,
        "developer_setup_f1": 0.0,
        "per_class_f1": {
            "api_reference": 0.5340314136125655,
            "configuration": 0.6824324324324325,
            "developer_setup": 0.0,
            "model_contract": 0.6086956521739131,
        },
    },
    "codebert_joint_512": {
        "model": "microsoft/codebert-base joint classifier",
        "macro_f1": 0.2105,
        "balanced_accuracy": 0.2702,
        "developer_setup_f1": 0.0,
        "developer_setup_correct": "0/19",
        "api_false_positives": 143,
    },
}

CODEBERT_V1_TRUNCATION_REFERENCE = {
    "train": {
        "average_original_code_tokens": 2701,
        "average_original_diff_tokens": 2591,
        "average_original_docs_tokens": 2191,
        "average_retained_code_tokens": 286,
        "average_retained_diff_tokens": 236,
        "average_retained_docs_tokens": 212,
        "percent_diff_tokens_retained": 9.10,
        "percent_rows_with_any_truncation": 99.9,
    },
    "validation": {
        "average_original_code_tokens": 2961,
        "average_original_diff_tokens": 2824,
        "average_original_docs_tokens": 1836,
        "average_retained_diff_tokens": 232,
        "percent_diff_tokens_retained": 8.23,
        "percent_rows_with_any_truncation": 100.0,
    },
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
            reject_forbidden_row(row, source=f"{path}:{line_number}")
            rows.append(row)
    return rows


def list_value(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        text = value.strip()
        if text.startswith("["):
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                parsed = None
            if isinstance(parsed, list):
                return [str(item) for item in parsed]
        return [text] if text else []
    return []


def sanitize_repository_identity(text: str, repository: str) -> str:
    repo = repository.strip().strip("/")
    sanitized = str(text)
    if not repo or "/" not in repo:
        return sanitized
    owner, name = repo.split("/", 1)
    patterns = [
        re.escape(repo),
        re.escape(f"github.com/{repo}"),
        re.escape(f"https://github.com/{repo}"),
        re.escape(f"http://github.com/{repo}"),
        re.escape(f"git@github.com:{repo}"),
    ]
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
    if partition in {"refresh_validation", "development_validation"} and source == "training":
        raise ValueError(f"{source}:{case_id}: validation row is forbidden for training")
    if row.get("controlled_design_supervision") is True:
        raise ValueError(f"{source}:{case_id}: controlled row is forbidden")
    for field in ("label_source", "supervision_source", "provenance_tier"):
        if "controlled" in str(row.get(field) or "").lower() or "synthetic" in str(row.get(field) or "").lower():
            raise ValueError(f"{source}:{case_id}: controlled/synthetic provenance is forbidden")


def validate_training_row(row: dict[str, Any]) -> None:
    reject_forbidden_row(row, source="training")
    partition = str(row.get("partition") or "")
    if partition != "development_train":
        raise ValueError(f"training:{row.get('case_id')}: only development_train rows may be used for training")


def validate_export_row(row: dict[str, Any], *, source: str) -> None:
    reject_forbidden_row(row, source=source)
    extra = set(row) - SAFE_EXPORT_FIELDS
    forbidden = set(row) & FORBIDDEN_EXPORT_FIELDS
    if extra:
        raise ValueError(f"{source}:{row.get('case_id')}: unexpected export fields: {sorted(extra)}")
    if forbidden:
        raise ValueError(f"{source}:{row.get('case_id')}: forbidden export fields: {sorted(forbidden)}")
    if row.get("gold_doc_category") not in LABEL_SET:
        raise ValueError(f"{source}:{row.get('case_id')}: invalid category {row.get('gold_doc_category')!r}")


def build_prefix_text(row: dict[str, Any]) -> str:
    repo = str(row.get("repository") or "")
    text = "\n".join(
        [
            f"language: {str(row.get('language') or 'unknown').lower()}",
            "changed files:",
            "\n".join(list_value(row.get("code_changed_files"))),
            "code change:",
        ]
    )
    return sanitize_repository_identity(text, repo)


def build_diff_text(row: dict[str, Any]) -> str:
    return sanitize_repository_identity(str(row.get("code_diff_excerpt") or ""), str(row.get("repository") or ""))


def build_code_text(row: dict[str, Any]) -> str:
    return build_prefix_text(row) + "\n" + build_diff_text(row)


def build_docs_text(row: dict[str, Any]) -> str:
    return sanitize_repository_identity(str(row.get("docs_before_excerpt") or ""), str(row.get("repository") or ""))


def head_tail(ids: list[int], budget: int) -> list[int]:
    if budget <= 0:
        return []
    if len(ids) <= budget:
        return list(ids)
    head = max(1, budget // 2)
    tail = budget - head
    return list(ids[:head]) + list(ids[-tail:])


def choose_max_length(total_gpu_memory_gb: float) -> tuple[int, str]:
    if total_gpu_memory_gb >= 35:
        return 4096, "gpu_memory_ge_35gb"
    if total_gpu_memory_gb >= 20:
        return 3072, "gpu_memory_ge_20gb"
    return 2048, "gpu_memory_lt_20gb"


def build_balanced_pair_inputs(
    tokenizer: Any,
    row: dict[str, Any],
    *,
    max_length: int = 2048,
    code_ratio: float = 0.58,
) -> tuple[dict[str, list[int]], dict[str, Any]]:
    """Build one unpadded joint code+docs example with deterministic retention."""
    prefix_text = build_prefix_text(row)
    diff_text = build_diff_text(row)
    docs_text = build_docs_text(row)

    prefix_ids = tokenizer.encode(prefix_text, add_special_tokens=False)
    diff_ids = tokenizer.encode(diff_text, add_special_tokens=False)
    docs_ids = tokenizer.encode(docs_text, add_special_tokens=False)

    special_tokens = len(tokenizer.build_inputs_with_special_tokens([], []))
    available = max_length - special_tokens
    if available <= 0:
        raise ValueError(f"max_length={max_length} leaves no room after special tokens")

    code_budget = max(8, int(available * code_ratio))
    docs_budget = max(1, available - code_budget)
    if len(docs_ids) > 0 and docs_budget < 1:
        docs_budget = 1
        code_budget = available - docs_budget

    prefix_cap = max(1, int(code_budget * 0.23))
    if diff_ids:
        prefix_budget = min(len(prefix_ids), prefix_cap)
        diff_budget = max(1, code_budget - prefix_budget)
    else:
        prefix_budget = min(len(prefix_ids), code_budget)
        diff_budget = 0

    kept_prefix = head_tail(prefix_ids, prefix_budget)
    kept_diff = head_tail(diff_ids, diff_budget)
    kept_docs = head_tail(docs_ids, docs_budget)
    kept_code = kept_prefix + kept_diff

    input_ids = tokenizer.build_inputs_with_special_tokens(kept_code, kept_docs)
    if len(input_ids) > max_length:
        overflow = len(input_ids) - max_length
        if len(kept_docs) > overflow and len(docs_ids) > 0:
            kept_docs = head_tail(kept_docs, len(kept_docs) - overflow)
        elif len(kept_diff) > overflow and len(diff_ids) > 0:
            kept_diff = head_tail(kept_diff, len(kept_diff) - overflow)
        else:
            raise AssertionError(f"Tokenizer pair construction produced {len(input_ids)} tokens")
        kept_code = kept_prefix + kept_diff
        input_ids = tokenizer.build_inputs_with_special_tokens(kept_code, kept_docs)
    if len(input_ids) > max_length:
        raise AssertionError(f"Tokenizer pair construction produced {len(input_ids)} tokens")

    stats = {
        "original_code_tokens": len(prefix_ids) + len(diff_ids),
        "original_prefix_tokens": len(prefix_ids),
        "original_diff_tokens": len(diff_ids),
        "original_docs_tokens": len(docs_ids),
        "retained_code_tokens": len(kept_code),
        "retained_prefix_tokens": len(kept_prefix),
        "retained_diff_tokens": len(kept_diff),
        "retained_docs_tokens": len(kept_docs),
        "input_tokens_with_specials": len(input_ids),
        "code_truncated": len(kept_code) < len(prefix_ids) + len(diff_ids),
        "diff_truncated": len(kept_diff) < len(diff_ids),
        "docs_truncated": len(kept_docs) < len(docs_ids),
        "diff_became_empty": bool(diff_ids) and not bool(kept_diff),
        "docs_became_empty": bool(docs_ids) and not bool(kept_docs),
    }
    if stats["diff_became_empty"]:
        raise AssertionError("non-empty code_diff_excerpt retained zero tokens")
    if stats["docs_became_empty"]:
        raise AssertionError("non-empty docs_before_excerpt retained zero tokens")
    return {"input_ids": input_ids, "attention_mask": [1] * len(input_ids)}, stats


def summarize_truncation(rows: list[dict[str, Any]], tokenizer: Any, *, max_length: int) -> dict[str, Any]:
    per_row = [build_balanced_pair_inputs(tokenizer, row, max_length=max_length)[1] for row in rows]

    def avg(key: str) -> float:
        return sum(float(item[key]) for item in per_row) / len(per_row) if per_row else 0.0

    original_code_total = sum(item["original_code_tokens"] for item in per_row)
    original_diff_total = sum(item["original_diff_tokens"] for item in per_row)
    original_docs_total = sum(item["original_docs_tokens"] for item in per_row)
    retained_code_total = sum(item["retained_code_tokens"] for item in per_row)
    retained_diff_total = sum(item["retained_diff_tokens"] for item in per_row)
    retained_docs_total = sum(item["retained_docs_tokens"] for item in per_row)
    rows_with_nonempty_original_diff = sum(1 for item in per_row if item["original_diff_tokens"] > 0)
    rows_with_nonempty_original_docs = sum(1 for item in per_row if item["original_docs_tokens"] > 0)
    rows_with_zero_retained_diff = sum(
        1 for item in per_row if item["original_diff_tokens"] > 0 and item["retained_diff_tokens"] == 0
    )
    rows_with_zero_retained_docs = sum(
        1 for item in per_row if item["original_docs_tokens"] > 0 and item["retained_docs_tokens"] == 0
    )
    rows_with_any_truncation = sum(
        1 for item in per_row if item["code_truncated"] or item["docs_truncated"]
    )
    rows_code_fully_preserved = sum(
        1 for item in per_row if item["retained_code_tokens"] == item["original_code_tokens"]
    )
    rows_docs_fully_preserved = sum(
        1 for item in per_row if item["retained_docs_tokens"] == item["original_docs_tokens"]
    )
    rows_both_fully_preserved = sum(
        1
        for item in per_row
        if item["retained_code_tokens"] == item["original_code_tokens"]
        and item["retained_docs_tokens"] == item["original_docs_tokens"]
    )
    summary = {
        "rows": len(rows),
        "MAX_LENGTH": max_length,
        "average_original_code_tokens": avg("original_code_tokens"),
        "average_original_prefix_tokens": avg("original_prefix_tokens"),
        "average_original_diff_tokens": avg("original_diff_tokens"),
        "average_original_docs_tokens": avg("original_docs_tokens"),
        "average_retained_code_tokens": avg("retained_code_tokens"),
        "average_retained_prefix_tokens": avg("retained_prefix_tokens"),
        "average_retained_diff_tokens": avg("retained_diff_tokens"),
        "average_retained_docs_tokens": avg("retained_docs_tokens"),
        "percent_code_tokens_retained": 100.0 * retained_code_total / original_code_total if original_code_total else 100.0,
        "percent_diff_tokens_retained": 100.0 * retained_diff_total / original_diff_total if original_diff_total else 100.0,
        "percent_docs_tokens_retained": 100.0 * retained_docs_total / original_docs_total if original_docs_total else 100.0,
        "rows_with_nonempty_original_diff": rows_with_nonempty_original_diff,
        "rows_with_zero_retained_diff": rows_with_zero_retained_diff,
        "rows_with_nonempty_original_docs": rows_with_nonempty_original_docs,
        "rows_with_zero_retained_docs": rows_with_zero_retained_docs,
        "percent_rows_with_any_truncation": 100.0 * rows_with_any_truncation / len(rows) if rows else 0.0,
        "percent_rows_code_fully_preserved": 100.0 * rows_code_fully_preserved / len(rows) if rows else 0.0,
        "percent_rows_docs_fully_preserved": 100.0 * rows_docs_fully_preserved / len(rows) if rows else 0.0,
        "percent_rows_both_sides_fully_preserved": 100.0 * rows_both_fully_preserved / len(rows) if rows else 0.0,
    }
    if rows_with_zero_retained_diff != 0:
        raise AssertionError("rows_with_zero_retained_diff must be zero")
    if rows_with_zero_retained_docs != 0:
        raise AssertionError("rows_with_zero_retained_docs must be zero")
    return summary


def load_manifest() -> dict[str, Any]:
    reject_confirmation_path(MANIFEST_PATH)
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def validate_v1_exports() -> dict[str, Any]:
    manifest = load_manifest()
    train = read_jsonl(TRAIN_PATH)
    validation = read_jsonl(VALIDATION_PATH)
    for row in train:
        validate_export_row(row, source="train")
        validate_training_row(row)
    for row in validation:
        validate_export_row(row, source="validation")
        if row.get("partition") != "development_validation":
            raise ValueError(f"validation:{row.get('case_id')}: expected development_validation")

    train_repos = {row["repository"] for row in train}
    validation_repos = {row["repository"] for row in validation}
    validation_hash = stable_json_hash([row["case_id"] for row in validation])
    audit = {
        "train_rows": len(train),
        "validation_rows": len(validation),
        "train_category_counts": dict(Counter(row["gold_doc_category"] for row in train)),
        "validation_category_counts": dict(Counter(row["gold_doc_category"] for row in validation)),
        "train_validation_repository_overlap": sorted(train_repos & validation_repos),
        "train_sha256": sha256_file(TRAIN_PATH),
        "validation_sha256": sha256_file(VALIDATION_PATH),
        "validation_case_ids_sha256": validation_hash,
        "manifest_validation_case_ids_sha256": manifest["audit"]["validation_case_ids_sha256"],
        "manifest": manifest,
    }
    if audit["train_rows"] != FROZEN_TRAIN_COUNT:
        raise AssertionError(audit["train_rows"])
    if audit["validation_rows"] != FROZEN_VALIDATION_COUNT:
        raise AssertionError(audit["validation_rows"])
    if audit["train_category_counts"] != FROZEN_TRAIN_CATEGORY_COUNTS:
        raise AssertionError(audit["train_category_counts"])
    if audit["validation_category_counts"] != FROZEN_VALIDATION_CATEGORY_COUNTS:
        raise AssertionError(audit["validation_category_counts"])
    if audit["train_validation_repository_overlap"]:
        raise AssertionError(audit["train_validation_repository_overlap"])
    if audit["train_sha256"] != FROZEN_TRAIN_SHA256:
        raise AssertionError(audit["train_sha256"])
    if audit["validation_sha256"] != FROZEN_VALIDATION_SHA256:
        raise AssertionError(audit["validation_sha256"])
    if validation_hash != FROZEN_VALIDATION_CASE_IDS_SHA256:
        raise AssertionError(validation_hash)
    if validation_hash != manifest["audit"]["validation_case_ids_sha256"]:
        raise AssertionError("manifest validation hash mismatch")
    if manifest["audit"]["confirmation_accessed"] is not False:
        raise AssertionError("confirmation access must be false")
    if manifest["controlled_or_synthetic_rows_used"] is not False:
        raise AssertionError("controlled/synthetic rows must not be used")
    if manifest["refresh_validation_used_for_training"] is not False:
        raise AssertionError("refresh validation must not be used for training")
    return audit


def notebook_cell(cell_type: str, source: str) -> dict[str, Any]:
    return {
        "cell_type": cell_type,
        "metadata": {},
        "source": [line + "\n" for line in source.strip("\n").splitlines()],
        **({"outputs": [], "execution_count": None} if cell_type == "code" else {}),
    }


def make_notebook() -> dict[str, Any]:
    """Return the Colab notebook JSON as a Python object."""
    title = """
# Stage-2 Architecture Challenge V2: ModernBERT long-context joint classifier

This notebook runs one bounded experiment: `answerdotai/ModernBERT-base` jointly classifies code change + pre-change documentation using the frozen Architecture Challenge V1 natural train/validation export. It does not acquire data, does not use controlled/synthetic rows, does not access confirmation, and does not rerun CodeBERT.
"""
    deps = """
# Python 3.13 compatible Colab dependency stack.
# Keep Colab's CUDA-enabled torch; do not reinstall/downgrade torch here.
!python -m pip install -q \\
  "tokenizers==0.22.0" \\
  "transformers==4.56.2" \\
  "accelerate==1.10.1" \\
  "huggingface_hub==0.34.4" \\
  "safetensors==0.6.2" \\
  "scikit-learn==1.7.2" \\
  "matplotlib==3.10.6"
"""
    imports = """
from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import random
import zipfile
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import sklearn
import torch
import tokenizers
import transformers
from accelerate import __version__ as accelerate_version
from huggingface_hub import HfApi, __version__ as hf_hub_version
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import GroupShuffleSplit
from torch.utils.data import Dataset
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
    set_seed,
)

print("Python:", sys.version)
print("torch:", torch.__version__)
print("CUDA availability:", torch.cuda.is_available())
print("CUDA device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "NONE")
print("transformers:", transformers.__version__)
print("tokenizers:", tokenizers.__version__)
print("accelerate:", accelerate_version)
print("huggingface_hub:", hf_hub_version)
assert torch.cuda.is_available(), "CUDA GPU is required; do not run this long-context experiment on CPU."
"""
    data_import = """
REQUIRED_EXPORT_FILES = [
    "natural_train_primary_four.jsonl",
    "natural_validation_primary_four.jsonl",
    "export_manifest.json",
]


def has_frozen_v1_export(root):
    export_dir = Path(root) / "data" / "final_v2" / "architecture_challenge_v1"
    return all((export_dir / name).exists() for name in REQUIRED_EXPORT_FILES)


def locate_frozen_v1_root():
    candidates = [
        Path.cwd(),
        Path("/content/MASTER-RAD-PROJEKAT"),
        Path("/content/MASTER RAD PROJEKAT"),
        Path("/content/drive/MyDrive/MASTER-RAD-PROJEKAT"),
        Path("/content/drive/MyDrive/MASTER RAD PROJEKAT"),
    ]
    for candidate in candidates:
        if has_frozen_v1_export(candidate):
            return candidate
    for candidate in Path("/content").glob("**/export_manifest.json"):
        possible_root = candidate.parent.parent.parent.parent
        if has_frozen_v1_export(possible_root):
            return possible_root
    return None


ROOT = locate_frozen_v1_root()
if ROOT is None:
    print("Frozen V1 export nije pronađen u Colab runtime-u.")
    print("Uploaduj ili ZIP koji sadrži data/final_v2/architecture_challenge_v1/, ili direktno ova 3 fajla:")
    for name in REQUIRED_EXPORT_FILES:
        print("-", name)
    from google.colab import files

    uploaded = files.upload()
    upload_dir = Path("/content/MASTER-RAD-PROJEKAT")
    upload_dir.mkdir(parents=True, exist_ok=True)
    direct_export_dir = upload_dir / "data" / "final_v2" / "architecture_challenge_v1"
    direct_export_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in uploaded.items():
        target_name = Path(name).name
        if target_name.lower().endswith(".zip"):
            zip_path = upload_dir / target_name
            zip_path.write_bytes(payload)
            with zipfile.ZipFile(zip_path) as archive:
                archive.extractall(upload_dir)
        elif target_name in REQUIRED_EXPORT_FILES:
            (direct_export_dir / target_name).write_bytes(payload)
        else:
            print(f"Preskačem nepoznati upload fajl: {name}")
    ROOT = locate_frozen_v1_root()

assert ROOT is not None and has_frozen_v1_export(ROOT), (
    "Nedostaju frozen V1 export fajlovi. Potrebni su: "
    "natural_train_primary_four.jsonl, natural_validation_primary_four.jsonl, export_manifest.json"
)
print("Using repository/data root:", ROOT)
"""
    config = f"""
EXPORT_DIR = ROOT / "data" / "final_v2" / "architecture_challenge_v1"
TRAIN_PATH = EXPORT_DIR / "natural_train_primary_four.jsonl"
VALIDATION_PATH = EXPORT_DIR / "natural_validation_primary_four.jsonl"
MANIFEST_PATH = EXPORT_DIR / "export_manifest.json"
MANIFEST_JSON = MANIFEST_PATH  # Backward-compatible alias for manual Colab cells.
OUTPUT_DIR = ROOT / "experiments" / "category_architecture_challenge_v2" / "modernbert_long_context"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "{MODEL_NAME}"
LABELS = {LABELS!r}
LABEL_TO_ID = {{label: idx for idx, label in enumerate(LABELS)}}
ID_TO_LABEL = {{idx: label for label, idx in LABEL_TO_ID.items()}}
SEED = 42
LEARNING_RATE = 2e-5
WEIGHT_DECAY = 0.01
MAX_EPOCHS = 5
TRAIN_BATCH_SIZE = 1
EVAL_BATCH_SIZE = 2
GRADIENT_ACCUMULATION_STEPS = 8

FROZEN_VALIDATION_CASE_IDS_SHA256 = "{FROZEN_VALIDATION_CASE_IDS_SHA256}"
FROZEN_BASELINES = {json.dumps(FROZEN_BASELINES, indent=2)}
CODEBERT_V1_TRUNCATION_REFERENCE = {json.dumps(CODEBERT_V1_TRUNCATION_REFERENCE, indent=2)}

set_seed(SEED)
random.seed(SEED)
np.random.seed(SEED)
"""
    helpers = r'''
def stable_json_hash(value):
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def reject_confirmation_path(path):
    text = str(path).replace("\\", "/").lower()
    if "confirmation" in text:
        raise ValueError(f"Confirmation path is forbidden: {path}")


def read_jsonl(path):
    reject_confirmation_path(path)
    rows = []
    with open(path, encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("partition") == "confirmation":
                raise ValueError(f"{path}:{line_number}: confirmation row is forbidden")
            rows.append(row)
    return rows


def list_value(value):
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


def sanitize_repository_identity(text, repository):
    repo = str(repository or "").strip().strip("/")
    sanitized = str(text)
    if not repo or "/" not in repo:
        return sanitized
    owner, name = repo.split("/", 1)
    patterns = [
        re.escape(repo),
        re.escape(f"github.com/{repo}"),
        re.escape(f"https://github.com/{repo}"),
        re.escape(f"http://github.com/{repo}"),
        re.escape(f"git@github.com:{repo}"),
    ]
    for pattern in patterns:
        sanitized = re.sub(pattern, "[REPOSITORY]", sanitized, flags=re.IGNORECASE)
    return re.sub(
        rf"github\.com/{re.escape(owner)}/{re.escape(name)}(?:\.git)?",
        "[REPOSITORY]",
        sanitized,
        flags=re.IGNORECASE,
    )


def build_prefix_text(row):
    text = "\n".join([
        f"language: {str(row.get('language') or 'unknown').lower()}",
        "changed files:",
        "\n".join(list_value(row.get("code_changed_files"))),
        "code change:",
    ])
    return sanitize_repository_identity(text, row.get("repository") or "")


def build_diff_text(row):
    return sanitize_repository_identity(row.get("code_diff_excerpt") or "", row.get("repository") or "")


def build_docs_text(row):
    return sanitize_repository_identity(row.get("docs_before_excerpt") or "", row.get("repository") or "")


def head_tail(ids, budget):
    if budget <= 0:
        return []
    if len(ids) <= budget:
        return list(ids)
    head = max(1, budget // 2)
    tail = budget - head
    return list(ids[:head]) + list(ids[-tail:])


def choose_max_length(total_gpu_memory_gb):
    if total_gpu_memory_gb >= 35:
        return 4096, "gpu_memory_ge_35gb"
    if total_gpu_memory_gb >= 20:
        return 3072, "gpu_memory_ge_20gb"
    return 2048, "gpu_memory_lt_20gb"


def build_balanced_pair_inputs(tokenizer, row, max_length, code_ratio=0.58):
    prefix_ids = tokenizer.encode(build_prefix_text(row), add_special_tokens=False)
    diff_ids = tokenizer.encode(build_diff_text(row), add_special_tokens=False)
    docs_ids = tokenizer.encode(build_docs_text(row), add_special_tokens=False)

    special_tokens = len(tokenizer.build_inputs_with_special_tokens([], []))
    available = max_length - special_tokens
    assert available > 0
    code_budget = max(8, int(available * code_ratio))
    docs_budget = max(1, available - code_budget)

    prefix_cap = max(1, int(code_budget * 0.23))
    if diff_ids:
        prefix_budget = min(len(prefix_ids), prefix_cap)
        diff_budget = max(1, code_budget - prefix_budget)
    else:
        prefix_budget = min(len(prefix_ids), code_budget)
        diff_budget = 0

    kept_prefix = head_tail(prefix_ids, prefix_budget)
    kept_diff = head_tail(diff_ids, diff_budget)
    kept_docs = head_tail(docs_ids, docs_budget)
    kept_code = kept_prefix + kept_diff
    input_ids = tokenizer.build_inputs_with_special_tokens(kept_code, kept_docs)

    if len(input_ids) > max_length:
        overflow = len(input_ids) - max_length
        if len(kept_docs) > overflow and docs_ids:
            kept_docs = head_tail(kept_docs, len(kept_docs) - overflow)
        elif len(kept_diff) > overflow and diff_ids:
            kept_diff = head_tail(kept_diff, len(kept_diff) - overflow)
        else:
            raise AssertionError(f"sequence length {len(input_ids)} exceeds MAX_LENGTH={max_length}")
        kept_code = kept_prefix + kept_diff
        input_ids = tokenizer.build_inputs_with_special_tokens(kept_code, kept_docs)

    if len(input_ids) > max_length:
        raise AssertionError(f"sequence length {len(input_ids)} exceeds MAX_LENGTH={max_length}")
    if diff_ids and not kept_diff:
        raise AssertionError("non-empty diff retained zero tokens")
    if docs_ids and not kept_docs:
        raise AssertionError("non-empty docs retained zero tokens")

    stats = {
        "original_code_tokens": len(prefix_ids) + len(diff_ids),
        "original_prefix_tokens": len(prefix_ids),
        "original_diff_tokens": len(diff_ids),
        "original_docs_tokens": len(docs_ids),
        "retained_code_tokens": len(kept_code),
        "retained_prefix_tokens": len(kept_prefix),
        "retained_diff_tokens": len(kept_diff),
        "retained_docs_tokens": len(kept_docs),
        "input_tokens_with_specials": len(input_ids),
        "code_truncated": len(kept_code) < len(prefix_ids) + len(diff_ids),
        "docs_truncated": len(kept_docs) < len(docs_ids),
    }
    return {"input_ids": input_ids, "attention_mask": [1] * len(input_ids)}, stats


def summarize_truncation(rows, tokenizer, max_length):
    all_stats = [build_balanced_pair_inputs(tokenizer, row, max_length)[1] for row in rows]
    def avg(key):
        return float(np.mean([s[key] for s in all_stats])) if all_stats else 0.0
    sums = {key: sum(s[key] for s in all_stats) for key in [
        "original_code_tokens", "original_diff_tokens", "original_docs_tokens",
        "retained_code_tokens", "retained_diff_tokens", "retained_docs_tokens"
    ]}
    rows_with_nonempty_original_diff = sum(1 for s in all_stats if s["original_diff_tokens"] > 0)
    rows_with_nonempty_original_docs = sum(1 for s in all_stats if s["original_docs_tokens"] > 0)
    rows_with_zero_retained_diff = sum(1 for s in all_stats if s["original_diff_tokens"] > 0 and s["retained_diff_tokens"] == 0)
    rows_with_zero_retained_docs = sum(1 for s in all_stats if s["original_docs_tokens"] > 0 and s["retained_docs_tokens"] == 0)
    rows_with_any_truncation = sum(1 for s in all_stats if s["code_truncated"] or s["docs_truncated"])
    rows_code_fully_preserved = sum(1 for s in all_stats if s["retained_code_tokens"] == s["original_code_tokens"])
    rows_docs_fully_preserved = sum(1 for s in all_stats if s["retained_docs_tokens"] == s["original_docs_tokens"])
    rows_both_sides_fully_preserved = sum(1 for s in all_stats if s["retained_code_tokens"] == s["original_code_tokens"] and s["retained_docs_tokens"] == s["original_docs_tokens"])
    summary = {
        "rows": len(rows),
        "MAX_LENGTH": max_length,
        "average_original_code_tokens": avg("original_code_tokens"),
        "average_original_prefix_tokens": avg("original_prefix_tokens"),
        "average_original_diff_tokens": avg("original_diff_tokens"),
        "average_original_docs_tokens": avg("original_docs_tokens"),
        "average_retained_code_tokens": avg("retained_code_tokens"),
        "average_retained_prefix_tokens": avg("retained_prefix_tokens"),
        "average_retained_diff_tokens": avg("retained_diff_tokens"),
        "average_retained_docs_tokens": avg("retained_docs_tokens"),
        "percent_code_tokens_retained": 100.0 * sums["retained_code_tokens"] / sums["original_code_tokens"] if sums["original_code_tokens"] else 100.0,
        "percent_diff_tokens_retained": 100.0 * sums["retained_diff_tokens"] / sums["original_diff_tokens"] if sums["original_diff_tokens"] else 100.0,
        "percent_docs_tokens_retained": 100.0 * sums["retained_docs_tokens"] / sums["original_docs_tokens"] if sums["original_docs_tokens"] else 100.0,
        "rows_with_nonempty_original_diff": rows_with_nonempty_original_diff,
        "rows_with_zero_retained_diff": rows_with_zero_retained_diff,
        "rows_with_nonempty_original_docs": rows_with_nonempty_original_docs,
        "rows_with_zero_retained_docs": rows_with_zero_retained_docs,
        "percent_rows_with_any_truncation": 100.0 * rows_with_any_truncation / len(rows),
        "percent_rows_code_fully_preserved": 100.0 * rows_code_fully_preserved / len(rows),
        "percent_rows_docs_fully_preserved": 100.0 * rows_docs_fully_preserved / len(rows),
        "percent_rows_both_sides_fully_preserved": 100.0 * rows_both_sides_fully_preserved / len(rows),
    }
    assert summary["rows_with_zero_retained_diff"] == 0
    assert summary["rows_with_zero_retained_docs"] == 0
    return summary


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
'''
    load_audit = """
manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
train_rows = read_jsonl(TRAIN_PATH)
validation_rows = read_jsonl(VALIDATION_PATH)

assert len(train_rows) == 1038
assert len(validation_rows) == 322
assert Counter(r["gold_doc_category"] for r in train_rows) == {"api_reference": 412, "configuration": 277, "developer_setup": 88, "model_contract": 261}
assert Counter(r["gold_doc_category"] for r in validation_rows) == {"api_reference": 85, "configuration": 154, "developer_setup": 19, "model_contract": 64}
assert set(r["partition"] for r in train_rows) == {"development_train"}
assert set(r["partition"] for r in validation_rows) == {"development_validation"}
assert not ({r["repository"] for r in train_rows} & {r["repository"] for r in validation_rows})
assert sha256_file(TRAIN_PATH) == manifest["artifacts"]["natural_train_primary_four.jsonl"]["sha256"]
assert sha256_file(VALIDATION_PATH) == manifest["artifacts"]["natural_validation_primary_four.jsonl"]["sha256"]
validation_case_hash = stable_json_hash([r["case_id"] for r in validation_rows])
assert validation_case_hash == manifest["audit"]["validation_case_ids_sha256"] == FROZEN_VALIDATION_CASE_IDS_SHA256
assert manifest["audit"]["confirmation_accessed"] is False
assert manifest["controlled_or_synthetic_rows_used"] is False
assert manifest["refresh_validation_used_for_training"] is False
print("Frozen V1 export is valid; train/validation membership unchanged.")
"""
    tokenizer_gpu = """
api = HfApi()
model_info = api.model_info(MODEL_NAME)
MODEL_REVISION_SHA = model_info.sha
print("Resolved model revision:", MODEL_REVISION_SHA)

gpu_props = torch.cuda.get_device_properties(0)
total_gpu_memory_gb = gpu_props.total_memory / (1024 ** 3)
MAX_LENGTH, max_length_policy_branch = choose_max_length(total_gpu_memory_gb)
print({"gpu_memory_gb": total_gpu_memory_gb, "MAX_LENGTH": MAX_LENGTH, "policy_branch": max_length_policy_branch})

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, revision=MODEL_REVISION_SHA, trust_remote_code=True)
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token or tokenizer.sep_token or tokenizer.cls_token
assert tokenizer.pad_token_id is not None

sample_encoded, sample_stats = build_balanced_pair_inputs(tokenizer, train_rows[0], MAX_LENGTH)
assert len(sample_encoded["input_ids"]) <= MAX_LENGTH
assert len(sample_encoded["attention_mask"]) <= MAX_LENGTH
assert sample_stats["retained_code_tokens"] > 0
assert sample_stats["retained_docs_tokens"] > 0
if sample_stats["original_diff_tokens"] > 0:
    assert sample_stats["retained_diff_tokens"] > 0
print("Tokenizer smoke test passed:", sample_stats)
"""
    truncation = """
truncation_stats = {
    "train": summarize_truncation(train_rows, tokenizer, MAX_LENGTH),
    "validation": summarize_truncation(validation_rows, tokenizer, MAX_LENGTH),
    "codebert_v1_reference": CODEBERT_V1_TRUNCATION_REFERENCE,
}
assert truncation_stats["train"]["rows_with_zero_retained_diff"] == 0
assert truncation_stats["validation"]["rows_with_zero_retained_diff"] == 0
assert truncation_stats["train"]["rows_with_zero_retained_docs"] == 0
assert truncation_stats["validation"]["rows_with_zero_retained_docs"] == 0
write_json(OUTPUT_DIR / "truncation_report.json", truncation_stats)
print(json.dumps(truncation_stats, indent=2))
"""
    dataset_split = """
def choose_internal_split(rows):
    labels = np.array([LABEL_TO_ID[r["gold_doc_category"]] for r in rows])
    groups = np.array([r["repository"] for r in rows])
    indices = np.arange(len(rows))
    for split_seed in [42, 43, 44, 45, 46]:
        splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=split_seed)
        train_idx, eval_idx = next(splitter.split(indices, labels, groups))
        train_groups = set(groups[train_idx])
        eval_groups = set(groups[eval_idx])
        train_labels = set(labels[train_idx])
        eval_labels = set(labels[eval_idx])
        if not (train_groups & eval_groups) and train_labels == set(range(4)) and eval_labels == set(range(4)):
            return train_idx.tolist(), eval_idx.tolist(), split_seed
    raise RuntimeError("No predefined internal repository-grouped split satisfied all structural constraints.")


internal_train_idx, internal_eval_idx, internal_split_seed = choose_internal_split(train_rows)
internal_train_rows = [train_rows[i] for i in internal_train_idx]
internal_eval_rows = [train_rows[i] for i in internal_eval_idx]
print("internal_split_seed:", internal_split_seed)
print("internal train counts:", Counter(r["gold_doc_category"] for r in internal_train_rows))
print("internal eval counts:", Counter(r["gold_doc_category"] for r in internal_eval_rows))
assert not ({r["repository"] for r in internal_train_rows} & {r["repository"] for r in internal_eval_rows})


class DocGuardPairDataset(Dataset):
    def __init__(self, rows, tokenizer, max_length):
        self.rows = rows
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, idx):
        row = self.rows[idx]
        encoded, _ = build_balanced_pair_inputs(self.tokenizer, row, self.max_length)
        encoded["labels"] = LABEL_TO_ID[row["gold_doc_category"]]
        assert len(encoded["input_ids"]) <= self.max_length
        return encoded


train_dataset = DocGuardPairDataset(internal_train_rows, tokenizer, MAX_LENGTH)
eval_dataset = DocGuardPairDataset(internal_eval_rows, tokenizer, MAX_LENGTH)
validation_dataset = DocGuardPairDataset(validation_rows, tokenizer, MAX_LENGTH)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer, pad_to_multiple_of=8)
"""
    metrics_model = """
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "macro_f1": f1_score(labels, preds, average="macro", zero_division=0),
        "weighted_f1": f1_score(labels, preds, average="weighted", zero_division=0),
        "balanced_accuracy": balanced_accuracy_score(labels, preds),
    }


model_kwargs = {
    "revision": MODEL_REVISION_SHA,
    "num_labels": len(LABELS),
    "id2label": ID_TO_LABEL,
    "label2id": LABEL_TO_ID,
    "trust_remote_code": True,
}
try:
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        attn_implementation="sdpa",
        **model_kwargs,
    )
    attention_implementation = "sdpa"
except TypeError:
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, **model_kwargs)
    attention_implementation = "default"

if hasattr(model, "gradient_checkpointing_enable"):
    model.gradient_checkpointing_enable()
if hasattr(model.config, "use_cache"):
    model.config.use_cache = False
model.to("cuda")

training_args = TrainingArguments(
    output_dir=str(OUTPUT_DIR / "checkpoints"),
    seed=SEED,
    learning_rate=LEARNING_RATE,
    weight_decay=WEIGHT_DECAY,
    num_train_epochs=MAX_EPOCHS,
    per_device_train_batch_size=TRAIN_BATCH_SIZE,
    per_device_eval_batch_size=EVAL_BATCH_SIZE,
    gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
    fp16=True,
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="macro_f1",
    greater_is_better=True,
    save_total_limit=2,
    report_to=[],
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    processing_class=tokenizer,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2, early_stopping_threshold=0.0)],
)
"""
    oom_train = """
# One-batch OOM smoke test before full training. This does not inspect external validation.
model.train()
one_batch = data_collator([train_dataset[0]])
one_batch = {k: v.to("cuda") for k, v in one_batch.items()}
try:
    outputs = model(**one_batch)
    outputs.loss.backward()
    model.zero_grad(set_to_none=True)
    torch.cuda.empty_cache()
    print("Forward/backward smoke test passed.")
except torch.cuda.OutOfMemoryError as exc:
    torch.cuda.empty_cache()
    raise RuntimeError(
        "OOM at the predeclared T4-safe setting. Stop and report; do not reduce MAX_LENGTH to 512/1024."
    ) from exc

start_time = time.time()
train_result = trainer.train()
training_seconds = time.time() - start_time
trainer.save_state()
"""
    evaluation = """
def predict_rows(dataset, rows):
    pred_output = trainer.predict(dataset)
    logits = pred_output.predictions
    labels = pred_output.label_ids
    probs = torch.softmax(torch.tensor(logits), dim=-1).numpy()
    preds = np.argmax(probs, axis=-1)
    records = []
    for row, gold_id, pred_id, prob in zip(rows, labels, preds, probs):
        records.append({
            "case_id": row["case_id"],
            "gold": ID_TO_LABEL[int(gold_id)],
            "prediction": ID_TO_LABEL[int(pred_id)],
            "correct": bool(int(gold_id) == int(pred_id)),
            "probabilities": {label: float(prob[LABEL_TO_ID[label]]) for label in LABELS},
        })
    return records, labels, preds, probs


def metrics_from_predictions(labels, preds):
    labels = np.array(labels)
    preds = np.array(preds)
    report = classification_report(labels, preds, target_names=LABELS, output_dict=True, zero_division=0)
    cm = confusion_matrix(labels, preds, labels=list(range(len(LABELS))))
    cm_norm = cm.astype(float) / np.maximum(cm.sum(axis=1, keepdims=True), 1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "macro_f1": f1_score(labels, preds, average="macro", zero_division=0),
        "weighted_f1": f1_score(labels, preds, average="weighted", zero_division=0),
        "balanced_accuracy": balanced_accuracy_score(labels, preds),
        "per_class": {label: report[label] for label in LABELS},
        "confusion_matrix": cm.tolist(),
        "normalized_confusion_matrix": cm_norm.tolist(),
        "predicted_class_counts": dict(Counter(ID_TO_LABEL[int(p)] for p in preds)),
        "support": int(len(labels)),
    }


internal_train_records, internal_train_y, internal_train_pred, internal_train_probs = predict_rows(
    DocGuardPairDataset(internal_train_rows, tokenizer, MAX_LENGTH), internal_train_rows
)
internal_eval_records, internal_eval_y, internal_eval_pred, internal_eval_probs = predict_rows(eval_dataset, internal_eval_rows)
validation_records, validation_y, validation_pred, validation_probs = predict_rows(validation_dataset, validation_rows)

internal_train_metrics = metrics_from_predictions(internal_train_y, internal_train_pred)
internal_eval_metrics = metrics_from_predictions(internal_eval_y, internal_eval_pred)
metrics = metrics_from_predictions(validation_y, validation_pred)
write_json(OUTPUT_DIR / "internal_train_metrics.json", internal_train_metrics)
write_json(OUTPUT_DIR / "internal_eval_metrics.json", internal_eval_metrics)
write_json(OUTPUT_DIR / "metrics.json", metrics)
with open(OUTPUT_DIR / "validation_predictions.jsonl", "w", encoding="utf-8", newline="\n") as handle:
    for record in validation_records:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
print(json.dumps(metrics, indent=2))
"""
    diagnostics = """
dev_label_id = LABEL_TO_ID["developer_setup"]
developer_setup_rows = []
rank_counts = Counter()
for row, record, prob in zip(validation_rows, validation_records, validation_probs):
    sorted_ids = list(np.argsort(prob)[::-1])
    dev_rank = sorted_ids.index(dev_label_id) + 1
    if row["gold_doc_category"] == "developer_setup":
        rank_counts[dev_rank] += 1
        developer_setup_rows.append({
            "case_id": row["case_id"],
            "gold": record["gold"],
            "prediction": record["prediction"],
            "probabilities": record["probabilities"],
            "developer_setup_rank": dev_rank,
            "top_2": [ID_TO_LABEL[int(i)] for i in sorted_ids[:2]],
            "developer_setup_probability": float(prob[dev_label_id]),
        })

dev_true_probs = [float(prob[dev_label_id]) for row, prob in zip(validation_rows, validation_probs) if row["gold_doc_category"] == "developer_setup"]
dev_other_probs = [float(prob[dev_label_id]) for row, prob in zip(validation_rows, validation_probs) if row["gold_doc_category"] != "developer_setup"]
dev_report = metrics["per_class"]["developer_setup"]
developer_setup_diagnostics = {
    "rows": developer_setup_rows,
    "correct_out_of_19": sum(1 for r in developer_setup_rows if r["gold"] == r["prediction"]),
    "support": len(developer_setup_rows),
    "precision": dev_report["precision"],
    "recall": dev_report["recall"],
    "f1": dev_report["f1-score"],
    "rank_counts": {str(rank): rank_counts.get(rank, 0) for rank in [1, 2, 3, 4]},
    "mean_developer_setup_probability_for_true_developer_setup": float(np.mean(dev_true_probs)),
    "mean_developer_setup_probability_for_non_developer_setup": float(np.mean(dev_other_probs)),
}
write_json(OUTPUT_DIR / "developer_setup_predictions.json", developer_setup_diagnostics)

api_fp = {
    "configuration_to_api_reference": 0,
    "developer_setup_to_api_reference": 0,
    "model_contract_to_api_reference": 0,
}
for record in validation_records:
    if record["prediction"] == "api_reference" and record["gold"] != "api_reference":
        api_fp[f"{record['gold']}_to_api_reference"] += 1
api_fp["total_api_false_positives"] = sum(api_fp.values())
api_fp["codebert_v1_total_api_false_positives"] = FROZEN_BASELINES["codebert_joint_512"]["api_false_positives"]
api_fp["frozen_hybrid_reference_model"] = FROZEN_BASELINES["hybrid_natural_only"]["model"]
write_json(OUTPUT_DIR / "api_catch_all_diagnostics.json", api_fp)
"""
    figures_bootstrap = """
def plot_confusion(cm, labels, path, title):
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_title(title)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Gold")
    ax.set_xticks(range(len(labels)), labels, rotation=30, ha="right")
    ax.set_yticks(range(len(labels)), labels)
    for i in range(len(labels)):
        for j in range(len(labels)):
            value = cm[i][j]
            text = f"{value:.2f}" if isinstance(value, float) else str(value)
            ax.text(j, i, text, ha="center", va="center")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


plot_confusion(np.array(metrics["confusion_matrix"]), LABELS, OUTPUT_DIR / "confusion_matrix.png", "ModernBERT confusion matrix")
plot_confusion(np.array(metrics["normalized_confusion_matrix"]), LABELS, OUTPUT_DIR / "normalized_confusion_matrix.png", "ModernBERT row-normalized confusion matrix")

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(LABELS, [metrics["per_class"][label]["f1-score"] for label in LABELS])
ax.set_ylim(0, 1)
ax.set_title("ModernBERT per-class F1 on frozen development validation")
ax.tick_params(axis="x", rotation=25)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "per_class_f1.png", dpi=180)
plt.close(fig)

history = trainer.state.log_history
eval_epochs = [item.get("epoch") for item in history if "eval_macro_f1" in item]
eval_macro = [item.get("eval_macro_f1") for item in history if "eval_macro_f1" in item]
eval_bal = [item.get("eval_balanced_accuracy") for item in history if "eval_balanced_accuracy" in item]
train_loss_epochs = [item.get("epoch") for item in history if "loss" in item]
train_losses = [item.get("loss") for item in history if "loss" in item]
eval_loss_epochs = [item.get("epoch") for item in history if "eval_loss" in item]
eval_losses = [item.get("eval_loss") for item in history if "eval_loss" in item]

fig, ax = plt.subplots(figsize=(7, 4))
if eval_epochs:
    ax.plot(eval_epochs, eval_macro, marker="o", label="internal eval Macro-F1")
    ax.plot(eval_epochs, eval_bal, marker="o", label="internal eval balanced accuracy")
ax.set_ylim(0, 1)
ax.set_xlabel("Epoch")
ax.set_title("Training history: internal validation metrics")
ax.legend()
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "training_macro_f1.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 4))
if train_losses:
    ax.plot(train_loss_epochs, train_losses, marker="o", label="train loss")
if eval_losses:
    ax.plot(eval_loss_epochs, eval_losses, marker="o", label="internal eval loss")
ax.set_xlabel("Epoch")
ax.set_title("Training history: loss")
ax.legend()
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "training_loss.png", dpi=180)
plt.close(fig)


def load_hybrid_predictions_if_valid():
    candidates = [
        ROOT / "experiments" / "natural_diversity_refresh_category_v1" / "old_development_validation_predictions.jsonl",
    ]
    validation_ids = [r["case_id"] for r in validation_rows]
    validation_hash = stable_json_hash(validation_ids)
    for path in candidates:
        if not path.exists():
            continue
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if [r.get("case_id") for r in records] == validation_ids and validation_hash == FROZEN_VALIDATION_CASE_IDS_SHA256:
            return path, records
    return None, None


def paired_bootstrap(hybrid_records):
    rng = np.random.default_rng(SEED)
    gold = np.array([LABEL_TO_ID[r["gold"]] for r in validation_records])
    modern = np.array([LABEL_TO_ID[r["prediction"]] for r in validation_records])
    hybrid = np.array([LABEL_TO_ID[r["prediction"]] for r in hybrid_records])
    deltas = {"macro_f1": [], "balanced_accuracy": []}
    n = len(gold)
    for _ in range(2000):
        idx = rng.integers(0, n, size=n)
        deltas["macro_f1"].append(
            f1_score(gold[idx], modern[idx], average="macro", zero_division=0)
            - f1_score(gold[idx], hybrid[idx], average="macro", zero_division=0)
        )
        deltas["balanced_accuracy"].append(
            balanced_accuracy_score(gold[idx], modern[idx])
            - balanced_accuracy_score(gold[idx], hybrid[idx])
        )
    return {
        metric: {
            "mean_delta": float(np.mean(values)),
            "ci_2_5": float(np.percentile(values, 2.5)),
            "ci_97_5": float(np.percentile(values, 97.5)),
            "probability_delta_gt_zero": float(np.mean(np.array(values) > 0)),
        }
        for metric, values in deltas.items()
    } | {"iterations": 2000, "seed": SEED, "paired_same_validation_cases": True}


hybrid_path, hybrid_records = load_hybrid_predictions_if_valid()
bootstrap_result = None
if hybrid_records is not None:
    bootstrap_result = paired_bootstrap(hybrid_records)
    bootstrap_result["hybrid_predictions_path"] = str(hybrid_path)
    write_json(OUTPUT_DIR / "paired_bootstrap_vs_hybrid.json", bootstrap_result)
else:
    print("Skipping paired bootstrap: exact frozen hybrid predictions could not be proven.")
"""
    report = """
comparison = {
    "tfidf_category_v8": FROZEN_BASELINES["tfidf_category_v8"],
    "frozen_hybrid_natural_only": FROZEN_BASELINES["hybrid_natural_only"],
    "codebert_joint_512": FROZEN_BASELINES["codebert_joint_512"],
    "modernbert_long_context": {
        "model": MODEL_NAME,
        "resolved_revision_sha": MODEL_REVISION_SHA,
        "macro_f1": metrics["macro_f1"],
        "balanced_accuracy": metrics["balanced_accuracy"],
        "developer_setup_f1": metrics["per_class"]["developer_setup"]["f1-score"],
    },
}
write_json(OUTPUT_DIR / "comparison_with_prior_models.json", comparison)

train_macro = internal_train_metrics["macro_f1"]
eval_macro = internal_eval_metrics["macro_f1"]
external_macro = metrics["macro_f1"]
hybrid_macro = FROZEN_BASELINES["hybrid_natural_only"]["macro_f1"]
modern_dev_f1 = metrics["per_class"]["developer_setup"]["f1-score"]
if external_macro > hybrid_macro + 0.03 and modern_dev_f1 >= 0:
    decision = "A. STRONG ARCHITECTURE SIGNAL"
elif abs(external_macro - hybrid_macro) <= 0.03 and modern_dev_f1 > 0:
    decision = "B. PARTIAL SIGNAL"
elif train_macro > 0.75 and (eval_macro < 0.45 or external_macro < 0.45):
    decision = "D. OVERFITTING"
elif train_macro < 0.45 and eval_macro < 0.45 and external_macro < 0.45:
    decision = "E. UNDERFITTING"
else:
    decision = "C. NO SIGNAL"

manifest_out = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "model_name": MODEL_NAME,
    "resolved_revision_sha": MODEL_REVISION_SHA,
    "attention_implementation": attention_implementation,
    "model_config": model.config.to_dict(),
    "python": sys.version,
    "torch": torch.__version__,
    "transformers": transformers.__version__,
    "tokenizers": tokenizers.__version__,
    "accelerate": accelerate_version,
    "huggingface_hub": hf_hub_version,
    "cuda_device": torch.cuda.get_device_name(0),
    "gpu_memory_gb": total_gpu_memory_gb,
    "max_length": MAX_LENGTH,
    "max_length_policy_branch": max_length_policy_branch,
    "seed": SEED,
    "learning_rate": LEARNING_RATE,
    "weight_decay": WEIGHT_DECAY,
    "max_epochs": MAX_EPOCHS,
    "train_batch_size": TRAIN_BATCH_SIZE,
    "eval_batch_size": EVAL_BATCH_SIZE,
    "gradient_accumulation_steps": GRADIENT_ACCUMULATION_STEPS,
    "best_checkpoint": trainer.state.best_model_checkpoint,
    "best_metric": trainer.state.best_metric,
    "internal_split_seed": internal_split_seed,
    "training_seconds": training_seconds,
    "v1_export_manifest": manifest,
    "no_class_balancing": True,
    "no_confirmation_access": True,
    "no_controlled_or_synthetic_data": True,
}
write_json(OUTPUT_DIR / "training_manifest.json", manifest_out)

results_md = f'''# ModernBERT long-context architecture challenge V2

This is a bounded Stage-2 architecture experiment using exactly the frozen natural Architecture Challenge V1 export.

## Main result

- Decision: **{decision}**
- Model: `{MODEL_NAME}`
- Resolved revision SHA: `{MODEL_REVISION_SHA}`
- MAX_LENGTH: **{MAX_LENGTH}** (`{max_length_policy_branch}`)
- External development validation rows: **{len(validation_rows)}**
- Macro-F1: **{metrics['macro_f1']:.4f}**
- Balanced accuracy: **{metrics['balanced_accuracy']:.4f}**
- Weighted-F1: **{metrics['weighted_f1']:.4f}**
- developer_setup F1: **{metrics['per_class']['developer_setup']['f1-score']:.4f}**

## Fit diagnostic

- Internal train Macro-F1: **{internal_train_metrics['macro_f1']:.4f}**
- Internal eval Macro-F1: **{internal_eval_metrics['macro_f1']:.4f}**
- Gap: **{internal_train_metrics['macro_f1'] - internal_eval_metrics['macro_f1']:.4f}**

## Developer setup diagnostic

- Correct / 19: **{developer_setup_diagnostics['correct_out_of_19']} / 19**
- Rank counts: `{developer_setup_diagnostics['rank_counts']}`

## API catch-all diagnostic

- Total API false positives: **{api_fp['total_api_false_positives']}**
- CodeBERT V1 API false positives: **{api_fp['codebert_v1_total_api_false_positives']}**

## Frozen baselines

| Model | Macro-F1 | Balanced accuracy | developer_setup F1 |
|---|---:|---:|---:|
| TF-IDF Category V8 | {FROZEN_BASELINES['tfidf_category_v8']['macro_f1']:.4f} | {FROZEN_BASELINES['tfidf_category_v8']['balanced_accuracy']:.4f} | 0.0000 |
| Frozen Hybrid Natural-Only | {FROZEN_BASELINES['hybrid_natural_only']['macro_f1']:.4f} | {FROZEN_BASELINES['hybrid_natural_only']['balanced_accuracy']:.4f} | 0.0000 |
| CodeBERT Joint 512 | {FROZEN_BASELINES['codebert_joint_512']['macro_f1']:.4f} | {FROZEN_BASELINES['codebert_joint_512']['balanced_accuracy']:.4f} | 0.0000 |
| ModernBERT Long Context | {metrics['macro_f1']:.4f} | {metrics['balanced_accuracy']:.4f} | {metrics['per_class']['developer_setup']['f1-score']:.4f} |

The external 322-row split is development validation, not a test set. It was evaluated once after selecting the best checkpoint by internal repository-grouped Macro-F1.
'''
(OUTPUT_DIR / "RESULTS.md").write_text(results_md, encoding="utf-8")
print(results_md)
"""
    cells = [
        notebook_cell("markdown", title),
        notebook_cell("code", deps),
        notebook_cell("code", imports),
        notebook_cell("code", data_import),
        notebook_cell("code", config),
        notebook_cell("code", helpers),
        notebook_cell("code", load_audit),
        notebook_cell("code", tokenizer_gpu),
        notebook_cell("code", truncation),
        notebook_cell("code", dataset_split),
        notebook_cell("code", metrics_model),
        notebook_cell("code", oom_train),
        notebook_cell("code", evaluation),
        notebook_cell("code", diagnostics),
        notebook_cell("code", figures_bootstrap),
        notebook_cell("code", report),
    ]
    return {
        "cells": cells,
        "metadata": {
            "accelerator": "GPU",
            "colab": {"provenance": []},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write_readmes(audit: dict[str, Any]) -> None:
    EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    readme = f"""# Stage-2 Architecture Challenge V2

Prepared notebook: `notebooks/category_modernbert_architecture_challenge_v2.ipynb`

This stage tests one bounded hypothesis: whether a long-context joint Transformer
(`{MODEL_NAME}`) improves over the frozen natural-only hybrid and the CodeBERT
512-token architecture challenge by retaining substantially more code/document
evidence.

Frozen data reused exactly from V1:

- `{TRAIN_PATH.relative_to(ROOT).as_posix()}` ({audit['train_rows']} rows)
- `{VALIDATION_PATH.relative_to(ROOT).as_posix()}` ({audit['validation_rows']} rows)
- `{MANIFEST_PATH.relative_to(ROOT).as_posix()}` (authoritative manifest)

Guardrails:

- no confirmation access;
- no controlled/synthetic rows;
- no data acquisition;
- no label or membership changes;
- no class balancing;
- repository identity is only used for grouping/audit, not model input.

Colab output target:

- `{OUTPUT_DIR.relative_to(ROOT).as_posix()}/`

Expected normal Colab T4 branch: `MAX_LENGTH=2048`.
"""
    (EXPERIMENT_DIR / "README.md").write_text(readme, encoding="utf-8")
    placeholder = """# ModernBERT long-context outputs

This directory is the expected Colab output target. The notebook will write
metrics, predictions, figures, manifests, truncation diagnostics, and final
RESULTS.md here after GPU execution.

Large checkpoint/model/cache folders are intentionally ignored by Git.
"""
    (OUTPUT_DIR / "README.md").write_text(placeholder, encoding="utf-8")


def write_notebook() -> None:
    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTEBOOK_PATH.write_text(json.dumps(make_notebook(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main() -> None:
    audit = validate_v1_exports()
    write_notebook()
    write_readmes(audit)
    print(json.dumps({
        "status": "prepared",
        "notebook": str(NOTEBOOK_PATH.relative_to(ROOT)),
        "output_dir": str(OUTPUT_DIR.relative_to(ROOT)),
        "validation_case_ids_sha256": audit["validation_case_ids_sha256"],
        "train_rows": audit["train_rows"],
        "validation_rows": audit["validation_rows"],
        "created_at": datetime.now(UTC).isoformat(),
    }, indent=2))


if __name__ == "__main__":
    main()
