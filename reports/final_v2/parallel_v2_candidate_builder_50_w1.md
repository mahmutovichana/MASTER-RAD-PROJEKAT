# DocGuard GitHub PR Candidate Builder V2 Report

V2 candidate construction is leak-free with respect to final labels and PR outcome documentation routing.

- Status: `complete`
- Accepted candidates: `50`
- Scientific rejects: `0`
- Operational pending: `0`
- Resolved total: `50`
- Operational/client stats: `{'outbound_request_count': 0, 'cache_hit_count': 496, 'blob_cache_hit_count': 346, 'tree_request_count': 0, 'document_content_request_count': 0, 'request_retry_count': 0, 'total_backoff_seconds': 0.0, 'operational_failures': {}, 'stop_reason': None, 'stop_snapshot': {}, 'rest_fallback_count': 0, 'git_repository_init_count': 0, 'git_repository_cache_hit_count': 0, 'git_fetch_count': 0, 'git_fetch_failure_count': 0, 'git_tree_read_count': 0, 'git_blob_read_count': 0, 'git_blob_read_failure_count': 0, 'git_command_failure_count': 0, 'tree_cache_hit_count': 0, 'in_memory_blob_cache_hit_count': 0, 'singleflight_wait_count': 0, 'status': 'complete', 'completed_seed_count': 50, 'checkpoint_count': 1, 'resume_completed_seed_count': 0, 'operational_pending_count': 0, 'scientific_reject_count': 0, 'operational_pending_created_count': 0, 'stage_profile': {'checkpoint_write_seconds': {'count': 1, 'total_seconds': 0.070544, 'mean_seconds': 0.070544, 'p50_seconds': 0.070544, 'p95_seconds': 0.070544}, 'document_discovery_seconds': {'count': 50, 'total_seconds': 50.416212, 'mean_seconds': 1.008324, 'p50_seconds': 0.953278, 'p95_seconds': 2.050016}, 'pull_files_seconds': {'count': 50, 'total_seconds': 1.706078, 'mean_seconds': 0.034122, 'p50_seconds': 0.033185, 'p95_seconds': 0.051874}, 'pull_metadata_seconds': {'count': 50, 'total_seconds': 3.645468, 'mean_seconds': 0.072909, 'p50_seconds': 0.06942, 'p95_seconds': 0.107388}, 'rest_cache_probe_seconds': {'count': 100, 'total_seconds': 5.347406, 'mean_seconds': 0.053474, 'p50_seconds': 0.050365, 'p95_seconds': 0.092285}, 'seed_total_seconds': {'count': 50, 'total_seconds': 55.813572, 'mean_seconds': 1.116271, 'p50_seconds': 1.067889, 'p95_seconds': 2.179856}}, 'workers': 1, 'rest_max_inflight': 1}`
- Max generator doc files: `12`
- Max generator doc chars per file: `1500`
- Language counts: `{'go': 50}`

Candidate records contain no `gold_*` fields. `docs_before_excerpt` is retrieved from `base_sha` using neutral documentation paths and code-path hints only; it never prioritizes `docs_changed_files`, `docs_diff_excerpt`, or `docs_after_excerpt`.