from __future__ import annotations

import argparse
import gc
import json
import os
import random
from collections import defaultdict
from pathlib import Path

from experiments.posthoc_stage3_s1.scripts.repository_corpus import (
    BareGitRepositoryProvider,
    DocumentChunk,
    discover_candidates,
    extract_headings,
    resolve_pre_change_source,
    semantic_chunks,
)
from experiments.posthoc_stage3_s1.scripts.retrieval import QwenDenseEncoder, QwenReranker, hybrid_retrieve, rerank_top_documents
from experiments.posthoc_stage3_s1.scripts.s1_pipeline import QwenStructuredGenerator, S1Agent, S1Configuration, build_retrieval_query


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def unload(*objects) -> None:
    import torch

    for value in objects:
        del value
    gc.collect()
    torch.cuda.empty_cache()


class MemoizedBackend:
    def __init__(self, backend):
        self.backend = backend
        self.cache = {}

    def generate_json(self, *, purpose, prompt):
        key = (purpose, prompt)
        if key not in self.cache:
            self.cache[key] = self.backend.generate_json(purpose=purpose, prompt=prompt)
        return self.cache[key]


def metrics(ranks, n):
    return {"n": n, "hit_at_1": sum(r == 1 for r in ranks) / n, "hit_at_3": sum(r is not None and r <= 3 for r in ranks) / n, "mrr": sum(0 if r is None else 1 / r for r in ranks) / n}


def outcome_summary(results, case_ids, threshold):
    selected = []
    for case_id in case_ids:
        value = results[case_id]
        target = value.get("target_decision") or {}
        confidence = float(target.get("confidence") or 0.0)
        if confidence < threshold:
            value = {"state": "ABSTAINED_NO_TARGET", "repair_count": 0, "target_decision": target}
        selected.append(value)
    n = len(selected)
    accepted = [item for item in selected if item["state"] == "ACCEPTED"]
    generated = [item for item in selected if item.get("patch")]
    unsupported = [item for item in selected if item["state"] == "ABSTAINED_UNSUPPORTED_CLAIMS" or (item.get("critic") or {}).get("unsupported_claims") or item.get("deterministic_unsupported_claims")]
    target_violations = [item for item in selected if item.get("patch") and str((item.get("patch") or {}).get("target_document") or "") != str((item.get("target_decision") or {}).get("target_document") or "")]
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
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Frozen Gate 4 development-only S1 GPU study")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("/kaggle/working/s1-development"))
    parser.add_argument("--cache-dir", default=os.environ.get("HF_HOME", "/kaggle/working/hf-cache"))
    args = parser.parse_args()
    if not os.environ.get("HF_TOKEN"):
        raise RuntimeError("HF_TOKEN must be supplied in the environment")
    import numpy as np
    import torch
    random.seed(42); np.random.seed(42); torch.manual_seed(42); torch.cuda.manual_seed_all(42)
    root = args.root.resolve()
    if "confirmation" in str(args.output).casefold() or "gate6" in str(args.output).casefold():
        raise ValueError("S1 development output must not target confirmation or Gate 6")
    args.output.mkdir(parents=True, exist_ok=True)
    sampled = read_jsonl(root / "reports/final_v2/gate4/primary_sample.jsonl") + read_jsonl(root / "reports/final_v2/gate4/secondary_stress_sample.jsonl")
    gold = {}
    for split in ("train", "validation"):
        for row in read_jsonl(root / f"experiments/consolidated_enriched_training_v2/gold/{split}.jsonl"):
            gold[row["case_id"]] = row
    rows = []
    for item in sampled:
        row = dict(gold.get(item["case_id"], {})); row.update(item); rows.append(row)
    provider = BareGitRepositoryProvider(args.output / "repository_cache")
    groups = defaultdict(set)
    sources = {}
    for row in rows:
        source = resolve_pre_change_source(row, root=root); sources[row["case_id"]] = source
        if source.kind == "git_commit": groups[source.repository].add(source.revision)
    for repo, revisions in groups.items():
        availability = provider.ensure_commits(repo, revisions)
        if not all(availability.values()):
            raise RuntimeError(f"Explicit pre-change object unavailable in {repo}; no HEAD fallback permitted")

    corpora = {}
    for row in rows:
        source = sources[row["case_id"]]
        if source.kind == "git_commit":
            paths = provider.list_paths(source.repository, source.revision)
            read = lambda p, s=source: provider.read_text(s.repository, s.revision, p)
        else:
            local = Path(source.local_root)
            paths = [p.relative_to(local).as_posix() for p in local.rglob("*") if p.is_file()]
            read = lambda p, local=local: (local / Path(p)).read_text(encoding="utf-8", errors="replace")
        discovered = discover_candidates(paths, changed_paths=list(row.get("code_changed_files") or []), code_diff=str(row.get("code_diff_excerpt") or ""))[:64]
        chunks = []
        for path, tier, distance, overlap in discovered:
            chunks.extend(semantic_chunks(path, read(path), max_chars=4000, priority_tier=tier, distance=distance, identifier_overlap=overlap))
        corpora[row["case_id"]] = chunks

    dense = QwenDenseEncoder(cache_dir=args.cache_dir, batch_size=8)
    reranker = QwenReranker(cache_dir=args.cache_dir)
    retrieval = {}
    scores = {}
    for lexical_k in (5, 10):
        for dense_k in (5, 10):
            key = f"l{lexical_k}_d{dense_k}"
            retrieval[key] = {}
            ranks = []
            eligible = 0
            for row in rows:
                query = build_retrieval_query(row)
                hybrid = hybrid_retrieve(query, corpora[row["case_id"]], dense_encoder=dense, lexical_top_k=lexical_k, dense_top_k=dense_k)
                top = rerank_top_documents(query, hybrid, reranker=reranker)
                retrieval[key][row["case_id"]] = top
                target = row.get("synthetic_target_doc_path")
                if target:
                    eligible += 1
                    paths = [item.chunk.path for item in top]
                    ranks.append(paths.index(target) + 1 if target in paths else None)
            scores[key] = metrics(ranks, eligible)
    selected_key = sorted(scores, key=lambda k: (-scores[k]["hit_at_3"], -scores[k]["mrr"], -scores[k]["hit_at_1"], int(k.split("_")[0][1:]), int(k.split("_")[1][1:])))[0]
    del dense, reranker
    gc.collect()
    torch.cuda.empty_cache()

    backend = MemoizedBackend(QwenStructuredGenerator(cache_dir=args.cache_dir))
    outcomes = {}
    lexical_k = int(selected_key.split("_")[0][1:]); dense_k = int(selected_key.split("_")[1][1:])
    for variant in ("P1", "P2"):
        agent = S1Agent(backend, S1Configuration(lexical_k, dense_k, 3, 0.35, variant))
        outcomes[variant] = {}
        for row in rows:
            outcomes[variant][row["case_id"]] = agent.run(row, retrieval[selected_key][row["case_id"]], document_corpus=corpora[row["case_id"]])
    case_groups = {
        "all_development": [row["case_id"] for row in rows],
        "primary": [row["case_id"] for row in rows if row.get("sample_name") == "primary_natural_distribution"],
        "secondary": [row["case_id"] for row in rows if row.get("sample_name") != "primary_natural_distribution"],
    }
    development_metrics = {
        variant: {
            str(threshold): {group: outcome_summary(values, case_ids, threshold) for group, case_ids in case_groups.items()}
            for threshold in (0.35, 0.50, 0.65)
        }
        for variant, values in outcomes.items()
    }
    serializable_retrieval = {
        key: {case_id: [{"path": item.chunk.path, "heading": item.chunk.heading, "relevant_chunk": item.chunk.text, "priority_tier": item.chunk.priority_tier, "path_distance": item.chunk.path_distance, "identifier_overlap": item.chunk.identifier_overlap, "lexical_score": item.lexical_score, "dense_score": item.dense_score, "reranker_score": item.reranker_score} for item in items] for case_id, items in cases.items()}
        for key, cases in retrieval.items()
    }
    payload = {
        "status": "DEVELOPMENT_GPU_EVIDENCE_COMPLETE_SELECTION_PENDING",
        "confirmation_accessed": False,
        "gate6_row_level_human_data_accessed": False,
        "retrieval_metrics_controlled_only": scores,
        "selected_retrieval_key": selected_key,
        "threshold_derivation": "Runs produced at 0.35; 0.50/0.65 must replace any lower-confidence target with ABSTAINED_NO_TARGET without additional inference.",
        "prompt_selection": "Do not select from self-critic outputs alone; use deterministic diagnostics or a separately frozen blind development review.",
        "development_metrics": development_metrics,
        "retrieval": serializable_retrieval,
        "outcomes_at_threshold_0_35": outcomes,
    }
    (args.output / "s1_development_gpu_results.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "selected_retrieval_key": selected_key, "output": str(args.output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
