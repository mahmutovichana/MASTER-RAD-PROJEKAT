"""Prepare the Stage-2 configuration-vs-developer_setup specialist V2 notebook.

Local preparation is intentionally limited to notebook/test/readme generation
and integrity checks over the already-frozen V1 specialist train-only export.
The nested OOF experiment is designed for Colab GPU and must not be executed
locally by this script.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
V1_EXPORT_DIR = ROOT / "data" / "final_v2" / "configuration_setup_specialist_v1"
EXPORT_JSONL = V1_EXPORT_DIR / "natural_train_configuration_setup.jsonl"
EXPORT_MANIFEST = V1_EXPORT_DIR / "export_manifest.json"
NOTEBOOK_PATH = ROOT / "notebooks" / "category_configuration_vs_developer_setup_specialist_v2.ipynb"
README_PATH = ROOT / "experiments" / "category_hierarchy_pilot_v2" / "configuration_vs_developer_setup" / "README.md"

EXPECTED_TOTAL = 365
EXPECTED_COUNTS = {"configuration": 277, "developer_setup": 88}
EXPECTED_EXPORT_SHA256 = "bae86d28a07883dc0fac8a0c6919cbd1e3adf9f50b1f2143289c69e0a9a7c495"
LABELS = ["configuration", "developer_setup"]
SAFE_FIELDS = [
    "case_id",
    "repository",
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
    "gold_doc_category",
    "partition",
]

MINILM_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MINILM_MODEL_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
CLASS_WEIGHT_GRID = [
    {"name": "none", "value": None, "rank": 0},
    {"name": "developer_1_5", "value": {"configuration": 1.0, "developer_setup": 1.5}, "rank": 1},
    {"name": "developer_2_0", "value": {"configuration": 1.0, "developer_setup": 2.0}, "rank": 2},
    {"name": "developer_3_0", "value": {"configuration": 1.0, "developer_setup": 3.0}, "rank": 3},
    {"name": "balanced", "value": "balanced", "rank": 4},
]
THRESHOLD_GRID = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
PRECISION_FLOOR = 0.30


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def verify_v1_export() -> None:
    rows = read_jsonl(EXPORT_JSONL)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["gold_doc_category"]] = counts.get(row["gold_doc_category"], 0) + 1
    manifest = json.loads(EXPORT_MANIFEST.read_text(encoding="utf-8"))
    if len(rows) != EXPECTED_TOTAL:
        raise AssertionError(f"Expected {EXPECTED_TOTAL} rows, got {len(rows)}")
    if counts != EXPECTED_COUNTS:
        raise AssertionError(f"Expected {EXPECTED_COUNTS}, got {counts}")
    if sha256_file(EXPORT_JSONL) != EXPECTED_EXPORT_SHA256:
        raise AssertionError("V1 specialist export SHA256 changed")
    if manifest["artifacts"]["natural_train_configuration_setup.jsonl"]["sha256"] != EXPECTED_EXPORT_SHA256:
        raise AssertionError("V1 specialist manifest does not point at the frozen export hash")
    if manifest.get("frozen_322_validation_accessed") is not False:
        raise AssertionError("V1 specialist manifest must remain train-only")


def nb_cell(cell_type: str, source: str) -> dict[str, Any]:
    return {
        "cell_type": cell_type,
        "metadata": {},
        "source": [line + "\n" for line in source.strip("\n").splitlines()],
        **({"outputs": [], "execution_count": None} if cell_type == "code" else {}),
    }


def py(value: Any) -> str:
    return repr(value)


def make_notebook() -> dict[str, Any]:
    title = """
# Stage-2 configuration vs developer_setup specialist V2

Nested repository-grouped cost-sensitive decision calibration over the frozen
winning MiniLM hybrid representation. This is development OOF evidence only;
it is not external validation.
"""
    deps = """
# Python 3.13 compatible Colab stack. Keep Colab's CUDA torch build.
!python -m pip install -q \\
  "sentence-transformers==5.1.2" \\
  "transformers==4.56.2" \\
  "tokenizers==0.22.0" \\
  "huggingface_hub==0.34.4" \\
  "accelerate==1.10.1" \\
  "scikit-learn==1.7.2" \\
  "matplotlib==3.10.6" \\
  "scipy"
"""
    imports = """
from __future__ import annotations

import hashlib
import json
import math
import os
import random
import re
import shutil
import sys
import time
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import accelerate
import huggingface_hub
import matplotlib.pyplot as plt
import numpy as np
import scipy
import sklearn
import tokenizers
import torch
import transformers
from huggingface_hub import HfApi
from scipy import sparse
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedGroupKFold

print("Python:", sys.version)
print("torch:", torch.__version__)
print("CUDA availability:", torch.cuda.is_available())
print("CUDA device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "NONE")
print("transformers:", transformers.__version__)
print("tokenizers:", tokenizers.__version__)
print("accelerate:", accelerate.__version__)
print("huggingface_hub:", huggingface_hub.__version__)
assert torch.cuda.is_available()
"""
    constants = f"""
LABELS = {py(LABELS)}
SAFE_FIELDS = {py(SAFE_FIELDS)}
EXPECTED_TOTAL = {EXPECTED_TOTAL}
EXPECTED_COUNTS = {py(EXPECTED_COUNTS)}
EXPECTED_EXPORT_SHA256 = "{EXPECTED_EXPORT_SHA256}"
SEED = 42

MINILM_MODEL_NAME = "{MINILM_MODEL_NAME}"
MINILM_MODEL_REVISION = "{MINILM_MODEL_REVISION}"
CHUNK_CHARS = 1000
MAX_CHUNKS = 2
EMBEDDING_BATCH_SIZE = 64

CLASS_WEIGHT_GRID = {py(CLASS_WEIGHT_GRID)}
THRESHOLD_GRID = {py(THRESHOLD_GRID)}
PRECISION_FLOOR = {PRECISION_FLOOR}
V1_FIXED_METRICS = {{
    "macro_f1": 0.5133333333333333,
    "balanced_accuracy": 0.5382343288480472,
    "configuration_f1": 0.8666666666666667,
    "developer_setup_precision": 0.6666666666666666,
    "developer_setup_recall": 0.09090909090909091,
    "developer_setup_f1": 0.16,
}}

OUTPUT_DIR = Path("/content/experiments/category_hierarchy_pilot_v2/configuration_vs_developer_setup")
CACHE_DIR = OUTPUT_DIR / "cache"
FIGURES_DIR = OUTPUT_DIR / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
"""
    data_helpers = r'''
def reject_supplied_path(path):
    lowered = str(path).replace("\\", "/").lower()
    if any(word in lowered for word in ["validation", "confirmation", "refresh"]):
        raise ValueError(f"Forbidden non-train artifact path: {path}")


def has_export(root):
    export_dir = Path(root) / "data" / "final_v2" / "configuration_setup_specialist_v1"
    return (export_dir / "natural_train_configuration_setup.jsonl").exists() and (export_dir / "export_manifest.json").exists()


def locate_export_root():
    candidates = [
        Path.cwd(),
        Path("/content/MASTER-RAD-PROJEKAT"),
        Path("/content/MASTER RAD PROJEKAT"),
        Path("/content/drive/MyDrive/MASTER-RAD-PROJEKAT"),
        Path("/content/drive/MyDrive/MASTER RAD PROJEKAT"),
    ]
    for candidate in candidates:
        if has_export(candidate):
            return candidate
    for manifest in Path("/content").glob("**/export_manifest.json"):
        reject_supplied_path(manifest)
        if "configuration_setup_specialist_v1" not in manifest.as_posix():
            continue
        possible = manifest.parent.parent.parent.parent
        if has_export(possible):
            return possible
    return None


ROOT = locate_export_root()
if ROOT is None:
    print("Upload the repository ZIP or these two train-only files: natural_train_configuration_setup.jsonl and export_manifest.json")
    from google.colab import files

    uploaded = files.upload()
    upload_root = Path("/content/MASTER-RAD-PROJEKAT")
    export_dir = upload_root / "data" / "final_v2" / "configuration_setup_specialist_v1"
    export_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in uploaded.items():
        reject_supplied_path(name)
        base = Path(name).name
        if base.lower().endswith(".zip"):
            zip_path = upload_root / base
            zip_path.write_bytes(payload)
            with zipfile.ZipFile(zip_path) as archive:
                for member in archive.namelist():
                    reject_supplied_path(member)
                archive.extractall(upload_root)
        elif base in {"natural_train_configuration_setup.jsonl", "export_manifest.json"}:
            (export_dir / base).write_bytes(payload)
    ROOT = locate_export_root()

assert ROOT is not None and has_export(ROOT)
EXPORT_DIR = ROOT / "data" / "final_v2" / "configuration_setup_specialist_v1"
DATA_PATH = EXPORT_DIR / "natural_train_configuration_setup.jsonl"
MANIFEST_PATH = EXPORT_DIR / "export_manifest.json"
print("Using train-only specialist export:", EXPORT_DIR)
'''
    helpers = r'''
def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_json_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def read_jsonl(path):
    reject_supplied_path(path)
    rows = []
    with open(path, encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("partition") != "development_train":
                raise ValueError(f"{path}:{line_number}: only development_train rows are allowed")
            rows.append(row)
    return rows


def list_value(value):
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("["):
            try:
                parsed = json.loads(stripped)
                if isinstance(parsed, list):
                    return [str(item) for item in parsed]
            except json.JSONDecodeError:
                pass
        return [stripped] if stripped else []
    return []


def sanitize_repository_identity(text, repository):
    repo = str(repository or "").strip().strip("/")
    sanitized = str(text or "")
    if not repo or "/" not in repo:
        return sanitized
    owner, name = repo.split("/", 1)
    patterns = [
        re.escape(repo),
        re.escape(f"github.com/{repo}"),
        re.escape(f"https://github.com/{repo}"),
        re.escape(f"http://github.com/{repo}"),
        re.escape(f"git@github.com:{repo}"),
        rf"github\.com/{re.escape(owner)}/{re.escape(name)}(?:\.git)?",
    ]
    for pattern in patterns:
        sanitized = re.sub(pattern, "[REPOSITORY]", sanitized, flags=re.IGNORECASE)
    return sanitized


def build_code_text(row):
    text = "\n".join([
        f"language: {str(row.get('language') or 'unknown').lower()}",
        "changed files:",
        "\n".join(list_value(row.get("code_changed_files"))),
        "code change:",
        str(row.get("code_diff_excerpt") or ""),
    ])
    return sanitize_repository_identity(text, row.get("repository"))


def build_docs_text(row):
    return sanitize_repository_identity(row.get("docs_before_excerpt") or "", row.get("repository"))


def deterministic_chunks(text, chunk_chars=CHUNK_CHARS, max_chunks=MAX_CHUNKS):
    normalized = re.sub(r"\x00", " ", str(text or "")).strip()
    if not normalized:
        return ["[empty]"]
    if len(normalized) <= chunk_chars:
        return [normalized]
    starts = np.linspace(0, max(0, len(normalized) - chunk_chars), num=max_chunks, dtype=int)
    return [normalized[int(start): int(start) + chunk_chars] for start in starts]


def encode_texts_cached(side, texts, encoder):
    key = stable_json_hash({
        "side": side,
        "model": MINILM_MODEL_NAME,
        "revision": MINILM_MODEL_REVISION,
        "chunk_chars": CHUNK_CHARS,
        "max_chunks": MAX_CHUNKS,
        "content_hash": stable_json_hash(texts),
    })
    target = CACHE_DIR / f"{side}_{key}.npy"
    meta_path = CACHE_DIR / f"{side}_{key}.json"
    if target.exists() and meta_path.exists():
        return np.load(target), json.loads(meta_path.read_text(encoding="utf-8")) | {"cache_hit": True}
    chunks, owners = [], []
    for row_index, text in enumerate(texts):
        for chunk in deterministic_chunks(text):
            chunks.append(chunk)
            owners.append(row_index)
    current_batch = EMBEDDING_BATCH_SIZE
    started = time.time()
    while True:
        try:
            with torch.inference_mode():
                chunk_vectors = encoder.encode(chunks, batch_size=current_batch, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True, device="cuda").astype(np.float32)
            break
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            if current_batch <= 1:
                raise
            current_batch = max(1, current_batch // 2)
            print("OOM; retrying MiniLM encode with batch_size=", current_batch)
    output = np.zeros((len(texts), chunk_vectors.shape[1]), dtype=np.float32)
    counts = np.zeros(len(texts), dtype=np.float32)
    for owner, vector in zip(owners, chunk_vectors):
        output[owner] += vector
        counts[owner] += 1.0
    output /= np.maximum(counts[:, None], 1.0)
    output /= np.maximum(np.linalg.norm(output, axis=1, keepdims=True), 1e-12)
    np.save(target, output)
    meta = {"side": side, "row_count": len(texts), "chunk_count": len(chunks), "embedding_dimension": int(output.shape[1]), "batch_size_used": int(current_batch), "elapsed_seconds": time.time() - started, "cache_hit": False}
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output, meta


TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{1,}")


def token_set(text):
    return {token.lower() for token in TOKEN_RE.findall(text)}


def lexical_relational_scalars(selected_rows):
    values = []
    for row in selected_rows:
        code_text = build_code_text(row)
        docs_text = build_docs_text(row)
        code_tokens = token_set(code_text)
        docs_tokens = token_set(docs_text)
        shared = code_tokens & docs_tokens
        union = code_tokens | docs_tokens
        identifiers = {token for token in code_tokens if "_" in token or any(char.isupper() for char in token)}
        path_tokens = token_set(" ".join(list_value(row.get("code_changed_files"))))
        values.append([
            math.log1p(len(shared)),
            len(shared) / max(1, len(union)),
            len(shared) / max(1, min(len(code_tokens), len(docs_tokens))),
            len(identifiers & docs_tokens) / max(1, len(identifiers)),
            len(path_tokens & docs_tokens) / max(1, len(path_tokens)),
            math.log1p(len(code_text)),
            math.log1p(len(docs_text)),
        ])
    return np.asarray(values, dtype=np.float32)


def relational_semantic_features(code, docs):
    cosine = np.sum(code * docs, axis=1, keepdims=True)
    return np.hstack([code, docs, np.abs(code - docs), code * docs, cosine]).astype(np.float32)


def labels_for(selected_rows):
    return np.asarray([row["gold_doc_category"] for row in selected_rows])


def metric_bundle(y_true, y_pred):
    precision, recall, f1, support = precision_recall_fscore_support(y_true, y_pred, labels=LABELS, zero_division=0)
    matrix = confusion_matrix(y_true, y_pred, labels=LABELS)
    normalized = matrix.astype(float) / np.maximum(matrix.sum(axis=1, keepdims=True), 1)
    return {
        "support": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "per_class": {label: {"precision": float(precision[i]), "recall": float(recall[i]), "f1": float(f1[i]), "support": int(support[i])} for i, label in enumerate(LABELS)},
        "confusion_matrix": matrix.tolist(),
        "normalized_confusion_matrix": normalized.tolist(),
        "predicted_class_counts": dict(sorted(Counter(map(str, y_pred)).items())),
    }


def setup_probability(classifier, features):
    raw = classifier.predict_proba(features)
    if "developer_setup" not in classifier.classes_:
        return np.zeros(features.shape[0], dtype=float)
    return raw[:, list(classifier.classes_).index("developer_setup")]


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
'''
    integrity = """
manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
rows = read_jsonl(DATA_PATH)
assert len(rows) == EXPECTED_TOTAL
assert Counter(row["gold_doc_category"] for row in rows) == EXPECTED_COUNTS
assert sha256_file(DATA_PATH) == EXPECTED_EXPORT_SHA256
assert manifest["artifacts"]["natural_train_configuration_setup.jsonl"]["sha256"] == EXPECTED_EXPORT_SHA256
assert set(row["partition"] for row in rows) == {"development_train"}
assert all(set(row) == set(SAFE_FIELDS) for row in rows)
assert manifest["confirmation_accessed"] is False
assert manifest["frozen_322_validation_accessed"] is False
assert manifest["controlled_or_synthetic_rows_used"] is False
for row in rows:
    combined = (build_code_text(row) + "\\n" + build_docs_text(row)).lower()
    repo = str(row.get("repository") or "").lower()
    assert not repo or "/" not in repo or repo not in combined
print("Verified frozen train-only specialist data:", manifest["category_counts"])
"""
    encoder = """
resolved_minilm_sha = HfApi().model_info(MINILM_MODEL_NAME, revision=MINILM_MODEL_REVISION).sha
print("Resolved MiniLM revision:", resolved_minilm_sha)
assert resolved_minilm_sha == MINILM_MODEL_REVISION
encoder = SentenceTransformer(MINILM_MODEL_NAME, revision=MINILM_MODEL_REVISION, device="cuda")
encoder.eval()
for parameter in encoder.parameters():
    parameter.requires_grad_(False)
assert all(not parameter.requires_grad for parameter in encoder.parameters())
with torch.inference_mode():
    smoke = encoder.encode([build_code_text(rows[0]), build_docs_text(rows[0])], batch_size=2, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False, device="cuda")
assert smoke.shape[0] == 2 and smoke.shape[1] > 0
assert np.all(np.isfinite(smoke))
"""
    features_splits = r'''
code_texts = [build_code_text(row) for row in rows]
docs_texts = [build_docs_text(row) for row in rows]
all_code_embeddings, code_cache = encode_texts_cached("code", code_texts, encoder)
all_docs_embeddings, docs_cache = encode_texts_cached("docs", docs_texts, encoder)
assert all_code_embeddings.shape == all_docs_embeddings.shape


def build_fold_features(train_idx, eval_idx):
    train_rows = [rows[int(i)] for i in train_idx]
    eval_rows = [rows[int(i)] for i in eval_idx]
    code_vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
        max_features=20000,
        sublinear_tf=True,
        dtype=np.float32,
    )
    code_train = code_vectorizer.fit_transform([build_code_text(row) for row in train_rows])
    code_eval = code_vectorizer.transform([build_code_text(row) for row in eval_rows])
    x_train = sparse.hstack([
        code_train,
        sparse.csr_matrix(relational_semantic_features(all_code_embeddings[train_idx], all_docs_embeddings[train_idx])),
        sparse.csr_matrix(lexical_relational_scalars(train_rows)),
    ], format="csr")
    x_eval = sparse.hstack([
        code_eval,
        sparse.csr_matrix(relational_semantic_features(all_code_embeddings[eval_idx], all_docs_embeddings[eval_idx])),
        sparse.csr_matrix(lexical_relational_scalars(eval_rows)),
    ], format="csr")
    return x_train, x_eval, {"tfidf_fit_rows": int(len(train_idx)), "tfidf_eval_rows": int(len(eval_idx)), "eval_enters_tfidf_fit": False}


def grouped_splits(indices, *, n_splits, seed):
    idx = np.asarray(indices, dtype=int)
    y = labels_for([rows[int(i)] for i in idx])
    groups = np.asarray([rows[int(i)]["repository"] for i in idx])
    splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    out = []
    for train_local, eval_local in splitter.split(np.arange(len(idx)), y, groups):
        train_idx = idx[train_local]
        eval_idx = idx[eval_local]
        y_train = labels_for([rows[int(i)] for i in train_idx])
        y_eval = labels_for([rows[int(i)] for i in eval_idx])
        g_train = {rows[int(i)]["repository"] for i in train_idx}
        g_eval = {rows[int(i)]["repository"] for i in eval_idx}
        if g_train & g_eval:
            raise AssertionError("Repository overlap inside grouped split")
        if set(y_train) != set(LABELS) or set(y_eval) != set(LABELS):
            raise ValueError("Fold missing one specialist class")
        out.append((train_idx, eval_idx))
    return out


def choose_inner_splits(outer_train_idx, outer_fold_id):
    for n_splits in [4, 3]:
        try:
            return n_splits, grouped_splits(outer_train_idx, n_splits=n_splits, seed=SEED + outer_fold_id)
        except ValueError:
            continue
    raise RuntimeError("No valid inner repository-grouped split with 4/3 folds.")


def deterministic_outer_splits():
    return grouped_splits(np.arange(len(rows)), n_splits=5, seed=SEED)


def load_exact_v1_outer_splits_if_available():
    candidates = [
        ROOT / "experiments" / "category_hierarchy_pilot_v1" / "configuration_vs_developer_setup" / "fold_manifest.json",
        Path("/content/fold_manifest.json"),
        Path("/content/configuration_setup_specialist_v1_results/fold_manifest.json"),
    ]
    by_case = {row["case_id"]: i for i, row in enumerate(rows)}
    for path in candidates:
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        folds = payload.get("folds", [])
        if len(folds) != 5:
            continue
        rebuilt = []
        usable = True
        for fold in folds:
            eval_case_ids = fold.get("eval_case_ids")
            if not eval_case_ids:
                usable = False
                break
            eval_idx = np.asarray([by_case[item] for item in eval_case_ids], dtype=int)
            train_idx = np.asarray([i for i in range(len(rows)) if i not in set(eval_idx)], dtype=int)
            rebuilt.append((train_idx, eval_idx))
        if usable:
            return rebuilt, {"exact_v1_outer_fold_manifest_reused": True, "path": str(path)}
    return deterministic_outer_splits(), {"exact_v1_outer_fold_manifest_reused": False, "path": None, "fallback": "deterministic StratifiedGroupKFold(seed=42)"}


outer_folds, outer_split_source = load_exact_v1_outer_splits_if_available()
outer_supports = []
for fold_id, (train_idx, eval_idx) in enumerate(outer_folds, 1):
    train_repos = {rows[int(i)]["repository"] for i in train_idx}
    eval_repos = {rows[int(i)]["repository"] for i in eval_idx}
    assert not train_repos & eval_repos
    eval_counts = Counter(labels_for([rows[int(i)] for i in eval_idx]))
    outer_supports.append({"fold": fold_id, "configuration": int(eval_counts["configuration"]), "developer_setup": int(eval_counts["developer_setup"])})
write_json(OUTPUT_DIR / "outer_fold_manifest.json", {"source": outer_split_source, "supports": outer_supports})
print("Outer split source:", outer_split_source)
print("Outer supports:", outer_supports)
'''
    nested = r'''
def predict_from_threshold(prob_setup, threshold):
    return np.where(prob_setup >= threshold, "developer_setup", "configuration")


def candidate_sort_key(item):
    metrics = item["metrics"]
    setup = metrics["per_class"]["developer_setup"]
    threshold_closeness = -abs(item["threshold"] - 0.5)
    lower_weight_rank = -item["class_weight_rank"]
    return (
        metrics["macro_f1"],
        setup["f1"],
        metrics["balanced_accuracy"],
        setup["precision"],
        threshold_closeness,
        lower_weight_rank,
    )


def select_inner_candidate(outer_fold_id, outer_train_idx):
    inner_n_splits, inner_folds = choose_inner_splits(outer_train_idx, outer_fold_id)
    candidate_probs = defaultdict(lambda: np.zeros(len(outer_train_idx), dtype=float))
    inner_position = {int(global_index): pos for pos, global_index in enumerate(outer_train_idx)}
    fit_audit = []
    for inner_fold_id, (inner_train_idx, inner_eval_idx) in enumerate(inner_folds, 1):
        assert not set(inner_eval_idx) & set(np.setdiff1d(np.arange(len(rows)), outer_train_idx))
        x_inner_train, x_inner_eval, feature_meta = build_fold_features(inner_train_idx, inner_eval_idx)
        y_inner_train = labels_for([rows[int(i)] for i in inner_train_idx])
        for weight_spec in CLASS_WEIGHT_GRID:
            clf = LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=SEED, class_weight=weight_spec["value"])
            clf.fit(x_inner_train, y_inner_train)
            prob_setup = setup_probability(clf, x_inner_eval)
            for global_index, prob in zip(inner_eval_idx, prob_setup):
                candidate_probs[weight_spec["name"]][inner_position[int(global_index)]] = float(prob)
            fit_audit.append({
                "inner_fold": inner_fold_id,
                "class_weight": weight_spec["name"],
                "train_rows": int(len(inner_train_idx)),
                "eval_rows": int(len(inner_eval_idx)),
                "feature_meta": feature_meta,
            })
    y_outer_train = labels_for([rows[int(i)] for i in outer_train_idx])
    scored = []
    for weight_spec in CLASS_WEIGHT_GRID:
        prob_setup = candidate_probs[weight_spec["name"]]
        for threshold in THRESHOLD_GRID:
            pred = predict_from_threshold(prob_setup, threshold)
            metrics = metric_bundle(y_outer_train, pred)
            setup_precision = metrics["per_class"]["developer_setup"]["precision"]
            scored.append({
                "class_weight": weight_spec["name"],
                "class_weight_value": weight_spec["value"],
                "class_weight_rank": int(weight_spec["rank"]),
                "threshold": float(threshold),
                "precision_floor_satisfied": bool(setup_precision >= PRECISION_FLOOR),
                "metrics": metrics,
            })
    eligible = [item for item in scored if item["precision_floor_satisfied"]]
    selected = max(eligible if eligible else scored, key=candidate_sort_key)
    selected["precision_floor_satisfied"] = bool(selected["precision_floor_satisfied"])
    return selected, scored, {"inner_n_splits": inner_n_splits, "fit_audit": fit_audit}


y_all = labels_for(rows)
outer_predictions = np.asarray([""] * len(rows), dtype=object)
outer_prob_setup = np.zeros(len(rows), dtype=float)
outer_fold_reports = []
inner_selection_reports = []
v1_fixed_predictions = np.asarray([""] * len(rows), dtype=object)

for outer_fold_id, (outer_train_idx, outer_eval_idx) in enumerate(outer_folds, 1):
    selected, inner_grid_report, inner_meta = select_inner_candidate(outer_fold_id, outer_train_idx)
    x_outer_train, x_outer_eval, feature_meta = build_fold_features(outer_train_idx, outer_eval_idx)
    y_outer_train = labels_for([rows[int(i)] for i in outer_train_idx])
    y_outer_eval = labels_for([rows[int(i)] for i in outer_eval_idx])
    selected_clf = LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=SEED, class_weight=selected["class_weight_value"])
    selected_clf.fit(x_outer_train, y_outer_train)
    prob_setup = setup_probability(selected_clf, x_outer_eval)
    pred = predict_from_threshold(prob_setup, selected["threshold"])
    outer_predictions[outer_eval_idx] = pred
    outer_prob_setup[outer_eval_idx] = prob_setup

    v1_clf = LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=SEED, class_weight=None)
    v1_clf.fit(x_outer_train, y_outer_train)
    v1_prob_setup = setup_probability(v1_clf, x_outer_eval)
    v1_fixed_predictions[outer_eval_idx] = predict_from_threshold(v1_prob_setup, 0.50)

    fold_metrics = metric_bundle(y_outer_eval, pred)
    outer_fold_reports.append({
        "fold": outer_fold_id,
        "selected_class_weight": selected["class_weight"],
        "selected_threshold": float(selected["threshold"]),
        "precision_floor_satisfied": bool(selected["precision_floor_satisfied"]),
        "metrics": fold_metrics,
        "feature_meta": feature_meta,
        "inner_n_splits": int(inner_meta["inner_n_splits"]),
    })
    inner_selection_reports.append({
        "outer_fold": outer_fold_id,
        "selected": selected,
        "grid": inner_grid_report,
        "inner_meta": inner_meta,
    })

assert all(item in LABELS for item in outer_predictions)
assert all(item in LABELS for item in v1_fixed_predictions)
write_json(OUTPUT_DIR / "outer_fold_metrics.json", outer_fold_reports)
write_json(OUTPUT_DIR / "inner_selection_by_outer_fold.json", inner_selection_reports)
'''
    reports = r'''
majority_predictions = np.asarray(["configuration"] * len(rows), dtype=object)
v2_metrics = metric_bundle(y_all, outer_predictions)
v1_reconstructed_metrics = metric_bundle(y_all, v1_fixed_predictions)
majority_metrics = metric_bundle(y_all, majority_predictions)

v2_setup_scores = outer_prob_setup
binary_gold = (y_all == "developer_setup").astype(int)
ranking = {
    "roc_auc": float(roc_auc_score(binary_gold, v2_setup_scores)),
    "pr_auc": float(average_precision_score(binary_gold, v2_setup_scores)),
    "note": "OOF scores come from different outer-fold models and are ranking diagnostics only.",
}

comparison = {
    "v1_reported": V1_FIXED_METRICS,
    "v1_reconstructed_same_outer_splits": {
        "macro_f1": v1_reconstructed_metrics["macro_f1"],
        "balanced_accuracy": v1_reconstructed_metrics["balanced_accuracy"],
        "configuration_f1": v1_reconstructed_metrics["per_class"]["configuration"]["f1"],
        "developer_setup_precision": v1_reconstructed_metrics["per_class"]["developer_setup"]["precision"],
        "developer_setup_recall": v1_reconstructed_metrics["per_class"]["developer_setup"]["recall"],
        "developer_setup_f1": v1_reconstructed_metrics["per_class"]["developer_setup"]["f1"],
    },
    "v2_nested": {
        "macro_f1": v2_metrics["macro_f1"],
        "balanced_accuracy": v2_metrics["balanced_accuracy"],
        "configuration_f1": v2_metrics["per_class"]["configuration"]["f1"],
        "developer_setup_precision": v2_metrics["per_class"]["developer_setup"]["precision"],
        "developer_setup_recall": v2_metrics["per_class"]["developer_setup"]["recall"],
        "developer_setup_f1": v2_metrics["per_class"]["developer_setup"]["f1"],
    },
}
comparison["deltas_v2_minus_v1_reported"] = {
    key: comparison["v2_nested"][key] - V1_FIXED_METRICS[key]
    for key in V1_FIXED_METRICS
}

selected_weights = Counter(item["selected_class_weight"] for item in outer_fold_reports)
selected_thresholds = Counter(str(item["selected_threshold"]) for item in outer_fold_reports)
decision_instability = len(selected_weights) > 2 or len(selected_thresholds) > 3

repo_setup = {}
for repository in sorted({row["repository"] for row in rows}):
    idx = np.asarray([row["repository"] == repository for row in rows])
    setup_idx = idx & (y_all == "developer_setup")
    if setup_idx.any():
        correct = setup_idx & (outer_predictions == "developer_setup")
        false_setup = idx & (y_all == "configuration") & (outer_predictions == "developer_setup")
        repo_setup[repository] = {
            "setup_support": int(setup_idx.sum()),
            "correct_setup_detections": int(correct.sum()),
            "setup_recall": float(correct.sum() / max(1, setup_idx.sum())),
            "false_setup_predictions": int(false_setup.sum()),
        }

language_diagnostics = {}
for language in sorted({str(row.get("language") or "unknown").lower() for row in rows} | {"typescript", "python", "go", "unknown"}):
    idx = np.asarray([str(row.get("language") or "unknown").lower() == language for row in rows])
    if idx.any():
        language_diagnostics[language] = metric_bundle(y_all[idx], outer_predictions[idx])

probability_diagnostics = {
    "ranking": ranking,
    "developer_setup_probability_by_true_class": {
        label: {
            "count": int(np.sum(y_all == label)),
            "mean": float(np.mean(v2_setup_scores[y_all == label])),
            "median": float(np.median(v2_setup_scores[y_all == label])),
            "p10": float(np.percentile(v2_setup_scores[y_all == label], 10)),
            "p90": float(np.percentile(v2_setup_scores[y_all == label], 90)),
        }
        for label in LABELS
    },
}

def cluster_bootstrap(metric_fn, pred):
    repositories = np.asarray([row["repository"] for row in rows])
    unique = np.asarray(sorted(set(repositories)))
    rng = np.random.default_rng(SEED)
    values = []
    for _ in range(2000):
        sampled = rng.choice(unique, size=len(unique), replace=True)
        idx = np.concatenate([np.where(repositories == repo)[0] for repo in sampled])
        values.append(metric_fn(y_all[idx], pred[idx]))
    arr = np.asarray(values, dtype=float)
    return {"mean": float(np.mean(arr)), "ci_2_5": float(np.percentile(arr, 2.5)), "ci_97_5": float(np.percentile(arr, 97.5))}

def delta_cluster_bootstrap(metric_fn, pred_a, pred_b):
    repositories = np.asarray([row["repository"] for row in rows])
    unique = np.asarray(sorted(set(repositories)))
    rng = np.random.default_rng(SEED)
    values = []
    for _ in range(2000):
        sampled = rng.choice(unique, size=len(unique), replace=True)
        idx = np.concatenate([np.where(repositories == repo)[0] for repo in sampled])
        values.append(metric_fn(y_all[idx], pred_a[idx]) - metric_fn(y_all[idx], pred_b[idx]))
    arr = np.asarray(values, dtype=float)
    return {"mean_delta": float(np.mean(arr)), "ci_2_5": float(np.percentile(arr, 2.5)), "ci_97_5": float(np.percentile(arr, 97.5))}

def setup_precision_metric(gold, pred):
    return precision_recall_fscore_support(gold, pred, labels=LABELS, zero_division=0)[0][1]

def setup_recall_metric(gold, pred):
    return precision_recall_fscore_support(gold, pred, labels=LABELS, zero_division=0)[1][1]

def setup_f1_metric(gold, pred):
    return precision_recall_fscore_support(gold, pred, labels=LABELS, zero_division=0)[2][1]

repository_cluster_bootstrap = {
    "macro_f1": cluster_bootstrap(lambda g, p: f1_score(g, p, labels=LABELS, average="macro", zero_division=0), outer_predictions),
    "balanced_accuracy": cluster_bootstrap(balanced_accuracy_score, outer_predictions),
    "developer_setup_f1": cluster_bootstrap(setup_f1_metric, outer_predictions),
    "developer_setup_precision": cluster_bootstrap(setup_precision_metric, outer_predictions),
    "developer_setup_recall": cluster_bootstrap(setup_recall_metric, outer_predictions),
}
paired_bootstrap_v2_vs_v1 = {
    "macro_f1": delta_cluster_bootstrap(lambda g, p: f1_score(g, p, labels=LABELS, average="macro", zero_division=0), outer_predictions, v1_fixed_predictions),
    "balanced_accuracy": delta_cluster_bootstrap(balanced_accuracy_score, outer_predictions, v1_fixed_predictions),
    "developer_setup_f1": delta_cluster_bootstrap(setup_f1_metric, outer_predictions, v1_fixed_predictions),
    "developer_setup_recall": delta_cluster_bootstrap(setup_recall_metric, outer_predictions, v1_fixed_predictions),
}

setup_correct_repos = [repo for repo, item in repo_setup.items() if item["correct_setup_detections"] > 0]
decision_gates = {
    "developer_setup_f1_ge_0_30": v2_metrics["per_class"]["developer_setup"]["f1"] >= 0.30,
    "balanced_accuracy_ge_0_60": v2_metrics["balanced_accuracy"] >= 0.60,
    "binary_macro_f1_ge_0_60": v2_metrics["macro_f1"] >= 0.60,
    "developer_setup_recall_ge_0_25": v2_metrics["per_class"]["developer_setup"]["recall"] >= 0.25,
    "setup_detections_across_multiple_repositories": len(setup_correct_repos) >= 2,
    "no_leakage_integrity_issue": True,
    "configuration_f1_ge_0_80": v2_metrics["per_class"]["configuration"]["f1"] >= 0.80,
}
decision = {
    "decision": "GO" if all(decision_gates.values()) else ("PARTIAL_SIGNAL_NO_GO" if v2_metrics["per_class"]["developer_setup"]["f1"] > V1_FIXED_METRICS["developer_setup_f1"] else "NO_IMPROVEMENT"),
    "gates": decision_gates,
    "decision_instability": bool(decision_instability),
    "selected_class_weights": dict(selected_weights),
    "selected_thresholds": dict(selected_thresholds),
}

with open(OUTPUT_DIR / "oof_predictions.jsonl", "w", encoding="utf-8", newline="\n") as handle:
    for index, (row, pred, score) in enumerate(zip(rows, outer_predictions, v2_setup_scores)):
        handle.write(json.dumps({"case_id": row["case_id"], "repository": row["repository"], "language": row["language"], "gold": row["gold_doc_category"], "prediction": str(pred), "developer_setup_score": float(score), "outer_row_index": index}, ensure_ascii=False, sort_keys=True) + "\n")

rescued = []
new_fp = []
with open(OUTPUT_DIR / "v1_to_v2_rescued_setup_cases.jsonl", "w", encoding="utf-8", newline="\n") as out:
    for row, v1_pred, v2_pred, score in zip(rows, v1_fixed_predictions, outer_predictions, v2_setup_scores):
        if row["gold_doc_category"] == "developer_setup" and v1_pred == "configuration" and v2_pred == "developer_setup":
            item = {"case_id": row["case_id"], "repository": row["repository"], "language": row["language"], "v1_prediction": str(v1_pred), "v2_prediction": str(v2_pred), "v2_setup_score": float(score)}
            rescued.append(item)
            out.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")
with open(OUTPUT_DIR / "new_v2_false_positive_cases.jsonl", "w", encoding="utf-8", newline="\n") as out:
    for row, v1_pred, v2_pred, score in zip(rows, v1_fixed_predictions, outer_predictions, v2_setup_scores):
        if row["gold_doc_category"] == "configuration" and v1_pred == "configuration" and v2_pred == "developer_setup":
            item = {"case_id": row["case_id"], "repository": row["repository"], "language": row["language"], "v1_prediction": str(v1_pred), "v2_prediction": str(v2_pred), "v2_setup_score": float(score)}
            new_fp.append(item)
            out.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")

write_json(OUTPUT_DIR / "v2_oof_metrics.json", v2_metrics)
write_json(OUTPUT_DIR / "v1_fixed_baseline_metrics.json", v1_reconstructed_metrics)
write_json(OUTPUT_DIR / "majority_baseline_metrics.json", majority_metrics)
write_json(OUTPUT_DIR / "v1_v2_comparison.json", comparison)
write_json(OUTPUT_DIR / "repository_setup_diagnostics.json", repo_setup)
write_json(OUTPUT_DIR / "language_diagnostics.json", language_diagnostics)
write_json(OUTPUT_DIR / "probability_diagnostics.json", probability_diagnostics)
write_json(OUTPUT_DIR / "repository_cluster_bootstrap.json", repository_cluster_bootstrap)
write_json(OUTPUT_DIR / "paired_bootstrap_v2_vs_v1.json", paired_bootstrap_v2_vs_v1)
write_json(OUTPUT_DIR / "decision.json", decision)

def plot_confusion(matrix, path, title, normalized=False):
    matrix = np.asarray(matrix)
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(matrix, cmap="Blues", vmin=0 if normalized else None, vmax=1 if normalized else None)
    ax.set_xticks(range(len(LABELS)), LABELS)
    ax.set_yticks(range(len(LABELS)), LABELS)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Gold")
    ax.set_title(title)
    for i in range(len(LABELS)):
        for j in range(len(LABELS)):
            ax.text(j, i, f"{matrix[i, j]:.2f}" if normalized else str(int(matrix[i, j])), ha="center", va="center")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)

plot_confusion(v2_metrics["confusion_matrix"], FIGURES_DIR / "v2_oof_confusion_matrix.png", "V2 OOF confusion matrix")
plot_confusion(v2_metrics["normalized_confusion_matrix"], FIGURES_DIR / "v2_oof_normalized_confusion_matrix.png", "V2 OOF normalized confusion matrix", normalized=True)

def simple_bar(path, labels, values, title, ylabel):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(labels, values)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, 1 if max(values or [0]) <= 1 else None)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)

simple_bar(FIGURES_DIR / "v1_vs_v2_setup_f1.png", ["V1", "V2"], [V1_FIXED_METRICS["developer_setup_f1"], v2_metrics["per_class"]["developer_setup"]["f1"]], "developer_setup F1", "F1")
simple_bar(FIGURES_DIR / "v1_vs_v2_setup_recall.png", ["V1", "V2"], [V1_FIXED_METRICS["developer_setup_recall"], v2_metrics["per_class"]["developer_setup"]["recall"]], "developer_setup recall", "Recall")
simple_bar(FIGURES_DIR / "outer_fold_setup_f1.png", [str(item["fold"]) for item in outer_fold_reports], [item["metrics"]["per_class"]["developer_setup"]["f1"] for item in outer_fold_reports], "Outer-fold developer_setup F1", "F1")
simple_bar(FIGURES_DIR / "outer_fold_macro_f1.png", [str(item["fold"]) for item in outer_fold_reports], [item["metrics"]["macro_f1"] for item in outer_fold_reports], "Outer-fold Macro-F1", "Macro-F1")
simple_bar(FIGURES_DIR / "selected_thresholds_by_fold.png", [str(item["fold"]) for item in outer_fold_reports], [item["selected_threshold"] for item in outer_fold_reports], "Selected thresholds", "Threshold")
simple_bar(FIGURES_DIR / "selected_weights_by_fold.png", list(selected_weights.keys()), list(selected_weights.values()), "Selected class weights", "Folds")

fig, ax = plt.subplots(figsize=(7, 4))
for label in LABELS:
    ax.hist(v2_setup_scores[y_all == label], alpha=0.6, bins=20, label=label)
ax.set_xlabel("OOF P(developer_setup)")
ax.set_ylabel("Rows")
ax.set_title("V2 setup score distribution")
ax.legend()
fig.tight_layout()
fig.savefig(FIGURES_DIR / "setup_probability_distribution_v2.png", dpi=180)
plt.close(fig)

results_md = f"""# Configuration vs developer_setup specialist V2

This is **not external validation**. It is nested repository-grouped OOF development evidence over the frozen V1 train-only specialist export.

## Decision

**{decision['decision']}**

## Main comparison

| metric | V1 fixed reported | V2 nested |
| --- | ---: | ---: |
| Macro-F1 | {V1_FIXED_METRICS['macro_f1']:.4f} | {v2_metrics['macro_f1']:.4f} |
| Balanced accuracy | {V1_FIXED_METRICS['balanced_accuracy']:.4f} | {v2_metrics['balanced_accuracy']:.4f} |
| configuration F1 | {V1_FIXED_METRICS['configuration_f1']:.4f} | {v2_metrics['per_class']['configuration']['f1']:.4f} |
| setup precision | {V1_FIXED_METRICS['developer_setup_precision']:.4f} | {v2_metrics['per_class']['developer_setup']['precision']:.4f} |
| setup recall | {V1_FIXED_METRICS['developer_setup_recall']:.4f} | {v2_metrics['per_class']['developer_setup']['recall']:.4f} |
| setup F1 | {V1_FIXED_METRICS['developer_setup_f1']:.4f} | {v2_metrics['per_class']['developer_setup']['f1']:.4f} |

## Selected decision layer per outer fold

| fold | class weight | threshold | precision floor |
| ---: | --- | ---: | --- |
""" + "\n".join(
    f"| {item['fold']} | {item['selected_class_weight']} | {item['selected_threshold']:.2f} | {item['precision_floor_satisfied']} |"
    for item in outer_fold_reports
) + "\n"
(OUTPUT_DIR / "RESULTS.md").write_text(results_md, encoding="utf-8")

zip_path = Path("/content/configuration_setup_specialist_v2_results.zip")
if zip_path.exists():
    zip_path.unlink()
lightweight_files = [
    "RESULTS.md",
    "outer_fold_manifest.json",
    "outer_fold_metrics.json",
    "inner_selection_by_outer_fold.json",
    "v2_oof_metrics.json",
    "v1_fixed_baseline_metrics.json",
    "majority_baseline_metrics.json",
    "v1_v2_comparison.json",
    "repository_setup_diagnostics.json",
    "language_diagnostics.json",
    "probability_diagnostics.json",
    "repository_cluster_bootstrap.json",
    "paired_bootstrap_v2_vs_v1.json",
    "oof_predictions.jsonl",
    "v1_to_v2_rescued_setup_cases.jsonl",
    "new_v2_false_positive_cases.jsonl",
    "decision.json",
]
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for name in lightweight_files:
        archive.write(OUTPUT_DIR / name, arcname=name)
    for figure in FIGURES_DIR.glob("*.png"):
        archive.write(figure, arcname=f"figures/{figure.name}")
print("Created lightweight result package:", zip_path)
'''
    download = """
from google.colab import files
files.download("/content/configuration_setup_specialist_v2_results.zip")
"""
    return {
        "cells": [
            nb_cell("markdown", title),
            nb_cell("code", deps),
            nb_cell("code", imports),
            nb_cell("code", constants),
            nb_cell("code", data_helpers),
            nb_cell("code", helpers),
            nb_cell("code", integrity),
            nb_cell("code", encoder),
            nb_cell("code", features_splits),
            nb_cell("code", nested),
            nb_cell("code", reports),
            nb_cell("code", download),
        ],
        "metadata": {
            "accelerator": "GPU",
            "colab": {"provenance": []},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write_notebook() -> None:
    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTEBOOK_PATH.write_text(json.dumps(make_notebook(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def compile_notebook_code_cells(path: Path = NOTEBOOK_PATH) -> list[str]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    for index, cell in enumerate(notebook.get("cells", []), 1):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        executable = [line.strip() for line in source.splitlines() if line.strip() and not line.strip().startswith("#")]
        if executable and executable[0].startswith("!"):
            continue
        try:
            ast.parse(source)
        except SyntaxError as exc:
            errors.append(f"cell {index}: {exc}")
    return errors


def write_readme() -> None:
    README_PATH.parent.mkdir(parents=True, exist_ok=True)
    README_PATH.write_text(
        f"""# Stage-2 configuration vs developer_setup specialist V2

This is the final bounded Stage-2 specialist experiment. It keeps the frozen
winning MiniLM hybrid representation unchanged and varies only the binary
decision layer: developer_setup class weight and decision threshold.

Data: `data/final_v2/configuration_setup_specialist_v1/natural_train_configuration_setup.jsonl`

- rows: {EXPECTED_TOTAL}
- category counts: {EXPECTED_COUNTS}
- SHA256: `{EXPECTED_EXPORT_SHA256}`
- frozen 322 validation accessed: no
- confirmation/refresh validation accessed: no
- controlled/synthetic rows used: no

Representation:

- encoder: `{MINILM_MODEL_NAME}`
- revision: `{MINILM_MODEL_REVISION}`
- chunking: 1000 chars, max 2 chunks per side
- semantic features: code, docs, abs diff, product, cosine
- lexical channel: code-only char_wb TF-IDF 3–5 grams, min_df=2, max_features=20000
- classifier: LogisticRegression(C=1.0, solver='lbfgs', max_iter=2000, random_state=42)

V2 selection:

- outer CV: 5-fold repository-grouped OOF, reusing exact V1 fold membership only if an integrity-usable fold manifest with eval case IDs is supplied
- inner CV: repository-grouped 4-fold, structural fallback to 3-fold
- class weights: {CLASS_WEIGHT_GRID}
- thresholds: {THRESHOLD_GRID}
- precision floor: developer_setup precision >= {PRECISION_FLOOR}

Colab notebook: `notebooks/category_configuration_vs_developer_setup_specialist_v2.ipynb`
""",
        encoding="utf-8",
    )


def main() -> None:
    verify_v1_export()
    write_notebook()
    write_readme()
    errors = compile_notebook_code_cells()
    if errors:
        raise SyntaxError("; ".join(errors))
    print(
        json.dumps(
            {
                "status": "prepared",
                "notebook": str(NOTEBOOK_PATH.relative_to(ROOT)),
                "readme": str(README_PATH.relative_to(ROOT)),
                "export": str(EXPORT_JSONL.relative_to(ROOT)),
                "export_sha256": sha256_file(EXPORT_JSONL),
                "exact_v1_outer_fold_manifest_reused_locally": False,
                "local_nested_oof_executed": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
