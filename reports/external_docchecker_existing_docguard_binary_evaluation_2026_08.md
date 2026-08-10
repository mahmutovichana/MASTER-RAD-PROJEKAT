# External DocChecker / Deep-JIT Existing DocGuard Binary Evaluation 2026-08

- Input: `data\external\docchecker_binary_sample_500.jsonl`
- Total records: `500`
- Positive count: `250`
- Negative count: `250`
- Accuracy: `50.40%`
- Precision: `50.20%`
- Recall: `100.00%`
- F1: `66.84%`
- False positives: `248`
- False negatives: `0`
- False positive rate: `99.20%`
- False negative rate: `0.00%`
- Median confidence: `0.1222`
- Average confidence: `0.1353`

## Confusion Matrix

|  | Predicted true | Predicted false |
| --- | ---: | ---: |
| Gold true | 250 | 0 |
| Gold false | 248 | 2 |

## Predicted Label Distribution

- `False`: 2
- `True`: 498

## Predicted Doc Category Distribution

- `workflow_documentation`: 228
- `testing_instructions`: 182
- `model_contract`: 26
- `configuration`: 25
- `architecture_flow`: 19
- `developer_setup`: 10
- `changelog`: 8
- `no_update`: 2

## Predicted Scenario Type Distribution

- `changed_testing_framework`: 153
- `removed_dto_model_field`: 60
- `changed_test_command`: 53
- `added_service_orchestration_flow`: 51
- `changed_validation_max`: 51
- `changelog_worthy_behavior_change`: 23
- `changed_validation_min`: 22
- `changed_enum_values`: 15
- `added_background_job_flow`: 14
- `removed_environment_variable`: 9
- `changed_caching_or_rate_limit_flow`: 9
- `changed_middleware_auth_flow`: 8
- `added_environment_variable`: 7
- `changed_seed_or_setup_flow`: 6
- `removed_endpoint`: 6
- `removed_request_field`: 5
- `changed_default_config_value`: 2
- `changed_background_job_schedule`: 2
- `changed_local_development_flow`: 2
- `docs_already_updated`: 2

## Top False Positives

### deep-jit-Atmosphere_atmosphere-157-ConstrainedReturn-0

- gold docs_update_required: `False`
- predicted docs_update_required: `True`
- predicted scenario: `changed_validation_max`
- predicted category: `workflow_documentation`
- confidence: `0.0749`
- code_diff: --- old_code\n+++ new_code\n@@ -14,7 +14,7 @@\n                 String body = headers.remove(ATMOSPHERE_POST_BODY);\n                 return cometSupport.service(new AtmosphereRequest.Builder()\n                         .headers(headers)\n-                        .method(req.getMethod())\n+                        .method(body != null ? req.getMethod() : "GET...[truncated]
- doc_diff: 

### deep-jit-Atmosphere_atmosphere-542-FirstSentence-0

- gold docs_update_required: `False`
- predicted docs_update_required: `True`
- predicted scenario: `changed_default_config_value`
- predicted category: `workflow_documentation`
- confidence: `0.0941`
- code_diff: --- old_code\n+++ new_code\n@@ -1,4 +1,4 @@\n-    protected DefaultMetaBroadcaster flushCache() {\n+    protected MetaBroadcaster flushCache() {\n         if (cache != null) cache.flushCache();\n         return this;\n     }
- doc_diff: 

### deep-jit-Atmosphere_atmosphere-531-ConstrainedReturn-0

- gold docs_update_required: `False`
- predicted docs_update_required: `True`
- predicted scenario: `removed_environment_variable`
- predicted category: `configuration`
- confidence: `0.0812`
- code_diff: --- old_code\n+++ new_code\n@@ -1,4 +1,7 @@\n     public Action doCometSupport(AtmosphereRequest req, AtmosphereResponse res) throws IOException, ServletException {\n+\n+        if (isDestroyed.get()) return Action.CANCELLED;\n+\n         Action a = null;\n         try {\n             configureRequestResponse(req, res);
- doc_diff: 

### deep-jit-Atmosphere_atmosphere-608-FirstSentence-0

- gold docs_update_required: `False`
- predicted docs_update_required: `True`
- predicted scenario: `changed_caching_or_rate_limit_flow`
- predicted category: `workflow_documentation`
- confidence: `0.1062`
- code_diff: --- old_code\n+++ new_code\n@@ -1,29 +1,32 @@\n     public List<ResourceFilter> create(AbstractMethod am) {\n         LinkedList<ResourceFilter> list = new LinkedList<ResourceFilter>();\n-\n+        Filter f;\n         if (logger.isLoggable(Level.FINE)) {\n             for (Annotation a : am.getAnnotations()) {\n                 logger.log(Level.FINE, "Atmos...[truncated]
- doc_diff: 

### deep-jit-Atmosphere_atmosphere-622-ConstrainedReturn-0

- gold docs_update_required: `False`
- predicted docs_update_required: `True`
- predicted scenario: `changed_caching_or_rate_limit_flow`
- predicted category: `workflow_documentation`
- confidence: `0.1053`
- code_diff: --- old_code\n+++ new_code\n@@ -6,6 +6,10 @@\n             for (Annotation annotation : am.getAnnotations()) {\n                 logger.debug("AtmosphereFilter processing annotation: {}", annotation);\n             }\n+        }\n+\n+        if (am.getMethod() == null) {\n+            return null;\n         }\n \n         if (SuspendResponse.class.isAssignab...[truncated]
- doc_diff: 

### deep-jit-Atmosphere_atmosphere-626-FirstSentence-0

- gold docs_update_required: `False`
- predicted docs_update_required: `True`
- predicted scenario: `removed_dto_model_field`
- predicted category: `workflow_documentation`
- confidence: `0.0861`
- code_diff: --- old_code\n+++ new_code\n@@ -1,5 +1,8 @@\n     public CometSupport defaultCometSupport(final boolean preferBlocking) {\n         if (!preferBlocking && testClassExists(SERVLET_30)) {\n+            if (detectWebSocketPresent().size() > 0) {\n+                return new Servlet30CometSupportWithWebSocket(config);\n+            }\n             return new Ser...[truncated]
- doc_diff: 

### deep-jit-Atmosphere_atmosphere-628-ConstrainedReturn-0

- gold docs_update_required: `False`
- predicted docs_update_required: `True`
- predicted scenario: `added_service_orchestration_flow`
- predicted category: `workflow_documentation`
- confidence: `0.1354`
- code_diff: --- old_code\n+++ new_code\n@@ -6,7 +6,11 @@\n         req.setAttribute(SUPPORT_TRACKABLE, config.getInitParameter(SUPPORT_TRACKABLE));\n \n         try {\n-            return cometSupport.service(req, res);\n+            if (config.getInitParameter(ALLOW_QUERYSTRING_AS_HEADER) != null) {\n+                return cometSupport.service(new AtmosphereRequest.Bu...[truncated]
- doc_diff: 

### deep-jit-Atmosphere_atmosphere-630-FirstSentence-0

- gold docs_update_required: `False`
- predicted docs_update_required: `True`
- predicted scenario: `added_service_orchestration_flow`
- predicted category: `workflow_documentation`
- confidence: `0.1727`
- code_diff: --- old_code\n+++ new_code\n@@ -20,8 +20,9 @@\n \n                     String transport = servletReq.getHeader(X_ATMOSPHERE_TRANSPORT);\n                     if (transport == null) {\n-                        throw new WebApplicationException(new IllegalStateException("Must specify transport using header value "\n-                                + X_ATMOSPHE...[truncated]
- doc_diff: 

### deep-jit-Atmosphere_atmosphere-631-ConstrainedReturn-0

- gold docs_update_required: `False`
- predicted docs_update_required: `True`
- predicted scenario: `added_service_orchestration_flow`
- predicted category: `workflow_documentation`
- confidence: `0.1435`
- code_diff: --- old_code\n+++ new_code\n@@ -19,14 +19,14 @@\n                     }\n \n                     String transport = servletReq.getHeader(X_ATMOSPHERE_TRANSPORT);\n-                    if (transport == null) {\n-                        logger.warn("Must specify transport using header value " + X_ATMOSPHERE_TRANSPORT);\n-                        response.setSta...[truncated]
- doc_diff: 

### deep-jit-Atmosphere_atmosphere-639-FirstSentence-0

- gold docs_update_required: `False`
- predicted docs_update_required: `True`
- predicted scenario: `added_service_orchestration_flow`
- predicted category: `workflow_documentation`
- confidence: `0.1752`
- code_diff: --- old_code\n+++ new_code\n@@ -25,7 +25,11 @@\n \n                 a = cometSupport.service(r, res);\n             } else {\n-                return cometSupport.service(AtmosphereRequest.wrap(req), res);\n+                if (AtmosphereRequest.class.isAssignableFrom(req.getClass())) {\n+                    return cometSupport.service(req, res);\n+         ...[truncated]
- doc_diff: 


## Top False Negatives

None.

## Limitations

This is the first external binary proxy evaluation using code-comment consistency labels. It is not full project-level Markdown documentation update detection.
