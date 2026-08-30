# DocGuard GitHub PR Candidate Builder V2 Report

V2 candidate construction is leak-free with respect to final labels and PR outcome documentation routing.

- Status: `complete`
- Accepted candidates: `50`
- Scientific rejects: `0`
- Operational pending: `0`
- Resolved total: `50`
- Operational/client stats: `{'outbound_request_count': 0, 'cache_hit_count': 496, 'blob_cache_hit_count': 346, 'tree_request_count': 0, 'document_content_request_count': 0, 'request_retry_count': 0, 'total_backoff_seconds': 0.0, 'operational_failures': {}, 'stop_reason': None, 'stop_snapshot': {}, 'rest_fallback_count': 0, 'git_repository_init_count': 0, 'git_repository_cache_hit_count': 0, 'git_fetch_count': 0, 'git_fetch_failure_count': 0, 'git_tree_read_count': 0, 'git_blob_read_count': 0, 'git_blob_read_failure_count': 0, 'git_command_failure_count': 0, 'tree_cache_hit_count': 0, 'in_memory_blob_cache_hit_count': 0, 'singleflight_wait_count': 0, 'status': 'complete', 'completed_seed_count': 50, 'checkpoint_count': 1, 'resume_completed_seed_count': 0, 'operational_pending_count': 0, 'scientific_reject_count': 0, 'operational_pending_created_count': 0, 'stage_profile': {'checkpoint_write_seconds': {'count': 1, 'total_seconds': 0.083788, 'mean_seconds': 0.083788, 'p50_seconds': 0.083788, 'p95_seconds': 0.083788}, 'document_discovery_seconds': {'count': 50, 'total_seconds': 590.905471, 'mean_seconds': 11.818109, 'p50_seconds': 8.638321, 'p95_seconds': 26.604207}, 'pull_files_seconds': {'count': 50, 'total_seconds': 15.967316, 'mean_seconds': 0.319346, 'p50_seconds': 0.192666, 'p95_seconds': 1.138104}, 'pull_metadata_seconds': {'count': 50, 'total_seconds': 11.329654, 'mean_seconds': 0.226593, 'p50_seconds': 0.053863, 'p95_seconds': 0.967514}, 'rest_cache_probe_seconds': {'count': 100, 'total_seconds': 27.292859, 'mean_seconds': 0.272929, 'p50_seconds': 0.096633, 'p95_seconds': 1.138035}, 'seed_total_seconds': {'count': 50, 'total_seconds': 618.291675, 'mean_seconds': 12.365833, 'p50_seconds': 9.27038, 'p95_seconds': 26.856111}}, 'workers': 8, 'rest_max_inflight': 4}`
- Max generator doc files: `12`
- Max generator doc chars per file: `1500`
- Language counts: `{'go': 50}`

Candidate records contain no `gold_*` fields. `docs_before_excerpt` is retrieved from `base_sha` using neutral documentation paths and code-path hints only; it never prioritizes `docs_changed_files`, `docs_diff_excerpt`, or `docs_after_excerpt`.