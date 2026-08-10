# CoDocBench Schema Inspection 2026-08

- Dataset: `guineapig/codocbench`
- Status: `ok`
- Available configs: default
- Available splits: train
- Column names: file, function, version_data, diff_code, diff_docstring, whitespace_only_code, whitespace_only_docstring, file_path, filename, project, owner
- Approximate inspected rows: `5`

## Sample Records

### Sample 1

Keys: `file, function, version_data, diff_code, diff_docstring, whitespace_only_code, whitespace_only_docstring, file_path, filename, project, owner`

- `file`: python_ccxt_oceanex.py
- `function`: oceanex.fetch_orders
- `version_data`: [{'v124': {'docstring_lines': {'start_line': 679, 'end_line': 688}, 'code_lines': {'start_line': 688, 'end_line': 709}}, 'commit_date_time': '2023-11-16 12:46:12+00:00', 'commit_sha': '8d2f99100013351c73cf0629d66e28e7a2e45c0a', 'commit_mess...[truncated]
- `diff_code`:   def fetch_orders(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Order]:\n          \n          \n          \n-         self.check_required_symbol('fetchOrders', symbol)\n+         if symbol is None:\n+ ...[truncated]
- `diff_docstring`:   fetches information on multiple orders made by the user\n          :see: https://api.oceanex.pro/doc/v1/#order-status-with-filters-post\n          :param str symbol: unified market symbol of the market orders were made in\n          :para...[truncated]
- `whitespace_only_code`: False
- `whitespace_only_docstring`: False
- `file_path`: python/ccxt/oceanex.py
- `filename`: oceanex.py
- `project`: ccxt
- `owner`: ccxt

### Sample 2

Keys: `file, function, version_data, diff_code, diff_docstring, whitespace_only_code, whitespace_only_docstring, file_path, filename, project, owner`

- `file`: tests_tests_pytorch_models_test_tpu.py
- `function`: test_accelerator_set_when_using_tpu
- `version_data`: [{'v85': {'docstring_lines': {'start_line': 266, 'end_line': 268}, 'code_lines': {'start_line': 268, 'end_line': 276}}, 'commit_date_time': '2022-10-04 22:54:14+00:00', 'commit_sha': '7ef87464ddd740f8af8388bd95130066c65874da', 'commit_messa...[truncated]
- `diff_code`: - def test_accelerator_set_when_using_tpu(tpu_cores):\n?                                         ^^^^ --\n\n+ def test_accelerator_set_when_using_tpu(devices):\n?                                         ^^^^\n\n      \n-     assert isinstan...[truncated]
- `diff_docstring`: - Test if the accelerator is set to `tpu` when tpu_cores is not None.\n?                                              ^^^^ --\n\n+ Test if the accelerator is set to `tpu` when devices is not None.\n?                                         ...[truncated]
- `whitespace_only_code`: False
- `whitespace_only_docstring`: False
- `file_path`: tests/tests_pytorch/models/test_tpu.py
- `filename`: test_tpu.py
- `project`: pytorch-lightning
- `owner`: Lightning-AI

### Sample 3

Keys: `file, function, version_data, diff_code, diff_docstring, whitespace_only_code, whitespace_only_docstring, file_path, filename, project, owner`

- `file`: homeassistant_components_feedreader___init__.py
- `function`: StoredData.__init__
- `version_data`: [{'v35': {'docstring_lines': {'start_line': 224, 'end_line': 226}, 'code_lines': {'start_line': 226, 'end_line': 231}}, 'commit_date_time': '2023-04-28 21:16:08+02:00', 'commit_sha': 'c303487c1bf234bad2901882476dceefec2243a9', 'commit_messa...[truncated]
- `diff_code`: - def __init__(self, data_file: str) -> None:\n+ def __init__(self, hass: HomeAssistant, legacy_data_file: str) -> None:\n?                    ++++++++++++++++++++++++++++\n\n          \n-         self._data_file = data_file\n+         self...[truncated]
- `diff_docstring`: - Initialize pickle data storage.\n?            -------\n\n+ Initialize data storage.
- `whitespace_only_code`: False
- `whitespace_only_docstring`: False
- `file_path`: homeassistant/components/feedreader/__init__.py
- `filename`: __init__.py
- `project`: core
- `owner`: home-assistant

### Sample 4

Keys: `file, function, version_data, diff_code, diff_docstring, whitespace_only_code, whitespace_only_docstring, file_path, filename, project, owner`

- `file`: python_ccxt_bitmex.py
- `function`: bitmex.fetch_funding_rate_history
- `version_data`: [{'v255': {'docstring_lines': {'start_line': 2369, 'end_line': 2382}, 'code_lines': {'start_line': 2382, 'end_line': 2420}}, 'commit_date_time': '2022-06-15 02:49:29+00:00', 'commit_sha': '9fb56f853b7e4893488e3bc55d0c2c324d7cfef5', 'commit_...[truncated]
- `diff_code`:   def fetch_funding_rate_history(self, symbol=None, since=None, limit=None, params={}):\n          \n          \n          \n          self.load_markets()\n          request = {}\n          market = None\n          if symbol in self.currenc...[truncated]
- `diff_docstring`:   Fetches the history of funding rates\n          :param str|None symbol: unified symbol of the market to fetch the funding rate history for\n          :param int|None since: timestamp in ms of the earliest funding rate to fetch\n          ...[truncated]
- `whitespace_only_code`: False
- `whitespace_only_docstring`: False
- `file_path`: python/ccxt/bitmex.py
- `filename`: bitmex.py
- `project`: ccxt
- `owner`: ccxt

### Sample 5

Keys: `file, function, version_data, diff_code, diff_docstring, whitespace_only_code, whitespace_only_docstring, file_path, filename, project, owner`

- `file`: python_ccxt_bitmex.py
- `function`: bitmex.fetch_my_trades
- `version_data`: [{'v325': {'docstring_lines': {'start_line': 1630, 'end_line': 1638}, 'code_lines': {'start_line': 1638, 'end_line': 1680}}, 'commit_date_time': '2023-09-14 23:49:35+00:00', 'commit_sha': '2e126035c9575c4748f136085bded8c4660286b1', 'commit_...[truncated]
- `diff_code`:   def fetch_my_trades(self, symbol: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):\n          \n          \n          \n          self.load_markets()\n+         paginate = False\n+         pagina...[truncated]
- `diff_docstring`: + see https://www.bitmex.com/api/explorer/#not /Execution/Execution_getTradeHistory\n- fetch all trades made by the user\n+         fetch all trades made by the user\n? ++++++++\n\n          :param str symbol: unified market symbol\n       ...[truncated]
- `whitespace_only_code`: False
- `whitespace_only_docstring`: False
- `file_path`: python/ccxt/bitmex.py
- `filename`: bitmex.py
- `project`: ccxt
- `owner`: ccxt
