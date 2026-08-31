# Current Training Provenance Audit

- Corpus rows: `21080`
- Positive rows: `1885` (`8.94%`)

## Source status

| Source | Rows | Protocol status |
|---|---:|---|
| `historical_300_gold_unique` | 3 | historical_gold_not_current_protocol_reviewed |
| `historical_4k_unique` | 1998 | historical_protocol_derived_not_current_protocol_reviewed |
| `natural_17880` | 17880 | current_docs_before_review |
| `targeted_enrichment_1199` | 1199 | current_docs_before_review |

The corpus is suitable as a training-enrichment pool, but historical rows are explicitly not current-protocol natural gold. No controlled synthetic rows are included in this corpus yet. Original natural data remains untouched.

- Manifest validation errors: `0`
- Duplicate rows skipped during consolidation: `2361`
- Duplicate label conflicts recorded: `1938`
