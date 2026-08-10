# External Deep-JIT Best Model Error Analysis 2026-08

- Best model: `tfidf_logreg`
- Input mode: `old_comment_plus_code_diff`
- Decision/confidence rule: max predicted class probability from LogisticRegression; not externally calibrated

## Confusion Matrix

- TP: `853`
- FP: `309`
- TN: `1144`
- FN: `600`
- Specificity: `78.73%`
- Balanced accuracy: `68.72%`
- MCC: `0.3821`

## Error Counts By Subset

- `Return`: 478
- `Summary`: 431

## Confidence/Margin Distribution

- Median: `0.6723`
- Mean: `0.6890`
- Min: `0.5002`
- Max: `0.9983`

## Top Error Examples

### deep-jit-querydsl_querydsl-355-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.9694`
- Old comment excerpt: @return this + str
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public EString append(String str) {\n-        return append(EString.__create(str));\n+        return append(EStringConst.create(str));\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-querydsl_querydsl-443-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.9679`
- Old comment excerpt: @return this.equalsIgnoreCase(str)
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public BooleanExpression equalsIgnoreCase(String str) {\n-        return equalsIgnoreCase(StringConstant.create(str));\n+        return equalsIgnoreCase(new StringConstant(str));\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-querydsl_querydsl-456-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.9577`
- Old comment excerpt: @return this.endsWith(str)
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public BooleanExpression endsWith(String str) {\n-        return endsWith(StringConstant.create(str));\n+        return endsWith(ConstantImpl.create(str));\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-stanfordnlp_CoreNLP-2074-FirstSentence-0

- Subset: `Summary`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.9576`
- Old comment excerpt: Accepts a String that is a sentence end punctuation tag, and rejects everything else.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n   public boolean isSentenceFinalPunctuationTag(String str) {\n-    return sFPunctTagStringAcceptFilter.accept(str);\n+    return sFPunctTagStringAcceptFilter.test(str);\n   }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-querydsl_querydsl-515-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.9236`
- Old comment excerpt: @return this.endsWith(str)
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public BooleanExpression endsWith(Expression<String> str) {\n-        return BooleanOperation.create(Ops.ENDS_WITH, this, str);\n+        return BooleanOperation.create(Ops.ENDS_WITH, mixin, str);\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-querydsl_querydsl-525-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.9149`
- Old comment excerpt: @return this.startsWith(str)
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public BooleanExpression startsWith(Expression<String> str) {\n-        return BooleanOperation.create(Ops.STARTS_WITH, this, str);\n+        return BooleanOperation.create(Ops.STARTS_WITH, mixin, str);\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_lenya-365-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.9056`
- Old comment excerpt: DOCUMENT ME!
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,5 +1,6 @@\n     public Reader getReader() {\n-        debug("\nContents: " + contentsBuffer.toString());\n+        debug("\nContents: " + this.contentsBuffer.toString());\n \n-        return new StringReader(contentsBuffer.toString());\n+        return new StringReader(this.contentsBuffer.toString());\n     }\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-docker_java_docker_java-76-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.8909`
- Old comment excerpt: @return a  Link matching the specification
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -4,7 +4,9 @@\n 			final String[] parts = serialized.split(":");\n 			switch (parts.length) {\n 			case 2: {\n-				return new Link(parts[0], parts[1]);\n+				String[] nameSplit = parts[0].split("/");\n+				String[] aliasSplit = parts[1].split("/");\n+				return new Link(nameSplit[nameSplit.length - 1], aliasSplit[aliasSplit.length - 1]);\n 			}\n 			default: {\n 				throw new IllegalArgu...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-nickman_qreactor-3-5172

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8806`
- Old comment excerpt: @return the wireType
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n public WireType getWireType() {\n-    return wireType;\n+    return queue.wireType();\n }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-nickman_qreactor-2-5171

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8806`
- Old comment excerpt: @return the rollCycle
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n public RollCycle getRollCycle() {\n-    return rollCycle;\n+    return queue.rollCycle();\n }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-querydsl_querydsl-525-FirstSentence-0

- Subset: `Summary`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.8775`
- Old comment excerpt: Return true if this starts with str
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public BooleanExpression startsWith(Expression<String> str) {\n-        return BooleanOperation.create(Ops.STARTS_WITH, this, str);\n+        return BooleanOperation.create(Ops.STARTS_WITH, mixin, str);\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-zaproxy_zaproxy-1974-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.8701`
- Old comment excerpt: @return the found occurrence or null if no match has been done
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,9 +1,9 @@\n     public String findInContent(String content) {\n         \n         // First check for a simple exact occurrence\n-        for (String str : strings) {\n-            if (content.contains(str))\n-                return str;\n+        for (BoyerMooreMatcher matcher : strings) {\n+            if (matcher.findInContent(content) >= 0)\n+                return matcher.getPat...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_drill-1551-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8633`
- Old comment excerpt: @return true if spilling is needed, false otherwise
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,12 +1,24 @@\n   private boolean isSpillNeeded(int incomingSize) {\n+\n+    if (bufferedBatches.size() >= config.getBufferedBatchLimit()) {\n+      return true;\n+    }\n \n     // Can't spill if less than two batches else the merge\n     // can't make progress.\n \n+    final boolean spillNeeded = memManager.isSpillNeeded(allocator.getAllocatedMemory(), incomingSize);\n     if (buffe...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-macalinao_albkit-16-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8582`
- Old comment excerpt: Checks whether this ChatSection's argument can be parsed as a boolean
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n     public boolean isBoolean() {\n-        return arg.equals("true") || arg.equals("false");\n+        return raw.equals("true") || raw.equals("false");\n     }\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-yahoo_fili-42-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8539`
- Old comment excerpt: Build a DruidDimensionsLoader.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,11 +1,13 @@\n-    protected DruidDimensionsLoader buildDruidDimensionsLoader(\n+    protected DimensionValueLoadTask buildDruidDimensionsLoader(\n             DruidWebService webService,\n             PhysicalTableDictionary physicalTableDictionary,\n             DimensionDictionary dimensionDictionary\n     ) {\n-        return new DruidDimensionsLoader(\n+        DruidDimensionValu...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_drill-1427-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8512`
- Old comment excerpt: @return - Single row indicating drop succeeded, raise exception otherwise
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -10,11 +10,19 @@\n       drillSchema = SchemaUtilites.resolveToMutableDrillSchema(defaultSchema, dropTableNode.getSchema());\n     }\n \n-    String tableName = ((SqlDropTable) sqlNode).getName();\n+    String tableName = dropTableNode.getName();\n     if (drillSchema == null) {\n       throw UserException.validationError()\n           .message("Invalid table_name [%s]", tableName)\n   ...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-debezium_debezium-266-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.8505`
- Old comment excerpt: @return the list of regular expression  Patterns included in the list; never null
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n-    public static Set<Pattern> listOfRegex(String input, int regexFlags) {\n+    public static List<Pattern> listOfRegex(String input, int regexFlags) {\n         return listOf(input, RegExSplitter::split, (str) -> Pattern.compile(str, regexFlags));\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-querydsl_querydsl-522-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.8493`
- Old comment excerpt: @return locate(str, this, start)
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public NumberExpression<Integer> locate(Expression<String> str, NumberExpression<Integer> start) {\n-        return NumberOperation.create(Integer.class, Ops.StringOps.LOCATE2, str, this, start);\n+        return NumberOperation.create(Integer.class, Ops.StringOps.LOCATE2, str, mixin, start);\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-iSoron_uhabits-3-2472

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8451`
- Old comment excerpt: @return true if habit has reminder
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n public boolean hasReminder() {\n-    return (reminderHour != null && reminderMin != null);\n+    return reminder != null;\n }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-yahoo_fili-42-5483

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8449`
- Old comment excerpt: @return A DruidDimensionsLoader
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n-protected DruidDimensionsLoader buildDruidDimensionsLoader(DruidWebService webService, PhysicalTableDictionary physicalTableDictionary, DimensionDictionary dimensionDictionary) {\n-    return new DruidDimensionsLoader(physicalTableDictionary, dimensionDictionary, webService);\n+protected DimensionValueLoadTask buildDruidDimensionsLoader(DruidWebService webService, Physica...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-JodaOrg_joda_time-421-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8393`
- Old comment excerpt: @return the created LocalDateTime
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -2,8 +2,10 @@\n         if (calendar == null) {\n             throw new IllegalArgumentException("The calendar must not be null");\n         }\n+        int era = calendar.get(Calendar.ERA);\n+        int yearOfEra = calendar.get(Calendar.YEAR);\n         return new LocalDateTime(\n-            calendar.get(Calendar.YEAR),\n+            (era == GregorianCalendar.AD ? yearOfEra : 1 - yea...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-JodaOrg_joda_time-420-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8377`
- Old comment excerpt: @return the created LocalDate
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -2,8 +2,10 @@\n         if (calendar == null) {\n             throw new IllegalArgumentException("The calendar must not be null");\n         }\n+        int era = calendar.get(Calendar.ERA);\n+        int yearOfEra = calendar.get(Calendar.YEAR);\n         return new LocalDate(\n-            calendar.get(Calendar.YEAR),\n+            (era == GregorianCalendar.AD ? yearOfEra : 1 - yearOfE...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-OpenAPITools_openapi_generator-1903-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.8357`
- Old comment excerpt: @return enumString
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,6 @@\n-  public EnumStringEnum getEnumString() {\n-    return enumString;\n+  public String getEnumString() {\n+    if (enumString == null) {\n+      return null;\n+    }\n+    return enumString.value();\n   }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-Atmosphere_atmosphere-879-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8345`
- Old comment excerpt: @return an instance of the specified class
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -3,9 +3,7 @@\n             return (AsyncSupport) targetClass.getDeclaredConstructor(new Class[]{AtmosphereConfig.class})\n                     .newInstance(config);\n         } catch (final Exception e) {\n-            logger.error("Failed to create comet support class: {}, error: {}", targetClass, e);\n-            logger.error("Switching to BlockingIO");\n-\n-            return new Bl...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_drill-1427-FirstSentence-0

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8301`
- Old comment excerpt: Function resolves the schema and invokes the drop method.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -10,11 +10,19 @@\n       drillSchema = SchemaUtilites.resolveToMutableDrillSchema(defaultSchema, dropTableNode.getSchema());\n     }\n \n-    String tableName = ((SqlDropTable) sqlNode).getName();\n+    String tableName = dropTableNode.getName();\n     if (drillSchema == null) {\n       throw UserException.validationError()\n           .message("Invalid table_name [%s]", tableName)\n   ...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-SeleniumHQ_selenium-441-FirstSentence-0

- Subset: `Summary`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.8291`
- Old comment excerpt: Gets the SOCKS version (4 or 5).
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n-  public String getSocksVersion() {\n+  public Integer getSocksVersion() {\n     return socksVersion;\n   }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-yahoo_fili-1-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8279`
- Old comment excerpt: Exports current thread's request log object as a JSON string without resetting it.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -2,11 +2,6 @@\n         RequestLog current = RLOG.get();\n         record(new Durations(current.aggregateDurations()));\n         record(new Threads(current.threadIds));\n-        try {\n-            return current.mapper.writeValueAsString(current.info);\n-        } catch (JsonProcessingException jpe) {\n-            String msg = String.format("Exporting mega log line with id: '%s' to ...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-SeleniumHQ_selenium-831-FirstSentence-0

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8232`
- Old comment excerpt: Convert an object that may or may not be a JSONArray or JSONObject into its JSON string representation, handling the case where it is neither in a graceful way.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -4,15 +4,8 @@\n     }\n \n     try {\n-      Object converted = convertObject(object, MAX_DEPTH);\n-      if (converted instanceof JSONObject\n-          || converted instanceof JSONArray\n-          || converted instanceof String\n-          || converted instanceof Number) {\n-        return converted.toString();\n-      }\n-\n-      return String.valueOf(object);\n+      JsonElement j...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-codehaus_picocontainer-69-3941

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8229`
- Old comment excerpt: @return the adapter to test
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,5 +1,5 @@\n private ComponentAdapter prepDEF_lifecycleManagerSupport(MutablePicoContainer picoContainer) {\n-    picoContainer.component(RecordingLifecycle.One.class);\n+    picoContainer.addComponent(RecordingLifecycle.One.class);\n     PoolingComponentAdapter poolingComponentAdapter = new PoolingComponentAdapter(new ConstructorInjectionComponentAdapter(RecordingLifecycle.Recorder.c...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-codehaus_picocontainer-70-3942

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8229`
- Old comment excerpt: @return the adapter to test
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,5 +1,5 @@\n private ComponentAdapter prepRES_lifecycleManagerHonorsInstantiationSequence(MutablePicoContainer picoContainer) {\n-    picoContainer.component(RecordingLifecycle.One.class);\n+    picoContainer.addComponent(RecordingLifecycle.One.class);\n     PoolingComponentAdapter poolingComponentAdapter = new PoolingComponentAdapter(new ConstructorInjectionComponentAdapter(Recording...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

## Limitations

This analysis is for the external code-comment consistency proxy only. It does not measure project-level Markdown documentation patching.
