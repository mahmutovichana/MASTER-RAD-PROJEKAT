# DocGuard Real PR Seed Collector Report

This report summarizes neutral repo-based sampling of merged public GitHub PRs.

The collector does not assign gold labels and does not decide whether documentation should be updated.
It only creates seed PR URLs for the later candidate builder and manual validation workflow.

- Repositories scanned: `769`
- Seeds accepted: `0`
- Rejected/skipped PRs: `12080`
- Acquisition status: `partial`
- Requirements satisfied: `False`
- Target observed/requested: `0` / `12000`
- Target deficit: `12000`
- Minimum language deficits: `{'python': 6000, 'typescript': 5000}`
- Collector bucket counts: `{}`
- Language hint counts: `{}`
- Repository counts per language: `{}`
- Candidate bucket counts per language: `{}`
- Reject reason counts: `{'fetch_closed_pulls_failed': 764, 'already_collected': 4906, 'docs_only_excluded': 589, 'too_many_changed_files': 365, 'other_or_binary_only_excluded': 644, 'not_merged': 3857, 'too_large_patch': 138, 'fetch_pr_files_failed': 817}`

## Methodological Boundary

- This is real public GitHub PR sampling.
- No synthetic examples are generated.
- No final labels are assigned here.
- `collector_bucket` is audit metadata for balancing and review planning, not a model label.
- Final evaluation must use only the safe fields produced later by the candidate builder.

## Accepted Seeds

| PR | Repository | Bucket | Language hint | Title |
| --- | --- | --- | --- | --- |

## Reject Summary Sample

| Repository | PR | Reason | Bucket |
| --- | ---: | --- | --- |
| `microsoft/typescript-go` | `None` | `fetch_closed_pulls_failed` | `None` |
| `0xradikal/free-v2ray-configs` | `None` | `fetch_closed_pulls_failed` | `None` |
| `1111mp/nvm-desktop` | `None` | `fetch_closed_pulls_failed` | `None` |
| `1catai/1cat-vllm` | `None` | `fetch_closed_pulls_failed` | `None` |
| `a2ui-project/a2ui` | `None` | `fetch_closed_pulls_failed` | `None` |
| `1panel-dev/maxkb` | `None` | `fetch_closed_pulls_failed` | `None` |
| `aaddrick/claude-desktop-debian` | `None` | `fetch_closed_pulls_failed` | `None` |
| `217heidai/adblockfilters` | `None` | `fetch_closed_pulls_failed` | `None` |
| `activepieces/activepieces` | `None` | `fetch_closed_pulls_failed` | `None` |
| `521xueweihan/github520` | `None` | `fetch_closed_pulls_failed` | `None` |
| `agalwood/motrix` | `None` | `fetch_closed_pulls_failed` | `None` |
| `abrignoni/ileapp` | `None` | `fetch_closed_pulls_failed` | `None` |
| `agentconnect-md/agentconnect` | `None` | `fetch_closed_pulls_failed` | `None` |
| `activeing123/mcptoon` | `None` | `fetch_closed_pulls_failed` | `None` |
| `agsh/onvif` | `None` | `fetch_closed_pulls_failed` | `None` |
| `acymz/autovpn` | `None` | `fetch_closed_pulls_failed` | `None` |
| `aipoch/open-science` | `None` | `fetch_closed_pulls_failed` | `None` |
| `adongwanai/learn-workbuddy` | `None` | `fetch_closed_pulls_failed` | `None` |
| `airbrake/airbrake-js` | `None` | `fetch_closed_pulls_failed` | `None` |
| `ag-ui-protocol/ag-ui` | `None` | `fetch_closed_pulls_failed` | `None` |
| `allen-xxa/comfynexus` | `None` | `fetch_closed_pulls_failed` | `None` |
| `agentmorris/megadetector` | `None` | `fetch_closed_pulls_failed` | `None` |
| `andymai/gridfinity-layout-tool` | `None` | `fetch_closed_pulls_failed` | `None` |
| `agentscope-ai/qwenpaw` | `None` | `fetch_closed_pulls_failed` | `None` |
| `angular/angular` | `None` | `fetch_closed_pulls_failed` | `None` |
| `agno-agi/agno` | `None` | `fetch_closed_pulls_failed` | `None` |
| `angular/angular-cli` | `None` | `fetch_closed_pulls_failed` | `None` |
| `ai-hypercomputer/maxtext` | `None` | `fetch_closed_pulls_failed` | `None` |
| `anomalyco/models.dev` | `None` | `fetch_closed_pulls_failed` | `None` |
| `aio-libs/aiohttp` | `None` | `fetch_closed_pulls_failed` | `None` |
| `anomalyco/opencode` | `None` | `fetch_closed_pulls_failed` | `None` |
| `airbytehq/airbyte` | `None` | `fetch_closed_pulls_failed` | `None` |
| `anomalyco/opentui` | `None` | `fetch_closed_pulls_failed` | `None` |
| `aiskillstore/marketplace` | `None` | `fetch_closed_pulls_failed` | `None` |
| `ant-design/ant-design` | `None` | `fetch_closed_pulls_failed` | `None` |
| `akfamily/akquant` | `None` | `fetch_closed_pulls_failed` | `None` |
| `anthropics/anthropic-sdk-typescript` | `None` | `fetch_closed_pulls_failed` | `None` |
| `alishahryar1/free-claude-code` | `None` | `fetch_closed_pulls_failed` | `None` |
| `anywhere-labs/dsh-desktop` | `None` | `fetch_closed_pulls_failed` | `None` |
| `amd-agi/primus` | `None` | `fetch_closed_pulls_failed` | `None` |
| `apache/echarts` | `None` | `fetch_closed_pulls_failed` | `None` |
| `anbeime/skill` | `None` | `fetch_closed_pulls_failed` | `None` |
| `apache/maka` | `None` | `fetch_closed_pulls_failed` | `None` |
| `aneasystone/github-trending` | `None` | `fetch_closed_pulls_failed` | `None` |
| `appstore-discounts/appstore-discounts` | `None` | `fetch_closed_pulls_failed` | `None` |
| `angr/angr` | `None` | `fetch_closed_pulls_failed` | `None` |
| `appwrite/appwrite` | `None` | `fetch_closed_pulls_failed` | `None` |
| `anonym0uswork1221/free-proxies` | `None` | `fetch_closed_pulls_failed` | `None` |
| `appwrite/sdk-for-web` | `None` | `fetch_closed_pulls_failed` | `None` |
| `ansible/ansible` | `None` | `fetch_closed_pulls_failed` | `None` |
| `artokun/comfyui-mcp` | `None` | `fetch_closed_pulls_failed` | `None` |
| `anthropics/anthropic-sdk-python` | `None` | `fetch_closed_pulls_failed` | `None` |
| `aspirin0000/zhouli-translator` | `None` | `fetch_closed_pulls_failed` | `None` |
| `apache/airflow` | `72080` | `already_collected` | `None` |
| `apache/airflow` | `72076` | `already_collected` | `None` |
| `apache/airflow` | `71120` | `already_collected` | `None` |
| `apache/airflow` | `72074` | `docs_only_excluded` | `docs_only` |
| `apache/airflow` | `71315` | `docs_only_excluded` | `docs_only` |
| `apache/airflow` | `72065` | `already_collected` | `None` |
| `apache/airflow` | `72069` | `already_collected` | `None` |
| `apache/airflow` | `70238` | `already_collected` | `None` |
| `apache/airflow` | `72067` | `already_collected` | `None` |
| `apache/airflow` | `71919` | `already_collected` | `None` |
| `apache/airflow` | `72066` | `already_collected` | `None` |
| `apache/airflow` | `64422` | `already_collected` | `None` |
| `apache/airflow` | `72017` | `already_collected` | `None` |
| `apache/airflow` | `68627` | `already_collected` | `None` |
| `apache/airflow` | `71956` | `already_collected` | `None` |
| `apache/airflow` | `71975` | `already_collected` | `None` |
| `apache/airflow` | `72022` | `already_collected` | `None` |
| `apache/airflow` | `71957` | `too_many_changed_files` | `code_and_docs` |
| `apache/airflow` | `72016` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `apache/airflow` | `71783` | `already_collected` | `None` |
| `apache/airflow` | `72021` | `not_merged` | `None` |
| `apache/airflow` | `72005` | `already_collected` | `None` |
| `apache/airflow` | `71799` | `already_collected` | `None` |
| `apache/airflow` | `69829` | `already_collected` | `None` |
| `apache/airflow` | `68685` | `already_collected` | `None` |
| `apache/airflow` | `68035` | `docs_only_excluded` | `docs_only` |
| `apache/airflow` | `72045` | `already_collected` | `None` |
| `apache/airflow` | `72029` | `already_collected` | `None` |
| `apache/airflow` | `71770` | `not_merged` | `None` |
| `apache/airflow` | `71916` | `already_collected` | `None` |
| `apache/airflow` | `69965` | `already_collected` | `None` |
| `apache/airflow` | `52330` | `too_many_changed_files` | `code_and_docs` |
| `apache/airflow` | `71158` | `already_collected` | `None` |
| `apache/airflow` | `72010` | `already_collected` | `None` |
| `apache/airflow` | `67881` | `already_collected` | `None` |
| `apache/airflow` | `69827` | `already_collected` | `None` |
| `apache/airflow` | `71170` | `already_collected` | `None` |
| `apache/airflow` | `65845` | `not_merged` | `None` |
| `apache/airflow` | `72037` | `not_merged` | `None` |
| `apache/airflow` | `68833` | `already_collected` | `None` |
| `apache/airflow` | `71900` | `already_collected` | `None` |
| `apache/airflow` | `70839` | `already_collected` | `None` |
| `apache/airflow` | `71933` | `already_collected` | `None` |
| `apache/airflow` | `71341` | `not_merged` | `None` |
| `apache/airflow` | `71920` | `already_collected` | `None` |
| `apache/airflow` | `68884` | `already_collected` | `None` |
| `apache/airflow` | `71963` | `already_collected` | `None` |
| `apache/airflow` | `71953` | `already_collected` | `None` |
| `apache/airflow` | `71952` | `already_collected` | `None` |
| `apache/airflow` | `72012` | `already_collected` | `None` |
| `apache/airflow` | `70517` | `already_collected` | `None` |
| `apache/airflow` | `71209` | `too_many_changed_files` | `code_only` |
| `apache/airflow` | `70665` | `already_collected` | `None` |
| `apache/airflow` | `70215` | `already_collected` | `None` |
| `apache/airflow` | `71751` | `not_merged` | `None` |
| `apache/airflow` | `71460` | `not_merged` | `None` |
| `apache/airflow` | `69617` | `not_merged` | `None` |
| `apache/airflow` | `70506` | `not_merged` | `None` |
| `apache/airflow` | `66213` | `not_merged` | `None` |
| `apache/airflow` | `66432` | `not_merged` | `None` |
| `apache/airflow` | `66761` | `not_merged` | `None` |
| `apache/airflow` | `72009` | `already_collected` | `None` |
| `apache/airflow` | `71682` | `already_collected` | `None` |
| `apache/airflow` | `71856` | `already_collected` | `None` |
| `apache/airflow` | `71611` | `already_collected` | `None` |
| `apache/airflow` | `71841` | `already_collected` | `None` |
| `apache/airflow` | `67532` | `too_many_changed_files` | `code_and_docs` |
| `apache/airflow` | `69231` | `already_collected` | `None` |
| `apache/airflow` | `71994` | `not_merged` | `None` |
| `apache/airflow` | `71993` | `not_merged` | `None` |
| `apache/airflow` | `71992` | `not_merged` | `None` |
| `apache/airflow` | `71991` | `not_merged` | `None` |
| `apache/airflow` | `71980` | `already_collected` | `None` |
| `apache/airflow` | `67187` | `not_merged` | `None` |
| `apache/airflow` | `67218` | `not_merged` | `None` |
| `apache/airflow` | `67223` | `not_merged` | `None` |
| `apache/airflow` | `71946` | `already_collected` | `None` |
| `apache/airflow` | `71728` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `apache/airflow` | `71937` | `already_collected` | `None` |
| `apache/airflow` | `71731` | `too_many_changed_files` | `code_only` |
| `apache/airflow` | `70228` | `already_collected` | `None` |
| `apache/airflow` | `71971` | `already_collected` | `None` |
| `apache/airflow` | `71972` | `not_merged` | `None` |
| `apache/airflow` | `71960` | `docs_only_excluded` | `docs_only` |
| `apache/airflow` | `71961` | `docs_only_excluded` | `docs_only` |
| `apache/airflow` | `70699` | `already_collected` | `None` |
| `apache/airflow` | `71180` | `already_collected` | `None` |
| `apache/airflow` | `71954` | `already_collected` | `None` |
| `apache/airflow` | `71517` | `already_collected` | `None` |
| `apache/airflow` | `71790` | `already_collected` | `None` |
| `apache/airflow` | `71857` | `already_collected` | `None` |
| `apache/airflow` | `71898` | `not_merged` | `None` |
| `apache/airflow` | `71789` | `already_collected` | `None` |
| `apache/airflow` | `71951` | `already_collected` | `None` |
| `apache/airflow` | `68795` | `already_collected` | `None` |
| `apache/airflow` | `71488` | `already_collected` | `None` |
| `apache/airflow` | `71943` | `already_collected` | `None` |
| `apache/airflow` | `71780` | `already_collected` | `None` |
| `apache/airflow` | `71803` | `already_collected` | `None` |
| `apache/airflow` | `71944` | `already_collected` | `None` |
| `apache/airflow` | `71849` | `already_collected` | `None` |
| `apache/airflow` | `71866` | `already_collected` | `None` |
| `apache/airflow` | `71935` | `already_collected` | `None` |
| `apache/airflow` | `71924` | `already_collected` | `None` |
| `apache/airflow` | `71912` | `already_collected` | `None` |
| `apache/airflow` | `71917` | `already_collected` | `None` |
| `apache/airflow` | `71889` | `already_collected` | `None` |
| `apache/airflow` | `71878` | `already_collected` | `None` |
| `apache/airflow` | `71643` | `already_collected` | `None` |
| `apache/airflow` | `71815` | `already_collected` | `None` |
| `apache/airflow` | `71057` | `already_collected` | `None` |
| `apache/airflow` | `71564` | `docs_only_excluded` | `docs_only` |
| `apache/airflow` | `71826` | `already_collected` | `None` |
| `apache/airflow` | `71819` | `docs_only_excluded` | `docs_only` |
| `apache/airflow` | `67676` | `not_merged` | `None` |
| `apache/airflow` | `71712` | `already_collected` | `None` |
| `apache/airflow` | `69125` | `already_collected` | `None` |
| `apache/airflow` | `64751` | `already_collected` | `None` |
| `apache/airflow` | `71888` | `already_collected` | `None` |
| `apache/airflow` | `71185` | `already_collected` | `None` |
| `apache/airflow` | `71910` | `already_collected` | `None` |
| `apache/airflow` | `71705` | `already_collected` | `None` |
| `apache/airflow` | `71902` | `already_collected` | `None` |
| `apache/airflow` | `71903` | `docs_only_excluded` | `docs_only` |
| `apache/airflow` | `71901` | `already_collected` | `None` |
| `apache/airflow` | `71896` | `already_collected` | `None` |
| `apache/airflow` | `71680` | `already_collected` | `None` |
| `apache/airflow` | `71904` | `already_collected` | `None` |
| `apache/airflow` | `71894` | `already_collected` | `None` |
| `apache/airflow` | `69400` | `already_collected` | `None` |
| `apache/airflow` | `71886` | `already_collected` | `None` |
| `apache/airflow` | `71823` | `already_collected` | `None` |
| `apache/airflow` | `71884` | `docs_only_excluded` | `docs_only` |
| `apache/airflow` | `71784` | `already_collected` | `None` |
| `apache/airflow` | `70993` | `already_collected` | `None` |
| `apache/airflow` | `71555` | `already_collected` | `None` |
| `apache/airflow` | `69899` | `not_merged` | `None` |
| `apache/airflow` | `69923` | `not_merged` | `None` |
| `apache/airflow` | `69920` | `not_merged` | `None` |
| `apache/airflow` | `70141` | `not_merged` | `None` |
| `apache/airflow` | `69926` | `not_merged` | `None` |
| `apache/airflow` | `70188` | `not_merged` | `None` |
| `apache/airflow` | `70168` | `not_merged` | `None` |
| `apache/airflow` | `71874` | `too_many_changed_files` | `code_and_docs` |
| `apache/airflow` | `71876` | `already_collected` | `None` |
| `apache/airflow` | `69138` | `not_merged` | `None` |
| `apache/airflow` | `71475` | `other_or_binary_only_excluded` | `other_or_binary_only` |