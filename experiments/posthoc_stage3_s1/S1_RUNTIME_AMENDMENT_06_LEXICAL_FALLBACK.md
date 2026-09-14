# S1 runtime amendment 06: compute-constrained lexical retrieval fallback

Status: **FROZEN BEFORE GENERATION, DEVELOPMENT METRICS, AND PROMPT SELECTION**.

Scientific label: **POST-HOC S1 COMPUTE-CONSTRAINED LEXICAL RETRIEVAL CHALLENGER**. This is neither the originally preregistered neural-reranker S1 nor a new unbiased confirmation.

The neural 8,192-token reranker is physically infeasible on the available Tesla T4 runtime. Amendment 03 correctly reached single-item inference, and Amendment 05 verified that last-token-only logits preserve the yes/no probability, but individual forwards still OOM inside `scaled_dot_product_attention`. At this boundary generation had zero rows; neural reranker metrics and development metrics had not been produced; prompt selection had not occurred. Partial reranker scores were not inspected or used to choose this fallback.

## Frozen active retrieval

For every frozen development case, use the unchanged reconstructed repository documentation corpus and unchanged retrieval query. Compute the existing `lexical_scores()`, then order chunks by descending lexical score, ascending document path, and ascending `chunk_index`. Traverse that order once, retain the first/highest-ranked chunk for each document path, and select the first three distinct paths. Pass those three `RankedChunk` candidates into the unchanged S1 target-selection and generation pipeline. Dense scores and neural reranker scores are null and do not participate; no fusion rule is introduced.

The only empirical motivation is the pre-existing Phase-0 audit on the 79 development rows with legitimate controlled target-document evidence: Hit@1 `0.9746835443037974`, Hit@3 `1.0`, Hit@5 `1.0`, Hit@10 `1.0`, and MRR `0.9873417721518988`. Before generation, the runtime recomputes Hit@1, Hit@3 and MRR from the actual active lexical top-3 results on exactly those 79 rows and requires exact deterministic equality. Any mismatch fails closed. The 121 natural rows have no target-document ground truth and are excluded from target accuracy.

## Runtime and historical evidence

When all 200 corpus checkpoints exist, neither the embedding model nor reranker model is loaded. Dense embedding artifacts may remain but are not required. Reranker completion is not required. The global and worker reranker JSONL files remain untouched as historical runtime evidence. At Amendment-06 startup, the runtime records only the number of newline-complete rows in each file; it does not parse or consume their score values for selection or execution.

## Preserved downstream protocol

Amendment 04 remains exact. Phase A runs P1 and P2 on the deterministic 25-primary/25-secondary subset, extends to 75 and at most 100 only if fewer than 20 pairs are reviewable, creates the identity-blind human comparison, and stops at `PROMPT_SELECTION_BLIND_REVIEW_REQUIRED`. Phase B runs only the human-selected prompt until it has all 200 development results; the losing prompt is not required outside the paired subset. Thresholds remain 0.35/0.50/0.65.

The pinned Qwen2.5-Coder-14B-Instruct generator/critic and revision, P1/P2 hashes, structured schemas, one schema retry, one semantic repair, corpus construction, pre-change reconstruction, frozen membership and seed remain unchanged. Confirmation and Gate 6 row-level human data remain inaccessible. Original freeze and Amendments 01–05 remain preserved in Git history.
