# DocGuard GitHub PR Candidate Builder V2 Report

V2 candidate construction is leak-free with respect to final labels and PR outcome documentation routing.

- Status: `ok`
- Accepted candidates: `50`
- Rejected seeds: `0`
- Operational/client stats: `{'outbound_request_count': 0, 'cache_hit_count': 496, 'blob_cache_hit_count': 346, 'tree_request_count': 0, 'document_content_request_count': 0, 'request_retry_count': 0, 'total_backoff_seconds': 0.0, 'operational_failures': {}, 'stop_reason': None, 'stop_snapshot': {}, 'rest_fallback_count': 0, 'git_repository_init_count': 0, 'git_repository_cache_hit_count': 0, 'git_fetch_count': 0, 'git_fetch_failure_count': 0, 'git_tree_read_count': 0, 'git_blob_read_count': 0, 'git_blob_read_failure_count': 0, 'git_command_failure_count': 0, 'status': 'ok', 'completed_seed_count': 50, 'checkpoint_count': 2, 'resume_completed_seed_count': 0}`
- Max generator doc files: `12`
- Max generator doc chars per file: `1500`
- Language counts: `{'go': 50}`

Candidate records contain no `gold_*` fields. `docs_before_excerpt` is retrieved from `base_sha` using neutral documentation paths and code-path hints only; it never prioritizes `docs_changed_files`, `docs_diff_excerpt`, or `docs_after_excerpt`.