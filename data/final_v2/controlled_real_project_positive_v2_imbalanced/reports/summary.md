# controlled_real_project_positive_v2_imbalanced

This dataset contains PR-like, code-only mutations over four copied real projects. The linked `.git` directories were not copied. Each mutation is independent from a documented baseline and leaves docs-before unchanged.

- Rows: **2000**
- Positive: **2000**
- Excluded: **0**
- Quality gates: **PASS**

## Category distribution

| Category | Rows |
|---|---:|
| `api_reference` | 580 |
| `configuration` | 520 |
| `developer_setup` | 460 |
| `model_contract` | 300 |
| `other_documentation` | 140 |

## Project distribution

| Project | Rows |
|---|---:|
| `controlled-v2/jobfair-platform-copy` | 560 |
| `controlled-v2/rbi-related-parties-portal-copy` | 520 |
| `controlled-v2/rbi-test-forge-copy` | 430 |
| `controlled-v2/rbi-property-valuation-copy` | 490 |

## Important use constraint

Rows are controlled/synthetic positives over real-project copies. They are deliberately marked `training_eligible=false` and `merge_status=pending_owner_acceptance` until the owner accepts the examples and chooses a leakage-safe split strategy.
