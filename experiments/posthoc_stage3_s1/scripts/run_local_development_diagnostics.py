from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

from experiments.posthoc_stage3_s1.scripts.repository_corpus import discover_candidates, resolve_pre_change_source
from experiments.posthoc_stage3_s1.scripts.retrieval import lexical_scores
from experiments.posthoc_stage3_s1.scripts.repository_corpus import DocumentChunk
from experiments.posthoc_stage3_s1.scripts.s1_pipeline import build_retrieval_query


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    output = root / "experiments/posthoc_stage3_s1/development"
    output.mkdir(parents=True, exist_ok=True)
    samples = read_jsonl(root / "reports/final_v2/gate4/primary_sample.jsonl") + read_jsonl(root / "reports/final_v2/gate4/secondary_stress_sample.jsonl")
    gold = {}
    for name in ("train", "validation"):
        for row in read_jsonl(root / f"experiments/consolidated_enriched_training_v2/gold/{name}.jsonl"):
            gold[row["case_id"]] = row
    ranks = []
    per_case = []
    for sampled in samples:
        base = gold.get(sampled["case_id"], {})
        if not base.get("synthetic_target_doc_path"):
            continue
        row = dict(base)
        row.update(sampled)
        source = resolve_pre_change_source(row, root=root)
        local_root = Path(source.local_root)
        paths = [item.relative_to(local_root).as_posix() for item in local_root.rglob("*") if item.is_file()]
        candidates = discover_candidates(paths, changed_paths=list(row.get("code_changed_files") or []), code_diff=str(row.get("code_diff_excerpt") or ""))
        chunks = []
        metadata = []
        for path, tier, distance, overlap in candidates:
            text = (local_root / Path(path)).read_text(encoding="utf-8", errors="replace")[:100_000]
            chunks.append(DocumentChunk(path, "", (), text, 0))
            metadata.append((tier, distance, overlap))
        scores = lexical_scores(build_retrieval_query(row), chunks)
        order = sorted(range(len(chunks)), key=lambda i: (-float(scores[i]), metadata[i][0], metadata[i][1], -metadata[i][2], chunks[i].path))
        ranked_paths = [chunks[i].path for i in order]
        target = base["synthetic_target_doc_path"]
        rank = ranked_paths.index(target) + 1 if target in ranked_paths else None
        if rank is not None:
            ranks.append(rank)
        per_case.append({"case_id": row["case_id"], "target_document": target, "lexical_rank": rank, "candidate_count": len(candidates)})
    n = len(per_case)
    results = {
        "status": "LOCAL_LEXICAL_ONLY_DEVELOPMENT_DIAGNOSTIC",
        "confirmation_accessed": False,
        "gate6_row_level_human_data_accessed": False,
        "population": "controlled Gate 4 development rows with legitimate synthetic target-document evidence",
        "n": n,
        "target_present": len(ranks),
        "target_hit_at_1": sum(rank <= 1 for rank in ranks) / n,
        "target_hit_at_3": sum(rank <= 3 for rank in ranks) / n,
        "target_hit_at_5": sum(rank <= 5 for rank in ranks) / n,
        "target_hit_at_10": sum(rank <= 10 for rank in ranks) / n,
        "mrr": sum(1 / rank for rank in ranks) / n,
        "limitations": "Filename/path-aware TF-IDF feasibility only; Qwen dense retrieval, reranking, target decisions, generation, critic, safety rates, and bounded selection require the GPU development run.",
        "membership_sha256": hashlib.sha256("\n".join(item["case_id"] for item in per_case).encode()).hexdigest(),
        "cases": per_case,
    }
    (output / "local_lexical_target_diagnostics.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output / "LOCAL_DEVELOPMENT_DIAGNOSTICS.md").write_text(
        "# S1 local development diagnostics\n\n"
        "This is a development-only, controlled-row, lexical-only feasibility diagnostic. It is not the S1 selected configuration and does not use confirmation or Gate 6 row-level human data.\n\n"
        f"- Eligible controlled target rows: **{n}**\n"
        f"- Target present in corpus: **{len(ranks)}/{n}**\n"
        f"- Lexical Hit@1: **{results['target_hit_at_1']:.3f}**\n"
        f"- Lexical Hit@3: **{results['target_hit_at_3']:.3f}**\n"
        f"- Lexical Hit@5: **{results['target_hit_at_5']:.3f}**\n"
        f"- Lexical Hit@10: **{results['target_hit_at_10']:.3f}**\n"
        f"- Lexical MRR: **{results['mrr']:.3f}**\n\n"
        "Dense retrieval, reranking, target decisions, generation, critic outcomes, and bounded configuration selection remain pending the GPU development run.\n",
        encoding="utf-8",
    )
    print(json.dumps({key: value for key, value in results.items() if key not in {"cases"}}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
