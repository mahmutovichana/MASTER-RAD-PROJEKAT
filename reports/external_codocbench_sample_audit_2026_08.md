# External CoDocBench Sample Audit 2026-08

- Records: `100`
- Source dataset: `codocbench` / `guineapig/codocbench`
- Output: `data\external\codocbench_sample.jsonl`

## Split Distribution

- `train`: 100

## Language Distribution

- `python`: 100

## Repository Distribution

- `faceswap`: 14
- `aws-sam-cli`: 8
- `ray`: 7
- `ccxt`: 6
- `models`: 6
- `speechbrain`: 6
- `core`: 5
- `datasets`: 5
- `cpython`: 5
- `mycroft-core`: 5
- `python-binance`: 4
- `Python`: 3
- `chainer`: 3
- `pytorch-image-models`: 2
- `localstack`: 2
- `readthedocs.org`: 2
- `Cura`: 2
- `pytorch-lightning`: 1
- `wttr.in`: 1
- `openpilot`: 1

## Label Source Distribution

- `strong_positive_code_doc_cochange`: 100

## Missing Field Counts


## Mapping Warnings

None.

## Truncated Examples

### codocbench-ccxt-dcf03a6defa85b205e46bddf47975aaff2990509-oceanex.fetch_orders-0

- repository: `ccxt`
- commit: `dcf03a6defa85b205e46bddf47975aaff2990509`
- label_source: `strong_positive_code_doc_cochange`
- code_diff:   def fetch_orders(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Order]:\n          \n          \n          \n-         self.check_required_symbol('fetchOrders', symbol)\n+         if symbol is None:\n+ ...[truncated]
- doc_diff:   fetches information on multiple orders made by the user\n          :see: https://api.oceanex.pro/doc/v1/#order-status-with-filters-post\n          :param str symbol: unified market symbol of the market orders were made in\n          :para...[truncated]

### codocbench-pytorch-lightning-c76a95ea127bba40826718c22c0c24fb711cab97-test_accelerator_set_when_using_tpu-1

- repository: `pytorch-lightning`
- commit: `c76a95ea127bba40826718c22c0c24fb711cab97`
- label_source: `strong_positive_code_doc_cochange`
- code_diff: - def test_accelerator_set_when_using_tpu(tpu_cores):\n?                                         ^^^^ --\n\n+ def test_accelerator_set_when_using_tpu(devices):\n?                                         ^^^^\n\n      \n-     assert isinstan...[truncated]
- doc_diff: - Test if the accelerator is set to `tpu` when tpu_cores is not None.\n?                                              ^^^^ --\n\n+ Test if the accelerator is set to `tpu` when devices is not None.\n?                                         ...[truncated]

### codocbench-core-91df9434d02b680388b168f8ed99bc9e7583d9ec-StoredData.__init__-2

- repository: `core`
- commit: `91df9434d02b680388b168f8ed99bc9e7583d9ec`
- label_source: `strong_positive_code_doc_cochange`
- code_diff: - def __init__(self, data_file: str) -> None:\n+ def __init__(self, hass: HomeAssistant, legacy_data_file: str) -> None:\n?                    ++++++++++++++++++++++++++++\n\n          \n-         self._data_file = data_file\n+         self...[truncated]
- doc_diff: - Initialize pickle data storage.\n?            -------\n\n+ Initialize data storage.

### codocbench-ccxt-79875da007ed3a880b5b4674d307fe052c269a44-bitmex.fetch_funding_rate_history-3

- repository: `ccxt`
- commit: `79875da007ed3a880b5b4674d307fe052c269a44`
- label_source: `strong_positive_code_doc_cochange`
- code_diff:   def fetch_funding_rate_history(self, symbol=None, since=None, limit=None, params={}):\n          \n          \n          \n          self.load_markets()\n          request = {}\n          market = None\n          if symbol in self.currenc...[truncated]
- doc_diff:   Fetches the history of funding rates\n          :param str|None symbol: unified symbol of the market to fetch the funding rate history for\n          :param int|None since: timestamp in ms of the earliest funding rate to fetch\n          ...[truncated]

### codocbench-ccxt-bac44507bafca2ee864c2f890997ddeade6eacc6-bitmex.fetch_my_trades-4

- repository: `ccxt`
- commit: `bac44507bafca2ee864c2f890997ddeade6eacc6`
- label_source: `strong_positive_code_doc_cochange`
- code_diff:   def fetch_my_trades(self, symbol: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):\n          \n          \n          \n          self.load_markets()\n+         paginate = False\n+         pagina...[truncated]
- doc_diff: + see https://www.bitmex.com/api/explorer/#not /Execution/Execution_getTradeHistory\n- fetch all trades made by the user\n+         fetch all trades made by the user\n? ++++++++\n\n          :param str symbol: unified market symbol\n       ...[truncated]

## Difference From Synthetic v0.4

CoDocBench records are real code/documentation or code/docstring co-changes. They should be used as real-world validation for code-comment/docstring update behavior, not as a direct replacement for DocGuard's synthetic project-level Markdown documentation benchmark.