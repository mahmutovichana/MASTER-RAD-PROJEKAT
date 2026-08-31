# Controlled real-project positive dataset v1

This dataset contains PR-like, code-only mutations over four copied real projects. The linked `.git` directories were not copied. Each mutation is independent from a documented baseline and leaves docs-before unchanged.

- Rows: **2000**
- Positive: **2000**
- Excluded: **0**
- Quality gates: **PASS**

## Category distribution

| Category | Rows |
|---|---:|
| `api_reference` | 400 |
| `configuration` | 400 |
| `developer_setup` | 400 |
| `model_contract` | 400 |
| `other_documentation` | 400 |

## Project distribution

| Project | Rows |
|---|---:|
| `controlled/jobfair-platform-copy` | 500 |
| `controlled/rbi-related-parties-portal-copy` | 500 |
| `controlled/rbi-test-forge-copy` | 500 |
| `controlled/rbi-property-valuation-copy` | 500 |

## Important use constraint

Rows are controlled/synthetic positives over real-project copies. They are deliberately marked `training_eligible=false` and `merge_status=pending_owner_acceptance` until the owner accepts the examples and chooses a leakage-safe split strategy.
