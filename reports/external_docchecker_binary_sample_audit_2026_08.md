# External DocChecker Binary Sample Audit 2026-08

- Total records: `500`
- Positive count: `250`
- Negative count: `250`

## Label Distribution

- `strong_external_consistent_comment`: 250
- `strong_external_inconsistent_comment`: 250

## Source File Distribution

- `data\external\raw\deep_jit_inconsistency\Return\test.json`: 250
- `data\external\raw\deep_jit_inconsistency\Summary\test.json`: 250

## Split Distribution

- `test`: 500

## Language Distribution

- `java`: 500

## Missing Fields

- `doc_diff`: 250

## Mapping Warnings

None.

## Positive Examples

### deep-jit-2dxgujun_AndroidTagGroup-0-2552

- label_source: `strong_external_inconsistent_comment`
- split: `test`
- source id: `2dxgujun_AndroidTagGroup-0-2552`
- code_diff: --- old_code\n+++ new_code\n@@ -1,13 +1,7 @@\n-protected TagView getInputTag() {\n-    if (isAppendMode) {\n-        final int inputTagIndex = getChildCount() - NUM;\n-        TagView inputTag = (TagView) getChildAt(inputTagIndex);\n-        if (inputTag != null && inputTag.mStat...[truncated]
- doc_diff: --- old_comment\n+++ new_comment\n@@ -1 +1 @@\n-@return The INPUT state tag or null if none.\n+@return the INPUT state tag view or null if not exists

### deep-jit-Atmosphere_atmosphere-54-Associations-FirstSentence

- label_source: `strong_external_inconsistent_comment`
- split: `test`
- source id: `Atmosphere_atmosphere-54-Associations-FirstSentence`
- code_diff: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n-    public HttpServletRequest getRequest() {\n+    public AtmosphereRequest getRequest() {\n         return atmosphereRequest;\n     }\n+
- doc_diff: --- old_comment\n+++ new_comment\n@@ -1 +1 @@\n-Return the associated  HttpServletRequest\n+Return the associated  AtmosphereRequest

### deep-jit-Atmosphere_atmosphere-1-1471

- label_source: `strong_external_inconsistent_comment`
- split: `test`
- source id: `Atmosphere_atmosphere-1-1471`
- code_diff: --- old_code\n+++ new_code\n@@ -2,8 +2,7 @@\n     try {\n         return (AsyncSupport) targetClass.getDeclaredConstructor(new Class[] { AtmosphereConfig.class }).newInstance(config);\n     } catch (final Exception e) {\n-        logger.error(STR, targetClass, e);\n-        logge...[truncated]
- doc_diff: --- old_comment\n+++ new_comment\n@@ -1 +1 @@\n-@return an instance of the specified class\n+@return an instance of the specified class or null if the class cannot be instantiated

### deep-jit-Atmosphere_atmosphere-79-Associations-FirstSentence

- label_source: `strong_external_inconsistent_comment`
- split: `test`
- source id: `Atmosphere_atmosphere-79-Associations-FirstSentence`
- code_diff: --- old_code\n+++ new_code\n@@ -1,3 +1,4 @@\n-    public static MetaBroadcaster metaBroadcaster() {\n+    public static DefaultMetaBroadcaster metaBroadcaster() {\n         return metaBroadcaster;\n     }\n+
- doc_diff: --- old_comment\n+++ new_comment\n@@ -1 +1 @@\n-Return the  org.atmosphere.cpr.MetaBroadcaster\n+Return the  DefaultMetaBroadcaster

### deep-jit-Atmosphere_atmosphere-5-1472

- label_source: `strong_external_inconsistent_comment`
- split: `test`
- source id: `Atmosphere_atmosphere-5-1472`
- code_diff: --- old_code\n+++ new_code\n@@ -1,6 +1,10 @@\n public String getInitParameter(String name) {\n     try {\n-        return framework.getServletConfig().getInitParameter(name);\n+        String value = framework.getServletConfig().getInitParameter(name);\n+        if (value == null...[truncated]
- doc_diff: --- old_comment\n+++ new_comment\n@@ -1 +1 @@\n-@return the list of init params defined in web.xml or application.xml\n+@return the value for the init parameter if defined


## Negative Examples

### deep-jit-Atmosphere_atmosphere-157-ConstrainedReturn-0

- label_source: `strong_external_consistent_comment`
- split: `test`
- source id: `Atmosphere_atmosphere-157-ConstrainedReturn-0`
- code_diff: --- old_code\n+++ new_code\n@@ -14,7 +14,7 @@\n                 String body = headers.remove(ATMOSPHERE_POST_BODY);\n                 return cometSupport.service(new AtmosphereRequest.Builder()\n                         .headers(headers)\n-                        .method(req.getM...[truncated]
- doc_diff: 

### deep-jit-Atmosphere_atmosphere-542-FirstSentence-0

- label_source: `strong_external_consistent_comment`
- split: `test`
- source id: `Atmosphere_atmosphere-542-FirstSentence-0`
- code_diff: --- old_code\n+++ new_code\n@@ -1,4 +1,4 @@\n-    protected DefaultMetaBroadcaster flushCache() {\n+    protected MetaBroadcaster flushCache() {\n         if (cache != null) cache.flushCache();\n         return this;\n     }
- doc_diff: 

### deep-jit-Atmosphere_atmosphere-531-ConstrainedReturn-0

- label_source: `strong_external_consistent_comment`
- split: `test`
- source id: `Atmosphere_atmosphere-531-ConstrainedReturn-0`
- code_diff: --- old_code\n+++ new_code\n@@ -1,4 +1,7 @@\n     public Action doCometSupport(AtmosphereRequest req, AtmosphereResponse res) throws IOException, ServletException {\n+\n+        if (isDestroyed.get()) return Action.CANCELLED;\n+\n         Action a = null;\n         try {\n       ...[truncated]
- doc_diff: 

### deep-jit-Atmosphere_atmosphere-608-FirstSentence-0

- label_source: `strong_external_consistent_comment`
- split: `test`
- source id: `Atmosphere_atmosphere-608-FirstSentence-0`
- code_diff: --- old_code\n+++ new_code\n@@ -1,29 +1,32 @@\n     public List<ResourceFilter> create(AbstractMethod am) {\n         LinkedList<ResourceFilter> list = new LinkedList<ResourceFilter>();\n-\n+        Filter f;\n         if (logger.isLoggable(Level.FINE)) {\n             for (Annot...[truncated]
- doc_diff: 

### deep-jit-Atmosphere_atmosphere-622-ConstrainedReturn-0

- label_source: `strong_external_consistent_comment`
- split: `test`
- source id: `Atmosphere_atmosphere-622-ConstrainedReturn-0`
- code_diff: --- old_code\n+++ new_code\n@@ -6,6 +6,10 @@\n             for (Annotation annotation : am.getAnnotations()) {\n                 logger.debug("AtmosphereFilter processing annotation: {}", annotation);\n             }\n+        }\n+\n+        if (am.getMethod() == null) {\n+      ...[truncated]
- doc_diff: 


## Limitations

This is a code-comment consistency proxy, not full project-level Markdown documentation update detection.
