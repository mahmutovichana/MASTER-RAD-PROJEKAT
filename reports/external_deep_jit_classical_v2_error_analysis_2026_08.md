# External Deep-JIT Classical V2 Error Analysis 2026-08

- Model: `logreg_balanced`
- Feature set: `word_char_tfidf_plus_manual_features`
- Input mode: `old_comment_plus_code_diff`
- Score rule: positive-class probability when available
- Selection rule: model selected on validation MCC; test is used once for final evaluation and error analysis.
- Leakage rule: inputs exclude `new_comment_raw`, `doc_after`, and `doc_diff`.

## Confusion Matrix

- TP: `1017`
- FP: `273`
- TN: `1180`
- FN: `436`
- Accuracy: `75.60%`
- Precision: `78.84%`
- Recall: `69.99%`
- F1: `74.15%`
- FPR: `18.79%`
- Specificity: `81.21%`
- Balanced accuracy: `75.60%`
- MCC: `0.5153`

## Per-Subset Metrics

| Subset | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `Return` | 679 | 132 | 788 | 241 | 79.73% | 83.72% | 73.80% | 78.45% | 14.35% | 85.65% | 79.73% | 0.5988 |
| `Summary` | 338 | 141 | 392 | 195 | 68.48% | 70.56% | 63.41% | 66.80% | 26.45% | 73.55% | 68.48% | 0.3715 |

## Confidence / Probability Summary

- Mean positive-class score: `0.4903`
- Median positive-class score: `0.4492`
- Minimum positive-class score: `0.0099`
- Maximum positive-class score: `0.9998`
- False positives: `273`
- False negatives: `436`

## Representative False Positives

### FP 1: `deep-jit-querydsl_querydsl-443-ConstrainedReturn-0`

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Positive-class score: `0.9656`
- Old comment excerpt: @return this.equalsIgnoreCase(str)
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public BooleanExpression equalsIgnoreCase(String str) {\n-        return equalsIgnoreCase(StringConstant.create(str));\n+        return equalsIgnoreCase(new StringConstant(str));\n     }

### FP 2: `deep-jit-querydsl_querydsl-355-ConstrainedReturn-0`

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Positive-class score: `0.9517`
- Old comment excerpt: @return this + str
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public EString append(String str) {\n-        return append(EString.__create(str));\n+        return append(EStringConst.create(str));\n     }

### FP 3: `deep-jit-querydsl_querydsl-456-ConstrainedReturn-0`

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Positive-class score: `0.9446`
- Old comment excerpt: @return this.endsWith(str)
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public BooleanExpression endsWith(String str) {\n-        return endsWith(StringConstant.create(str));\n+        return endsWith(ConstantImpl.create(str));\n     }

### FP 4: `deep-jit-OpenAPITools_openapi_generator-1903-ConstrainedReturn-0`

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Positive-class score: `0.9406`
- Old comment excerpt: @return enumString
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,6 @@\n-  public EnumStringEnum getEnumString() {\n-    return enumString;\n+  public String getEnumString() {\n+    if (enumString == null) {\n+      return null;\n+    }\n+    return enumString.value();\n   }

### FP 5: `deep-jit-stanfordnlp_CoreNLP-2181-ConstrainedReturn-0`

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Positive-class score: `0.9247`
- Old comment excerpt: @return A new collection of Runnables with the Redwood overhead taken care of
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,53 +1,77 @@\n-    public static ArrayList<Runnable> thread(final String title, Iterable<Runnable> runnables){\n+    public static Iterable<Runnable> thread(final String title, Iterable<Runnable> runnables){\n       //--Preparation\n       //(variables)\n       final AtomicBoolean haveStarted = new AtomicBoolean(false);\n       final ReentrantLock metaInfoLock = new ReentrantLock();\n...[truncated]

### FP 6: `deep-jit-querydsl_querydsl-515-ConstrainedReturn-0`

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Positive-class score: `0.9239`
- Old comment excerpt: @return this.endsWith(str)
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public BooleanExpression endsWith(Expression<String> str) {\n-        return BooleanOperation.create(Ops.ENDS_WITH, this, str);\n+        return BooleanOperation.create(Ops.ENDS_WITH, mixin, str);\n     }

### FP 7: `deep-jit-querydsl_querydsl-525-ConstrainedReturn-0`

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Positive-class score: `0.9200`
- Old comment excerpt: @return this.startsWith(str)
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public BooleanExpression startsWith(Expression<String> str) {\n-        return BooleanOperation.create(Ops.STARTS_WITH, this, str);\n+        return BooleanOperation.create(Ops.STARTS_WITH, mixin, str);\n     }

### FP 8: `deep-jit-debezium_debezium-1301-FirstSentence-0`

- Subset: `Summary`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Positive-class score: `0.9051`
- Old comment excerpt: Determine if the supplied value is one of the predefined options.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,7 +1,15 @@\n-        public static Version parse(String value, String defaultValue) {\n-            Version mode = parse(value);\n-            if (mode == null && defaultValue != null) {\n-                mode = parse(defaultValue);\n+        public static EventProcessingFailureHandlingMode parse(String value) {\n+            if (value == null) {\n+                return null;\n     ...[truncated]

### FP 9: `deep-jit-debezium_debezium-1302-FirstSentence-0`

- Subset: `Summary`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Positive-class score: `0.8948`
- Old comment excerpt: Determine if the supplied value is one of the predefined options.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,15 +1,7 @@\n-        public static EventProcessingFailureHandlingMode parse(String value) {\n-            if (value == null) {\n-                return null;\n+        public static GtidNewChannelPosition parse(String value, String defaultValue) {\n+            GtidNewChannelPosition mode = parse(value);\n+            if (mode == null && defaultValue != null) {\n+                mode...[truncated]

### FP 10: `deep-jit-stanfordnlp_CoreNLP-2074-FirstSentence-0`

- Subset: `Summary`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Positive-class score: `0.8838`
- Old comment excerpt: Accepts a String that is a sentence end punctuation tag, and rejects everything else.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n   public boolean isSentenceFinalPunctuationTag(String str) {\n-    return sFPunctTagStringAcceptFilter.accept(str);\n+    return sFPunctTagStringAcceptFilter.test(str);\n   }


## Representative False Negatives

### FN 1: `deep-jit-apache_lenya-365-Associations-FirstSentence`

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Positive-class score: `0.0422`
- Old comment excerpt: DOCUMENT ME!
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,5 +1,6 @@\n     public Reader getReader() {\n-        debug("\nContents: " + contentsBuffer.toString());\n+        debug("\nContents: " + this.contentsBuffer.toString());\n \n-        return new StringReader(contentsBuffer.toString());\n+        return new StringReader(this.contentsBuffer.toString());\n     }\n+

### FN 2: `deep-jit-hibernate_hibernate_orm-1980-ConstrainedReturn-0`

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Positive-class score: `0.0477`
- Old comment excerpt: @return The appropriate StandardProperty definition.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -22,7 +22,6 @@\n \n 			return new StandardProperty(\n 					singularAttributeBinding.getAttribute().getName(),\n-					null,\n 					type,\n 					lazyAvailable && singularAttributeBinding.isLazy(),\n 					true, // insertable\n@@ -48,7 +47,6 @@\n \n 			return new StandardProperty(\n 					pluralAttributeBinding.getAttribute().getName(),\n-					null,\n 					type,\n 					lazyAvailable && plura...[truncated]

### FN 3: `deep-jit-apache_lenya-390-Associations-FirstSentence`

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Positive-class score: `0.0503`
- Old comment excerpt: DOCUMENT ME!
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,7 +1,7 @@\n     public List getImageSrcs(boolean duplicate) {\n         if (duplicate) {\n-            return htmlHandler.getAllImageSrcs();\n-        } else {\n-            return htmlHandler.getImageSrcs();\n+            return this.htmlHandler.getAllImageSrcs();\n         }\n+        return this.htmlHandler.getImageSrcs();\n     }\n+

### FN 4: `deep-jit-JodaOrg_joda_time-420-ConstrainedReturn-0`

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Positive-class score: `0.0505`
- Old comment excerpt: @return the created LocalDate
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -2,8 +2,10 @@\n         if (calendar == null) {\n             throw new IllegalArgumentException("The calendar must not be null");\n         }\n+        int era = calendar.get(Calendar.ERA);\n+        int yearOfEra = calendar.get(Calendar.YEAR);\n         return new LocalDate(\n-            calendar.get(Calendar.YEAR),\n+            (era == GregorianCalendar.AD ? yearOfEra : 1 - yearOfE...[truncated]

### FN 5: `deep-jit-JodaOrg_joda_time-421-ConstrainedReturn-0`

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Positive-class score: `0.0540`
- Old comment excerpt: @return the created LocalDateTime
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -2,8 +2,10 @@\n         if (calendar == null) {\n             throw new IllegalArgumentException("The calendar must not be null");\n         }\n+        int era = calendar.get(Calendar.ERA);\n+        int yearOfEra = calendar.get(Calendar.YEAR);\n         return new LocalDateTime(\n-            calendar.get(Calendar.YEAR),\n+            (era == GregorianCalendar.AD ? yearOfEra : 1 - yea...[truncated]

### FN 6: `deep-jit-apache_lenya-389-Associations-FirstSentence`

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Positive-class score: `0.0630`
- Old comment excerpt: DOCUMENT ME!
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,7 +1,7 @@\n     public List getLinkHRefs(boolean duplicate) {\n         if (duplicate) {\n-            return htmlHandler.getAllLinkHRefs();\n-        } else {\n-            return htmlHandler.getLinkHRefs();\n+            return this.htmlHandler.getAllLinkHRefs();\n         }\n+        return this.htmlHandler.getLinkHRefs();\n     }\n+

### FN 7: `deep-jit-LawnchairLauncher_Lawnchair-421-FirstSentence-0`

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Positive-class score: `0.0650`
- Old comment excerpt: Finds the upper-left coordinate of the first rectangle in the grid that can hold a cell of the specified dimensions.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,51 +1,3 @@\n         boolean findCellForSpan(int[] cellXY, int spanX, int spanY) {\n-            // return the span represented by the CellInfo only there is no view there\n-            //   (this.cell == null) and there is enough space\n-\n-            if (this.cell == null && this.spanX >= spanX && this.spanY >= spanY) {\n-                if (cellXY != null) {\n-                   ...[truncated]

### FN 8: `deep-jit-apache_axis1-java-113-6690`

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Positive-class score: `0.0729`
- Old comment excerpt: @return Iterator The ports specified in the WSDL file
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -2,5 +2,5 @@\n     if (wsdlService == null || wsdlService.getPorts() == null) {\n         return new Vector().iterator();\n     }\n-    return wsdlService.getPorts().values().iterator();\n+    return wsdlService.getPorts().keySet().iterator();\n }

### FN 9: `deep-jit-macalinao_albkit-16-Associations-FirstSentence`

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Positive-class score: `0.0758`
- Old comment excerpt: Checks whether this ChatSection's argument can be parsed as a boolean
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n     public boolean isBoolean() {\n-        return arg.equals("true") || arg.equals("false");\n+        return raw.equals("true") || raw.equals("false");\n     }\n+

### FN 10: `deep-jit-apache_lenya-388-Associations-FirstSentence`

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Positive-class score: `0.0767`
- Old comment excerpt: DOCUMENT ME!
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,7 +1,7 @@\n     public List getAnchorHRefs(boolean duplicate) {\n         if (duplicate) {\n-            return htmlHandler.getAllAHRefs();\n-        } else {\n-            return htmlHandler.getAHRefs();\n+            return this.htmlHandler.getAllAHRefs();\n         }\n+        return this.htmlHandler.getAHRefs();\n     }\n+


## Likely Error Reasons

- Some false positives look like semantically meaningful code changes where the old comment still remains technically acceptable under the Deep-JIT label.
- Some false negatives involve small textual or structural diffs where the inconsistency signal is subtle after truncation to old comment plus code diff.
- The classifier likely benefits from lexical and structural cues, but it does not execute code or reason over full project context.

## Return vs Summary

- Summary remains harder than Return: `True`.
- Return MCC: `0.5988`.
- Summary MCC: `0.3715`.

The Summary subset has lower accuracy, F1, specificity, and MCC than Return for the best v2 model, so the remaining error surface is not uniformly distributed across comment types.
