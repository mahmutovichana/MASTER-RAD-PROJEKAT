from __future__ import annotations

import argparse
import csv
import gc
import hashlib
import json
import logging
import os
import random
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np

from experiments.posthoc_stage3_s1.scripts.kaggle_development_runner import cuda_snapshot, host_ram, package_versions
from experiments.posthoc_stage3_s1.scripts.repository_corpus import (
    BareGitRepositoryProvider,
    DocumentChunk,
    discover_candidates,
    resolve_pre_change_source,
    semantic_chunks,
)
from experiments.posthoc_stage3_s1.scripts.retrieval import (
    EMBEDDING_MODEL_ID,
    EMBEDDING_REVISION,
    RERANKER_MODEL_ID,
    RERANKER_REVISION,
    QwenDenseEncoder,
    QwenReranker,
    RankedChunk,
    chunk_text,
    cosine_dense_scores,
    lexical_scores,
)
from experiments.posthoc_stage3_s1.scripts.s1_pipeline import (
    GENERATOR_MODEL_ID,
    GENERATOR_REVISION,
    QwenStructuredGenerator,
    S1Agent,
    S1Configuration,
    build_retrieval_query,
)


FROZEN_SHA = "38f9afb479f738081301172176d3133e4056bd7c"
MEMBERSHIP_COUNT = 200
CONTROLLED_TARGET_COUNT = 79
GRID = ((5, 5), (5, 10), (10, 5), (10, 10))
THRESHOLDS = (0.35, 0.50, 0.65)
VARIANTS = ("P1", "P2")


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def append_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_case_id(case_id: str) -> str:
    return hashlib.sha256(case_id.encode()).hexdigest()[:20]


def safe_model_row(row: dict[str, Any]) -> dict[str, Any]:
    """Whitelist the only fields allowed to reach retrieval/generation prompts."""
    allowed = (
        "case_id", "repository", "language", "code_changed_files", "code_diff_excerpt", "docs_before_excerpt",
        "frozen_category_prediction", "predicted_category", "sample_name", "partition",
    )
    return {key: row.get(key) for key in allowed}


def git_head(root: Path) -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()


def assert_frozen_checkout(root: Path) -> None:
    actual = git_head(root)
    if actual != FROZEN_SHA:
        raise RuntimeError(f"Frozen checkout mismatch: expected {FROZEN_SHA}, got {actual}")


def assert_materialized(path: Path) -> None:
    prefix = path.read_bytes()[:80]
    if prefix.startswith(b"version https://git-lfs.github.com/spec"):
        raise RuntimeError(f"Required Git LFS object is not materialized: {path}")


def valid_score_checkpoint(path: Path, case_id: str, document_count: int) -> bool:
    if not path.is_file() or path.name.endswith(".tmp"):
        return False
    try:
        with np.load(path, allow_pickle=False) as arrays:
            required = {"case_id", "query_embedding", "document_embeddings", "lexical_scores", "dense_scores"}
            if not required.issubset(arrays.files) or str(arrays["case_id"].item()) != case_id:
                return False
            query = arrays["query_embedding"]
            documents = arrays["document_embeddings"]
            lexical = arrays["lexical_scores"]
            dense = arrays["dense_scores"]
            if query.shape != (1024,) or documents.shape != (document_count, 1024):
                return False
            if lexical.shape != (document_count,) or dense.shape != (document_count,):
                return False
            return bool(np.isfinite(query).all() and np.isfinite(documents).all() and np.isfinite(lexical).all() and np.isfinite(dense).all())
    except (OSError, ValueError, KeyError, EOFError):
        return False


def chunk_to_dict(value: DocumentChunk) -> dict[str, Any]:
    return {
        "path": value.path,
        "heading": value.heading,
        "heading_path": list(value.heading_path),
        "text": value.text,
        "chunk_index": value.chunk_index,
        "priority_tier": value.priority_tier,
        "path_distance": value.path_distance,
        "identifier_overlap": value.identifier_overlap,
    }


def chunk_from_dict(value: dict[str, Any]) -> DocumentChunk:
    return DocumentChunk(
        value["path"], value["heading"], tuple(value["heading_path"]), value["text"], value["chunk_index"],
        value["priority_tier"], value["path_distance"], value["identifier_overlap"],
    )


def load_unique_jsonl(path: Path, key_name: str) -> dict[str, dict[str, Any]]:
    values = {}
    for row in read_jsonl(path):
        key = str(row[key_name])
        if key in values and values[key] != row:
            raise RuntimeError(f"Conflicting duplicate checkpoint key {key} in {path}")
        if key in values:
            raise RuntimeError(f"Duplicate checkpoint key {key} in {path}")
        values[key] = row
    return values


class PersistentBackend:
    def __init__(self, backend: QwenStructuredGenerator, path: Path):
        self.backend = backend
        self.path = path
        self.cache = {}
        for row in read_jsonl(path):
            key = (row["purpose"], row["prompt_sha256"])
            if key in self.cache and self.cache[key] != row["response"]:
                raise RuntimeError(f"Conflicting cached model call: {key}")
            self.cache[key] = row["response"]

    def generate_json(self, *, purpose: str, prompt: str) -> dict[str, Any]:
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
        key = (purpose, prompt_hash)
        if key in self.cache:
            return self.cache[key]
        response = self.backend.generate_json(purpose=purpose, prompt=prompt)
        append_jsonl(self.path, {"purpose": purpose, "prompt_sha256": prompt_hash, "response": response})
        self.cache[key] = response
        return response


def retrieval_metric(ranks: list[int | None]) -> dict[str, Any]:
    n = len(ranks)
    return {
        "n": n,
        "hit_at_1": sum(rank == 1 for rank in ranks) / n,
        "hit_at_3": sum(rank is not None and rank <= 3 for rank in ranks) / n,
        "mrr": sum(0.0 if rank is None else 1.0 / rank for rank in ranks) / n,
    }


def outcome_summary(results: dict[str, dict[str, Any]], case_ids: list[str], threshold: float) -> dict[str, Any]:
    selected = []
    for case_id in case_ids:
        value = results[case_id]
        confidence = float((value.get("target_decision") or {}).get("confidence") or 0.0)
        if confidence < threshold:
            value = {"state": "ABSTAINED_NO_TARGET", "repair_count": 0, "target_decision": value.get("target_decision")}
        selected.append(value)
    n = len(selected)
    accepted = [item for item in selected if item["state"] == "ACCEPTED"]
    generated = [item for item in selected if item.get("patch")]
    unsupported = [item for item in selected if item["state"] == "ABSTAINED_UNSUPPORTED_CLAIMS" or (item.get("critic") or {}).get("unsupported_claims") or item.get("deterministic_unsupported_claims")]
    target_violations = [item for item in selected if item.get("patch") and str(item["patch"].get("target_document") or "") != str((item.get("target_decision") or {}).get("target_document") or "")]
    return {
        "n": n,
        "generation_invocation_rate": len(generated) / n,
        "accepted_output_coverage": len(accepted) / n,
        "abstention_rate": sum(str(item["state"]).startswith("ABSTAINED_") for item in selected) / n,
        "execution_error_rate": sum(item["state"] == "FAILED_EXECUTION" for item in selected) / n,
        "unsupported_fact_violation_rate": len(unsupported) / n,
        "target_not_retrieved_rate": len(target_violations) / n,
        "first_pass_accept_rate": sum(item["state"] == "ACCEPTED" and item.get("repair_count") == 0 for item in selected) / n,
        "repaired_accept_rate": sum(item["state"] == "ACCEPTED" and item.get("repair_count") == 1 for item in selected) / n,
        "state_counts": dict(sorted(Counter(item["state"] for item in selected).items())),
    }


def write_blind_review(output: Path, rows: list[dict[str, Any]], outcomes: dict[str, dict[str, dict[str, Any]]]) -> dict[str, Any]:
    columns = [
        "review_item_id", "case_id", "code_changed_files", "code_diff_excerpt", "docs_before_excerpt",
        "candidate_A_target_document", "candidate_A_patch", "candidate_B_target_document", "candidate_B_patch",
        "reviewer_preference", "reviewer_target_fit_A", "reviewer_target_fit_B", "reviewer_grounding_A", "reviewer_grounding_B",
        "reviewer_usefulness_A", "reviewer_usefulness_B", "reviewer_style_fit_A", "reviewer_style_fit_B", "reviewer_notes",
    ]
    review_rows = []
    private_mapping = []
    by_id = {row["case_id"]: row for row in rows}
    for case_id in [row["case_id"] for row in rows]:
        p1 = outcomes["P1"][case_id]; p2 = outcomes["P2"][case_id]
        patch1 = str((p1.get("patch") or {}).get("patch_markdown") or "")
        patch2 = str((p2.get("patch") or {}).get("patch_markdown") or "")
        if not patch1 or not patch2 or patch1 == patch2:
            continue
        swap = int(hashlib.sha256(f"42:{case_id}".encode()).hexdigest(), 16) % 2 == 1
        a, b = (p2, p1) if swap else (p1, p2)
        item_id = f"S1-DEV-{len(review_rows) + 1:03d}"
        source = by_id[case_id]
        review_rows.append({
            "review_item_id": item_id, "case_id": case_id,
            "code_changed_files": json.dumps(source.get("code_changed_files") or []),
            "code_diff_excerpt": source.get("code_diff_excerpt") or "", "docs_before_excerpt": source.get("docs_before_excerpt") or "",
            "candidate_A_target_document": (a.get("target_decision") or {}).get("target_document") or "",
            "candidate_A_patch": (a.get("patch") or {}).get("patch_markdown") or "",
            "candidate_B_target_document": (b.get("target_decision") or {}).get("target_document") or "",
            "candidate_B_patch": (b.get("patch") or {}).get("patch_markdown") or "",
            **{column: "" for column in columns if column.startswith("reviewer_")},
        })
        private_mapping.append({"review_item_id": item_id, "candidate_A": "P2" if swap else "P1", "candidate_B": "P1" if swap else "P2"})
    sheet = output / "s1_development_blind_prompt_review.csv"
    with sheet.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns); writer.writeheader(); writer.writerows(review_rows)
    atomic_json(output / "checkpoints/blind_review_private_mapping.json", {"seed": 42, "rows": private_mapping})
    return {"status": "BLIND_DEVELOPMENT_REVIEW_REQUIRED", "row_count": len(review_rows), "path": str(sheet), "sha256": sha256(sheet)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Frozen, resumable Gate 4 development-only S1 GPU study")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("/kaggle/working/s1-development"))
    parser.add_argument("--cache-dir", default=os.environ.get("HF_HOME", "/kaggle/working/hf-cache"))
    parser.add_argument("--canary-receipt", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    if not os.environ.get("HF_TOKEN"):
        raise RuntimeError("HF_TOKEN must be supplied through the Kaggle Secret environment")
    canary = json.loads(args.canary_receipt.read_text(encoding="utf-8"))
    if canary.get("state") != "CANARY_PASS" or canary.get("confirmation_accessed") is not False:
        raise RuntimeError("Development run forbidden unless the frozen canary receipt says CANARY_PASS")
    root = args.root.resolve(); output = args.output.resolve(); output.mkdir(parents=True, exist_ok=True)
    assert_frozen_checkout(root)
    if any(term in str(output).casefold() for term in ("confirmation", "gate6", "e0", "e1", "e2")):
        raise ValueError("Development output path enters a forbidden evaluation area")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", handlers=[logging.FileHandler(output / "execution.log", encoding="utf-8"), logging.StreamHandler()])
    log = logging.getLogger("s1-development")
    random.seed(42); np.random.seed(42)
    import torch
    torch.manual_seed(42); torch.cuda.manual_seed_all(42)

    primary_path = root / "reports/final_v2/gate4/primary_sample.jsonl"
    secondary_path = root / "reports/final_v2/gate4/secondary_stress_sample.jsonl"
    gold_paths = [root / "experiments/consolidated_enriched_training_v2/gold/train.jsonl", root / "experiments/consolidated_enriched_training_v2/gold/validation.jsonl"]
    for path in (primary_path, secondary_path, *gold_paths):
        assert_materialized(path)
    sampled = read_jsonl(primary_path) + read_jsonl(secondary_path)
    if len(sampled) != MEMBERSHIP_COUNT or len({row["case_id"] for row in sampled}) != MEMBERSHIP_COUNT:
        raise RuntimeError("Frozen development membership is not exactly 200 unique cases")
    gold = {}
    for path in gold_paths:
        for row in read_jsonl(path): gold[row["case_id"]] = row
    rows = []
    for item in sampled:
        row = dict(gold.get(item["case_id"], {})); row.update(item); rows.append(row)
    if sum(bool(row.get("synthetic_target_doc_path")) for row in rows) != CONTROLLED_TARGET_COUNT:
        raise RuntimeError("Controlled target evidence is not exactly 79 rows")

    runtime_manifest = {
        "state": "RUNNING", "frozen_git_sha": FROZEN_SHA, "confirmation_accessed": False,
        "gate6_row_level_human_data_accessed": False, "development_case_count": 200,
        "controlled_target_evidence_count": 79, "seed": 42, "cuda": cuda_snapshot(), "host_ram": host_ram(),
        "package_versions": package_versions(),
        "models": {EMBEDDING_MODEL_ID: EMBEDDING_REVISION, RERANKER_MODEL_ID: RERANKER_REVISION, GENERATOR_MODEL_ID: GENERATOR_REVISION},
        "source_sha256": {str(path.relative_to(root)): sha256(path) for path in (primary_path, secondary_path, *gold_paths)},
    }
    atomic_json(output / "runtime_manifest.json", runtime_manifest)
    checkpoints = output / "checkpoints"; corpus_dir = checkpoints / "repository_corpus"; score_dir = checkpoints / "retrieval_scores"
    corpus_dir.mkdir(parents=True, exist_ok=True); score_dir.mkdir(parents=True, exist_ok=True)

    provider = BareGitRepositoryProvider(checkpoints / "repository_cache")
    groups: dict[str, set[str]] = defaultdict(set); sources = {}
    for row in rows:
        source = resolve_pre_change_source(row, root=root); sources[row["case_id"]] = source
        if source.kind == "git_commit": groups[source.repository].add(source.revision)
    for repository, revisions in groups.items():
        if not all(provider.ensure_commits(repository, revisions).values()):
            raise RuntimeError(f"Explicit pre-change object unavailable in {repository}; HEAD fallback is forbidden")

    corpora: dict[str, list[DocumentChunk]] = {}
    for index, row in enumerate(rows, 1):
        path = corpus_dir / f"{safe_case_id(row['case_id'])}.json"
        if path.is_file():
            cached = json.loads(path.read_text(encoding="utf-8"))
            if cached["case_id"] != row["case_id"]: raise RuntimeError("Corpus cache identity mismatch")
            chunks = [chunk_from_dict(value) for value in cached["chunks"]]
        else:
            source = sources[row["case_id"]]
            if source.kind == "git_commit":
                paths = provider.list_paths(source.repository, source.revision)
                read = lambda p, s=source: provider.read_text(s.repository, s.revision, p)
            else:
                local = Path(source.local_root); paths = [p.relative_to(local).as_posix() for p in local.rglob("*") if p.is_file()]
                read = lambda p, local=local: (local / Path(p)).read_text(encoding="utf-8", errors="replace")
            discovered = discover_candidates(paths, changed_paths=list(row.get("code_changed_files") or []), code_diff=str(row.get("code_diff_excerpt") or ""))[:64]
            chunks = []
            for document, tier, distance, overlap in discovered:
                chunks.extend(semantic_chunks(document, read(document), max_chars=4000, priority_tier=tier, distance=distance, identifier_overlap=overlap))
            atomic_json(path, {"case_id": row["case_id"], "chunks": [chunk_to_dict(value) for value in chunks]})
        corpora[row["case_id"]] = chunks
    atomic_json(checkpoints / "repository_corpus_complete.json", {"state": "COMPLETE", "case_count": len(corpora)})
    log.info("Repository corpus complete: %d cases", len(corpora))

    missing_scores = [
        row for row in rows
        if not valid_score_checkpoint(score_dir / f"{safe_case_id(row['case_id'])}.npz", row["case_id"], len(corpora[row["case_id"]]))
    ]
    if missing_scores:
        dense = QwenDenseEncoder(cache_dir=args.cache_dir, batch_size=8)
        if getattr(dense.model.config, "_commit_hash", None) != EMBEDDING_REVISION: raise RuntimeError("Embedding revision mismatch")
        for row in missing_scores:
            case_id = row["case_id"]; chunks = corpora[case_id]; query = build_retrieval_query(safe_model_row(row))
            lexical = lexical_scores(query, chunks); embeddings = dense.encode([query, *[chunk_text(chunk) for chunk in chunks]])
            dense_scores = cosine_dense_scores(embeddings[0], embeddings[1:])
            target = score_dir / f"{safe_case_id(case_id)}.npz"; temporary = target.with_suffix(".npz.tmp")
            embedding_diagnostics = json.dumps(dense.last_encode_diagnostics, sort_keys=True)
            with temporary.open("wb") as handle: np.savez_compressed(handle, case_id=case_id, query_embedding=embeddings[0], document_embeddings=embeddings[1:], lexical_scores=lexical, dense_scores=dense_scores, embedding_runtime_diagnostics=embedding_diagnostics)
            os.replace(temporary, target)
        del dense; gc.collect(); torch.cuda.empty_cache(); torch.cuda.synchronize()
    atomic_json(checkpoints / "embedding_candidate_retrieval_complete.json", {"state": "COMPLETE", "case_count": 200})
    embedding_diagnostics = []
    for row in rows:
        path = score_dir / f"{safe_case_id(row['case_id'])}.npz"
        with np.load(path, allow_pickle=False) as arrays:
            if "embedding_runtime_diagnostics" in arrays.files:
                diagnostic = json.loads(str(arrays["embedding_runtime_diagnostics"].item()))
                diagnostic.update({"case_id": row["case_id"], "reused_without_recorded_diagnostics": False})
            else:
                diagnostic = {"case_id": row["case_id"], "configured_max_batch_size": 8, "effective_batch_sizes_used": None, "oom_split_count": None, "minimum_effective_batch_size": None, "single_item_oom": None, "reused_without_recorded_diagnostics": True}
            embedding_diagnostics.append(diagnostic)
    atomic_json(checkpoints / "embedding_runtime_diagnostics.json", {"case_count": 200, "cases": embedding_diagnostics})
    known_diagnostics = [item for item in embedding_diagnostics if not item["reused_without_recorded_diagnostics"]]
    effective_sizes = [size for item in known_diagnostics for size in item["effective_batch_sizes_used"]]
    runtime_manifest["embedding_microbatch"] = {
        "configured_max_batch_size": 8,
        "effective_batch_sizes_used": sorted(set(effective_sizes)),
        "oom_split_count": sum(item["oom_split_count"] for item in known_diagnostics),
        "minimum_effective_batch_size": min(effective_sizes) if effective_sizes else None,
        "single_item_oom": any(item["single_item_oom"] for item in known_diagnostics),
        "valid_pre_amendment_checkpoints_reused_without_diagnostics": sum(item["reused_without_recorded_diagnostics"] for item in embedding_diagnostics),
    }
    atomic_json(output / "runtime_manifest.json", runtime_manifest)
    log.info("Embedding and candidate retrieval complete: 200 cases")

    rerank_cache = load_unique_jsonl(checkpoints / "reranker_scores.jsonl", "case_id")
    missing_rerank = [row for row in rows if row["case_id"] not in rerank_cache]
    if missing_rerank:
        reranker = QwenReranker(cache_dir=args.cache_dir)
        if getattr(reranker.model.config, "_commit_hash", None) != RERANKER_REVISION: raise RuntimeError("Reranker revision mismatch")
        for row in missing_rerank:
            case_id = row["case_id"]; chunks = corpora[case_id]; arrays = np.load(score_dir / f"{safe_case_id(case_id)}.npz")
            lexical = arrays["lexical_scores"]; dense_values = arrays["dense_scores"]
            union = set()
            for lexical_k, dense_k in GRID:
                union.update(sorted(range(len(chunks)), key=lambda i: (-float(lexical[i]), chunks[i].path, chunks[i].chunk_index))[:lexical_k])
                union.update(sorted(range(len(chunks)), key=lambda i: (-float(dense_values[i]), chunks[i].path, chunks[i].chunk_index))[:dense_k])
            indices = sorted(union); values = reranker.score(build_retrieval_query(safe_model_row(row)), [chunk_text(chunks[i]) for i in indices])
            record = {"case_id": case_id, "scores": {str(i): float(score) for i, score in zip(indices, values)}}
            append_jsonl(checkpoints / "reranker_scores.jsonl", record); rerank_cache[case_id] = record
        del reranker; gc.collect(); torch.cuda.empty_cache(); torch.cuda.synchronize()
    atomic_json(checkpoints / "reranking_complete.json", {"state": "COMPLETE", "case_count": 200})
    log.info("Reranking complete: 200 cases")

    retrieval: dict[str, dict[str, list[RankedChunk]]] = {f"l{l}_d{d}": {} for l, d in GRID}
    retrieval_metrics = {}
    retrieval_rows = []
    for lexical_k, dense_k in GRID:
        key = f"l{lexical_k}_d{dense_k}"; ranks = []
        for row in rows:
            case_id = row["case_id"]; chunks = corpora[case_id]; arrays = np.load(score_dir / f"{safe_case_id(case_id)}.npz")
            lexical = arrays["lexical_scores"]; dense_values = arrays["dense_scores"]
            lex_ids = sorted(range(len(chunks)), key=lambda i: (-float(lexical[i]), chunks[i].path, chunks[i].chunk_index))[:lexical_k]
            den_ids = sorted(range(len(chunks)), key=lambda i: (-float(dense_values[i]), chunks[i].path, chunks[i].chunk_index))[:dense_k]
            score_map = rerank_cache[case_id]["scores"]; ranked = [RankedChunk(chunks[i], float(lexical[i]), float(dense_values[i]), float(score_map[str(i)])) for i in set(lex_ids) | set(den_ids)]
            best = {}
            for value in ranked:
                if value.chunk.path not in best or value.reranker_score > best[value.chunk.path].reranker_score: best[value.chunk.path] = value
            top = sorted(best.values(), key=lambda value: (-value.reranker_score, value.chunk.path))[:3]; retrieval[key][case_id] = top
            retrieval_rows.append({"configuration": key, "case_id": case_id, "candidates": [{"path": v.chunk.path, "heading": v.chunk.heading, "lexical_score": v.lexical_score, "dense_score": v.dense_score, "reranker_score": v.reranker_score} for v in top]})
            target = row.get("synthetic_target_doc_path")
            if target:
                paths = [value.chunk.path for value in top]; ranks.append(paths.index(target) + 1 if target in paths else None)
        retrieval_metrics[key] = retrieval_metric(ranks)
    if any(value["n"] != 79 for value in retrieval_metrics.values()): raise RuntimeError("Target metrics escaped the controlled 79-row denominator")
    selected_key = sorted(retrieval_metrics, key=lambda key: (-retrieval_metrics[key]["hit_at_3"], -retrieval_metrics[key]["mrr"], -retrieval_metrics[key]["hit_at_1"], int(key.split("_")[0][1:]), int(key.split("_")[1][1:])))[0]
    atomic_json(output / "retrieval_metrics.json", {"controlled_only": True, "natural_target_ground_truth": False, "metrics": retrieval_metrics, "selected_retrieval_key": selected_key})
    retrieval_jsonl = output / "retrieval_results.jsonl"
    temporary = retrieval_jsonl.with_suffix(".jsonl.tmp"); temporary.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in retrieval_rows), encoding="utf-8"); os.replace(temporary, retrieval_jsonl)

    generation_path = output / "generation_results.jsonl"; completed_rows = load_unique_jsonl(generation_path, "run_key")
    required_keys = [f"{variant}:{row['case_id']}" for variant in VARIANTS for row in rows]
    missing_generation = [key for key in required_keys if key not in completed_rows]
    if missing_generation:
        generator = QwenStructuredGenerator(cache_dir=args.cache_dir)
        if getattr(generator.model.config, "_commit_hash", None) != GENERATOR_REVISION: raise RuntimeError("Generator revision mismatch")
        backend = PersistentBackend(generator, checkpoints / "model_call_cache.jsonl")
        row_map = {row["case_id"]: row for row in rows}; lexical_k = int(selected_key.split("_")[0][1:]); dense_k = int(selected_key.split("_")[1][1:])
        newly_completed = 0
        for run_key in required_keys:
            if run_key in completed_rows: continue
            variant, case_id = run_key.split(":", 1); row = row_map[case_id]
            agent = S1Agent(backend, S1Configuration(lexical_k, dense_k, 3, 0.35, variant))
            result = agent.run(safe_model_row(row), retrieval[selected_key][case_id], document_corpus=corpora[case_id])
            record = {"run_key": run_key, "variant": variant, "case_id": case_id, "result": result}
            append_jsonl(generation_path, record); completed_rows[run_key] = record; newly_completed += 1
            if newly_completed % 25 == 0:
                atomic_json(checkpoints / "generation_progress.json", {"state": "RUNNING", "completed": len(completed_rows), "required": len(required_keys), "last_run_key": run_key})
                log.info("Generation checkpoint: %d/%d", len(completed_rows), len(required_keys))
        del generator; gc.collect(); torch.cuda.empty_cache(); torch.cuda.synchronize()
    if set(completed_rows) != set(required_keys): raise RuntimeError("Generation checkpoint is incomplete or contains unexpected keys")
    atomic_json(checkpoints / "generation_progress.json", {"state": "COMPLETE", "completed": len(completed_rows), "required": len(required_keys)})
    outcomes = {variant: {row["case_id"]: completed_rows[f"{variant}:{row['case_id']}"]["result"] for row in rows} for variant in VARIANTS}
    groups = {"all_development": [row["case_id"] for row in rows], "primary": [row["case_id"] for row in rows[:100]], "secondary": [row["case_id"] for row in rows[100:]]}
    development_metrics = {variant: {str(threshold): {group: outcome_summary(outcomes[variant], ids, threshold) for group, ids in groups.items()} for threshold in THRESHOLDS} for variant in VARIANTS}
    atomic_json(output / "development_metrics.json", {"confirmation_accessed": False, "self_critic_is_human_ground_truth": False, "metrics": development_metrics})
    review = write_blind_review(output, rows, outcomes)
    selection = {"state": "SELECTION_REQUIRES_BLIND_DEVELOPMENT_REVIEW", "selected_retrieval_key": selected_key, "selected_threshold": None, "selected_prompt_variant": None, "review": review}
    atomic_json(output / "development_selection_status.json", selection)
    prompt_dir = Path(__file__).resolve().parents[1] / "prompts"
    atomic_json(output / "prompt_hashes.json", {path.name: sha256(path) for path in sorted(prompt_dir.glob("*.txt"))})
    atomic_json(output / "model_revision_receipt.json", canary.get("resolved_revisions", {}))
    runtime_manifest.update({"state": "DEVELOPMENT_METRICS_COMPLETE_SELECTION_PENDING_BLIND_REVIEW", "runtime_seconds": time.monotonic() - started, "final_cuda": cuda_snapshot(), "final_host_ram": host_ram()})
    atomic_json(output / "runtime_manifest.json", runtime_manifest)
    atomic_json(checkpoints / "development_metrics_complete.json", {"state": "COMPLETE", "selection_state": selection["state"]})
    log.info("Development metrics complete; prompt/threshold selection remains pending blind development review")
    print("DEVELOPMENT_METRICS_COMPLETE_SELECTION_PENDING_BLIND_REVIEW")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
