# DocGuard GitHub PR Candidate Builder V2 Report

V2 candidate construction is leak-free with respect to final labels and PR outcome documentation routing.

- Status: `partial`
- Accepted candidates: `180`
- Rejected seeds: `1`
- Operational/client stats: `{'outbound_request_count': 7, 'cache_hit_count': 1822, 'blob_cache_hit_count': 1312, 'tree_request_count': 0, 'document_content_request_count': 0, 'request_retry_count': 0, 'total_backoff_seconds': 0.0, 'operational_failures': {'403': 1}, 'stop_reason': 'primary_rate_limit_exhausted', 'stop_snapshot': {'status_code': 403, 'url': 'https://api.github.com/repos/apache/superset/pulls/42411', 'retry_after': None, 'rate_limit_remaining': 0, 'rate_limit_reset': 1787840066, 'rate_limit_resource': 'core', 'is_authentication_failure': False, 'is_primary_rate_limit': True, 'is_secondary_rate_limit': False, 'is_transient': False}, 'rest_fallback_count': 0, 'git_repository_init_count': 0, 'git_repository_cache_hit_count': 404, 'git_fetch_count': 0, 'git_fetch_failure_count': 0, 'git_tree_read_count': 37, 'git_blob_read_count': 367, 'git_blob_read_failure_count': 0, 'git_command_failure_count': 0, 'status': 'partial', 'completed_seed_count': 181, 'checkpoint_count': 4, 'resume_completed_seed_count': 0}`
- Max generator doc files: `12`
- Max generator doc chars per file: `1500`
- Language counts: `{'go': 50, 'typescript': 100, 'python': 30}`

Candidate records contain no `gold_*` fields. `docs_before_excerpt` is retrieved from `base_sha` using neutral documentation paths and code-path hints only; it never prioritizes `docs_changed_files`, `docs_diff_excerpt`, or `docs_after_excerpt`.