# External CoDocBench Sample Audit 2026-08

- Records written: `500`
- Skipped records: `0`
- Source dataset: `codocbench` / `guineapig/codocbench`
- Output: `data\external\codocbench_sample_500.jsonl`
- Requested limit: `500`
- Shuffle: `True`
- Seed: `42`
- Max per project: `50`
- Exclude whitespace-only: `True`
- Whitespace-only skipped count: `0`
- Commit date range: `1998-06-18 14:24:28+00:00` to `2024-05-15 08:19:08-04:00`

## Split Distribution

- `train`: 500

## Language Distribution

- `python`: 500

## Repository Distribution

- `django`: 33
- `chainer`: 32
- `core`: 31
- `cpython`: 26
- `ray`: 25
- `faceswap`: 24
- `models`: 24
- `ccxt`: 23
- `freqtrade`: 21
- `scikit-image`: 20
- `scikit-learn`: 16
- `localstack`: 15
- `readthedocs.org`: 14
- `speechbrain`: 14
- `aws-sam-cli`: 13
- `Theano`: 9
- `gensim`: 8
- `datasets`: 8
- `pytorch-lightning`: 8
- `Python`: 7

## Owner Distribution

- `django`: 33
- `chainer`: 32
- `home-assistant`: 31
- `python`: 26
- `ray-project`: 25
- `deepfakes`: 24
- `tensorflow`: 24
- `ccxt`: 23
- `freqtrade`: 21
- `scikit-image`: 20
- `scikit-learn`: 16
- `localstack`: 15
- `readthedocs`: 14
- `speechbrain`: 14
- `aws`: 13
- `huggingface`: 10
- `Theano`: 9
- `piskvorky`: 8
- `Lightning-AI`: 8
- `TheAlgorithms`: 7

## Top 10 Repositories

- `django`: 33
- `chainer`: 32
- `core`: 31
- `cpython`: 26
- `ray`: 25
- `faceswap`: 24
- `models`: 24
- `ccxt`: 23
- `freqtrade`: 21
- `scikit-image`: 20

## Label Source Distribution

- `strong_positive_code_doc_cochange`: 500

## Missing Field Counts

None.

## Mapping Warnings

None.

## Truncated Examples

### codocbench-ccxt-dcf03a6defa85b205e46bddf47975aaff2990509-currencycom.cancel_order-0

- repository: `ccxt`
- commit: `dcf03a6defa85b205e46bddf47975aaff2990509`
- label_source: `strong_positive_code_doc_cochange`
- code_diff:   def cancel_order(self, id: str, symbol: Str = None, params={}):\n          \n          \n          \n-         self.check_required_symbol('cancelOrder', symbol)\n+         if symbol is None:\n+             raise ArgumentsRequired(self.id ...[truncated]
- doc_diff:   cancels an open order\n          :param str id: order id\n          :param str symbol: unified symbol of the market the order was made in\n          :param dict [params]: extra parameters specific to the currencycom api endpoint\n-       ...[truncated]

### codocbench-readthedocs.org-24adafcd88d76ab6dde1363e87a5fca00af3fdc0-remove_indexed_files-1

- repository: `readthedocs.org`
- commit: `24adafcd88d76ab6dde1363e87a5fca00af3fdc0`
- label_source: `strong_positive_code_doc_cochange`
- code_diff: - def remove_indexed_files(model, version):\n+ def remove_indexed_files(model, version, build):\n?                                        +++++++\n\n+     \n+     \n      \n  \n      if not DEDConfig.autosync_enabled():\n          log.info(...[truncated]
- doc_diff:   Remove files from the version from the search index.\n+ \n+     This excludes files from the current build.

### codocbench-saleor-f8df1aa0dbed6846f41788f92eb8d61522869c91-requestor_has_access-2

- repository: `saleor`
- commit: `f8df1aa0dbed6846f41788f92eb8d61522869c91`
- label_source: `strong_positive_code_doc_cochange`
- code_diff:   def requestor_has_access(\n      requestor: Union["User", "App"], owner: Optional["User"], *perms\n- ):\n+ ) -> bool:\n      \n- \n      \n      return requestor == owner or has_one_of_permissions(requestor, perms)
- doc_diff:   Check if requestor can access data.\n  \n-     Args:\n-         requestor: requestor user or app\n?     ^^^            ^\n\n+     :param requestor: Requestor user or app.\n?     ^^^^^^            ^                    +\n\n-         owner:...[truncated]

### codocbench-readthedocs.org-9a911f9c3c4559dc9dfa81623db0a7c44ce2b4f9-SphinxParser._generate_domains_data-3

- repository: `readthedocs.org`
- commit: `9a911f9c3c4559dc9dfa81623db0a7c44ce2b4f9`
- label_source: `strong_positive_code_doc_cochange`
- code_diff:   def _generate_domains_data(self, body):\n          \n          \n          \n  \n          domain_data = {}\n          dl_tags = body.css('dl')\n+         number_of_domains = 0\n  \n          for dl_tag in dl_tags:\n  \n              dt =...[truncated]
- doc_diff:   Generate sphinx domain objects' docstrings.\n  \n          Returns a dict with the generated data.\n          The returned dict is in the following form::\n  \n              {\n                  "domain-id-1": "docstrings for the domain-i...[truncated]

### codocbench-gensim-5dbfb1e231e72a8f4ebc1bf099675116848f1d05-SoftCosineSimilarity.__init__-4

- repository: `gensim`
- commit: `5dbfb1e231e72a8f4ebc1bf099675116848f1d05`
- label_source: `strong_positive_code_doc_cochange`
- code_diff: - def __init__(self, corpus, similarity_matrix, num_best=None, chunksize=256, normalized=(True, True)):\n?                                                                                        ^^^^  --------\n\n+ def __init__(self, corpus,...[truncated]
- doc_diff:   Parameters\n          ----------\n          corpus: iterable of list of (int, float)\n              A list of documents in the BoW format.\n          similarity_matrix : :class:`gensim.similarities.SparseTermSimilarityMatrix`\n           ...[truncated]

## Difference From Synthetic v0.4

CoDocBench records are real code/documentation or code/docstring co-changes. They should be used as real-world validation for code-comment/docstring update behavior, not as a direct replacement for DocGuard's synthetic project-level Markdown documentation benchmark.