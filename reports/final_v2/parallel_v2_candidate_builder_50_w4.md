# DocGuard GitHub PR Candidate Builder V2 Report

V2 candidate construction is leak-free with respect to final labels and PR outcome documentation routing.

- Status: `complete`
- Accepted candidates: `50`
- Scientific rejects: `0`
- Operational pending: `0`
- Resolved total: `50`
- Operational/client stats: `{'outbound_request_count': 0, 'cache_hit_count': 496, 'blob_cache_hit_count': 346, 'tree_request_count': 0, 'document_content_request_count': 0, 'request_retry_count': 0, 'total_backoff_seconds': 0.0, 'operational_failures': {}, 'stop_reason': None, 'stop_snapshot': {}, 'rest_fallback_count': 0, 'git_repository_init_count': 0, 'git_repository_cache_hit_count': 0, 'git_fetch_count': 0, 'git_fetch_failure_count': 0, 'git_tree_read_count': 0, 'git_blob_read_count': 0, 'git_blob_read_failure_count': 0, 'git_command_failure_count': 0, 'tree_cache_hit_count': 0, 'in_memory_blob_cache_hit_count': 0, 'singleflight_wait_count': 0, 'status': 'complete', 'completed_seed_count': 50, 'checkpoint_count': 1, 'resume_completed_seed_count': 0, 'operational_pending_count': 0, 'scientific_reject_count': 0, 'operational_pending_created_count': 0, 'stage_profile': {'checkpoint_write_seconds': {'count': 1, 'total_seconds': 0.127186, 'mean_seconds': 0.127186, 'p50_seconds': 0.127186, 'p95_seconds': 0.127186}, 'document_discovery_seconds': {'count': 50, 'total_seconds': 204.298762, 'mean_seconds': 4.085975, 'p50_seconds': 4.13785, 'p95_seconds': 5.568514}, 'pull_files_seconds': {'count': 50, 'total_seconds': 1.856116, 'mean_seconds': 0.037122, 'p50_seconds': 0.004444, 'p95_seconds': 0.328412}, 'pull_metadata_seconds': {'count': 50, 'total_seconds': 1.827307, 'mean_seconds': 0.036546, 'p50_seconds': 0.007975, 'p95_seconds': 0.210599}, 'rest_cache_probe_seconds': {'count': 100, 'total_seconds': 3.680768, 'mean_seconds': 0.036808, 'p50_seconds': 0.005499, 'p95_seconds': 0.307429}, 'seed_total_seconds': {'count': 50, 'total_seconds': 208.032946, 'mean_seconds': 4.160659, 'p50_seconds': 4.264087, 'p95_seconds': 5.658475}}, 'workers': 4, 'rest_max_inflight': 4}`
- Max generator doc files: `12`
- Max generator doc chars per file: `1500`
- Language counts: `{'go': 50}`

Candidate records contain no `gold_*` fields. `docs_before_excerpt` is retrieved from `base_sha` using neutral documentation paths and code-path hints only; it never prioritizes `docs_changed_files`, `docs_diff_excerpt`, or `docs_after_excerpt`.