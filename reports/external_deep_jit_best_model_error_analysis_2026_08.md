# External Deep-JIT Best Model Error Analysis 2026-08

- Best model: `tfidf_logreg`
- Input mode: `code_diff_only`
- Decision/confidence rule: max predicted class probability from LogisticRegression; not externally calibrated

## Confusion Matrix

- TP: `879`
- FP: `339`
- TN: `1114`
- FN: `574`

## Error Counts By Subset

- `Return`: 492
- `Summary`: 421

## Confidence/Margin Distribution

- Median: `0.6574`
- Mean: `0.6829`
- Min: `0.5000`
- Max: `0.9956`

## Top Error Examples

### deep-jit-stanfordnlp_CoreNLP-2074-FirstSentence-0

- Subset: `Summary`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.9947`
- Old comment excerpt: Accepts a String that is a sentence end punctuation tag, and rejects everything else.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n   public boolean isSentenceFinalPunctuationTag(String str) {\n-    return sFPunctTagStringAcceptFilter.accept(str);\n+    return sFPunctTagStringAcceptFilter.test(str);\n   }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-querydsl_querydsl-443-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.9639`
- Old comment excerpt: @return this.equalsIgnoreCase(str)
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public BooleanExpression equalsIgnoreCase(String str) {\n-        return equalsIgnoreCase(StringConstant.create(str));\n+        return equalsIgnoreCase(new StringConstant(str));\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-querydsl_querydsl-355-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.9595`
- Old comment excerpt: @return this + str
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public EString append(String str) {\n-        return append(EString.__create(str));\n+        return append(EStringConst.create(str));\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-rstudio_rstudio-5-2024

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.9537`
- Old comment excerpt: @return Opaque string handle for this terminal instance, or null if terminal has never been attached to a process
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -2,5 +2,5 @@\n     if (consoleProcess_ == null) {\n         return terminalHandle_;\n     }\n-    return consoleProcess_.getProcessInfo().getTerminalHandle();\n+    return consoleProcess_.getProcessInfo().getHandle();\n }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-debezium_debezium-266-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.9528`
- Old comment excerpt: @return the list of regular expression  Patterns included in the list; never null
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n-    public static Set<Pattern> listOfRegex(String input, int regexFlags) {\n+    public static List<Pattern> listOfRegex(String input, int regexFlags) {\n         return listOf(input, RegExSplitter::split, (str) -> Pattern.compile(str, regexFlags));\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-querydsl_querydsl-456-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.9378`
- Old comment excerpt: @return this.endsWith(str)
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public BooleanExpression endsWith(String str) {\n-        return endsWith(StringConstant.create(str));\n+        return endsWith(ConstantImpl.create(str));\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-heuermh_ensembl-rest-client-2-5256

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.9206`
- Old comment excerpt: @return a new feature service with the default server URL
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n public FeatureService createFeatureService() {\n-    return createFeatureService(defaultServerUrl);\n+    return createFeatureService(defaultEndpointUrl);\n }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_batik-50-4420

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.9206`
- Old comment excerpt: @return the extension handler used by this SVGGraphics2D instance
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n public ExtensionHandler getExtensionHandler() {\n-    return extensionHandler;\n+    return generatorContext.getExtensionHandler();\n }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-heuermh_ensembl-rest-client-6-5258

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.9206`
- Old comment excerpt: @return a new variation service with the default server URL
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n public VariationService createVariationService() {\n-    return createVariationService(defaultServerUrl);\n+    return createVariationService(defaultEndpointUrl);\n }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-heuermh_ensembl-rest-client-4-5257

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.9206`
- Old comment excerpt: @return a new lookup service with the default server URL
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n public LookupService createLookupService() {\n-    return createLookupService(defaultServerUrl);\n+    return createLookupService(defaultEndpointUrl);\n }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-heuermh_ensembl-rest-client-8-5259

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.9206`
- Old comment excerpt: @return a new sequence service with the default server URL
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n public SequenceService createSequenceService() {\n-    return createSequenceService(defaultServerUrl);\n+    return createSequenceService(defaultEndpointUrl);\n }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-heuermh_ensembl-rest-client-2-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.9206`
- Old comment excerpt: Create and return a new feature service with the default server URL.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n     public FeatureService createFeatureService() {\n-        return createFeatureService(defaultServerUrl);\n+        return createFeatureService(defaultEndpointUrl);\n     }\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-heuermh_ensembl-rest-client-8-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.9206`
- Old comment excerpt: Create and return a new sequence service with the default server URL.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n     public SequenceService createSequenceService() {\n-        return createSequenceService(defaultServerUrl);\n+        return createSequenceService(defaultEndpointUrl);\n     }\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-heuermh_ensembl-rest-client-6-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.9206`
- Old comment excerpt: Create and return a new variation service with the default server URL.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n     public VariationService createVariationService() {\n-        return createVariationService(defaultServerUrl);\n+        return createVariationService(defaultEndpointUrl);\n     }\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-heuermh_ensembl-rest-client-4-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.9206`
- Old comment excerpt: C6reate and return a new lookup service with the default server URL.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n     public LookupService createLookupService() {\n-        return createLookupService(defaultServerUrl);\n+        return createLookupService(defaultEndpointUrl);\n     }\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-querydsl_querydsl-515-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.9065`
- Old comment excerpt: @return this.endsWith(str)
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public BooleanExpression endsWith(Expression<String> str) {\n-        return BooleanOperation.create(Ops.ENDS_WITH, this, str);\n+        return BooleanOperation.create(Ops.ENDS_WITH, mixin, str);\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_lenya-365-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.9013`
- Old comment excerpt: DOCUMENT ME!
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,5 +1,6 @@\n     public Reader getReader() {\n-        debug("\nContents: " + contentsBuffer.toString());\n+        debug("\nContents: " + this.contentsBuffer.toString());\n \n-        return new StringReader(contentsBuffer.toString());\n+        return new StringReader(this.contentsBuffer.toString());\n     }\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-querydsl_querydsl-525-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.8973`
- Old comment excerpt: @return this.startsWith(str)
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public BooleanExpression startsWith(Expression<String> str) {\n-        return BooleanOperation.create(Ops.STARTS_WITH, this, str);\n+        return BooleanOperation.create(Ops.STARTS_WITH, mixin, str);\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-querydsl_querydsl-525-FirstSentence-0

- Subset: `Summary`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.8973`
- Old comment excerpt: Return true if this starts with str
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public BooleanExpression startsWith(Expression<String> str) {\n-        return BooleanOperation.create(Ops.STARTS_WITH, this, str);\n+        return BooleanOperation.create(Ops.STARTS_WITH, mixin, str);\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-SeleniumHQ_selenium-441-FirstSentence-0

- Subset: `Summary`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.8906`
- Old comment excerpt: Gets the SOCKS version (4 or 5).
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n-  public String getSocksVersion() {\n+  public Integer getSocksVersion() {\n     return socksVersion;\n   }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-eclipse_mylyn.reviews-3-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8777`
- Old comment excerpt: Returns the meta object for the containment reference list '  org.eclipse.mylyn.reviews.core.model.IComment#getReplies Replies'.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n 	public EReference getComment_Replies() {\n-		return (EReference) commentEClass.getEStructuralFeatures().get(4);\n+		return (EReference) commentEClass.getEStructuralFeatures().get(3);\n 	}\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-eclipse_mylyn.reviews-1-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8777`
- Old comment excerpt: Returns the meta object for the reference ' org.eclipse.mylyn.reviews.core.model.ITopic#getItem Item'.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n 	public EReference getTopic_Item() {\n-		return (EReference) topicEClass.getEStructuralFeatures().get(5);\n+		return (EReference) topicEClass.getEStructuralFeatures().get(4);\n 	}\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-eclipse_mylyn.reviews-0-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8777`
- Old comment excerpt: Returns the meta object for the reference list ' org.eclipse.mylyn.reviews.core.model.ITopic#getComments Comments'.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n 	public EReference getTopic_Comments() {\n-		return (EReference) topicEClass.getEStructuralFeatures().get(2);\n+		return (EReference) topicEClass.getEStructuralFeatures().get(1);\n 	}\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-zaproxy_zaproxy-1974-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `0.8731`
- Old comment excerpt: @return the found occurrence or null if no match has been done
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,9 +1,9 @@\n     public String findInContent(String content) {\n         \n         // First check for a simple exact occurrence\n-        for (String str : strings) {\n-            if (content.contains(str))\n-                return str;\n+        for (BoyerMooreMatcher matcher : strings) {\n+            if (matcher.findInContent(content) >= 0)\n+                return matcher.getPat...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-codehaus_picocontainer-69-3941

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8630`
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
- Confidence/margin: `0.8630`
- Old comment excerpt: @return the adapter to test
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,5 +1,5 @@\n private ComponentAdapter prepRES_lifecycleManagerHonorsInstantiationSequence(MutablePicoContainer picoContainer) {\n-    picoContainer.component(RecordingLifecycle.One.class);\n+    picoContainer.addComponent(RecordingLifecycle.One.class);\n     PoolingComponentAdapter poolingComponentAdapter = new PoolingComponentAdapter(new ConstructorInjectionComponentAdapter(Recording...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-RobotiumTech_robotium-1504-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8570`
- Old comment excerpt: @return true if no more scrolling can be done
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -9,15 +9,13 @@\n 		\n 		if (checkTextView != null\n 				&& !checkTextView.getText().equals(\n-						soloView.getCurrentTextViews(null).get(\n-								soloView.getCurrentTextViews(null).size()\n-										- constant).getText())) {\n+						textViewList.get(size - constant).getText())) {\n 			checkTextView = textViewList.get(size - constant);\n-			return true;\n+			return false;\n 		} else...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-RobotiumTech_robotium-1504-FirstSentence-0

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8570`
- Old comment excerpt: Determines if no more scrolling can be done.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -9,15 +9,13 @@\n 		\n 		if (checkTextView != null\n 				&& !checkTextView.getText().equals(\n-						soloView.getCurrentTextViews(null).get(\n-								soloView.getCurrentTextViews(null).size()\n-										- constant).getText())) {\n+						textViewList.get(size - constant).getText())) {\n 			checkTextView = textViewList.get(size - constant);\n-			return true;\n+			return false;\n 		} else...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_drill-1427-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8530`
- Old comment excerpt: @return - Single row indicating drop succeeded, raise exception otherwise
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -10,11 +10,19 @@\n       drillSchema = SchemaUtilites.resolveToMutableDrillSchema(defaultSchema, dropTableNode.getSchema());\n     }\n \n-    String tableName = ((SqlDropTable) sqlNode).getName();\n+    String tableName = dropTableNode.getName();\n     if (drillSchema == null) {\n       throw UserException.validationError()\n           .message("Invalid table_name [%s]", tableName)\n   ...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_drill-1427-FirstSentence-0

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `0.8530`
- Old comment excerpt: Function resolves the schema and invokes the drop method.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -10,11 +10,19 @@\n       drillSchema = SchemaUtilites.resolveToMutableDrillSchema(defaultSchema, dropTableNode.getSchema());\n     }\n \n-    String tableName = ((SqlDropTable) sqlNode).getName();\n+    String tableName = dropTableNode.getName();\n     if (drillSchema == null) {\n       throw UserException.validationError()\n           .message("Invalid table_name [%s]", tableName)\n   ...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

## Limitations

This analysis is for the external code-comment consistency proxy only. It does not measure project-level Markdown documentation patching.
