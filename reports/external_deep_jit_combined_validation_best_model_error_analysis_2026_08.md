# External Deep-JIT Best Model Error Analysis 2026-08

- Best model: `tfidf_linear_svc`
- Input mode: `old_comment_plus_code_diff`
- Decision/confidence rule: absolute LinearSVC decision margin; not calibrated probability

## Confusion Matrix

- TP: `872`
- FP: `395`
- TN: `1058`
- FN: `581`
- Specificity: `72.81%`
- Balanced accuracy: `66.41%`
- MCC: `0.3310`

## Error Counts By Subset

- `Return`: 531
- `Summary`: 445

## Confidence/Margin Distribution

- Median: `0.4629`
- Mean: `0.5856`
- Min: `0.0001`
- Max: `3.4488`

## Top Error Examples

### deep-jit-SeleniumHQ_selenium-441-FirstSentence-0

- Subset: `Summary`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `1.7148`
- Old comment excerpt: Gets the SOCKS version (4 or 5).
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n-  public String getSocksVersion() {\n+  public Integer getSocksVersion() {\n     return socksVersion;\n   }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-macalinao_albkit-16-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.5867`
- Old comment excerpt: Checks whether this ChatSection's argument can be parsed as a boolean
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n     public boolean isBoolean() {\n-        return arg.equals("true") || arg.equals("false");\n+        return raw.equals("true") || raw.equals("false");\n     }\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_lenya-365-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.5813`
- Old comment excerpt: DOCUMENT ME!
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,5 +1,6 @@\n     public Reader getReader() {\n-        debug("\nContents: " + contentsBuffer.toString());\n+        debug("\nContents: " + this.contentsBuffer.toString());\n \n-        return new StringReader(contentsBuffer.toString());\n+        return new StringReader(this.contentsBuffer.toString());\n     }\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-OpenAPITools_openapi_generator-1903-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `1.4811`
- Old comment excerpt: @return enumString
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,6 @@\n-  public EnumStringEnum getEnumString() {\n-    return enumString;\n+  public String getEnumString() {\n+    if (enumString == null) {\n+      return null;\n+    }\n+    return enumString.value();\n   }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-querydsl_querydsl-443-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `1.4214`
- Old comment excerpt: @return this.equalsIgnoreCase(str)
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public BooleanExpression equalsIgnoreCase(String str) {\n-        return equalsIgnoreCase(StringConstant.create(str));\n+        return equalsIgnoreCase(new StringConstant(str));\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-stanfordnlp_CoreNLP-2074-FirstSentence-0

- Subset: `Summary`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `1.3888`
- Old comment excerpt: Accepts a String that is a sentence end punctuation tag, and rejects everything else.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n   public boolean isSentenceFinalPunctuationTag(String str) {\n-    return sFPunctTagStringAcceptFilter.accept(str);\n+    return sFPunctTagStringAcceptFilter.test(str);\n   }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-kaendfinger_pircbotx-109-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.3642`
- Old comment excerpt: Attempts to establish a DCC CHAT session with a client.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,22 +1,4 @@\n-	public DccChat dccSendChatRequest(User sender, int timeout) throws IOException, SocketTimeoutException {\n-		if (sender == null)\n-			throw new IllegalArgumentException("Can't send chat request to null user");\n-		ServerSocket ss = null;//dccManager.createServerSocket();\n-		ss.setSoTimeout(timeout);\n-		int serverPort = ss.getLocalPort();\n+	public Chat dccSendChatRequ...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_drill-1427-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.3309`
- Old comment excerpt: @return - Single row indicating drop succeeded, raise exception otherwise
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -10,11 +10,19 @@\n       drillSchema = SchemaUtilites.resolveToMutableDrillSchema(defaultSchema, dropTableNode.getSchema());\n     }\n \n-    String tableName = ((SqlDropTable) sqlNode).getName();\n+    String tableName = dropTableNode.getName();\n     if (drillSchema == null) {\n       throw UserException.validationError()\n           .message("Invalid table_name [%s]", tableName)\n   ...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-nickman_qreactor-2-5171

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.2808`
- Old comment excerpt: @return the rollCycle
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n public RollCycle getRollCycle() {\n-    return rollCycle;\n+    return queue.rollCycle();\n }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-nickman_qreactor-3-5172

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.2808`
- Old comment excerpt: @return the wireType
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n public WireType getWireType() {\n-    return wireType;\n+    return queue.wireType();\n }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-google_physical-web-10-839

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.2658`
- Old comment excerpt: @return true if the ranks are equal.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,7 +1,11 @@\n+@Override\n public boolean equals(Object other) {\n+    if (this == other) {\n+        return true;\n+    }\n     if (other instanceof PwPair) {\n         PwPair otherPwPair = (PwPair) other;\n-        return getRank() == otherPwPair.getRank();\n+        return getRank() == otherPwPair.getRank() && mUrlDevice.equals(otherPwPair.mUrlDevice) && mPwsResult.equals(otherPwPai...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-querydsl_querydsl-456-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `1.2425`
- Old comment excerpt: @return this.endsWith(str)
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public BooleanExpression endsWith(String str) {\n-        return endsWith(StringConstant.create(str));\n+        return endsWith(ConstantImpl.create(str));\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-querydsl_querydsl-355-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `1.2355`
- Old comment excerpt: @return this + str
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n     public EString append(String str) {\n-        return append(EString.__create(str));\n+        return append(EStringConst.create(str));\n     }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-LawnchairLauncher_Lawnchair-442-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.2325`
- Old comment excerpt: @return ActivityOptions with remote animations that controls how the window of the opening targets are displayed.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,33 +1,44 @@\n-    public ActivityOptions getActivityLaunchOptions(Launcher launcher, View v) {\n+    public Bundle getActivityLaunchOptions(Launcher launcher, View v) {\n         if (hasControlRemoteAppTransitionPermission()) {\n             try {\n-                RemoteAnimationRunnerCompat runner = new LauncherAnimationRunner(mHandler) {\n+                RemoteAnimationRunnerComp...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-google_physical-web-11-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.2296`
- Old comment excerpt: Check if two PwPairs are equal based on rank.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,7 +1,15 @@\n+  @Override\n   public boolean equals(Object other) {\n+    if (this == other) {\n+      return true;\n+    }\n+\n     if (other instanceof PwPair) {\n       PwPair otherPwPair = (PwPair) other;\n-      return getRank() == otherPwPair.getRank();\n+      return getRank() == otherPwPair.getRank() &&\n+          mUrlDevice.equals(otherPwPair.mUrlDevice) &&\n+          mPwsR...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_lenya-393-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.2047`
- Old comment excerpt: DOCUMENT ME!
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n     public ArrayList getImageSrcs() {\n-        return img_src;\n+        return this.img_src;\n     }\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_lenya-394-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.2047`
- Old comment excerpt: DOCUMENT ME!
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n     public ArrayList getAllImageSrcs() {\n-        return img_src_all;\n+        return this.img_src_all;\n     }\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_lenya-395-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.2047`
- Old comment excerpt: DOCUMENT ME!
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n     public ArrayList getLinkHRefs() {\n-        return link_href;\n+        return this.link_href;\n     }\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_lenya-396-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.2047`
- Old comment excerpt: DOCUMENT ME!
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n     public ArrayList getAllLinkHRefs() {\n-        return link_href_all;\n+        return this.link_href_all;\n     }\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_lenya-397-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.2047`
- Old comment excerpt: DOCUMENT ME!
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n     public ArrayList getAHRefs() {\n-        return a_href;\n+        return this.a_href;\n     }\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_lenya-398-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.2047`
- Old comment excerpt: DOCUMENT ME!
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n     public ArrayList getAllAHRefs() {\n-        return a_href_all;\n+        return this.a_href_all;\n     }\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_drill-1427-FirstSentence-0

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.1880`
- Old comment excerpt: Function resolves the schema and invokes the drop method.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -10,11 +10,19 @@\n       drillSchema = SchemaUtilites.resolveToMutableDrillSchema(defaultSchema, dropTableNode.getSchema());\n     }\n \n-    String tableName = ((SqlDropTable) sqlNode).getName();\n+    String tableName = dropTableNode.getName();\n     if (drillSchema == null) {\n       throw UserException.validationError()\n           .message("Invalid table_name [%s]", tableName)\n   ...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-jmoses_android-smspopup-6-4253

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.1491`
- Old comment excerpt: @return true if a message was removed, false otherwise.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n-public boolean removeActiveMessage() {\n+public int removeActiveMessage() {\n     return removeMessage(currentPage);\n }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-ansell_openrdf-sesame-162-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.1354`
- Old comment excerpt: Encodes a value for use in a URL.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,10 @@\n 	public static String encodeValue(Value value) {\n+		if (value instanceof BNode) {\n+			// SES-2129 special treatment of blank node names to avoid problems with round-tripping.\n+			return ((BNode)value).getID();\n+		}\n+		\n+		// for everything else we just use N-Triples serialization.\n 		return NTriplesUtil.toNTriplesString(value);\n 	}\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-jenkinsci_testlink-plugin-8-4553

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.1207`
- Old comment excerpt: @return the parsed Test Suite or null if no Test Suite was found.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n-public TestSuite getSuite() {\n-    return this.testSuite;\n+public List<TestSuite> getSuite() {\n+    return this.testSuites;\n }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_calcite-977-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.1173`
- Old comment excerpt: @return threshold, default 20
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,3 +1,3 @@\n   protected int getInSubqueryThreshold() {\n-    return 20;\n+    return IN_SUBQUERY_THRESHOLD;\n   }

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-docker_java_docker_java-76-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `1.1151`
- Old comment excerpt: @return a  Link matching the specification
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -4,7 +4,9 @@\n 			final String[] parts = serialized.split(":");\n 			switch (parts.length) {\n 			case 2: {\n-				return new Link(parts[0], parts[1]);\n+				String[] nameSplit = parts[0].split("/");\n+				String[] aliasSplit = parts[1].split("/");\n+				return new Link(nameSplit[nameSplit.length - 1], aliasSplit[aliasSplit.length - 1]);\n 			}\n 			default: {\n 				throw new IllegalArgu...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-sparklemotion_nokogiri-8-ConstrainedReturn-0

- Subset: `Return`
- Raw label: `0`
- Gold: `False`
- Predicted: `True`
- Confidence/margin: `1.1116`
- Old comment excerpt: @return String Local name of this node.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,7 +1,7 @@\n     public String getLocalName(int nodeHandle)\n     {\n-        if(JJK_NEWCODE)\n-        {\n+//        if(JJK_NEWCODE)\n+//        {\n             int id=makeNodeIdentity(nodeHandle);\n             if(NULL==id) return null;\n             Node newnode=(Node)m_nodes.elementAt(id);\n@@ -23,36 +23,36 @@\n                 }\n             }\n             return newname;\n-   ...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-yahoo_fili-1-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.0840`
- Old comment excerpt: Exports current thread's request log object as a JSON string without resetting it.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -2,11 +2,6 @@\n         RequestLog current = RLOG.get();\n         record(new Durations(current.aggregateDurations()));\n         record(new Threads(current.threadIds));\n-        try {\n-            return current.mapper.writeValueAsString(current.info);\n-        } catch (JsonProcessingException jpe) {\n-            String msg = String.format("Exporting mega log line with id: '%s' to ...[truncated]

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

### deep-jit-apache_axis1-java-93-Associations-FirstSentence

- Subset: `Summary`
- Raw label: `1`
- Gold: `True`
- Predicted: `False`
- Confidence/margin: `1.0787`
- Old comment excerpt: Returns the value associated with the named property - or null if not defined/set.
- Code diff excerpt: --- old_code\n+++ new_code\n@@ -1,5 +1,6 @@\n     public Object getProperty(String name) {\n-        if (name != null)\n-            return callProperties.get(name);\n-        return null;\n+        if (name == null || !isPropertySupported(name))\n+            throw new IllegalArgumentException();\n+        return callProperties.get(name);\n     } // getProperty\n+

- [ ] possible label noise
- [ ] insufficient context
- [ ] model error
- [ ] mapping concern

## Limitations

This analysis is for the external code-comment consistency proxy only. It does not measure project-level Markdown documentation patching.
