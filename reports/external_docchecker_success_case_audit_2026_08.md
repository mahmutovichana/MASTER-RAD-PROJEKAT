# External DocChecker Success Case Audit 2026-08

- True positives: `250`
- True negatives: `2`

## True Negatives

### deep-jit-JodaOrg_joda_time-944-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `False`
- Confidence: `0.2261`
- Predicted doc_category: `no_update`
- Predicted scenario_type: `docs_already_updated`
- Code excerpt:     public static long safeSubtract(long val1, long val2) {\n        long diff = val1 - val2;\n        // If there is a sign change, but the two values have different signs...\n        if ((val1 ^ diff) < 0 && (val1 ^ val2) < 0) {\n            throw new ArithmeticException\n                ("The calculation caused an overflow: " + val1 + " - " + val2);\n        }\n        return diff;\n    }\n
- Comment excerpt: Subtracts two values throwing an exception if overflow occurs.

- [ ] notes

### deep-jit-JodaOrg_joda_time-887-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `False`
- Confidence: `0.2953`
- Predicted doc_category: `no_update`
- Predicted scenario_type: `docs_already_updated`
- Code excerpt:     public String getShortName(long instant, Locale locale) {\n        if (locale == null) {\n            locale = Locale.getDefault();\n        }\n        String nameKey = getNameKey(instant);\n        if (nameKey == null) {\n            return iID;\n        }\n        String name = cNameProvider.getShortName(locale, iID, nameKey);\n        if (name != null) {\n            return name;\n        }\n        return pri...[truncated]
- Comment excerpt: @return the human-readable short name in the specified locale

- [ ] notes


## Representative True Positives

### deep-jit-ansell_openrdf-sesame-162-Associations-FirstSentence

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `1`
- Mapped label: `True`
- Predicted label: `True`
- Confidence: `0.0697`
- Predicted doc_category: `testing_instructions`
- Predicted scenario_type: `changed_test_command`
- Code excerpt: 	public static String encodeValue(Value value) {\r\n		if (value instanceof BNode) {\r\n			// SES-2129 special treatment of blank node names to avoid problems with round-tripping.\r\n			return ((BNode)value).getID();\r\n		}\r\n		\r\n		// for everything else we just use N-Triples serialization.\r\n		return NTriplesUtil.toNTriplesString(value);\r\n	}\r\n\n
- Comment excerpt: Encodes a value in a canonical serialized string format, for use in a URL query parameter.

- [ ] notes

### deep-jit-albfan_sqlworkbenchj-61-4376

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `1`
- Mapped label: `True`
- Predicted label: `True`
- Confidence: `0.0908`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `changed_test_command`
- Code excerpt: public int getRowStatus(int aRow) throws IndexOutOfBoundsException {\n    RowData row = this.getRow(aRow);\n    if (row.isNew()) {\n        return RowData.NEW;\n    } else if (row.isModified()) {\n        return RowData.MODIFIED;\n    } else {\n        return RowData.NOT_MODIFIED;\n    }\n}
- Comment excerpt: @return an int identifying the status

- [ ] notes

### deep-jit-NanoHttpd_nanohttpd-24-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `1`
- Mapped label: `True`
- Predicted label: `True`
- Confidence: `0.1008`
- Predicted doc_category: `testing_instructions`
- Predicted scenario_type: `changed_validation_max`
- Code excerpt:     protected boolean useGzipWhenAccepted(Response r) {\n        return r.getMimeType() != null && r.getMimeType().toLowerCase().contains("text/");\n    }\n
- Comment excerpt: @return true if the gzip compression should be used if the client accespts it. Default this option is on for text content and off for everything else.

- [ ] notes

### deep-jit-JodaOrg_joda_time-453-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `1`
- Mapped label: `True`
- Predicted label: `True`
- Confidence: `0.1098`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `added_service_orchestration_flow`
- Code excerpt:     public IntervalConverter removeIntervalConverter(IntervalConverter converter)\n            throws SecurityException {\n        \n        checkAlterIntervalConverters();\n        if (converter == null) {\n            return null;\n        }\n        IntervalConverter[] removed = new IntervalConverter[1];\n        iIntervalConverters = iIntervalConverters.remove(converter, removed);\n        return removed[0];\n   ...[truncated]
- Comment excerpt: Removes a converter from the set of converters.

- [ ] notes

### deep-jit-SeleniumHQ_selenium-996-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `1`
- Mapped label: `True`
- Predicted label: `True`
- Confidence: `0.1178`
- Predicted doc_category: `configuration`
- Predicted scenario_type: `removed_environment_variable`
- Code excerpt:   public Level getLevel(String logType) {\n    return prefs.get(logType) == null ? Level.OFF : prefs.get(logType);\n  }\n
- Comment excerpt: @return the  Level for the given  LogType if enabled. Otherwise returns  Level.OFF.

- [ ] notes

### deep-jit-akibsayyed_jain-slee-40-7297

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `1`
- Mapped label: `True`
- Predicted label: `True`
- Confidence: `0.1289`
- Predicted doc_category: `configuration`
- Predicted scenario_type: `changelog_worthy_behavior_change`
- Code excerpt: public boolean isProfileReadOnly() {\n    return profileReadOnly && !isManagementView() && getProfileName() != null;\n}
- Comment excerpt: @return false if the object is currently assigned to an mbean or if it is not read only or if it is default profile

- [ ] notes

### deep-jit-Vexatos_Resonant-Induction-1-0-6840

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `1`
- Mapped label: `True`
- Predicted label: `True`
- Confidence: `0.1444`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `added_service_orchestration_flow`
- Code excerpt: @Override\npublic int onReceiveLiquid(int type, int vol, byte side) {\n    if (type == this.type) {\n        int rejectedVolume = Math.max((this.getStoredLiquid(type) + vol) - this.capacity, NUM);\n        this.liquidStored = vol - rejectedVolume;\n        return rejectedVolume;\n    }\n    return vol;\n}
- Comment excerpt: @return vol - The amount of rejected power to be sent back into the conductor

- [ ] notes

### deep-jit-Graylog2_graylog2-server-22-Associations-FirstSentence

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `1`
- Mapped label: `True`
- Predicted label: `True`
- Confidence: `0.1648`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `added_service_orchestration_flow`
- Code excerpt:     public boolean isConnected() {\n        final Health request = new Health.Builder()\n                .local()\n                .timeout(Ints.saturatedCast(requestTimeout.toSeconds()))\n                .build();\n\n        final JestResult result = JestUtils.execute(jestClient, request, () -> "Couldn't check connection status of Elasticsearch");\n        final int numberOfDataNodes = Optional.of(result.getJsonObje...[truncated]
- Comment excerpt: Check if Elasticsearch is available and that there are data nodes in the cluster.

- [ ] notes

### deep-jit-RobotiumTech_robotium-1486-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `1`
- Mapped label: `True`
- Predicted label: `True`
- Confidence: `0.2030`
- Predicted doc_category: `model_contract`
- Predicted scenario_type: `removed_dto_model_field`
- Code excerpt: 	private boolean searchForToggleButton(String regex, int matches) {\n		sleeper.sleep();\n		inst.waitForIdleSync();\n		Pattern p = Pattern.compile(regex);\n		Matcher matcher;\n		ArrayList<ToggleButton> toggleButtonList = viewFetcher.getCurrentViews(ToggleButton.class);\n		if(matches == 0)\n			matches = 1;\n		for(ToggleButton toggleButton : toggleButtonList){\n			matcher = p.matcher(toggleButton.getText().toString());\...[truncated]
- Comment excerpt: Searches for a toggle button with the given regex string and returns true if the searched toggle button is found a given number of times

- [ ] notes

### deep-jit-SeleniumHQ_selenium-993-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `1`
- Mapped label: `True`
- Predicted label: `True`
- Confidence: `0.3267`
- Predicted doc_category: `testing_instructions`
- Predicted scenario_type: `changed_test_command`
- Code excerpt:     static Object wrapArgumentForScriptExecution(Object argument) {\n      JSONObject wrappedArgument = new JSONObject();\n      try {\n        if (argument instanceof String) {\n          wrappedArgument.put("type", "STRING");\n          wrappedArgument.put("value", argument);\n        } else if (argument instanceof Boolean) {\n          wrappedArgument.put("type", "BOOLEAN");\n          wrappedArgument.put("value",...[truncated]
- Comment excerpt: @return wrapped up value TODO(danielwh): See if JSONObject and JSONArray have a useful common superclass

- [ ] notes

