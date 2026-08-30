# DocGuard GitHub PR Candidate Builder V2 Report

V2 candidate construction is leak-free with respect to final labels and PR outcome documentation routing.

- Status: `retry_operational_pending`
- Accepted candidates: `17880`
- Scientific rejects: `120`
- Operational pending: `0`
- Resolved total: `18000`
- Operational/client stats: `{'outbound_request_count': 528, 'cache_hit_count': 509, 'blob_cache_hit_count': 505, 'tree_request_count': 0, 'document_content_request_count': 0, 'request_retry_count': 0, 'total_backoff_seconds': 0.0, 'operational_failures': {}, 'stop_reason': None, 'stop_snapshot': {}, 'rest_fallback_count': 0, 'git_repository_init_count': 0, 'git_repository_cache_hit_count': 609, 'git_fetch_count': 0, 'git_fetch_failure_count': 0, 'git_tree_read_count': 219, 'git_blob_read_count': 390, 'git_blob_read_failure_count': 0, 'git_command_failure_count': 0, 'tree_cache_hit_count': 92, 'in_memory_blob_cache_hit_count': 1552, 'singleflight_wait_count': 0, 'processed_pending': 265, 'operational_pending_resolved_count': 350, 'operational_pending_retry_failure_count': 0, 'operational_pending_count': 0, 'accepted_added': 265, 'scientific_rejects_added': 0}`
- Max generator doc files: `12`
- Max generator doc chars per file: `1500`
- Language counts: `{'go': 260, 'python': 7827, 'typescript': 9793}`

Candidate records contain no `gold_*` fields. `docs_before_excerpt` is retrieved from `base_sha` using neutral documentation paths and code-path hints only; it never prioritizes `docs_changed_files`, `docs_diff_excerpt`, or `docs_after_excerpt`.