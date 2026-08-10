# External CoDocBench Existing DocGuard Positive Recall 2026-08

- Input: `data\external\codocbench_sample_500.jsonl`
- Predictor used: `hf_embedding_staged_raw_diff_plus_docs`
- Model path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\models\hf_v0_4\raw_diff_plus_docs\embedding_classifier_staged.joblib`
- Model type: `LogisticRegression`
- Model name: `sentence-transformers/all-MiniLM-L6-v2`
- Input mode: `raw_diff_plus_docs`
- Classifier architecture: `staged`
- External input mode: `code_diff_plus_doc_before`
- External input leakage label: `assisted`
- External input mode definition: Uses changed file, function name, code_diff, and doc_before only. No future doc diff or doc_after is included.
- Decision rule: docs_update_required is true when the staged docs_update_required classifier top label is `true`.
- Confidence definition: minimum probability across docs_update_required, positive doc_category, positive scenario_type, and positive target_doc_file classifiers for positive predictions
- Threshold used for binary decision: `none for binary decision; confidence thresholds are analyzed only as abstention/review policies`
- Total positives evaluated: `500`
- Predicted update-required count: `499`
- False negative count: `1`
- Positive recall: `99.80%`
- Low-confidence threshold: `0.25`
- Low-confidence count below 0.25: `473`
- Low-confidence percentage: `94.60%`
- Min confidence: `0.0634`
- Max confidence: `0.5493`
- Mean confidence: `0.1404`
- Median confidence: `0.1245`
- Q1 confidence: `0.1029`
- Q3 confidence: `0.1568`

## Leakage Warning

This run does not include `doc_diff` or `doc_after` in the predictor input. See `reports/external_codocbench_evaluation_leakage_audit_2026_08.md` for the input construction audit.

## What This Evaluation Can and Cannot Measure

This positive-only CoDocBench pilot can measure positive recall, false negatives, confidence distribution, and predicted label distributions.

It cannot measure precision, F1, false-positive rate, or negative classification quality because no defensible external negative set is included.

## Confidence Deciles

| Percentile | Confidence |
| --- | ---: |
| `p10` | 0.0911 |
| `p20` | 0.0984 |
| `p30` | 0.1060 |
| `p40` | 0.1142 |
| `p50` | 0.1245 |
| `p60` | 0.1340 |
| `p70` | 0.1505 |
| `p80` | 0.1679 |
| `p90` | 0.2114 |

## Confidence Histogram

| Bin | Count | Percentage |
| --- | ---: | ---: |
| `0.0-0.1` | 110 | 22.00% |
| `0.1-0.2` | 332 | 66.40% |
| `0.2-0.3` | 43 | 8.60% |
| `0.3-0.4` | 11 | 2.20% |
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
| 0.10 | 390 | 78.00% | 389 | 110 | 77.80% | 99.74% |
| 0.20 | 58 | 11.60% | 57 | 442 | 11.40% | 98.28% |
| 0.25 | 27 | 5.40% | 26 | 473 | 5.20% | 96.30% |
| 0.30 | 15 | 3.00% | 14 | 485 | 2.80% | 93.33% |
| 0.40 | 4 | 0.80% | 3 | 496 | 0.60% | 75.00% |
| 0.50 | 2 | 0.40% | 1 | 498 | 0.20% | 50.00% |
| 0.75 | 0 | 0.00% | 0 | 500 | 0.00% | 0.00% |

The accepted-only recall column is positive-only and does not measure precision. The all-positives recall column treats abstentions as missed positives.

## Predicted Doc Category Distribution

- `architecture_flow`: 170
- `developer_setup`: 127
- `testing_instructions`: 69
- `workflow_documentation`: 59
- `configuration`: 47
- `api_reference`: 18
- `changelog`: 6
- `model_contract`: 3
- `no_update`: 1

## Predicted Scenario Type Distribution

- `changed_validation_max`: 103
- `added_environment_variable`: 75
- `changed_local_development_flow`: 58
- `changed_caching_or_rate_limit_flow`: 44
- `changed_test_command`: 43
- `changed_testing_framework`: 32
- `added_background_job_flow`: 29
- `changed_seed_or_setup_flow`: 19
- `changed_middleware_auth_flow`: 18
- `changed_enum_values`: 13
- `changed_validation_min`: 10
- `removed_dto_model_field`: 9
- `removed_endpoint`: 8
- `changed_error_handling_flow`: 7
- `added_dto_model_field`: 6
- `changelog_worthy_behavior_change`: 6
- `changed_endpoint_path`: 4
- `changed_default_config_value`: 4
- `added_service_orchestration_flow`: 3
- `changed_http_method`: 3
- `changed_background_job_schedule`: 1
- `added_response_field`: 1
- `removed_environment_variable`: 1
- `docs_already_updated`: 1
- `changed_auth_requirement`: 1
- `removed_request_field`: 1

## Predicted Target Doc File Distribution

- `docs/architecture.md`: 170
- `docs/developer-setup.md`: 127
- `docs/testing.md`: 69
- `docs/workflows.md`: 59
- `docs/configuration.md`: 47
- `docs/api.md`: 18
- `CHANGELOG.md`: 6
- `docs/models.md`: 3
- `unknown`: 1

## Top 20 Lowest-Confidence True Positives

### codocbench-aws-sam-cli-bedd5d53d99ae64dacc487d72108c2b7cef58f5d-SamFunctionProvider._extract_functions-364

- repo/project: `aws-sam-cli`
- function: `SamFunctionProvider._extract_functions`
- commit hash: `bedd5d53d99ae64dacc487d72108c2b7cef58f5d`
- confidence: `0.0634`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_endpoint_path`
- predicted target: `docs/architecture.md`
- short code diff:   def _extract_functions(\n-         stacks: List[Stack], use_raw_codeuri: bool = False, ignore_code_extraction_warnings: bool = False\n+         stacks: List[Stack],\n+         use_raw_codeuri: bool = False,\n+         ignore_code_extraction_warnings: bool = False,\n+         locate_layer_nested: bool = False,\n      ) -> Dict[str, Function]:\n          \n          \n          \n  \n          result: Dict[str, Funct...[truncated]
- short doc diff:   Extracts and returns function information from the given dictionary of SAM/CloudFormation resources. This\n          method supports functions defined with AWS::Serverless::Function and AWS::Lambda::Function\n  \n          :param stacks: List of SAM/CloudFormation stacks to extract functions from\n          :param bool use_raw_codeuri: Do not resolve adjus...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-faceswap-6ee896d175145297ecae001d1a6f4628b5b4e6ef-_EventParser._parse_outputs-251

- repo/project: `faceswap`
- function: `_EventParser._parse_outputs`
- commit hash: `6ee896d175145297ecae001d1a6f4628b5b4e6ef`
- confidence: `0.0648`
- predicted doc category: `workflow_documentation`
- predicted scenario: `removed_dto_model_field`
- predicted target: `docs/workflows.md`
- short code diff:   def _parse_outputs(self, event):\n           \n          \n          serializer = get_serializer("json")\n          struct = event.summary.value[0].tensor.string_val[0]\n+ \n+         config = serializer.unmarshal(struct)["config"]\n+         model_outputs = self._get_outputs(config)\n+         split_output = len(np.unique(model_outputs[..., 1])) == 1\n+ \n-         outputs = np.array(serializer.unmarshal(struct)["...[truncated]
- short doc diff:   Parse the outputs from the stored model structure for mapping loss names to\n          model outputs.\n  \n          Loss names are added to :attr:`_loss_labels`\n  \n+         Notes\n+         -----\n+         The master model does not actually contain the specified output name, so we dig into the\n+         sub-model to obtain the name of the output laye...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-image-8432b90eb84d5ec4dea04631f087402bf61c1a12-rotate-297

- repo/project: `scikit-image`
- function: `rotate`
- commit hash: `8432b90eb84d5ec4dea04631f087402bf61c1a12`
- confidence: `0.0677`
- predicted doc category: `developer_setup`
- predicted scenario: `changed_local_development_flow`
- predicted target: `docs/developer-setup.md`
- short code diff: - def rotate(image, angle, resize=False, order=1, mode='constant', cval=0.):\n?                                                                         ^^\n\n+ def rotate(image, angle, resize=False, order=1, mode='constant', cval=0.,\n?                                                                         ^\n\n+            center=None):\n      \n  \n      \n  \n      rows, cols = image.shape[0], image.shape[1]\n  \...[truncated]
- short doc diff:   Rotate image by a certain angle around its center.\n  \n      Parameters\n      ----------\n      image : ndarray\n          Input image.\n      angle : float\n          Rotation angle in degrees in counter-clockwise direction.\n      resize : bool, optional\n          Determine whether the shape of the output image will be automatically\n          calcula...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-django-cb0da637a69b79ab371be9ee202335190a3a506e-GDALRaster.transform-64

- repo/project: `django`
- function: `GDALRaster.transform`
- commit hash: `cb0da637a69b79ab371be9ee202335190a3a506e`
- confidence: `0.0678`
- predicted doc category: `workflow_documentation`
- predicted scenario: `changed_testing_framework`
- predicted target: `docs/workflows.md`
- short code diff: - def transform(self, srid, driver=None, name=None, resampling='NearestNeighbour',\n?                       ^^\n\n+ def transform(self, srs, driver=None, name=None, resampling='NearestNeighbour',\n?                       ^\n\n                    max_error=0.0):\n          \n          \n          \n          # Convert the resampling algorithm name into an algorithm id\n          algorithm = GDAL_RESAMPLE_ALGORITHMS[re...[truncated]
- short doc diff: - Return a copy of this raster reprojected into the given SRID.\n?                                                         ^^^^^\n\n+ Return a copy of this raster reprojected into the given spatial\n?                                                         ^^^^^^^\n\n+         reference system.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-image-7ea6a37634d4656955fefeede0ae815814d5efef-checkerboard-270

- repo/project: `scikit-image`
- function: `checkerboard`
- commit hash: `7ea6a37634d4656955fefeede0ae815814d5efef`
- confidence: `0.0700`
- predicted doc category: `configuration`
- predicted scenario: `changed_testing_framework`
- predicted target: `docs/configuration.md`
- short code diff:   def checkerboard():\n      \n  \n      \n-     return load("chessboard_RGB.png")\n?                              ^^\n\n+     return load("chessboard_GRAY_U8.png")\n?                             + ^^^^^\n
- short doc diff:   Checkerboard image.\n+ \n+     Checkerboards are often used in image calibration, since the\n+     corner-points are easy to locate.  Because of the many parallel\n+     edges, they also visualise distortions particularly well.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-rf-1b02349352d40d7bb0cf76455d28b84a847970b0-LRRM.__init__-462

- repo/project: `scikit-rf`
- function: `LRRM.__init__`
- commit hash: `1b02349352d40d7bb0cf76455d28b84a847970b0`
- confidence: `0.0716`
- predicted doc category: `architecture_flow`
- predicted scenario: `removed_dto_model_field`
- predicted target: `docs/architecture.md`
- short code diff:   def __init__(self, measured, ideals, switch_terms=None, isolation=None,\n              z0=50, match_fit='l', *args, **kwargs):\n          \n          \n          \n  \n          self.z0 = z0\n          # TODO: Second port not implemented.\n          self.match_port = 0\n+         # Maximum frequency to assume that open behaves like ideal capacitor when\n+         # using match_fit == 'lc'.\n+         self.lc_fit_c_...[truncated]
- short doc diff:   LRRM Initializer.\n-         \n+ \n          Parameters\n          ----------\n          measured : list of :class:`~skrf.network.Network` objects\n              Raw measurements of the calibration standards. The order\n              must be line, reflect, reflect, match and must align with the\n              `ideals` parameter\n  \n          ideals : list...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-twine-09fe3a40c09f3cdddb42af6331dcc6ee8d923779-Tiddler.displays-147

- repo/project: `twine`
- function: `Tiddler.displays`
- commit hash: `09fe3a40c09f3cdddb42af6331dcc6ee8d923779`
- confidence: `0.0723`
- predicted doc category: `configuration`
- predicted scenario: `changelog_worthy_behavior_change`
- predicted target: `docs/configuration.md`
- short code diff:   def displays(self):\n  		\n  		\n  		\n- 		if ('script' in self.tags) or ('stylesheet' in self.tags):\n+ 		if not self.isStoryText():\n  			return []\n  		return re.findall(r'\<\<display\s+[\'"]?(.+?)[\'"]?\s?\>\>', self.text, re.IGNORECASE)
- short doc diff: - Returns a list of all passages <<display>>ed by this one. By default,\n?                                                          ------------\n\n+ Returns a list of all passages <<display>>ed by this one.\n- 		returns internal links and dis
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-faceswap-d8557c1970939ee9bb90bd41edcd86c6fcf84d19-PixelShuffler.call-463

- repo/project: `faceswap`
- function: `PixelShuffler.call`
- commit hash: `d8557c1970939ee9bb90bd41edcd86c6fcf84d19`
- confidence: `0.0741`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_validation_max`
- predicted target: `docs/testing.md`
- short code diff: - def call(self, inputs, **kwargs):\n+ def call(self, inputs, **kwargs):  # pylint:disable=unused-argument\n          \n          \n          input_shape = K.int_shape(inputs)\n          if len(input_shape) != 4:\n              raise ValueError('Inputs should have rank ' +\n                               str(4) +\n                               '; Received input shape:', str(input_shape))\n  \n          if self.data_...[truncated]
- short doc diff:   This is where the layer's logic lives.\n  \n          Parameters\n          ----------\n          inputs: tensor\n              Input tensor, or list/tuple of input tensors\n          kwargs: dict\n-             Additional keyword arguments\n+             Additional keyword arguments. Unused\n?                                         ++++++++\n\n  \n      ...[truncated]
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

### codocbench-langchain-e83250cc5f4dc5edd1ae8fb0a41c40454d13fb9d-StringRunEvaluatorChain.from_run_and_data_type-195

- repo/project: `langchain`
- function: `StringRunEvaluatorChain.from_run_and_data_type`
- commit hash: `e83250cc5f4dc5edd1ae8fb0a41c40454d13fb9d`
- confidence: `0.0769`
- predicted doc category: `developer_setup`
- predicted scenario: `added_environment_variable`
- predicted target: `docs/developer-setup.md`
- short code diff:   def from_run_and_data_type(\n          cls,\n          evaluator: StringEvaluator,\n-         run_type: RunTypeEnum,\n+         run_type: str,\n          data_type: DataType,\n          input_key: Optional[str] = None,\n          prediction_key: Optional[str] = None,\n          reference_key: Optional[str] = None,\n          tags: Optional[List[str]] = None,\n      ) -> StringRunEvaluatorChain:\n          \n       ...[truncated]
- short doc diff:   Create a StringRunEvaluatorChain from an evaluator and the run and dataset types.\n  \n          This method provides an easy way to instantiate a StringRunEvaluatorChain, by\n          taking an evaluator and information about the type of run and the data.\n          The method supports LLM and chain runs.\n  \n          Args:\n              evaluator (St...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-pytorch-lightning-71a1dd210f3a10f51bee831bf9eeb732b7ddc52f-_LoggerConnector.metrics-335

- repo/project: `pytorch-lightning`
- function: `_LoggerConnector.metrics`
- commit hash: `71a1dd210f3a10f51bee831bf9eeb732b7ddc52f`
- confidence: `0.0773`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_caching_or_rate_limit_flow`
- predicted target: `docs/architecture.md`
- short code diff:   def metrics(self) -> _METRICS:\n          \n-         on_step = not self._epoch_end_reached\n+         on_step = self._first_loop_iter is not None\n          assert self.trainer._results is not None\n          return self.trainer._results.metrics(on_step)
- short doc diff: - This function returns either batch or epoch metrics depending on ``_epoch_end_reached``.\n+ This function returns either batch or epoch metrics.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-ray-9a8ca6a69d98c639f4ed0d747a84bc55c760fe40-wrap_deepmind-164

- repo/project: `ray`
- function: `wrap_deepmind`
- commit hash: `9a8ca6a69d98c639f4ed0d747a84bc55c760fe40`
- confidence: `0.0780`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_caching_or_rate_limit_flow`
- predicted target: `docs/architecture.md`
- short code diff: + def wrap_deepmind(env, dim=84, framestack=True):\n- def wrap_deepmind(\n-         env,\n-         dim=84,\n-         # TODO: (sven) Remove once traj. view is norm.\n-         framestack=True,\n-         framestack_via_traj_view_api=False):\n      \n      \n      env = MonitorEnv(env)\n      env = NoopResetEnv(env, noop_max=30)\n      if env.spec is not None and "NoFrameskip" in env.spec.id:\n          env = MaxAndS...[truncated]
- short doc diff:   Configure environment for DeepMind-style Atari.\n  \n      Note that we assume reward clipping is done outside the wrapper.\n  \n      Args:\n+         env (EnvType): The env object to wrap.\n          dim (int): Dimension to resize observations to (dim x dim).\n          framestack (bool): Whether to framestack observations.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-rf-48729401374e2b1583cad31d788c7b4990684d10-plot_complex_polar-247

- repo/project: `scikit-rf`
- function: `plot_complex_polar`
- commit hash: `48729401374e2b1583cad31d788c7b4990684d10`
- confidence: `0.0783`
- predicted doc category: `developer_setup`
- predicted scenario: `changed_validation_max`
- predicted target: `docs/developer-setup.md`
- short code diff: - def plot_complex_polar(z, x_label=None, y_label=None,\n-     title=None, show_legend=True, axis_equal=False, ax=None,\n-     *args, **kwargs):\n-     '''\n+ def plot_complex_polar(z: NumberLike,\n+                        x_label: Union[str, None] = None, y_label: Union[str, None] = None,\n+                        title: Union[str, None] = None, show_legend: bool = True,\n+                        axis_equal: bool = ...[truncated]
- short doc diff: - plot complex data in polar format.\n? ^\n\n+ Plot complex data in polar format.\n? ^\n\n  \n      Parameters\n-     ------------\n?               --\n\n+     ----------\n      z : array-like, of complex data\n          data to plot\n-     x_label : string\n-         x-axis label\n-     y_label : string\n-         y-axis label\n-     title : string\n-      ...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-django-6fe2b001dba45134d7c10729c57959995e241a88-Query.promote_joins-86

- repo/project: `django`
- function: `Query.promote_joins`
- commit hash: `6fe2b001dba45134d7c10729c57959995e241a88`
- confidence: `0.0787`
- predicted doc category: `workflow_documentation`
- predicted scenario: `removed_endpoint`
- predicted target: `docs/workflows.md`
- short code diff:   def promote_joins(self, aliases):\n          \n          \n          \n          aliases = list(aliases)\n          while aliases:\n              alias = aliases.pop(0)\n              if self.alias_map[alias].join_cols[0][1] is None:\n                  # This is the base table (first FROM entry) - this table\n                  # isn't really joined at all in the query, so we should not\n                  # alter it...[truncated]
- short doc diff:   Promotes recursively the join type of given aliases and its children to\n          an outer join. If 'unconditional' is False, the join is only promoted if\n          it is nullable or the parent join is an outer join.\n  \n+         The children promotion is done to avoid join chains that contain a LOUTER\n+         b INNER c. So, if we have currently a I...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-django-5074c75a37f88726f3ae057999144545881d3cfc-QuerySet.select_related-12

- repo/project: `django`
- function: `QuerySet.select_related`
- commit hash: `5074c75a37f88726f3ae057999144545881d3cfc`
- confidence: `0.0794`
- predicted doc category: `configuration`
- predicted scenario: `added_environment_variable`
- predicted target: `docs/configuration.md`
- short code diff:   def select_related(self, *fields, **kwargs):\n          \n          \n          \n          if 'depth' in kwargs:\n              warnings.warn('The "depth" keyword argument has been deprecated.\n'\n                      'Use related field names instead.', DeprecationWarning, stacklevel=2)\n          depth = kwargs.pop('depth', 0)\n          if kwargs:\n              raise TypeError('Unexpected keyword arguments to ...[truncated]
- short doc diff:   Returns a new QuerySet instance that will select related objects.\n  \n          If fields are specified, they must be ForeignKey fields and only those\n          related objects are included in the selection.\n+ \n+         If select_related(None) is called, the list is cleared.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-core-411cc6542ca034694eadaa7502fac4c68b516cf1-lookup_plex_media-360

- repo/project: `core`
- function: `lookup_plex_media`
- commit hash: `411cc6542ca034694eadaa7502fac4c68b516cf1`
- confidence: `0.0802`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_error_handling_flow`
- predicted target: `docs/architecture.md`
- short code diff:   def lookup_plex_media(hass, content_type, content_id):\n      \n      content = json.loads(content_id)\n  \n      if isinstance(content, int):\n          content = {"plex_key": content}\n          content_type = DOMAIN\n  \n      plex_server_name = content.pop("plex_server", None)\n      shuffle = content.pop("shuffle", 0)\n  \n      plex_server = get_plex_server(hass, plex_server_name=plex_server_name)\n-     if n...[truncated]
- short doc diff: - Look up Plex media using media_player.play_media service payloads.\n+ Look up Plex media for other integrations using media_player.play_media service payloads.\n?                    +++++++++++++++++++++++\n
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-langchain-c80e406e95b5dd7b0d2c08f215b7ee0a6d49740e-CubeSemanticLoader.load-293

- repo/project: `langchain`
- function: `CubeSemanticLoader.load`
- commit hash: `c80e406e95b5dd7b0d2c08f215b7ee0a6d49740e`
- confidence: `0.0804`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_validation_max`
- predicted target: `docs/architecture.md`
- short code diff:   def load(self) -> List[Document]:\n          \n          \n          headers = {\n              "Content-Type": "application/json",\n              "Authorization": self.cube_api_token,\n          }\n  \n+         logger.info(f"Loading metadata from {self.cube_api_url}...")\n          response = requests.get(f"{self.cube_api_url}/meta", headers=headers)\n          response.raise_for_status()\n          raw_meta_json...[truncated]
- short doc diff:   Makes a call to Cube's REST API metadata endpoint.\n  \n          Returns:\n              A list of documents with attributes:\n                  - page_content=column_title + column_description\n                  - metadata\n                      - table_name\n                      - column_name\n                      - column_data_type\n                 ...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-models-e0dade52dc470e8696556760516b65a5864e1f6d-flip_horizontal-235

- repo/project: `models`
- function: `flip_horizontal`
- commit hash: `e0dade52dc470e8696556760516b65a5864e1f6d`
- confidence: `0.0816`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_local_development_flow`
- predicted target: `docs/architecture.md`
- short code diff: - def flip_horizontal(keypoints, flip_point, flip_permutation, scope=None):\n+ def flip_horizontal(keypoints, flip_point, flip_permutation=None, scope=None):\n?                                                            +++++\n\n    \n    \n    with tf.name_scope(scope, 'FlipHorizontal'):\n      keypoints = tf.transpose(keypoints, [1, 0, 2])\n+     if flip_permutation:\n-     keypoints = tf.gather(keypoints, flip_per...[truncated]
- short doc diff:   Flips the keypoints horizontally around the flip_point.\n  \n    This operation flips the x coordinate for each keypoint around the flip_point\n    and also permutes the keypoints in a manner specified by flip_permutation.\n  \n    Args:\n      keypoints: a tensor of shape [num_instances, num_keypoints, 2]\n      flip_point:  (float) scalar tensor represen...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-learn-0bdc754e5dcfb155ce1a042d2a123b515a05efcb-_BaseNMF.inverse_transform-436

- repo/project: `scikit-learn`
- function: `_BaseNMF.inverse_transform`
- commit hash: `0bdc754e5dcfb155ce1a042d2a123b515a05efcb`
- confidence: `0.0819`
- predicted doc category: `developer_setup`
- predicted scenario: `changed_testing_framework`
- predicted target: `docs/developer-setup.md`
- short code diff: - def inverse_transform(self, Xt=None, W=None):\n?                                    --------\n\n+ def inverse_transform(self, X=None, *, Xt=None):\n?                             +++++++++++\n\n          \n          \n-         if Xt is None and W is None:\n-             raise TypeError("Missing required positional argument: Xt")\n  \n+         X = _deprecate_Xt_in_inverse_transform(X, Xt)\n-         if W is not Non...[truncated]
- short doc diff:   Transform data back to its original space.\n  \n          .. versionadded:: 0.18\n  \n          Parameters\n          ----------\n+         X : {ndarray, sparse matrix} of shape (n_samples, n_components)\n+             Transformed data matrix.\n+ \n          Xt : {ndarray, sparse matrix} of shape (n_samples, n_components)\n              Transformed data ma...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-aws-sam-cli-6733ccdcd026b364cc56bd66616f767bd9635b1f-CfnUtils.get_stack_template-65

- repo/project: `aws-sam-cli`
- function: `CfnUtils.get_stack_template`
- commit hash: `6733ccdcd026b364cc56bd66616f767bd9635b1f`
- confidence: `0.0821`
- predicted doc category: `developer_setup`
- predicted scenario: `added_environment_variable`
- predicted target: `docs/developer-setup.md`
- short code diff: - def get_stack_template(self, stack_name: str, stage: str) -> Dict:\n?                                                              ^^^\n\n+ def get_stack_template(self, stack_name: str, stage: str) -> str:\n?                                                              ^ +\n\n          \n          \n          \n          try:\n              resp = self._client.get_template(StackName=stack_name, TemplateStage=stage)...[truncated]
- short doc diff:   Return the Cloudformation template of the given stack_name\n  \n-         :param stack_name: Name or ID of the stack\n+         Parameters\n+         ----------\n+ \n+         stack_name: str\n+             Name or ID of the stack\n+         stage: str\n-         :param stage: The Stage of the template Original or Processed\n?         ^^^^^^^^^^^^^\n\n+   ...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue


## All False Negative Examples

### codocbench-cpython-6ffface4293f20e504de6a7ca012c482a203409d-move-338

- repo/project: `cpython`
- function: `move`
- commit hash: `6ffface4293f20e504de6a7ca012c482a203409d`
- confidence: `0.5493`
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
- confidence: `0.5348`
- predicted doc category: `workflow_documentation`
- predicted scenario: `added_background_job_flow`
- predicted target: `docs/workflows.md`
- short code diff:   def _get_next_execution(self):\n          \n          \n          \n          query = {\n              'scheduled_start_timestamp__lte': date.get_datetime_utc_now(),\n              'handling': False,\n              'limit': 1,\n              'order_by': [\n                  '+scheduled_start_timestamp',\n              ]\n          }\n  \n          execution_queue_item_db = ActionExecutionSchedulingQueue.query(**que...[truncated]
- short doc diff: - Sort executions by FIFO and priority and get the latest, highest priority item from the\n?                                                                                    ----\n\n+ Sort execution requests by FIFO and priority and get the latest, highest priority item from\n?               ++++++ ++\n\n-         queue and pop it off.\n+         the queue...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-cpython-a4e018889ac3537e10b48811b4be6356e633b8a0-scheduler.run-98

- repo/project: `cpython`
- function: `scheduler.run`
- commit hash: `a4e018889ac3537e10b48811b4be6356e633b8a0`
- confidence: `0.4128`
- predicted doc category: `workflow_documentation`
- predicted scenario: `added_background_job_flow`
- predicted target: `docs/workflows.md`
- short code diff:   def run(self, blocking=True):\n          \n  \n          \n          # localize variable access to minimize overhead\n          # and to improve thread safety\n          with self._lock:\n              q = self._queue\n              delayfunc = self.delayfunc\n              timefunc = self.timefunc\n              pop = heapq.heappop\n              while q:\n                  time, priority, action, argument, kwargs...[truncated]
- short doc diff:   Execute events until the queue is empty.\n          If blocking is False executes the scheduled events due to\n-         expire soonest (if any) and then return.\n?                                                ^\n\n+         expire soonest (if any) and then return the deadline of the\n?                                                ^^^^^^^^^^^^^^^^^^^^\...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-cpython-eda960a1dde94e0c3a172889d22588f839e4b2de-IMAP4.authenticate-100

- repo/project: `cpython`
- function: `IMAP4.authenticate`
- commit hash: `eda960a1dde94e0c3a172889d22588f839e4b2de`
- confidence: `0.4085`
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
- confidence: `0.3750`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_test_command`
- predicted target: `docs/testing.md`
- short code diff:   def stop(self):\n-         ""\n?         --\n\n+         \n          self.shouldStop = True
- short doc diff: - Indicates that the tests should be aborted\n+ Indicates that the tests should be aborted.\n?                                           +\n
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-ansible-0d5a9f2138b0626e1c836333e3af0b73bdc31ec8-run_command-327

- repo/project: `ansible`
- function: `run_command`
- commit hash: `0d5a9f2138b0626e1c836333e3af0b73bdc31ec8`
- confidence: `0.3741`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_test_command`
- predicted target: `docs/testing.md`
- short code diff: - def run_command(args, cmd, capture=False, env=None, data=None, cwd=None, always=False, stdin=None, stdout=None,\n-                 cmd_verbosity=1, str_errors='strict', error_callback=None):\n-     \n-     \n+ def run_command(\n+         args,  # type: CommonConfig\n+         cmd,  # type: t.Iterable[str]\n+         capture=False,  # type: bool\n+         env=None,  # type: t.Optional[t.Dict[str, str]]\n+         d...[truncated]
- short doc diff: + Run the specified command and return stdout and stderr as a tuple.\n- :type args: CommonConfig\n-     :type cmd: collections.Iterable[str]\n-     :type capture: bool\n-     :type env: dict[str, str] | None\n-     :type data: str | None\n-     :type cwd: str | None\n-     :type always: bool\n-     :type stdin: file | None\n-     :type stdout: file | None\n-...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-st2-65804951f641f512f2d8571af2112f860907f0d3-BaseActionAliasTestCase.assertExtractedParametersMatch-284

- repo/project: `st2`
- function: `BaseActionAliasTestCase.assertExtractedParametersMatch`
- commit hash: `65804951f641f512f2d8571af2112f860907f0d3`
- confidence: `0.3624`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_test_command`
- predicted target: `docs/testing.md`
- short code diff:   def assertExtractedParametersMatch(self, format_string, command, values):\n          \n          \n          \n-         extracted_params = extract_parameters(action_alias_db=self.action_alias_db,\n?                                              ^               ^^^^^^^^^^^^^^^^^^^^^^\n\n+         extracted_params = extract_parameters_for_action_alias_db(\n?                                              ^^^^^         ...[truncated]
- short doc diff: + Assert that the provided command matches the format string.\n- Assert that the parameters extracted from the user provided command string match the\n-         provided values.\n  \n          In addition to that, also assert that the parameters which have been extracted from the\n-         user input also match the provided parameters.\n+         user input...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-freqtrade-16cd1f06b22de6dd80d023ac979bcc75b7548fad-DataProvider.orderbook-163

- repo/project: `freqtrade`
- function: `DataProvider.orderbook`
- commit hash: `16cd1f06b22de6dd80d023ac979bcc75b7548fad`
- confidence: `0.3598`
- predicted doc category: `api_reference`
- predicted scenario: `changed_validation_max`
- predicted target: `docs/api.md`
- short code diff:   def orderbook(self, pair: str, maximum: int) -> Dict[str, List]:\n          \n          \n          \n-         return self._exchange.get_order_book(pair, maximum)\n?                               ^\n\n+         return self._exchange.fetch_l2_order_book(pair, maximum)\n?                               ^  +++++\n
- short doc diff: - fetch latest orderbook data\n? ^\n\n+ Fetch latest l2 orderbook data\n? ^           +++\n\n+         Warning: Does a network request - so use with common sense.\n          :param pair: pair to get the data for\n          :param maximum: Maximum number of orderbook entries to query\n          :return: dict including bids/asks with a total of `maximum` entri...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-cpython-fdc0e09c3316098b038996c428e88931f0a4fcdb-__init__-431

- repo/project: `cpython`
- function: `__init__`
- commit hash: `fdc0e09c3316098b038996c428e88931f0a4fcdb`
- confidence: `0.3283`
- predicted doc category: `workflow_documentation`
- predicted scenario: `added_background_job_flow`
- predicted target: `docs/workflows.md`
- short code diff:   def __init__(self, max_workers=None, mp_context=None,\n-                  initializer=None, initargs=()):\n+                  initializer=None, initargs=(), *, max_tasks_per_child=None):\n?                                               +++++++++++++++++++++++++++++\n\n          \n          \n          _check_system_limits()\n  \n          if max_workers is None:\n              self._max_workers = os.cpu_count() or ...[truncated]
- short doc diff:   Initializes a new ProcessPoolExecutor instance.\n  \n          Args:\n              max_workers: The maximum number of processes that can be used to\n                  execute the given calls. If None or not given then as many\n                  worker processes will be created as the machine has processors.\n              mp_context: A multiprocessing con...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-django-b1e33ceceda1e75ff68c7deed8f6659683a195d3-FixtureTestCase.test_pseudo_empty_fixtures-495

- repo/project: `django`
- function: `FixtureTestCase.test_pseudo_empty_fixtures`
- commit hash: `b1e33ceceda1e75ff68c7deed8f6659683a195d3`
- confidence: `0.3129`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_test_command`
- predicted target: `docs/testing.md`
- short code diff:   def test_pseudo_empty_fixtures(self):\n-         ""\n?         --\n\n+         \n+         \n+         \n          new_io = StringIO()\n          management.call_command('loaddata', 'pets', stdout=new_io, stderr=new_io)\n          command_output = new_io.getvalue().strip()\n          # No objects will actually be loaded\n          self.assertEqual(command_output, "Installed 0 object(s) (of 2) from 1 fixture(s)")
- short doc diff: - A fixture can contain entries, but lead to nothing in the database; this shouldn't raise an error (ref #14068)\n?                                                                    -------------------------------------------\n\n+ A fixture can contain entries, but lead to nothing in the database;\n+         this shouldn't raise an error (#14068).
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-faceswap-7f5391145318ebe8012818eb810070e76be7e3b7-QueueManager.add_queue-44

- repo/project: `faceswap`
- function: `QueueManager.add_queue`
- commit hash: `7f5391145318ebe8012818eb810070e76be7e3b7`
- confidence: `0.3073`
- predicted doc category: `workflow_documentation`
- predicted scenario: `added_response_field`
- predicted target: `docs/workflows.md`
- short code diff:   def add_queue(self, name, maxsize=0):\n            \n+ \n+         logger.debug("QueueManager adding: (name: '%s', maxsize: %s)", name, maxsize)\n          if name in self.queues.keys():\n              raise ValueError("Queue '{}' already exists.".format(name))\n          queue = self.manager.Queue(maxsize=maxsize)\n+         setattr(queue, "shutdown", self.shutdown)\n          self.queues[name] = queue\n+         ...[truncated]
- short doc diff:   Add a queue to the manager\n+ \n+             Adds an event "shutdown" to the queue that can be used to indicate\n+             to a process that any activity on the queue should cease
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue


## 10 Representative Low-Confidence True Positives

### codocbench-aws-sam-cli-bedd5d53d99ae64dacc487d72108c2b7cef58f5d-SamFunctionProvider._extract_functions-364

- repo/project: `aws-sam-cli`
- function: `SamFunctionProvider._extract_functions`
- commit hash: `bedd5d53d99ae64dacc487d72108c2b7cef58f5d`
- confidence: `0.0634`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_endpoint_path`
- predicted target: `docs/architecture.md`
- short code diff:   def _extract_functions(\n-         stacks: List[Stack], use_raw_codeuri: bool = False, ignore_code_extraction_warnings: bool = False\n+         stacks: List[Stack],\n+         use_raw_codeuri: bool = False,\n+         ignore_code_extraction_warnings: bool = False,\n+         locate_layer_nested: bool = False,\n      ) -> Dict[str, Function]:\n          \n          \n          \n  \n          result: Dict[str, Funct...[truncated]
- short doc diff:   Extracts and returns function information from the given dictionary of SAM/CloudFormation resources. This\n          method supports functions defined with AWS::Serverless::Function and AWS::Lambda::Function\n  \n          :param stacks: List of SAM/CloudFormation stacks to extract functions from\n          :param bool use_raw_codeuri: Do not resolve adjus...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-faceswap-6ee896d175145297ecae001d1a6f4628b5b4e6ef-_EventParser._parse_outputs-251

- repo/project: `faceswap`
- function: `_EventParser._parse_outputs`
- commit hash: `6ee896d175145297ecae001d1a6f4628b5b4e6ef`
- confidence: `0.0648`
- predicted doc category: `workflow_documentation`
- predicted scenario: `removed_dto_model_field`
- predicted target: `docs/workflows.md`
- short code diff:   def _parse_outputs(self, event):\n           \n          \n          serializer = get_serializer("json")\n          struct = event.summary.value[0].tensor.string_val[0]\n+ \n+         config = serializer.unmarshal(struct)["config"]\n+         model_outputs = self._get_outputs(config)\n+         split_output = len(np.unique(model_outputs[..., 1])) == 1\n+ \n-         outputs = np.array(serializer.unmarshal(struct)["...[truncated]
- short doc diff:   Parse the outputs from the stored model structure for mapping loss names to\n          model outputs.\n  \n          Loss names are added to :attr:`_loss_labels`\n  \n+         Notes\n+         -----\n+         The master model does not actually contain the specified output name, so we dig into the\n+         sub-model to obtain the name of the output laye...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-image-8432b90eb84d5ec4dea04631f087402bf61c1a12-rotate-297

- repo/project: `scikit-image`
- function: `rotate`
- commit hash: `8432b90eb84d5ec4dea04631f087402bf61c1a12`
- confidence: `0.0677`
- predicted doc category: `developer_setup`
- predicted scenario: `changed_local_development_flow`
- predicted target: `docs/developer-setup.md`
- short code diff: - def rotate(image, angle, resize=False, order=1, mode='constant', cval=0.):\n?                                                                         ^^\n\n+ def rotate(image, angle, resize=False, order=1, mode='constant', cval=0.,\n?                                                                         ^\n\n+            center=None):\n      \n  \n      \n  \n      rows, cols = image.shape[0], image.shape[1]\n  \...[truncated]
- short doc diff:   Rotate image by a certain angle around its center.\n  \n      Parameters\n      ----------\n      image : ndarray\n          Input image.\n      angle : float\n          Rotation angle in degrees in counter-clockwise direction.\n      resize : bool, optional\n          Determine whether the shape of the output image will be automatically\n          calcula...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-django-cb0da637a69b79ab371be9ee202335190a3a506e-GDALRaster.transform-64

- repo/project: `django`
- function: `GDALRaster.transform`
- commit hash: `cb0da637a69b79ab371be9ee202335190a3a506e`
- confidence: `0.0678`
- predicted doc category: `workflow_documentation`
- predicted scenario: `changed_testing_framework`
- predicted target: `docs/workflows.md`
- short code diff: - def transform(self, srid, driver=None, name=None, resampling='NearestNeighbour',\n?                       ^^\n\n+ def transform(self, srs, driver=None, name=None, resampling='NearestNeighbour',\n?                       ^\n\n                    max_error=0.0):\n          \n          \n          \n          # Convert the resampling algorithm name into an algorithm id\n          algorithm = GDAL_RESAMPLE_ALGORITHMS[re...[truncated]
- short doc diff: - Return a copy of this raster reprojected into the given SRID.\n?                                                         ^^^^^\n\n+ Return a copy of this raster reprojected into the given spatial\n?                                                         ^^^^^^^\n\n+         reference system.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-image-7ea6a37634d4656955fefeede0ae815814d5efef-checkerboard-270

- repo/project: `scikit-image`
- function: `checkerboard`
- commit hash: `7ea6a37634d4656955fefeede0ae815814d5efef`
- confidence: `0.0700`
- predicted doc category: `configuration`
- predicted scenario: `changed_testing_framework`
- predicted target: `docs/configuration.md`
- short code diff:   def checkerboard():\n      \n  \n      \n-     return load("chessboard_RGB.png")\n?                              ^^\n\n+     return load("chessboard_GRAY_U8.png")\n?                             + ^^^^^\n
- short doc diff:   Checkerboard image.\n+ \n+     Checkerboards are often used in image calibration, since the\n+     corner-points are easy to locate.  Because of the many parallel\n+     edges, they also visualise distortions particularly well.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-rf-1b02349352d40d7bb0cf76455d28b84a847970b0-LRRM.__init__-462

- repo/project: `scikit-rf`
- function: `LRRM.__init__`
- commit hash: `1b02349352d40d7bb0cf76455d28b84a847970b0`
- confidence: `0.0716`
- predicted doc category: `architecture_flow`
- predicted scenario: `removed_dto_model_field`
- predicted target: `docs/architecture.md`
- short code diff:   def __init__(self, measured, ideals, switch_terms=None, isolation=None,\n              z0=50, match_fit='l', *args, **kwargs):\n          \n          \n          \n  \n          self.z0 = z0\n          # TODO: Second port not implemented.\n          self.match_port = 0\n+         # Maximum frequency to assume that open behaves like ideal capacitor when\n+         # using match_fit == 'lc'.\n+         self.lc_fit_c_...[truncated]
- short doc diff:   LRRM Initializer.\n-         \n+ \n          Parameters\n          ----------\n          measured : list of :class:`~skrf.network.Network` objects\n              Raw measurements of the calibration standards. The order\n              must be line, reflect, reflect, match and must align with the\n              `ideals` parameter\n  \n          ideals : list...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-twine-09fe3a40c09f3cdddb42af6331dcc6ee8d923779-Tiddler.displays-147

- repo/project: `twine`
- function: `Tiddler.displays`
- commit hash: `09fe3a40c09f3cdddb42af6331dcc6ee8d923779`
- confidence: `0.0723`
- predicted doc category: `configuration`
- predicted scenario: `changelog_worthy_behavior_change`
- predicted target: `docs/configuration.md`
- short code diff:   def displays(self):\n  		\n  		\n  		\n- 		if ('script' in self.tags) or ('stylesheet' in self.tags):\n+ 		if not self.isStoryText():\n  			return []\n  		return re.findall(r'\<\<display\s+[\'"]?(.+?)[\'"]?\s?\>\>', self.text, re.IGNORECASE)
- short doc diff: - Returns a list of all passages <<display>>ed by this one. By default,\n?                                                          ------------\n\n+ Returns a list of all passages <<display>>ed by this one.\n- 		returns internal links and dis
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-faceswap-d8557c1970939ee9bb90bd41edcd86c6fcf84d19-PixelShuffler.call-463

- repo/project: `faceswap`
- function: `PixelShuffler.call`
- commit hash: `d8557c1970939ee9bb90bd41edcd86c6fcf84d19`
- confidence: `0.0741`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_validation_max`
- predicted target: `docs/testing.md`
- short code diff: - def call(self, inputs, **kwargs):\n+ def call(self, inputs, **kwargs):  # pylint:disable=unused-argument\n          \n          \n          input_shape = K.int_shape(inputs)\n          if len(input_shape) != 4:\n              raise ValueError('Inputs should have rank ' +\n                               str(4) +\n                               '; Received input shape:', str(input_shape))\n  \n          if self.data_...[truncated]
- short doc diff:   This is where the layer's logic lives.\n  \n          Parameters\n          ----------\n          inputs: tensor\n              Input tensor, or list/tuple of input tensors\n          kwargs: dict\n-             Additional keyword arguments\n+             Additional keyword arguments. Unused\n?                                         ++++++++\n\n  \n      ...[truncated]
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

### codocbench-langchain-e83250cc5f4dc5edd1ae8fb0a41c40454d13fb9d-StringRunEvaluatorChain.from_run_and_data_type-195

- repo/project: `langchain`
- function: `StringRunEvaluatorChain.from_run_and_data_type`
- commit hash: `e83250cc5f4dc5edd1ae8fb0a41c40454d13fb9d`
- confidence: `0.0769`
- predicted doc category: `developer_setup`
- predicted scenario: `added_environment_variable`
- predicted target: `docs/developer-setup.md`
- short code diff:   def from_run_and_data_type(\n          cls,\n          evaluator: StringEvaluator,\n-         run_type: RunTypeEnum,\n+         run_type: str,\n          data_type: DataType,\n          input_key: Optional[str] = None,\n          prediction_key: Optional[str] = None,\n          reference_key: Optional[str] = None,\n          tags: Optional[List[str]] = None,\n      ) -> StringRunEvaluatorChain:\n          \n       ...[truncated]
- short doc diff:   Create a StringRunEvaluatorChain from an evaluator and the run and dataset types.\n  \n          This method provides an easy way to instantiate a StringRunEvaluatorChain, by\n          taking an evaluator and information about the type of run and the data.\n          The method supports LLM and chain runs.\n  \n          Args:\n              evaluator (St...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue


## Limitations

- CoDocBench labels are code-docstring/comment co-change positives, not project-level Markdown documentation labels.
- Positive recall here should be treated as an external robustness signal.
- External precision and F1 require a defensible external negative set with separately reported label provenance.
