# External CoDocBench Existing DocGuard Positive Recall 2026-08

- Input: `data\external\codocbench_sample_500.jsonl`
- Predictor used: `hf_embedding_staged_raw_diff_plus_docs`
- Model path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\models\hf_v0_4\raw_diff_plus_docs\embedding_classifier_staged.joblib`
- Model type: `LogisticRegression`
- Model name: `sentence-transformers/all-MiniLM-L6-v2`
- Input mode: `raw_diff_plus_docs`
- Classifier architecture: `staged`
- External input mode: `code_diff_plus_doc_diff_upper_bound`
- External input leakage label: `upper_bound_leakage_risk`
- External input mode definition: Uses code_diff and doc_diff. This exposes the future documentation change and is not a primary fair result.
- Decision rule: docs_update_required is true when the staged docs_update_required classifier top label is `true`.
- Confidence definition: minimum probability across docs_update_required, positive doc_category, positive scenario_type, and positive target_doc_file classifiers for positive predictions
- Threshold used for binary decision: `none for binary decision; confidence thresholds are analyzed only as abstention/review policies`
- Total positives evaluated: `500`
- Predicted update-required count: `499`
- False negative count: `1`
- Positive recall: `99.80%`
- Low-confidence threshold: `0.25`
- Low-confidence count below 0.25: `472`
- Low-confidence percentage: `94.40%`
- Min confidence: `0.0630`
- Max confidence: `0.5329`
- Mean confidence: `0.1406`
- Median confidence: `0.1247`
- Q1 confidence: `0.1041`
- Q3 confidence: `0.1558`

## Leakage Warning

This run includes `doc_diff` / `diff_docstring` as input. That exposes future documentation changes and should be treated only as an upper-bound diagnostic, not final thesis evidence.

## What This Evaluation Can and Cannot Measure

This positive-only CoDocBench pilot can measure positive recall, false negatives, confidence distribution, and predicted label distributions.

It cannot measure precision, F1, false-positive rate, or negative classification quality because no defensible external negative set is included.

## Confidence Deciles

| Percentile | Confidence |
| --- | ---: |
| `p10` | 0.0890 |
| `p20` | 0.1009 |
| `p30` | 0.1083 |
| `p40` | 0.1152 |
| `p50` | 0.1247 |
| `p60` | 0.1371 |
| `p70` | 0.1497 |
| `p80` | 0.1670 |
| `p90` | 0.2084 |

## Confidence Histogram

| Bin | Count | Percentage |
| --- | ---: | ---: |
| `0.0-0.1` | 98 | 19.60% |
| `0.1-0.2` | 345 | 69.00% |
| `0.2-0.3` | 44 | 8.80% |
| `0.3-0.4` | 9 | 1.80% |
| `0.4-0.5` | 2 | 0.40% |
| `0.5-0.6` | 2 | 0.40% |
| `0.6-0.7` | 0 | 0.00% |
| `0.7-0.8` | 0 | 0.00% |
| `0.8-0.9` | 0 | 0.00% |
| `0.9-1.0` | 0 | 0.00% |

## Recall At Confidence Thresholds

| Threshold | Accepted predictions | Accepted % | Accepted true positives | Rejected positives | Recall all positives | Recall among accepted |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.00 | 500 | 100.00% | 499 | 0 | 99.80% | 99.80% |
| 0.10 | 402 | 80.40% | 401 | 98 | 80.20% | 99.75% |
| 0.20 | 57 | 11.40% | 56 | 443 | 11.20% | 98.25% |
| 0.25 | 28 | 5.60% | 27 | 472 | 5.40% | 96.43% |
| 0.30 | 13 | 2.60% | 12 | 487 | 2.40% | 92.31% |
| 0.40 | 4 | 0.80% | 3 | 496 | 0.60% | 75.00% |
| 0.50 | 2 | 0.40% | 1 | 498 | 0.20% | 50.00% |
| 0.75 | 0 | 0.00% | 0 | 500 | 0.00% | 0.00% |

The accepted-only recall column is positive-only and does not measure precision. The all-positives recall column treats abstentions as missed positives.

## Predicted Doc Category Distribution

- `architecture_flow`: 170
- `developer_setup`: 124
- `testing_instructions`: 67
- `workflow_documentation`: 65
- `configuration`: 49
- `api_reference`: 15
- `model_contract`: 5
- `changelog`: 4
- `no_update`: 1

## Predicted Scenario Type Distribution

- `changed_validation_max`: 104
- `added_environment_variable`: 68
- `changed_local_development_flow`: 51
- `changed_test_command`: 50
- `changed_caching_or_rate_limit_flow`: 40
- `added_background_job_flow`: 39
- `changed_testing_framework`: 31
- `changed_middleware_auth_flow`: 26
- `changed_seed_or_setup_flow`: 20
- `changed_enum_values`: 16
- `changed_validation_min`: 10
- `removed_endpoint`: 6
- `added_dto_model_field`: 6
- `changed_error_handling_flow`: 6
- `changed_default_config_value`: 4
- `removed_dto_model_field`: 4
- `changelog_worthy_behavior_change`: 4
- `changed_endpoint_path`: 3
- `added_service_orchestration_flow`: 3
- `changed_http_method`: 2
- `removed_environment_variable`: 2
- `changed_auth_requirement`: 2
- `removed_request_field`: 1
- `added_response_field`: 1
- `docs_already_updated`: 1

## Predicted Target Doc File Distribution

- `docs/architecture.md`: 170
- `docs/developer-setup.md`: 124
- `docs/testing.md`: 67
- `docs/workflows.md`: 65
- `docs/configuration.md`: 49
- `docs/api.md`: 15
- `docs/models.md`: 5
- `CHANGELOG.md`: 4
- `unknown`: 1

## Top 20 Lowest-Confidence True Positives

### codocbench-core-411cc6542ca034694eadaa7502fac4c68b516cf1-lookup_plex_media-360

- repo/project: `core`
- function: `lookup_plex_media`
- commit hash: `411cc6542ca034694eadaa7502fac4c68b516cf1`
- confidence: `0.0630`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_test_command`
- predicted target: `docs/architecture.md`
- short code diff:   def lookup_plex_media(hass, content_type, content_id):\n      \n      content = json.loads(content_id)\n  \n      if isinstance(content, int):\n          content = {"plex_key": content}\n          content_type = DOMAIN\n  \n      plex_server_name = content.pop("plex_server", None)\n      shuffle = content.pop("shuffle", 0)\n  \n      plex_server = get_plex_server(hass, plex_server_name=plex_server_name)\n-     if n...[truncated]
- short doc diff: - Look up Plex media using media_player.play_media service payloads.\n+ Look up Plex media for other integrations using media_player.play_media service payloads.\n?                    +++++++++++++++++++++++\n
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-aws-sam-cli-bedd5d53d99ae64dacc487d72108c2b7cef58f5d-SamFunctionProvider._extract_functions-364

- repo/project: `aws-sam-cli`
- function: `SamFunctionProvider._extract_functions`
- commit hash: `bedd5d53d99ae64dacc487d72108c2b7cef58f5d`
- confidence: `0.0635`
- predicted doc category: `architecture_flow`
- predicted scenario: `removed_environment_variable`
- predicted target: `docs/architecture.md`
- short code diff:   def _extract_functions(\n-         stacks: List[Stack], use_raw_codeuri: bool = False, ignore_code_extraction_warnings: bool = False\n+         stacks: List[Stack],\n+         use_raw_codeuri: bool = False,\n+         ignore_code_extraction_warnings: bool = False,\n+         locate_layer_nested: bool = False,\n      ) -> Dict[str, Function]:\n          \n          \n          \n  \n          result: Dict[str, Funct...[truncated]
- short doc diff:   Extracts and returns function information from the given dictionary of SAM/CloudFormation resources. This\n          method supports functions defined with AWS::Serverless::Function and AWS::Lambda::Function\n  \n          :param stacks: List of SAM/CloudFormation stacks to extract functions from\n          :param bool use_raw_codeuri: Do not resolve adjus...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-image-8432b90eb84d5ec4dea04631f087402bf61c1a12-rotate-297

- repo/project: `scikit-image`
- function: `rotate`
- commit hash: `8432b90eb84d5ec4dea04631f087402bf61c1a12`
- confidence: `0.0650`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_local_development_flow`
- predicted target: `docs/architecture.md`
- short code diff: - def rotate(image, angle, resize=False, order=1, mode='constant', cval=0.):\n?                                                                         ^^\n\n+ def rotate(image, angle, resize=False, order=1, mode='constant', cval=0.,\n?                                                                         ^\n\n+            center=None):\n      \n  \n      \n  \n      rows, cols = image.shape[0], image.shape[1]\n  \...[truncated]
- short doc diff:   Rotate image by a certain angle around its center.\n  \n      Parameters\n      ----------\n      image : ndarray\n          Input image.\n      angle : float\n          Rotation angle in degrees in counter-clockwise direction.\n      resize : bool, optional\n          Determine whether the shape of the output image will be automatically\n          calcula...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-django-ce3c71faf1ff83494193b48a6f99256d0628b2a2-Query.join_parent_model-385

- repo/project: `django`
- function: `Query.join_parent_model`
- commit hash: `ce3c71faf1ff83494193b48a6f99256d0628b2a2`
- confidence: `0.0686`
- predicted doc category: `workflow_documentation`
- predicted scenario: `added_background_job_flow`
- predicted target: `docs/workflows.md`
- short code diff:   def join_parent_model(self, opts, model, alias, seen):\n          \n          \n          \n          if model in seen:\n              return seen[model]\n          int_opts = opts\n          chain = opts.get_base_chain(model)\n          if chain is None:\n              return alias\n          for int_model in chain:\n              if int_model in seen:\n                  return seen[int_model]\n              # Pro...[truncated]
- short doc diff:   Makes sure the given 'model' is joined in the query. If 'model' isn't\n          a parent of 'opts' or if it is None this method is a no-op.\n  \n          The 'alias' is the root alias for starting the join, 'seen' is a dict\n-         of model -> alias of existing joins.\n+         of model -> alias of existing joins. It must also contain a mapping\n+   ...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-faceswap-6ee896d175145297ecae001d1a6f4628b5b4e6ef-_EventParser._parse_outputs-251

- repo/project: `faceswap`
- function: `_EventParser._parse_outputs`
- commit hash: `6ee896d175145297ecae001d1a6f4628b5b4e6ef`
- confidence: `0.0687`
- predicted doc category: `workflow_documentation`
- predicted scenario: `added_background_job_flow`
- predicted target: `docs/workflows.md`
- short code diff:   def _parse_outputs(self, event):\n           \n          \n          serializer = get_serializer("json")\n          struct = event.summary.value[0].tensor.string_val[0]\n+ \n+         config = serializer.unmarshal(struct)["config"]\n+         model_outputs = self._get_outputs(config)\n+         split_output = len(np.unique(model_outputs[..., 1])) == 1\n+ \n-         outputs = np.array(serializer.unmarshal(struct)["...[truncated]
- short doc diff:   Parse the outputs from the stored model structure for mapping loss names to\n          model outputs.\n  \n          Loss names are added to :attr:`_loss_labels`\n  \n+         Notes\n+         -----\n+         The master model does not actually contain the specified output name, so we dig into the\n+         sub-model to obtain the name of the output laye...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-django-cb0da637a69b79ab371be9ee202335190a3a506e-GDALRaster.transform-64

- repo/project: `django`
- function: `GDALRaster.transform`
- commit hash: `cb0da637a69b79ab371be9ee202335190a3a506e`
- confidence: `0.0700`
- predicted doc category: `workflow_documentation`
- predicted scenario: `changed_testing_framework`
- predicted target: `docs/workflows.md`
- short code diff: - def transform(self, srid, driver=None, name=None, resampling='NearestNeighbour',\n?                       ^^\n\n+ def transform(self, srs, driver=None, name=None, resampling='NearestNeighbour',\n?                       ^\n\n                    max_error=0.0):\n          \n          \n          \n          # Convert the resampling algorithm name into an algorithm id\n          algorithm = GDAL_RESAMPLE_ALGORITHMS[re...[truncated]
- short doc diff: - Return a copy of this raster reprojected into the given SRID.\n?                                                         ^^^^^\n\n+ Return a copy of this raster reprojected into the given spatial\n?                                                         ^^^^^^^\n\n+         reference system.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-twine-09fe3a40c09f3cdddb42af6331dcc6ee8d923779-Tiddler.displays-147

- repo/project: `twine`
- function: `Tiddler.displays`
- commit hash: `09fe3a40c09f3cdddb42af6331dcc6ee8d923779`
- confidence: `0.0712`
- predicted doc category: `configuration`
- predicted scenario: `changed_test_command`
- predicted target: `docs/configuration.md`
- short code diff:   def displays(self):\n  		\n  		\n  		\n- 		if ('script' in self.tags) or ('stylesheet' in self.tags):\n+ 		if not self.isStoryText():\n  			return []\n  		return re.findall(r'\<\<display\s+[\'"]?(.+?)[\'"]?\s?\>\>', self.text, re.IGNORECASE)
- short doc diff: - Returns a list of all passages <<display>>ed by this one. By default,\n?                                                          ------------\n\n+ Returns a list of all passages <<display>>ed by this one.\n- 		returns internal links and dis
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-datasets-6be722dbbc212d88eb5e550e56431cdcab180eee-Dataset.from_sql-31

- repo/project: `datasets`
- function: `Dataset.from_sql`
- commit hash: `6be722dbbc212d88eb5e550e56431cdcab180eee`
- confidence: `0.0715`
- predicted doc category: `developer_setup`
- predicted scenario: `removed_request_field`
- predicted target: `docs/developer-setup.md`
- short code diff:   def from_sql(\n          sql: Union[str, "sqlalchemy.sql.Selectable"],\n-         con: str,\n+         con: Union[str, "sqlalchemy.engine.Connection", "sqlalchemy.engine.Engine", "sqlite3.Connection"],\n          features: Optional[Features] = None,\n          cache_dir: str = None,\n          keep_in_memory: bool = False,\n          **kwargs,\n      ):\n          \n          \n          from .io.sql import SqlData...[truncated]
- short doc diff:   Create Dataset from SQL query or database table.\n  \n          Args:\n              sql (`str` or :obj:`sqlalchemy.sql.Selectable`): SQL query to be executed or a table name.\n-             con (`str`): A connection URI string used to instantiate a database connection.\n+             con (`str` or :obj:`sqlite3.Connection` or :obj:`sqlalchemy.engine.Conne...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-langchain-1c7b3c75a7b1235d6cf26fe00e8bc25b33ac29a6-create_pandas_dataframe_agent-330

- repo/project: `langchain`
- function: `create_pandas_dataframe_agent`
- commit hash: `1c7b3c75a7b1235d6cf26fe00e8bc25b33ac29a6`
- confidence: `0.0728`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_local_development_flow`
- predicted target: `docs/architecture.md`
- short code diff:   def create_pandas_dataframe_agent(\n      llm: LanguageModelLike,\n      df: Any,\n      agent_type: Union[\n-         AgentType, Literal["openai-tools"]\n+         AgentType, Literal["openai-tools", "tool-calling"]\n?                                          ++++++++++++++++\n\n      ] = AgentType.ZERO_SHOT_REACT_DESCRIPTION,\n      callback_manager: Optional[BaseCallbackManager] = None,\n      prefix: Optional[st...[truncated]
- short doc diff:   Construct a Pandas agent from an LLM and dataframe(s).\n  \n      Args:\n-         llm: Language model to use for the agent.\n+         llm: Language model to use for the agent. If agent_type is "tool-calling" then\n+             llm is expected to support tool calling.\n          df: Pandas dataframe or list of Pandas dataframes.\n-         agent_type: On...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-rf-1b02349352d40d7bb0cf76455d28b84a847970b0-LRRM.__init__-462

- repo/project: `scikit-rf`
- function: `LRRM.__init__`
- commit hash: `1b02349352d40d7bb0cf76455d28b84a847970b0`
- confidence: `0.0740`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_middleware_auth_flow`
- predicted target: `docs/architecture.md`
- short code diff:   def __init__(self, measured, ideals, switch_terms=None, isolation=None,\n              z0=50, match_fit='l', *args, **kwargs):\n          \n          \n          \n  \n          self.z0 = z0\n          # TODO: Second port not implemented.\n          self.match_port = 0\n+         # Maximum frequency to assume that open behaves like ideal capacitor when\n+         # using match_fit == 'lc'.\n+         self.lc_fit_c_...[truncated]
- short doc diff:   LRRM Initializer.\n-         \n+ \n          Parameters\n          ----------\n          measured : list of :class:`~skrf.network.Network` objects\n              Raw measurements of the calibration standards. The order\n              must be line, reflect, reflect, match and must align with the\n              `ideals` parameter\n  \n          ideals : list...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-learn-0bd45b5179196c1c87db6b6de4433647accaa88c-_check_psd_eigenvalues-326

- repo/project: `scikit-learn`
- function: `_check_psd_eigenvalues`
- commit hash: `0bd45b5179196c1c87db6b6de4433647accaa88c`
- confidence: `0.0744`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_testing_framework`
- predicted target: `docs/architecture.md`
- short code diff:   def _check_psd_eigenvalues(lambdas, enable_warnings=False):\n      \n  \n      \n  \n      lambdas = np.array(lambdas)\n      is_double_precision = lambdas.dtype == np.float64\n  \n      # note: the minimum value available is\n      #  - single-precision: np.finfo('float32').eps = 1.2e-07\n      #  - double-precision: np.finfo('float64').eps = 2.2e-16\n  \n      # the various thresholds used for validation\n      #...[truncated]
- short doc diff:   Check the eigenvalues of a positive semidefinite (PSD) matrix.\n  \n      Checks the provided array of PSD matrix eigenvalues for numerical or\n      conditioning issues and returns a fixed validated version. This method\n      should typically be used if the PSD matrix is user-provided (e.g. a\n      Gram matrix) or computed using a user-provided dissimil...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-models-d90f5580d932b801ea3a9715d0dee00fc58ab55a-DeepSpeechDecoder.cer-166

- repo/project: `models`
- function: `DeepSpeechDecoder.cer`
- commit hash: `d90f5580d932b801ea3a9715d0dee00fc58ab55a`
- confidence: `0.0749`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_testing_framework`
- predicted target: `docs/architecture.md`
- short code diff: - def cer(self, output, target):\n?                ^^^^^\n\n+ def cer(self, decode, target):\n?               +++ ^^\n\n      \n      \n-     return distance.edit_distance(output, target)\n?                                    ^^^^^\n\n+     return distance.edit_distance(decode, target)\n?                                   +++ ^^\n
- short doc diff:   Computes the Character Error Rate (CER).\n  \n-     CER is  defined as the edit distance between the given strings.\n?           -\n\n+     CER is defined as the edit distance between the two given strings.\n?                                                    ++++\n\n  \n      Args:\n-       output: a string of the decoded output.\n?        ^^^^^\n\n+    ...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-rf-c7aedbd0abd8862c3cc25a72f98f94bd2802e60b-Media.splitter-381

- repo/project: `scikit-rf`
- function: `Media.splitter`
- commit hash: `c7aedbd0abd8862c3cc25a72f98f94bd2802e60b`
- confidence: `0.0755`
- predicted doc category: `workflow_documentation`
- predicted scenario: `added_background_job_flow`
- predicted target: `docs/workflows.md`
- short code diff:   def splitter(self, nports: int, **kwargs) -> Network:\n          \n          \n          result = self.match(nports, **kwargs)\n- \n-         result.s =  splitter_s(self.frequency, nports, z0=result.z0)\n+         \n+         y0s = npy.array(1./result.z0)\n+         y_k = y0s.sum(axis=1)\n+         s = npy.zeros((self.frequency.npoints, nports, nports),\n+                       dtype='complex')\n+         s = 2 *np...[truncated]
- short doc diff:   r"""\n          Ideal, lossless n-way splitter.\n+         \n+         The port impedances can be mismatched and the power is split\n+         accordingly.\n+         \n+         For n > 2, the splitter is not matched because the power wave entering\n+         one port meet the equivalent impedance of the other ports in parallel.\n+         \n+         .. ...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-speechbrain-c5b6a4854a76386c481f5c2b871e70596d6ab5de-Mvdr._mvdr-368

- repo/project: `speechbrain`
- function: `Mvdr._mvdr`
- commit hash: `c5b6a4854a76386c481f5c2b871e70596d6ab5de`
- confidence: `0.0758`
- predicted doc category: `developer_setup`
- predicted scenario: `changed_testing_framework`
- predicted target: `docs/developer-setup.md`
- short code diff: - def _mvdr(Xs, XXs, As, eps=1e-20):\n?               ^^\n\n+ def _mvdr(Xs, NNs, As, eps=1e-20):\n?               ^^\n\n          \n          \n  \n          # Get unique covariance values to reduce the number of computations\n-         XXs_val, XXs_idx = torch.unique(XXs, return_inverse=True, dim=1)\n?         ^^       ^^                     ^^\n\n+         NNs_val, NNs_idx = torch.unique(NNs, return_inverse=True, d...[truncated]
- short doc diff:   Perform minimum variance distortionless response beamforming.\n  \n          Arguments\n          ---------\n          Xs : tensor\n              A batch of audio signals in the frequency domain.\n              The tensor must have the following format:\n              (batch, time_step, n_fft/2 + 1, 2, n_mics).\n-         XXs : tensor\n?         ^^\n\n+   ...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-models-e0dade52dc470e8696556760516b65a5864e1f6d-flip_horizontal-235

- repo/project: `models`
- function: `flip_horizontal`
- commit hash: `e0dade52dc470e8696556760516b65a5864e1f6d`
- confidence: `0.0758`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_middleware_auth_flow`
- predicted target: `docs/architecture.md`
- short code diff: - def flip_horizontal(keypoints, flip_point, flip_permutation, scope=None):\n+ def flip_horizontal(keypoints, flip_point, flip_permutation=None, scope=None):\n?                                                            +++++\n\n    \n    \n    with tf.name_scope(scope, 'FlipHorizontal'):\n      keypoints = tf.transpose(keypoints, [1, 0, 2])\n+     if flip_permutation:\n-     keypoints = tf.gather(keypoints, flip_per...[truncated]
- short doc diff:   Flips the keypoints horizontally around the flip_point.\n  \n    This operation flips the x coordinate for each keypoint around the flip_point\n    and also permutes the keypoints in a manner specified by flip_permutation.\n  \n    Args:\n      keypoints: a tensor of shape [num_instances, num_keypoints, 2]\n      flip_point:  (float) scalar tensor represen...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-pytorch-lightning-71a1dd210f3a10f51bee831bf9eeb732b7ddc52f-_LoggerConnector.metrics-335

- repo/project: `pytorch-lightning`
- function: `_LoggerConnector.metrics`
- commit hash: `71a1dd210f3a10f51bee831bf9eeb732b7ddc52f`
- confidence: `0.0792`
- predicted doc category: `developer_setup`
- predicted scenario: `changed_caching_or_rate_limit_flow`
- predicted target: `docs/developer-setup.md`
- short code diff:   def metrics(self) -> _METRICS:\n          \n-         on_step = not self._epoch_end_reached\n+         on_step = self._first_loop_iter is not None\n          assert self.trainer._results is not None\n          return self.trainer._results.metrics(on_step)
- short doc diff: - This function returns either batch or epoch metrics depending on ``_epoch_end_reached``.\n+ This function returns either batch or epoch metrics.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-pytorch-image-models-9cc289f18c80100c8630808cf0842f4eb03f0b5d-list_models-307

- repo/project: `pytorch-image-models`
- function: `list_models`
- commit hash: `9cc289f18c80100c8630808cf0842f4eb03f0b5d`
- confidence: `0.0799`
- predicted doc category: `workflow_documentation`
- predicted scenario: `added_background_job_flow`
- predicted target: `docs/workflows.md`
- short code diff: - def list_models(filter='', module='', pretrained=False):\n+ def list_models(filter='', module='', pretrained=False, exclude_filters=''):\n?                                                       ++++++++++++++++++++\n\n       \n      \n      if module:\n          models = list(_module_to_models[module])\n      else:\n          models = _model_entrypoints.keys()\n      if filter:\n-         models = fnmatch.filter(mo...[truncated]
- short doc diff:   Return list of available model names, sorted alphabetically\n  \n      Args:\n          filter (str) - Wildcard filter string that works with fnmatch\n          module (str) - Limit model selection to a specific sub-module (ie 'gen_efficientnet')\n+         pretrained (bool) - Include only models with pretrained weights if True\n+         exclude_filters (...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-speechbrain-01c8a112f34bb61f26102a584268ec2d65f4a60e-_wordwise_detokenize-11

- repo/project: `speechbrain`
- function: `_wordwise_detokenize`
- commit hash: `01c8a112f34bb61f26102a584268ec2d65f4a60e`
- confidence: `0.0801`
- predicted doc category: `workflow_documentation`
- predicted scenario: `added_background_job_flow`
- predicted target: `docs/workflows.md`
- short code diff: - def _wordwise_detokenize(tokenizer, sequence, output_separtor, token_separator):\n+ def _wordwise_detokenize(tokenizer, sequence, output_separator, token_separator):\n?                                                           +\n\n      \n  \n      \n      if isinstance(sequence, str) and sequence == "":\n          return ""\n      if token_separator not in sequence:\n          sequence_list = (\n              seq...[truncated]
- short doc diff:   Detokenizes a sequence wordwise\n  \n      Arguments\n      ---------\n      tokenizer: speechbrain.tokenizers.SentencePiece.SentencePiece\n          a tokenizer instance\n      sequence: iterable\n          the original sequence\n      output_separator: str\n-         the separator used in the output seauence\n?                                            ...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-cpython-24aa249a6633249570978d6aae6f7b21581ee085-findlinestarts-487

- repo/project: `cpython`
- function: `findlinestarts`
- commit hash: `24aa249a6633249570978d6aae6f7b21581ee085`
- confidence: `0.0802`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_testing_framework`
- predicted target: `docs/testing.md`
- short code diff:   def findlinestarts(code):\n      \n      \n-     lastline = None\n+ \n+     lastline = False # None is a valid line number\n      for start, end, line in code.co_lines():\n-         if line is not None and line != lastline:\n?                       -----------------\n\n+         if line is not lastline:\n              lastline = line\n              yield start, line\n      return
- short doc diff:   Find the offsets in a byte code which are start of lines in the source.\n  \n      Generate pairs (offset, lineno)\n+     lineno will be an integer or None the offset does not have a source line.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-models-9fce9c641e7f51b5931ebb8dc78858baa357adf5-create_tf_record-423

- repo/project: `models`
- function: `create_tf_record`
- commit hash: `9fce9c641e7f51b5931ebb8dc78858baa357adf5`
- confidence: `0.0806`
- predicted doc category: `model_contract`
- predicted scenario: `added_environment_variable`
- predicted target: `docs/models.md`
- short code diff:   def create_tf_record(output_filename,\n+                      num_shards,\n                       label_map_dict,\n                       annotations_dir,\n                       image_dir,\n                       examples,\n                       faces_only=True,\n                       mask_type='png'):\n    \n    \n-   writer = tf.python_io.TFRecordWriter(output_filename)\n+   with contextlib2.ExitStack() as tf_...[truncated]
- short doc diff:   Creates a TFRecord file from examples.\n  \n    Args:\n      output_filename: Path to where output file is saved.\n+     num_shards: Number of shards for output file.\n      label_map_dict: The label map dictionary.\n      annotations_dir: Directory where annotation files are stored.\n      image_dir: Directory where image files are stored.\n      examples...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue


## All False Negative Examples

### codocbench-cpython-6ffface4293f20e504de6a7ca012c482a203409d-move-338

- repo/project: `cpython`
- function: `move`
- commit hash: `6ffface4293f20e504de6a7ca012c482a203409d`
- confidence: `0.5329`
- predicted doc category: `no_update`
- predicted scenario: `docs_already_updated`
- predicted target: ``
- short code diff: - def move(src, dst):\n+ def move(src, dst, copy_function=copy2):\n      \n  \n      \n      real_dst = dst\n      if os.path.isdir(dst):\n          if _samefile(src, dst):\n              # We might be on a case insensitive filesystem,\n              # perform the rename anyway.\n              os.rename(src, dst)\n              return\n  \n          real_dst = os.path.join(dst, _basename(src))\n          if os.path.e...[truncated]
- short doc diff:   Recursively move a file or directory to another location. This is\n      similar to the Unix "mv" command. Return the file or directory's\n      destination.\n  \n      If the destination is a directory or a symlink to a directory, the source\n      is moved inside the directory. The destination path must not already\n      exist.\n  \n      If the destina...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue


## 10 Representative High-Confidence True Positives

### codocbench-st2-e0c6c4e10511bf30e9a01acfa26953736d0e8b01-ActionExecutionSchedulingQueueHandler._get_next_execution-134

- repo/project: `st2`
- function: `ActionExecutionSchedulingQueueHandler._get_next_execution`
- commit hash: `e0c6c4e10511bf30e9a01acfa26953736d0e8b01`
- confidence: `0.5293`
- predicted doc category: `workflow_documentation`
- predicted scenario: `added_background_job_flow`
- predicted target: `docs/workflows.md`
- short code diff:   def _get_next_execution(self):\n          \n          \n          \n          query = {\n              'scheduled_start_timestamp__lte': date.get_datetime_utc_now(),\n              'handling': False,\n              'limit': 1,\n              'order_by': [\n                  '+scheduled_start_timestamp',\n              ]\n          }\n  \n          execution_queue_item_db = ActionExecutionSchedulingQueue.query(**que...[truncated]
- short doc diff: - Sort executions by FIFO and priority and get the latest, highest priority item from the\n?                                                                                    ----\n\n+ Sort execution requests by FIFO and priority and get the latest, highest priority item from\n?               ++++++ ++\n\n-         queue and pop it off.\n+         the queue...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-ansible-0d5a9f2138b0626e1c836333e3af0b73bdc31ec8-run_command-327

- repo/project: `ansible`
- function: `run_command`
- commit hash: `0d5a9f2138b0626e1c836333e3af0b73bdc31ec8`
- confidence: `0.4318`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_test_command`
- predicted target: `docs/testing.md`
- short code diff: - def run_command(args, cmd, capture=False, env=None, data=None, cwd=None, always=False, stdin=None, stdout=None,\n-                 cmd_verbosity=1, str_errors='strict', error_callback=None):\n-     \n-     \n+ def run_command(\n+         args,  # type: CommonConfig\n+         cmd,  # type: t.Iterable[str]\n+         capture=False,  # type: bool\n+         env=None,  # type: t.Optional[t.Dict[str, str]]\n+         d...[truncated]
- short doc diff: + Run the specified command and return stdout and stderr as a tuple.\n- :type args: CommonConfig\n-     :type cmd: collections.Iterable[str]\n-     :type capture: bool\n-     :type env: dict[str, str] | None\n-     :type data: str | None\n-     :type cwd: str | None\n-     :type always: bool\n-     :type stdin: file | None\n-     :type stdout: file | None\n-...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-cpython-eda960a1dde94e0c3a172889d22588f839e4b2de-IMAP4.authenticate-100

- repo/project: `cpython`
- function: `IMAP4.authenticate`
- commit hash: `eda960a1dde94e0c3a172889d22588f839e4b2de`
- confidence: `0.4154`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_middleware_auth_flow`
- predicted target: `docs/architecture.md`
- short code diff: - def authenticate(self, func):\n+ def authenticate(self, mechanism, authobject):\n  		\n  		\n- 		raise self.error('UNIMPLEMENTED')\n+ 		mech = string.upper(mechanism)\n+ 		cap = 'AUTH=%s' % mech\n+ 		if not cap in self.capabilities:\n+ 			raise self.error("Server doesn't allow %s authentication." % mech)\n+ 		self.literal = _Authenticator(authobject).process\n+ 		typ, dat = self._simple_command('AUTHENTICATE', mech...[truncated]
- short doc diff:   Authenticate command - requires response processing.\n  \n- 		UNIMPLEMENTED\n+ 		'mechanism' specifies which authentication mechanism is to\n+ 		be used - it must appear in <instance>.capabilities in the\n+ 		form AUTH=<mechanism>.\n+ \n+ 		'authobject' must be a callable object:\n+ \n+ 			data = authobject(response)\n+ \n+ 		It will be called to process s...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-cpython-5a6d4bf671699152fb417e8f8ba899aa5e1d8d42-TestResult.stop-135

- repo/project: `cpython`
- function: `TestResult.stop`
- commit hash: `5a6d4bf671699152fb417e8f8ba899aa5e1d8d42`
- confidence: `0.3801`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_test_command`
- predicted target: `docs/testing.md`
- short code diff:   def stop(self):\n-         ""\n?         --\n\n+         \n          self.shouldStop = True
- short doc diff: - Indicates that the tests should be aborted\n+ Indicates that the tests should be aborted.\n?                                           +\n
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-freqtrade-16cd1f06b22de6dd80d023ac979bcc75b7548fad-DataProvider.orderbook-163

- repo/project: `freqtrade`
- function: `DataProvider.orderbook`
- commit hash: `16cd1f06b22de6dd80d023ac979bcc75b7548fad`
- confidence: `0.3502`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_validation_max`
- predicted target: `docs/architecture.md`
- short code diff:   def orderbook(self, pair: str, maximum: int) -> Dict[str, List]:\n          \n          \n          \n-         return self._exchange.get_order_book(pair, maximum)\n?                               ^\n\n+         return self._exchange.fetch_l2_order_book(pair, maximum)\n?                               ^  +++++\n
- short doc diff: - fetch latest orderbook data\n? ^\n\n+ Fetch latest l2 orderbook data\n? ^           +++\n\n+         Warning: Does a network request - so use with common sense.\n          :param pair: pair to get the data for\n          :param maximum: Maximum number of orderbook entries to query\n          :return: dict including bids/asks with a total of `maximum` entri...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-django-b1e33ceceda1e75ff68c7deed8f6659683a195d3-FixtureTestCase.test_pseudo_empty_fixtures-495

- repo/project: `django`
- function: `FixtureTestCase.test_pseudo_empty_fixtures`
- commit hash: `b1e33ceceda1e75ff68c7deed8f6659683a195d3`
- confidence: `0.3420`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_test_command`
- predicted target: `docs/testing.md`
- short code diff:   def test_pseudo_empty_fixtures(self):\n-         ""\n?         --\n\n+         \n+         \n+         \n          new_io = StringIO()\n          management.call_command('loaddata', 'pets', stdout=new_io, stderr=new_io)\n          command_output = new_io.getvalue().strip()\n          # No objects will actually be loaded\n          self.assertEqual(command_output, "Installed 0 object(s) (of 2) from 1 fixture(s)")
- short doc diff: - A fixture can contain entries, but lead to nothing in the database; this shouldn't raise an error (ref #14068)\n?                                                                    -------------------------------------------\n\n+ A fixture can contain entries, but lead to nothing in the database;\n+         this shouldn't raise an error (#14068).
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-cpython-a4e018889ac3537e10b48811b4be6356e633b8a0-scheduler.run-98

- repo/project: `cpython`
- function: `scheduler.run`
- commit hash: `a4e018889ac3537e10b48811b4be6356e633b8a0`
- confidence: `0.3322`
- predicted doc category: `workflow_documentation`
- predicted scenario: `added_background_job_flow`
- predicted target: `docs/workflows.md`
- short code diff:   def run(self, blocking=True):\n          \n  \n          \n          # localize variable access to minimize overhead\n          # and to improve thread safety\n          with self._lock:\n              q = self._queue\n              delayfunc = self.delayfunc\n              timefunc = self.timefunc\n              pop = heapq.heappop\n              while q:\n                  time, priority, action, argument, kwargs...[truncated]
- short doc diff:   Execute events until the queue is empty.\n          If blocking is False executes the scheduled events due to\n-         expire soonest (if any) and then return.\n?                                                ^\n\n+         expire soonest (if any) and then return the deadline of the\n?                                                ^^^^^^^^^^^^^^^^^^^^\...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-localstack-41b4d232735084f906778549432b3f8266d2c11d-test_loading_own_specs-422

- repo/project: `localstack`
- function: `test_loading_own_specs`
- commit hash: `41b4d232735084f906778549432b3f8266d2c11d`
- confidence: `0.3277`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_test_command`
- predicted target: `docs/testing.md`
- short code diff:   def test_loading_own_specs():\n      \n      loader = CustomLoader({})\n      # first test that specs remain intact\n-     sqs_query_description = loader.load_service_model("sqs-query", "service-2")\n?                                                           ------\n\n+     sqs_query_description = loader.load_service_model("sqs", "service-2")\n      assert sqs_query_description["metadata"]["protocol"] == "query"\n...[truncated]
- short doc diff: - Ensure that the internalized specifications (f.e. the sqs-query spec) can be handled by the CustomLoader.\n?                                                           ^^^^^\n\n+ Ensure that the internalized specifications (f.e. the sqs-json spec) can be handled by the CustomLoader.\n?                                                           ^^^^\n
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-st2-65804951f641f512f2d8571af2112f860907f0d3-BaseActionAliasTestCase.assertExtractedParametersMatch-284

- repo/project: `st2`
- function: `BaseActionAliasTestCase.assertExtractedParametersMatch`
- commit hash: `65804951f641f512f2d8571af2112f860907f0d3`
- confidence: `0.3230`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_test_command`
- predicted target: `docs/testing.md`
- short code diff:   def assertExtractedParametersMatch(self, format_string, command, values):\n          \n          \n          \n-         extracted_params = extract_parameters(action_alias_db=self.action_alias_db,\n?                                              ^               ^^^^^^^^^^^^^^^^^^^^^^\n\n+         extracted_params = extract_parameters_for_action_alias_db(\n?                                              ^^^^^         ...[truncated]
- short doc diff: + Assert that the provided command matches the format string.\n- Assert that the parameters extracted from the user provided command string match the\n-         provided values.\n  \n          In addition to that, also assert that the parameters which have been extracted from the\n-         user input also match the provided parameters.\n+         user input...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-Open-Assistant-48c438041890422019976902f636fc9f71bc4a22-get_current_user_id-378

- repo/project: `Open-Assistant`
- function: `get_current_user_id`
- commit hash: `48c438041890422019976902f636fc9f71bc4a22`
- confidence: `0.3159`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_middleware_auth_flow`
- predicted target: `docs/architecture.md`
- short code diff:   def get_current_user_id(token: str = Security(oauth2_scheme)) -> str | None:\n      \n      if not settings.use_auth:\n          return None\n+     if token is None:\n+         raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authenticated")\n  \n      # Generate a key from the auth secret\n-     key = derive_key()\n+     key: bytes = derive_key()\n?        +++++++\n\n  \n      # Decrypt the JWE toke...[truncated]
- short doc diff: - Decode the current user JWT token and return the payload.\n+ Get the current user ID by decoding the JWT token.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue


## 10 Representative Low-Confidence True Positives

### codocbench-core-411cc6542ca034694eadaa7502fac4c68b516cf1-lookup_plex_media-360

- repo/project: `core`
- function: `lookup_plex_media`
- commit hash: `411cc6542ca034694eadaa7502fac4c68b516cf1`
- confidence: `0.0630`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_test_command`
- predicted target: `docs/architecture.md`
- short code diff:   def lookup_plex_media(hass, content_type, content_id):\n      \n      content = json.loads(content_id)\n  \n      if isinstance(content, int):\n          content = {"plex_key": content}\n          content_type = DOMAIN\n  \n      plex_server_name = content.pop("plex_server", None)\n      shuffle = content.pop("shuffle", 0)\n  \n      plex_server = get_plex_server(hass, plex_server_name=plex_server_name)\n-     if n...[truncated]
- short doc diff: - Look up Plex media using media_player.play_media service payloads.\n+ Look up Plex media for other integrations using media_player.play_media service payloads.\n?                    +++++++++++++++++++++++\n
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-aws-sam-cli-bedd5d53d99ae64dacc487d72108c2b7cef58f5d-SamFunctionProvider._extract_functions-364

- repo/project: `aws-sam-cli`
- function: `SamFunctionProvider._extract_functions`
- commit hash: `bedd5d53d99ae64dacc487d72108c2b7cef58f5d`
- confidence: `0.0635`
- predicted doc category: `architecture_flow`
- predicted scenario: `removed_environment_variable`
- predicted target: `docs/architecture.md`
- short code diff:   def _extract_functions(\n-         stacks: List[Stack], use_raw_codeuri: bool = False, ignore_code_extraction_warnings: bool = False\n+         stacks: List[Stack],\n+         use_raw_codeuri: bool = False,\n+         ignore_code_extraction_warnings: bool = False,\n+         locate_layer_nested: bool = False,\n      ) -> Dict[str, Function]:\n          \n          \n          \n  \n          result: Dict[str, Funct...[truncated]
- short doc diff:   Extracts and returns function information from the given dictionary of SAM/CloudFormation resources. This\n          method supports functions defined with AWS::Serverless::Function and AWS::Lambda::Function\n  \n          :param stacks: List of SAM/CloudFormation stacks to extract functions from\n          :param bool use_raw_codeuri: Do not resolve adjus...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-image-8432b90eb84d5ec4dea04631f087402bf61c1a12-rotate-297

- repo/project: `scikit-image`
- function: `rotate`
- commit hash: `8432b90eb84d5ec4dea04631f087402bf61c1a12`
- confidence: `0.0650`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_local_development_flow`
- predicted target: `docs/architecture.md`
- short code diff: - def rotate(image, angle, resize=False, order=1, mode='constant', cval=0.):\n?                                                                         ^^\n\n+ def rotate(image, angle, resize=False, order=1, mode='constant', cval=0.,\n?                                                                         ^\n\n+            center=None):\n      \n  \n      \n  \n      rows, cols = image.shape[0], image.shape[1]\n  \...[truncated]
- short doc diff:   Rotate image by a certain angle around its center.\n  \n      Parameters\n      ----------\n      image : ndarray\n          Input image.\n      angle : float\n          Rotation angle in degrees in counter-clockwise direction.\n      resize : bool, optional\n          Determine whether the shape of the output image will be automatically\n          calcula...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-django-ce3c71faf1ff83494193b48a6f99256d0628b2a2-Query.join_parent_model-385

- repo/project: `django`
- function: `Query.join_parent_model`
- commit hash: `ce3c71faf1ff83494193b48a6f99256d0628b2a2`
- confidence: `0.0686`
- predicted doc category: `workflow_documentation`
- predicted scenario: `added_background_job_flow`
- predicted target: `docs/workflows.md`
- short code diff:   def join_parent_model(self, opts, model, alias, seen):\n          \n          \n          \n          if model in seen:\n              return seen[model]\n          int_opts = opts\n          chain = opts.get_base_chain(model)\n          if chain is None:\n              return alias\n          for int_model in chain:\n              if int_model in seen:\n                  return seen[int_model]\n              # Pro...[truncated]
- short doc diff:   Makes sure the given 'model' is joined in the query. If 'model' isn't\n          a parent of 'opts' or if it is None this method is a no-op.\n  \n          The 'alias' is the root alias for starting the join, 'seen' is a dict\n-         of model -> alias of existing joins.\n+         of model -> alias of existing joins. It must also contain a mapping\n+   ...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-faceswap-6ee896d175145297ecae001d1a6f4628b5b4e6ef-_EventParser._parse_outputs-251

- repo/project: `faceswap`
- function: `_EventParser._parse_outputs`
- commit hash: `6ee896d175145297ecae001d1a6f4628b5b4e6ef`
- confidence: `0.0687`
- predicted doc category: `workflow_documentation`
- predicted scenario: `added_background_job_flow`
- predicted target: `docs/workflows.md`
- short code diff:   def _parse_outputs(self, event):\n           \n          \n          serializer = get_serializer("json")\n          struct = event.summary.value[0].tensor.string_val[0]\n+ \n+         config = serializer.unmarshal(struct)["config"]\n+         model_outputs = self._get_outputs(config)\n+         split_output = len(np.unique(model_outputs[..., 1])) == 1\n+ \n-         outputs = np.array(serializer.unmarshal(struct)["...[truncated]
- short doc diff:   Parse the outputs from the stored model structure for mapping loss names to\n          model outputs.\n  \n          Loss names are added to :attr:`_loss_labels`\n  \n+         Notes\n+         -----\n+         The master model does not actually contain the specified output name, so we dig into the\n+         sub-model to obtain the name of the output laye...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-django-cb0da637a69b79ab371be9ee202335190a3a506e-GDALRaster.transform-64

- repo/project: `django`
- function: `GDALRaster.transform`
- commit hash: `cb0da637a69b79ab371be9ee202335190a3a506e`
- confidence: `0.0700`
- predicted doc category: `workflow_documentation`
- predicted scenario: `changed_testing_framework`
- predicted target: `docs/workflows.md`
- short code diff: - def transform(self, srid, driver=None, name=None, resampling='NearestNeighbour',\n?                       ^^\n\n+ def transform(self, srs, driver=None, name=None, resampling='NearestNeighbour',\n?                       ^\n\n                    max_error=0.0):\n          \n          \n          \n          # Convert the resampling algorithm name into an algorithm id\n          algorithm = GDAL_RESAMPLE_ALGORITHMS[re...[truncated]
- short doc diff: - Return a copy of this raster reprojected into the given SRID.\n?                                                         ^^^^^\n\n+ Return a copy of this raster reprojected into the given spatial\n?                                                         ^^^^^^^\n\n+         reference system.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-twine-09fe3a40c09f3cdddb42af6331dcc6ee8d923779-Tiddler.displays-147

- repo/project: `twine`
- function: `Tiddler.displays`
- commit hash: `09fe3a40c09f3cdddb42af6331dcc6ee8d923779`
- confidence: `0.0712`
- predicted doc category: `configuration`
- predicted scenario: `changed_test_command`
- predicted target: `docs/configuration.md`
- short code diff:   def displays(self):\n  		\n  		\n  		\n- 		if ('script' in self.tags) or ('stylesheet' in self.tags):\n+ 		if not self.isStoryText():\n  			return []\n  		return re.findall(r'\<\<display\s+[\'"]?(.+?)[\'"]?\s?\>\>', self.text, re.IGNORECASE)
- short doc diff: - Returns a list of all passages <<display>>ed by this one. By default,\n?                                                          ------------\n\n+ Returns a list of all passages <<display>>ed by this one.\n- 		returns internal links and dis
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-datasets-6be722dbbc212d88eb5e550e56431cdcab180eee-Dataset.from_sql-31

- repo/project: `datasets`
- function: `Dataset.from_sql`
- commit hash: `6be722dbbc212d88eb5e550e56431cdcab180eee`
- confidence: `0.0715`
- predicted doc category: `developer_setup`
- predicted scenario: `removed_request_field`
- predicted target: `docs/developer-setup.md`
- short code diff:   def from_sql(\n          sql: Union[str, "sqlalchemy.sql.Selectable"],\n-         con: str,\n+         con: Union[str, "sqlalchemy.engine.Connection", "sqlalchemy.engine.Engine", "sqlite3.Connection"],\n          features: Optional[Features] = None,\n          cache_dir: str = None,\n          keep_in_memory: bool = False,\n          **kwargs,\n      ):\n          \n          \n          from .io.sql import SqlData...[truncated]
- short doc diff:   Create Dataset from SQL query or database table.\n  \n          Args:\n              sql (`str` or :obj:`sqlalchemy.sql.Selectable`): SQL query to be executed or a table name.\n-             con (`str`): A connection URI string used to instantiate a database connection.\n+             con (`str` or :obj:`sqlite3.Connection` or :obj:`sqlalchemy.engine.Conne...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-langchain-1c7b3c75a7b1235d6cf26fe00e8bc25b33ac29a6-create_pandas_dataframe_agent-330

- repo/project: `langchain`
- function: `create_pandas_dataframe_agent`
- commit hash: `1c7b3c75a7b1235d6cf26fe00e8bc25b33ac29a6`
- confidence: `0.0728`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_local_development_flow`
- predicted target: `docs/architecture.md`
- short code diff:   def create_pandas_dataframe_agent(\n      llm: LanguageModelLike,\n      df: Any,\n      agent_type: Union[\n-         AgentType, Literal["openai-tools"]\n+         AgentType, Literal["openai-tools", "tool-calling"]\n?                                          ++++++++++++++++\n\n      ] = AgentType.ZERO_SHOT_REACT_DESCRIPTION,\n      callback_manager: Optional[BaseCallbackManager] = None,\n      prefix: Optional[st...[truncated]
- short doc diff:   Construct a Pandas agent from an LLM and dataframe(s).\n  \n      Args:\n-         llm: Language model to use for the agent.\n+         llm: Language model to use for the agent. If agent_type is "tool-calling" then\n+             llm is expected to support tool calling.\n          df: Pandas dataframe or list of Pandas dataframes.\n-         agent_type: On...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-rf-1b02349352d40d7bb0cf76455d28b84a847970b0-LRRM.__init__-462

- repo/project: `scikit-rf`
- function: `LRRM.__init__`
- commit hash: `1b02349352d40d7bb0cf76455d28b84a847970b0`
- confidence: `0.0740`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_middleware_auth_flow`
- predicted target: `docs/architecture.md`
- short code diff:   def __init__(self, measured, ideals, switch_terms=None, isolation=None,\n              z0=50, match_fit='l', *args, **kwargs):\n          \n          \n          \n  \n          self.z0 = z0\n          # TODO: Second port not implemented.\n          self.match_port = 0\n+         # Maximum frequency to assume that open behaves like ideal capacitor when\n+         # using match_fit == 'lc'.\n+         self.lc_fit_c_...[truncated]
- short doc diff:   LRRM Initializer.\n-         \n+ \n          Parameters\n          ----------\n          measured : list of :class:`~skrf.network.Network` objects\n              Raw measurements of the calibration standards. The order\n              must be line, reflect, reflect, match and must align with the\n              `ideals` parameter\n  \n          ideals : list...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue


## Limitations

- CoDocBench labels are code-docstring/comment co-change positives, not project-level Markdown documentation labels.
- Positive recall here should be treated as an external robustness signal.
- External precision and F1 require a defensible external negative set with separately reported label provenance.
