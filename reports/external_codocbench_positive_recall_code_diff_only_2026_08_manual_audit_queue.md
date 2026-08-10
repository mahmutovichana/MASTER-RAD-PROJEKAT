# External CoDocBench Manual Audit Queue 2026-08

## False Negative Examples

None.

## 20 Lowest-Confidence True Positives

### codocbench-mycroft-core-8ce1615d759d8b579234a57a10798302abc4c5df-SimpleAudioService._play-43

- repo/project: `mycroft-core`
- function: `SimpleAudioService._play`
- commit hash: `8ce1615d759d8b579234a57a10798302abc4c5df`
- confidence: `0.0633`
- predicted doc category: `workflow_documentation`
- predicted scenario: `added_background_job_flow`
- predicted target: `docs/workflows.md`
- short code diff:   def _play(self, message):\n-          \n?         -\n\n+         \n          \n          LOG.info('SimpleAudioService._play')\n  \n          # Stop any existing audio playback\n          self._stop_running_process()\n  \n          repeat = message.data.get('repeat', False)\n          self._is_playing = True\n          self._paused = False\n+         with self.track_lock:\n-         if isinstance(self.tracks[self.in...[truncated]
- short doc diff:   Implementation specific async method to handle playback.\n+ \n-             This allows mpg123 service to use the "next method as well\n? ----                                              -\n\n+         This allows mpg123 service to use the next method as well\n-             as basic play/stop.\n? ----\n\n+         as basic play/stop.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-django-183442864837386df1f24d9cd0b39a3671ef3b04-Query.promote_alias-25

- repo/project: `django`
- function: `Query.promote_alias`
- commit hash: `183442864837386df1f24d9cd0b39a3671ef3b04`
- confidence: `0.0681`
- predicted doc category: `developer_setup`
- predicted scenario: `changed_seed_or_setup_flow`
- predicted target: `docs/developer-setup.md`
- short code diff:   def promote_alias(self, alias, unconditional=False):\n          \n          \n          \n          if ((unconditional or self.alias_map[alias][NULLABLE]) and\n                  self.alias_map[alias] != self.LOUTER):\n              data = list(self.alias_map[alias])\n              data[JOIN_TYPE] = self.LOUTER\n              self.alias_map[alias] = tuple(data)\n+             return True\n+         return False
- short doc diff:   Promotes the join type of an alias to an outer join if it's possible\n          for the join to contain NULL values on the left. If 'unconditional' is\n          False, the join is only promoted if it is nullable, otherwise it is\n          always promoted.\n+ \n+         Returns True if the join was promoted.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-speechbrain-e5a4856deb858c570fb7e0f182fc0e7146b81edb-Conv2d._check_input-263

- repo/project: `speechbrain`
- function: `Conv2d._check_input`
- commit hash: `e5a4856deb858c570fb7e0f182fc0e7146b81edb`
- confidence: `0.0682`
- predicted doc category: `workflow_documentation`
- predicted scenario: `changed_local_development_flow`
- predicted target: `docs/workflows.md`
- short code diff: - def _check_input(self, x):\n?                        ^\n\n+ def _check_input(self, shape):\n?                        ^^^^^\n\n          \n          \n          \n-         if len(x.shape) == 3:\n?                --\n\n+         if len(shape) == 3:\n              self.unsqueeze = True\n              in_channels = 1\n  \n-         elif len(x.shape) == 4:\n?                  --\n\n+         elif len(shape) == 4:\n-   ...[truncated]
- short doc diff: - Checks the input and returns the number of input channels.\n+ Checks the input shape and returns the number of input channels.\n?                  ++++++\n
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-rf-6e3a8a6948bb828bbfa29765c07fc5ce76593e08-RectangularWaveguide.Z0-346

- repo/project: `scikit-rf`
- function: `RectangularWaveguide.Z0`
- commit hash: `6e3a8a6948bb828bbfa29765c07fc5ce76593e08`
- confidence: `0.0700`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_middleware_auth_flow`
- predicted target: `docs/architecture.md`
- short code diff: + def Z0(self) -> NumberLike:\n- def Z0(self):\n-         '''\n          \n-         '''\n?         ---\n\n+         \n+         \n          omega = self.frequency.w\n          impedance_dict = {'te':   1j*omega*self.mu/(self.gamma),\n                            'tm':   -1j*self.gamma/(omega*self.ep),\\n                           }\n  \n          return impedance_dict[self.mode_type]
- short doc diff: - The characteristic impedance\n+ The characteristic impedance.\n?                             +\n\n+ \n+         The characteristic impedance depends of the mode ('te' or 'tm').
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-chainer-7af06dd4dba55d1a87e08da62e82ac1b478788f3-rrelu-393

- repo/project: `chainer`
- function: `rrelu`
- commit hash: `7af06dd4dba55d1a87e08da62e82ac1b478788f3`
- confidence: `0.0704`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_http_method`
- predicted target: `docs/architecture.md`
- short code diff:   def rrelu(x, l=1. / 8, u=1. / 3, **kwargs):\n      \n      \n      r = None\n      return_r = False\n      if kwargs:\n          r, return_r = argument.parse_kwargs(\n              kwargs, ('r', r), ('return_r', r),\n              train='train argument is not supported anymore.'\n                    'Use chainer.using_config')\n  \n      func = RReLU(l, u, r)\n-     out = func.apply((x,))[0]\n?                     ...[truncated]
- short doc diff:   rrelu(x, l=1. / 8, u=1. / 3, *, r=None, return_r=False)\n  \n      Randomized Leaky Rectified Liner Unit function.\n  \n      This function is expressed as\n  \n      .. math:: f(x)=\\max(x, ax),\n  \n      where :math:`a` is a random number sampled from a uniform distribution\n      :math:`U(l, u)`.\n  \n      See: https://arxiv.org/pdf/1505.00853.pdf\n  ...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-django-03281d8fe7a32f580a85235659d4fbb143eeb867-uri_to_iri-255

- repo/project: `django`
- function: `uri_to_iri`
- commit hash: `03281d8fe7a32f580a85235659d4fbb143eeb867`
- confidence: `0.0737`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_test_command`
- predicted target: `docs/architecture.md`
- short code diff:   def uri_to_iri(uri):\n      \n      \n      \n      if uri is None:\n          return uri\n      uri = force_bytes(uri)\n-     iri = unquote_to_bytes(uri)\n+     # Fast selective unqote: First, split on '%' and then starting with the\n+     # second block, decode the first 2 bytes if they represent a hex code to\n+     # decode. The rest of the block is the part after '%AB', not containing\n+     # any '%'. Add tha...[truncated]
- short doc diff:   Converts a Uniform Resource Identifier(URI) into an Internationalized\n      Resource Identifier(IRI).\n  \n-     This is the algorithm from section 3.2 of RFC 3987.\n+     This is the algorithm from section 3.2 of RFC 3987, excluding step 4.\n?                                                       ++++++++++++++++++\n\n  \n      Takes an URI in ASCII byte...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-django-c3a0dcf6e9e7859a4a990954cbab0a44e7cb1307-Query.__str__-466

- repo/project: `django`
- function: `Query.__str__`
- commit hash: `c3a0dcf6e9e7859a4a990954cbab0a44e7cb1307`
- confidence: `0.0746`
- predicted doc category: `configuration`
- predicted scenario: `changed_testing_framework`
- predicted target: `docs/configuration.md`
- short code diff:   def __str__(self):\n          \n          \n          \n-         sql, params = self.get_compiler(DEFAULT_DB_ALIAS).as_sql()\n+         sql, params = self.sql_with_params()\n          return sql % params
- short doc diff:   Returns the query as a string of SQL with the parameter values\n-         substituted in.\n+         substituted in (use sql_with_params() to see the unsubstituted string).\n  \n          Parameter values won't necessarily be quoted correctly, since that is\n          done by the database interface at execution time.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-image-7ea6a37634d4656955fefeede0ae815814d5efef-checkerboard-270

- repo/project: `scikit-image`
- function: `checkerboard`
- commit hash: `7ea6a37634d4656955fefeede0ae815814d5efef`
- confidence: `0.0746`
- predicted doc category: `developer_setup`
- predicted scenario: `changed_background_job_schedule`
- predicted target: `docs/developer-setup.md`
- short code diff:   def checkerboard():\n      \n  \n      \n-     return load("chessboard_RGB.png")\n?                              ^^\n\n+     return load("chessboard_GRAY_U8.png")\n?                             + ^^^^^\n
- short doc diff:   Checkerboard image.\n+ \n+     Checkerboards are often used in image calibration, since the\n+     corner-points are easy to locate.  Because of the many parallel\n+     edges, they also visualise distortions particularly well.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-speechbrain-c5b6a4854a76386c481f5c2b871e70596d6ab5de-Mvdr._mvdr-368

- repo/project: `speechbrain`
- function: `Mvdr._mvdr`
- commit hash: `c5b6a4854a76386c481f5c2b871e70596d6ab5de`
- confidence: `0.0748`
- predicted doc category: `architecture_flow`
- predicted scenario: `added_background_job_flow`
- predicted target: `docs/architecture.md`
- short code diff: - def _mvdr(Xs, XXs, As, eps=1e-20):\n?               ^^\n\n+ def _mvdr(Xs, NNs, As, eps=1e-20):\n?               ^^\n\n          \n          \n  \n          # Get unique covariance values to reduce the number of computations\n-         XXs_val, XXs_idx = torch.unique(XXs, return_inverse=True, dim=1)\n?         ^^       ^^                     ^^\n\n+         NNs_val, NNs_idx = torch.unique(NNs, return_inverse=True, d...[truncated]
- short doc diff:   Perform minimum variance distortionless response beamforming.\n  \n          Arguments\n          ---------\n          Xs : tensor\n              A batch of audio signals in the frequency domain.\n              The tensor must have the following format:\n              (batch, time_step, n_fft/2 + 1, 2, n_mics).\n-         XXs : tensor\n?         ^^\n\n+   ...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-ray-e968b52cb7de4e6c2fcc6e7d5ccb98d984745715-_do_policy_eval-21

- repo/project: `ray`
- function: `_do_policy_eval`
- commit hash: `e968b52cb7de4e6c2fcc6e7d5ccb98d984745715`
- confidence: `0.0750`
- predicted doc category: `model_contract`
- predicted scenario: `changed_validation_max`
- predicted target: `docs/models.md`
- short code diff:   def _do_policy_eval(\n          *,\n          to_eval: Dict[PolicyID, List[PolicyEvalData]],\n          policies: Dict[PolicyID, Policy],\n          active_episodes: Dict[str, MultiAgentEpisode],\n          tf_sess=None,\n-         _use_trajectory_view_api=False\n  ) -> Dict[PolicyID, Tuple[TensorStructType, StateBatch, dict]]:\n      \n      \n  \n      eval_results: Dict[PolicyID, TensorStructType] = {}\n  \n    ...[truncated]
- short doc diff:   Call compute_actions on collected episode/model data to get next action.\n  \n      Args:\n          to_eval (Dict[PolicyID, List[PolicyEvalData]]): Mapping of policy\n              IDs to lists of PolicyEvalData objects (items in these lists will\n              be the batch's items for the model forward pass).\n          policies (Dict[PolicyID, Policy]):...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-core-251d8919eab9c765563417a32b6c0a2e897274ff-StateMachine.async_all-128

- repo/project: `core`
- function: `StateMachine.async_all`
- commit hash: `251d8919eab9c765563417a32b6c0a2e897274ff`
- confidence: `0.0750`
- predicted doc category: `architecture_flow`
- predicted scenario: `added_environment_variable`
- predicted target: `docs/architecture.md`
- short code diff: - def async_all(self) -> List[State]:\n+ def async_all(\n+         self, domain_filter: Optional[Union[str, Iterable]] = None\n+     ) -> List[State]:\n          \n          \n+         if domain_filter is None:\n-         return list(self._states.values())\n+             return list(self._states.values())\n? ++++\n\n+ \n+         if isinstance(domain_filter, str):\n+             domain_filter = (domain_filter.lower(...[truncated]
- short doc diff: - Create a list of all states.\n+ Create a list of all states matching the filter.\n  \n          This method must be run in the event loop.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-faceswap-a99049711f289b435e710d5b15f9c0e45c4251c3-Encoder._get_encoder_model-113

- repo/project: `faceswap`
- function: `Encoder._get_encoder_model`
- commit hash: `a99049711f289b435e710d5b15f9c0e45c4251c3`
- confidence: `0.0754`
- predicted doc category: `architecture_flow`
- predicted scenario: `added_environment_variable`
- predicted target: `docs/architecture.md`
- short code diff: - def _get_encoder_model(self):\n+ def _get_encoder_model(self) -> keras.models.Model:\n           \n          \n-         if self._selected_model.get("keras_name"):\n-             kwargs = self._selected_model["kwargs"]\n?         ^^^                              ----------\n\n+         model, kwargs = self._selected_model\n?         ^^^^^^\n\n+         if model.keras_name:\n              kwargs["input_shape"] = sel...[truncated]
- short doc diff:   Return the model defined by the selected architecture.\n- \n-         Parameters\n-         ----------\n-         input_shape: tuple\n-             The input shape for the model\n  \n          Returns\n          -------\n          :class:`keras.Model`\n              The selected keras model for the chosen encoder architecture
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-prophet-53b9b1a6be994a513677ec3c1d6b601b151d07a4-cross_validation-315

- repo/project: `prophet`
- function: `cross_validation`
- commit hash: `53b9b1a6be994a513677ec3c1d6b601b151d07a4`
- confidence: `0.0760`
- predicted doc category: `architecture_flow`
- predicted scenario: `removed_endpoint`
- predicted target: `docs/architecture.md`
- short code diff: - def cross_validation(model, horizon, period=None, initial=None, parallel=None, cutoffs=None, disable_tqdm=False):\n+ def cross_validation(model, horizon, period=None, initial=None, parallel=None, cutoffs=None, disable_tqdm=False, extra_output_columns=None):\n?                                                                                                                +++++++++++++++++++++++++++\n\n      \n      \...[truncated]
- short doc diff:   Cross-Validation for time series.\n  \n      Computes forecasts from historical cutoff points, which user can input.\n      If not provided, begins from (end - horizon) and works backwards, making\n      cutoffs with a spacing of period until initial is reached.\n  \n      When period is equal to the time interval of the data, this is the\n      technique ...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-rf-48729401374e2b1583cad31d788c7b4990684d10-plot_complex_polar-247

- repo/project: `scikit-rf`
- function: `plot_complex_polar`
- commit hash: `48729401374e2b1583cad31d788c7b4990684d10`
- confidence: `0.0763`
- predicted doc category: `api_reference`
- predicted scenario: `changed_local_development_flow`
- predicted target: `docs/api.md`
- short code diff: - def plot_complex_polar(z, x_label=None, y_label=None,\n-     title=None, show_legend=True, axis_equal=False, ax=None,\n-     *args, **kwargs):\n-     '''\n+ def plot_complex_polar(z: NumberLike,\n+                        x_label: Union[str, None] = None, y_label: Union[str, None] = None,\n+                        title: Union[str, None] = None, show_legend: bool = True,\n+                        axis_equal: bool = ...[truncated]
- short doc diff: - plot complex data in polar format.\n? ^\n\n+ Plot complex data in polar format.\n? ^\n\n  \n      Parameters\n-     ------------\n?               --\n\n+     ----------\n      z : array-like, of complex data\n          data to plot\n-     x_label : string\n-         x-axis label\n-     y_label : string\n-         y-axis label\n-     title : string\n-      ...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-Python-876087be998d5b366d68cbb9394b6b92b7f619f6-pretty_print-265

- repo/project: `Python`
- function: `pretty_print`
- commit hash: `876087be998d5b366d68cbb9394b6b92b7f619f6`
- confidence: `0.0767`
- predicted doc category: `api_reference`
- predicted scenario: `changed_local_development_flow`
- predicted target: `docs/api.md`
- short code diff:   def pretty_print(n):\n      \n-         \n+     \n      \n      if n <= 0:\n-         print("       ...       ....        nothing printing :(")\n?         - ^ ^^                                                  -\n\n+         return "       ...       ....        nothing printing :("\n?          ^^^^ ^\n\n-         return\n-     floyd(n)  # upper half\n+     upper_half = floyd(n)  # upper half\n?    +++++++++++++\n\...[truncated]
- short doc diff: - Parameters:\n-     n : size of pattern\n+ Print a complete diamond pattern with '*' characters.\n+ \n+     Args:\n+         n (int): Size of the pattern.\n+ \n+     Examples:\n+         >>> pretty_print(0)\n+         '       ...       ....        nothing printing :('\n+ \n+         >>> pretty_print(3)\n+         '  * \\n * * \\n* * * \\n* * * \\n * * \\n  ...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-chainer-ea449a2f42c3003f97d4a75364d8f894d4980670-ResNet50Layers.__call__-127

- repo/project: `chainer`
- function: `ResNet50Layers.__call__`
- commit hash: `ea449a2f42c3003f97d4a75364d8f894d4980670`
- confidence: `0.0769`
- predicted doc category: `architecture_flow`
- predicted scenario: `added_environment_variable`
- predicted target: `docs/architecture.md`
- short code diff: - def __call__(self, x, layers=['prob']):\n+ def __call__(self, x, layers=['prob'], test=True):\n?                                      +++++++++++\n\n          \n  \n          \n  \n          h = x\n          activations = {}\n          target_layers = set(layers)\n          for key, funcs in self.functions.items():\n              if len(target_layers) == 0:\n                  break\n              for func in funcs:...[truncated]
- short doc diff:   Computes all the feature maps specified by ``layers``.\n  \n          Args:\n              x (~chainer.Variable): Input variable.\n              layers (list of str): The list of layernames you want to extract.\n+             test (bool): If ``True``, it runs in test mode.\n  \n          Returns:\n              Dictionary of ~chainer.Variable: The director...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-faceswap-2beceffad9b15c1fd78f06b9b272563321c5a41e-Extract._output_faces-362

- repo/project: `faceswap`
- function: `Extract._output_faces`
- commit hash: `2beceffad9b15c1fd78f06b9b272563321c5a41e`
- confidence: `0.0770`
- predicted doc category: `developer_setup`
- predicted scenario: `changed_local_development_flow`
- predicted target: `docs/developer-setup.md`
- short code diff: - def _output_faces(self, saver: ImagesSaver, extract_media: ExtractMedia) -> None:\n+ def _output_faces(self, saver: Optional[ImagesSaver], extract_media: ExtractMedia) -> None:\n?                                +++++++++           +\n\n           \n          \n-         logger.trace("Outputting faces for %s", extract_media.filename)\n+         logger.trace("Outputting faces for %s", extract_media.filename)  # type:...[truncated]
- short doc diff:   Output faces to save thread\n  \n          Set the face filename based on the frame name and put the face to the\n          :class:`~lib.image.ImagesSaver` save queue and add the face information to the alignments\n          data.\n  \n          Parameters\n          ----------\n-         saver: lib.images.ImagesSaver\n+         saver: :class:`lib.images.I...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-faceswap-6ee896d175145297ecae001d1a6f4628b5b4e6ef-_EventParser._parse_outputs-251

- repo/project: `faceswap`
- function: `_EventParser._parse_outputs`
- commit hash: `6ee896d175145297ecae001d1a6f4628b5b4e6ef`
- confidence: `0.0775`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_validation_max`
- predicted target: `docs/architecture.md`
- short code diff:   def _parse_outputs(self, event):\n           \n          \n          serializer = get_serializer("json")\n          struct = event.summary.value[0].tensor.string_val[0]\n+ \n+         config = serializer.unmarshal(struct)["config"]\n+         model_outputs = self._get_outputs(config)\n+         split_output = len(np.unique(model_outputs[..., 1])) == 1\n+ \n-         outputs = np.array(serializer.unmarshal(struct)["...[truncated]
- short doc diff:   Parse the outputs from the stored model structure for mapping loss names to\n          model outputs.\n  \n          Loss names are added to :attr:`_loss_labels`\n  \n+         Notes\n+         -----\n+         The master model does not actually contain the specified output name, so we dig into the\n+         sub-model to obtain the name of the output laye...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-twine-09fe3a40c09f3cdddb42af6331dcc6ee8d923779-Tiddler.displays-147

- repo/project: `twine`
- function: `Tiddler.displays`
- commit hash: `09fe3a40c09f3cdddb42af6331dcc6ee8d923779`
- confidence: `0.0779`
- predicted doc category: `configuration`
- predicted scenario: `changed_testing_framework`
- predicted target: `docs/configuration.md`
- short code diff:   def displays(self):\n  		\n  		\n  		\n- 		if ('script' in self.tags) or ('stylesheet' in self.tags):\n+ 		if not self.isStoryText():\n  			return []\n  		return re.findall(r'\<\<display\s+[\'"]?(.+?)[\'"]?\s?\>\>', self.text, re.IGNORECASE)
- short doc diff: - Returns a list of all passages <<display>>ed by this one. By default,\n?                                                          ------------\n\n+ Returns a list of all passages <<display>>ed by this one.\n- 		returns internal links and dis
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-pytorch-lightning-71a1dd210f3a10f51bee831bf9eeb732b7ddc52f-_LoggerConnector.metrics-335

- repo/project: `pytorch-lightning`
- function: `_LoggerConnector.metrics`
- commit hash: `71a1dd210f3a10f51bee831bf9eeb732b7ddc52f`
- confidence: `0.0780`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_testing_framework`
- predicted target: `docs/architecture.md`
- short code diff:   def metrics(self) -> _METRICS:\n          \n-         on_step = not self._epoch_end_reached\n+         on_step = self._first_loop_iter is not None\n          assert self.trainer._results is not None\n          return self.trainer._results.metrics(on_step)
- short doc diff: - This function returns either batch or epoch metrics depending on ``_epoch_end_reached``.\n+ This function returns either batch or epoch metrics.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue


## 10 Random True Positives

### codocbench-ansible-0d5a9f2138b0626e1c836333e3af0b73bdc31ec8-run_command-327

- repo/project: `ansible`
- function: `run_command`
- commit hash: `0d5a9f2138b0626e1c836333e3af0b73bdc31ec8`
- confidence: `0.3513`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_test_command`
- predicted target: `docs/testing.md`
- short code diff: - def run_command(args, cmd, capture=False, env=None, data=None, cwd=None, always=False, stdin=None, stdout=None,\n-                 cmd_verbosity=1, str_errors='strict', error_callback=None):\n-     \n-     \n+ def run_command(\n+         args,  # type: CommonConfig\n+         cmd,  # type: t.Iterable[str]\n+         capture=False,  # type: bool\n+         env=None,  # type: t.Optional[t.Dict[str, str]]\n+         d...[truncated]
- short doc diff: + Run the specified command and return stdout and stderr as a tuple.\n- :type args: CommonConfig\n-     :type cmd: collections.Iterable[str]\n-     :type capture: bool\n-     :type env: dict[str, str] | None\n-     :type data: str | None\n-     :type cwd: str | None\n-     :type always: bool\n-     :type stdin: file | None\n-     :type stdout: file | None\n-...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-ArchiveBox-ae1484b8bf94a386c07305ec88fddca4a4e997a6-write_main_index-57

- repo/project: `ArchiveBox`
- function: `write_main_index`
- commit hash: `ae1484b8bf94a386c07305ec88fddca4a4e997a6`
- confidence: `0.1375`
- predicted doc category: `developer_setup`
- predicted scenario: `added_background_job_flow`
- predicted target: `docs/developer-setup.md`
- short code diff:   def write_main_index(links: List[Link], out_dir: Path=OUTPUT_DIR, finished: bool=False) -> None:\n      \n  \n      log_indexing_process_started(len(links))\n  \n      try:\n          with timed_index_update(out_dir / SQL_INDEX_FILENAME):\n              write_sql_main_index(links, out_dir=out_dir)\n              os.chmod(out_dir / SQL_INDEX_FILENAME, int(OUTPUT_PERMISSIONS, base=8)) # set here because we don't writ...[truncated]
- short doc diff: - create index.html file for a given list of links\n+ Writes links to sqlite3 file for a given list of links
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-django-5074c75a37f88726f3ae057999144545881d3cfc-QuerySet.select_related-12

- repo/project: `django`
- function: `QuerySet.select_related`
- commit hash: `5074c75a37f88726f3ae057999144545881d3cfc`
- confidence: `0.0918`
- predicted doc category: `configuration`
- predicted scenario: `removed_endpoint`
- predicted target: `docs/configuration.md`
- short code diff:   def select_related(self, *fields, **kwargs):\n          \n          \n          \n          if 'depth' in kwargs:\n              warnings.warn('The "depth" keyword argument has been deprecated.\n'\n                      'Use related field names instead.', DeprecationWarning, stacklevel=2)\n          depth = kwargs.pop('depth', 0)\n          if kwargs:\n              raise TypeError('Unexpected keyword arguments to ...[truncated]
- short doc diff:   Returns a new QuerySet instance that will select related objects.\n  \n          If fields are specified, they must be ForeignKey fields and only those\n          related objects are included in the selection.\n+ \n+         If select_related(None) is called, the list is cleared.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-uiautomator2-ce727fd8988e0fed27c1a155ed2b6f22d9443012-Session.long_click-379

- repo/project: `uiautomator2`
- function: `Session.long_click`
- commit hash: `ce727fd8988e0fed27c1a155ed2b6f22d9443012`
- confidence: `0.1700`
- predicted doc category: `changelog`
- predicted scenario: `changelog_worthy_behavior_change`
- predicted target: `CHANGELOG.md`
- short code diff: - def long_click(self, x, y, duration=0.5):\n?                                     ^^^\n\n+ def long_click(self, x, y, duration=None):\n?                                     ^^^^\n\n-         ''''''\n?            ---\n\n+         '''\n+         '''\n+         if not duration:\n+             duration = 0.5\n          x, y = self.pos_rel2abs(x, y)\n          self.touch.down(x, y)\n          time.sleep(duration)\n      ...[truncated]
- short doc diff:   long click at arbitrary coordinates.\n+         Args:\n+             duration (float): seconds of pressed
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-readthedocs.org-7b7bcbce56c8e9b93d5c508f5da46dff65e1decd-is_project_user-140

- repo/project: `readthedocs.org`
- function: `is_project_user`
- commit hash: `7b7bcbce56c8e9b93d5c508f5da46dff65e1decd`
- confidence: `0.1223`
- predicted doc category: `configuration`
- predicted scenario: `changed_local_development_flow`
- predicted target: `docs/configuration.md`
- short code diff:   def is_project_user(user, project):\n      \n-     return user in project.users.all()\n+     return user in AdminPermission.members(project)
- short doc diff: - Return if user is a member of project.users.\n+ Checks if the user has access to the project.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-faceswap-7da2cc3dd266aabebf41a31384cc2e0e7e5af6e5-Train._process_gui_triggers-125

- repo/project: `faceswap`
- function: `Train._process_gui_triggers`
- commit hash: `7da2cc3dd266aabebf41a31384cc2e0e7e5af6e5`
- confidence: `0.1040`
- predicted doc category: `workflow_documentation`
- predicted scenario: `changelog_worthy_behavior_change`
- predicted target: `docs/workflows.md`
- short code diff: - def _process_gui_triggers(self) -> None:\n+ def _process_gui_triggers(self) -> Dict[Literal["mask", "refresh"], bool]:\n-           \n?          -\n\n+          \n+         \n+         retval: Dict[Literal["mask", "refresh"], bool] = {key: False for key in self._gui_triggers}\n          if not self._args.redirect_gui:\n-             return\n+             return retval\n?                   +++++++\n\n  \n+         f...[truncated]
- short doc diff:   Check whether a file drop has occurred from the GUI to manually update the preview.\n+ \n+         Returns\n+         -------\n+         dict\n+             The trigger name as key and boolean as value
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-sanic-d255d1aae12593af346b575e51725710ddb1c54a-ErrorHandler.add-114

- repo/project: `sanic`
- function: `ErrorHandler.add`
- commit hash: `d255d1aae12593af346b575e51725710ddb1c54a`
- confidence: `0.0834`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_error_handling_flow`
- predicted target: `docs/architecture.md`
- short code diff:   def add(self, exception, handler, route_names: Optional[List[str]] = None):\n          \n-         \n-         \n+ \n+           # noqa: E501\n          if route_names:\n              for route in route_names:\n                  self._add((exception, route), handler)\n          else:\n              self._add((exception, None), handler)
- short doc diff:   Add a new exception handler to an already existing handler object.\n  \n-         :param exception: Type of exception that need to be handled\n-         :param handler: Reference to the method that will handle the exception\n+         Args:\n+             exception (sanic.exceptions.SanicException or Exception): Type\n+                 of exception that ne...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-faceswap-cf4b567cc68267855767025bab9e10a3e2af64b3-get_folder-71

- repo/project: `faceswap`
- function: `get_folder`
- commit hash: `cf4b567cc68267855767025bab9e10a3e2af64b3`
- confidence: `0.1168`
- predicted doc category: `developer_setup`
- predicted scenario: `added_environment_variable`
- predicted target: `docs/developer-setup.md`
- short code diff:   def get_folder(path, make_folder=True):\n       \n      \n      logger = logging.getLogger(__name__)  # pylint:disable=invalid-name\n      logger.debug("Requested path: '%s'", path)\n-     output_dir = Path(path)\n-     if not make_folder and not output_dir.exists():\n?                                 ^ ^^^^   ^^^^^ ^^\n\n+     if not make_folder and not os.path.isdir(path):\n?                                 ^^^^ ...[truncated]
- short doc diff:   Return a path to a folder, creating it if it doesn't exist\n  \n      Parameters\n      ----------\n      path: str\n          The path to the folder to obtain\n      make_folder: bool, optional\n          ``True`` if the folder should be created if it does not already exist, ``False`` if the\n          folder should not be created\n  \n      Returns\n    ...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-models-7a9934df2afdf95be9405b4e9f1f2480d748dc40-BoxPredictor.predict-377

- repo/project: `models`
- function: `BoxPredictor.predict`
- commit hash: `7a9934df2afdf95be9405b4e9f1f2480d748dc40`
- confidence: `0.1418`
- predicted doc category: `architecture_flow`
- predicted scenario: `added_environment_variable`
- predicted target: `docs/architecture.md`
- short code diff: - def predict(self, image_features, num_predictions_per_location, scope,\n?                                                                -------\n\n+ def predict(self, image_features, num_predictions_per_location,\n-               **params):\n+               scope=None, **params):\n?              ++++++++++++\n\n      \n      \n+     if len(image_features) != len(num_predictions_per_location):\n+       raise ValueE...[truncated]
- short doc diff:   Computes encoded object locations and corresponding confidences.\n  \n      Takes a high level image feature map as input and produce two predictions,\n      (1) a tensor encoding box locations, and\n      (2) a tensor encoding class scores for each corresponding box.\n      In this interface, we only assume that two tensors are returned as output\n      a...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-django-414ad25b090a63eaaf297b1164c8f7d814a710a2-activate-52

- repo/project: `django`
- function: `activate`
- commit hash: `414ad25b090a63eaaf297b1164c8f7d814a710a2`
- confidence: `0.0785`
- predicted doc category: `developer_setup`
- predicted scenario: `changed_seed_or_setup_flow`
- predicted target: `docs/developer-setup.md`
- short code diff:   def activate(timezone):\n      \n      \n      \n      if isinstance(timezone, tzinfo):\n          _active.value = timezone\n-     elif isinstance(timezone, six.string_types) and pytz is not None:\n?                                                ---------------------\n\n+     elif isinstance(timezone, six.string_types):\n          _active.value = pytz.timezone(timezone)\n      else:\n          raise ValueError("In...[truncated]
- short doc diff:   Sets the time zone for the current thread.\n  \n      The ``timezone`` argument must be an instance of a tzinfo subclass or a\n-     time zone name. If it is a time zone name, pytz is required.\n+     time zone name.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue


## 10 Highest-Confidence True Positives

### codocbench-st2-e0c6c4e10511bf30e9a01acfa26953736d0e8b01-ActionExecutionSchedulingQueueHandler._get_next_execution-134

- repo/project: `st2`
- function: `ActionExecutionSchedulingQueueHandler._get_next_execution`
- commit hash: `e0c6c4e10511bf30e9a01acfa26953736d0e8b01`
- confidence: `0.5594`
- predicted doc category: `workflow_documentation`
- predicted scenario: `added_background_job_flow`
- predicted target: `docs/workflows.md`
- short code diff:   def _get_next_execution(self):\n          \n          \n          \n          query = {\n              'scheduled_start_timestamp__lte': date.get_datetime_utc_now(),\n              'handling': False,\n              'limit': 1,\n              'order_by': [\n                  '+scheduled_start_timestamp',\n              ]\n          }\n  \n          execution_queue_item_db = ActionExecutionSchedulingQueue.query(**que...[truncated]
- short doc diff: - Sort executions by FIFO and priority and get the latest, highest priority item from the\n?                                                                                    ----\n\n+ Sort execution requests by FIFO and priority and get the latest, highest priority item from\n?               ++++++ ++\n\n-         queue and pop it off.\n+         the queue...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-st2-65804951f641f512f2d8571af2112f860907f0d3-BaseActionAliasTestCase.assertExtractedParametersMatch-284

- repo/project: `st2`
- function: `BaseActionAliasTestCase.assertExtractedParametersMatch`
- commit hash: `65804951f641f512f2d8571af2112f860907f0d3`
- confidence: `0.4180`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_test_command`
- predicted target: `docs/testing.md`
- short code diff:   def assertExtractedParametersMatch(self, format_string, command, values):\n          \n          \n          \n-         extracted_params = extract_parameters(action_alias_db=self.action_alias_db,\n?                                              ^               ^^^^^^^^^^^^^^^^^^^^^^\n\n+         extracted_params = extract_parameters_for_action_alias_db(\n?                                              ^^^^^         ...[truncated]
- short doc diff: + Assert that the provided command matches the format string.\n- Assert that the parameters extracted from the user provided command string match the\n-         provided values.\n  \n          In addition to that, also assert that the parameters which have been extracted from the\n-         user input also match the provided parameters.\n+         user input...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-cpython-eda960a1dde94e0c3a172889d22588f839e4b2de-IMAP4.authenticate-100

- repo/project: `cpython`
- function: `IMAP4.authenticate`
- commit hash: `eda960a1dde94e0c3a172889d22588f839e4b2de`
- confidence: `0.3805`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_middleware_auth_flow`
- predicted target: `docs/architecture.md`
- short code diff: - def authenticate(self, func):\n+ def authenticate(self, mechanism, authobject):\n  		\n  		\n- 		raise self.error('UNIMPLEMENTED')\n+ 		mech = string.upper(mechanism)\n+ 		cap = 'AUTH=%s' % mech\n+ 		if not cap in self.capabilities:\n+ 			raise self.error("Server doesn't allow %s authentication." % mech)\n+ 		self.literal = _Authenticator(authobject).process\n+ 		typ, dat = self._simple_command('AUTHENTICATE', mech...[truncated]
- short doc diff:   Authenticate command - requires response processing.\n  \n- 		UNIMPLEMENTED\n+ 		'mechanism' specifies which authentication mechanism is to\n+ 		be used - it must appear in <instance>.capabilities in the\n+ 		form AUTH=<mechanism>.\n+ \n+ 		'authobject' must be a callable object:\n+ \n+ 			data = authobject(response)\n+ \n+ 		It will be called to process s...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-django-b1e33ceceda1e75ff68c7deed8f6659683a195d3-FixtureTestCase.test_pseudo_empty_fixtures-495

- repo/project: `django`
- function: `FixtureTestCase.test_pseudo_empty_fixtures`
- commit hash: `b1e33ceceda1e75ff68c7deed8f6659683a195d3`
- confidence: `0.3548`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_test_command`
- predicted target: `docs/testing.md`
- short code diff:   def test_pseudo_empty_fixtures(self):\n-         ""\n?         --\n\n+         \n+         \n+         \n          new_io = StringIO()\n          management.call_command('loaddata', 'pets', stdout=new_io, stderr=new_io)\n          command_output = new_io.getvalue().strip()\n          # No objects will actually be loaded\n          self.assertEqual(command_output, "Installed 0 object(s) (of 2) from 1 fixture(s)")
- short doc diff: - A fixture can contain entries, but lead to nothing in the database; this shouldn't raise an error (ref #14068)\n?                                                                    -------------------------------------------\n\n+ A fixture can contain entries, but lead to nothing in the database;\n+         this shouldn't raise an error (#14068).
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-ansible-0d5a9f2138b0626e1c836333e3af0b73bdc31ec8-run_command-327

- repo/project: `ansible`
- function: `run_command`
- commit hash: `0d5a9f2138b0626e1c836333e3af0b73bdc31ec8`
- confidence: `0.3513`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_test_command`
- predicted target: `docs/testing.md`
- short code diff: - def run_command(args, cmd, capture=False, env=None, data=None, cwd=None, always=False, stdin=None, stdout=None,\n-                 cmd_verbosity=1, str_errors='strict', error_callback=None):\n-     \n-     \n+ def run_command(\n+         args,  # type: CommonConfig\n+         cmd,  # type: t.Iterable[str]\n+         capture=False,  # type: bool\n+         env=None,  # type: t.Optional[t.Dict[str, str]]\n+         d...[truncated]
- short doc diff: + Run the specified command and return stdout and stderr as a tuple.\n- :type args: CommonConfig\n-     :type cmd: collections.Iterable[str]\n-     :type capture: bool\n-     :type env: dict[str, str] | None\n-     :type data: str | None\n-     :type cwd: str | None\n-     :type always: bool\n-     :type stdin: file | None\n-     :type stdout: file | None\n-...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-cpython-5a6d4bf671699152fb417e8f8ba899aa5e1d8d42-TestResult.stop-135

- repo/project: `cpython`
- function: `TestResult.stop`
- commit hash: `5a6d4bf671699152fb417e8f8ba899aa5e1d8d42`
- confidence: `0.3368`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_test_command`
- predicted target: `docs/testing.md`
- short code diff:   def stop(self):\n-         ""\n?         --\n\n+         \n          self.shouldStop = True
- short doc diff: - Indicates that the tests should be aborted\n+ Indicates that the tests should be aborted.\n?                                           +\n
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-localstack-41b4d232735084f906778549432b3f8266d2c11d-test_loading_own_specs-422

- repo/project: `localstack`
- function: `test_loading_own_specs`
- commit hash: `41b4d232735084f906778549432b3f8266d2c11d`
- confidence: `0.3329`
- predicted doc category: `testing_instructions`
- predicted scenario: `changed_test_command`
- predicted target: `docs/testing.md`
- short code diff:   def test_loading_own_specs():\n      \n      loader = CustomLoader({})\n      # first test that specs remain intact\n-     sqs_query_description = loader.load_service_model("sqs-query", "service-2")\n?                                                           ------\n\n+     sqs_query_description = loader.load_service_model("sqs", "service-2")\n      assert sqs_query_description["metadata"]["protocol"] == "query"\n...[truncated]
- short doc diff: - Ensure that the internalized specifications (f.e. the sqs-query spec) can be handled by the CustomLoader.\n?                                                           ^^^^^\n\n+ Ensure that the internalized specifications (f.e. the sqs-json spec) can be handled by the CustomLoader.\n?                                                           ^^^^\n
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-faceswap-7f5391145318ebe8012818eb810070e76be7e3b7-QueueManager.add_queue-44

- repo/project: `faceswap`
- function: `QueueManager.add_queue`
- commit hash: `7f5391145318ebe8012818eb810070e76be7e3b7`
- confidence: `0.3221`
- predicted doc category: `workflow_documentation`
- predicted scenario: `added_response_field`
- predicted target: `docs/workflows.md`
- short code diff:   def add_queue(self, name, maxsize=0):\n            \n+ \n+         logger.debug("QueueManager adding: (name: '%s', maxsize: %s)", name, maxsize)\n          if name in self.queues.keys():\n              raise ValueError("Queue '{}' already exists.".format(name))\n          queue = self.manager.Queue(maxsize=maxsize)\n+         setattr(queue, "shutdown", self.shutdown)\n          self.queues[name] = queue\n+         ...[truncated]
- short doc diff:   Add a queue to the manager\n+ \n+             Adds an event "shutdown" to the queue that can be used to indicate\n+             to a process that any activity on the queue should cease
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-Open-Assistant-48c438041890422019976902f636fc9f71bc4a22-get_current_user_id-378

- repo/project: `Open-Assistant`
- function: `get_current_user_id`
- commit hash: `48c438041890422019976902f636fc9f71bc4a22`
- confidence: `0.3125`
- predicted doc category: `architecture_flow`
- predicted scenario: `changed_middleware_auth_flow`
- predicted target: `docs/architecture.md`
- short code diff:   def get_current_user_id(token: str = Security(oauth2_scheme)) -> str | None:\n      \n      if not settings.use_auth:\n          return None\n+     if token is None:\n+         raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authenticated")\n  \n      # Generate a key from the auth secret\n-     key = derive_key()\n+     key: bytes = derive_key()\n?        +++++++\n\n  \n      # Decrypt the JWE toke...[truncated]
- short doc diff: - Decode the current user JWT token and return the payload.\n+ Get the current user ID by decoding the JWT token.
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

### codocbench-scikit-learn-eb901df93f90aa8420d1183ea0fa1fb84da1d80a-RFE.fit-421

- repo/project: `scikit-learn`
- function: `RFE.fit`
- commit hash: `eb901df93f90aa8420d1183ea0fa1fb84da1d80a`
- confidence: `0.3082`
- predicted doc category: `configuration`
- predicted scenario: `added_environment_variable`
- predicted target: `docs/configuration.md`
- short code diff: - def fit(self, X, y):\n+ def fit(self, X, y, **fit_params):\n          \n          \n-         return self._fit(X, y)\n+         return self._fit(X, y, **fit_params)\n?                              ++++++++++++++\n
- short doc diff:   Fit the RFE model and then the underlying estimator on the selected features.\n  \n          Parameters\n          ----------\n          X : {array-like, sparse matrix} of shape (n_samples, n_features)\n              The training input samples.\n  \n          y : array-like of shape (n_samples,)\n              The target values.\n  \n+         **fit_params...[truncated]
- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue

