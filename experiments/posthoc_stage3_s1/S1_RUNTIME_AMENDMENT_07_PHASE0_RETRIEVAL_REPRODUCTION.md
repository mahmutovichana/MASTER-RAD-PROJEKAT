# S1 Runtime Amendment 07 — Exact Phase-0 retrieval reproduction

## Status

**PRE-GENERATION IMPLEMENTATION CORRECTION TO AMENDMENT 06**

This amendment was frozen before generation, prompt selection, or development metrics. Confirmation remains inaccessible, and no Gate 6 row-level human data is accessed.

## Reason for correction

Amendment 06 incorrectly applied the frozen lexical scorer to semantic chunks and then deduplicated document paths. That implementation produced an observed controlled result of Hit@1/Hit@3/MRR = 1.0/1.0/1.0. This result is explicitly not adopted and is not evidence for method selection. The mismatch was identified by comparing the Amendment 06 source with the already-frozen Phase-0 implementation at commit `38f9afb479f738081301172176d3133e4056bd7c`.

Frozen Phase 0 applied `lexical_scores` to one whole-file representation for every discovered candidate document. Amendment 07 restores that exact procedure.

## Active retrieval

Document ranking and representative-section localization are separate operations.

For document ranking, the exact pre-change source and frozen `discover_candidates` semantics are used. Each candidate becomes one `DocumentChunk(path, "", (), text[:100_000], 0)` carrying its priority tier, path distance, and identifier overlap. Documents are ordered by:

1. descending lexical score;
2. ascending priority tier;
3. ascending path distance;
4. descending identifier overlap;
5. ascending document path.

The first three document paths are frozen before localization. Controlled rows use the exact authoritative Phase-0 candidate population. Natural rows may retain the existing locality-ordered S1 candidate cap because they have no target ground truth.

For representative-section localization, existing semantic chunks are scored only within each already-selected document. The highest lexical score wins, with ascending `chunk_index` as the deterministic tie-break. This step cannot change top-three membership or order. The downstream `RankedChunk.lexical_score` remains the document-level score, and the complete semantic `document_corpus` remains available for same-document style examples.

Dense embeddings, the reranker, and partial reranker scores do not participate and their models are not loaded. Historical checkpoints remain preserved.

## Mandatory validation before generation

The frozen artifact `development/local_lexical_target_diagnostics.json` is a validation oracle only. For all 79 controlled cases, membership, target document, and document rank must match case by case. Aggregate Hit@1, Hit@3, Hit@5, Hit@10, and MRR must equal `0.9746835443037974`, `1.0`, `1.0`, `1.0`, and `0.9873417721518988`. `CRPP2-RPP-API_REFERENCE-220` and `CRPP2-JOB-API_REFERENCE-188` must both remain rank 2. Any mismatch fails closed before generator loading.

At freeze time, generation rows were 0, prompt selection had not occurred, development metrics had not been produced, `confirmation_accessed=false`, and `gate6_row_level_human_data_accessed=false`. Amendment 04 Phase A/B, the pinned generator revision, P1/P2, thresholds, schema retry, semantic repair, seed, and 200-case membership are unchanged.
