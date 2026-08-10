# External DocChecker False Positive Audit Queue 2026-08

## Highest-Confidence False Positives

### deep-jit-JodaOrg_joda_time-640-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.2915`
- Predicted doc_category: `testing_instructions`
- Predicted scenario_type: `changed_validation_max`
- Code excerpt:     public int getMaximumValue() {\n        return getField().getMaximumValue(getReadablePartial());\n    }\n
- Comment excerpt: @return the maximum value

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-Atmosphere_atmosphere-673-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.2885`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `added_service_orchestration_flow`
- Code excerpt:     public Action cancelled(AtmosphereRequest req, AtmosphereResponse res)\n            throws IOException, ServletException {\n\n        synchronized (req) {\n            SessionTimeoutSupport.restoreTimeout(req);\n\n            AtmosphereResourceImpl r = null;\n            try {\n                if (trackActiveRequest) {\n                    long l = (Long) req.getAttribute(MAX_INACTIVE);\n                    if (l...[truncated]
- Comment excerpt: All proprietary Comet based  Servlet must invoke the cancelled method when the underlying WebServer detect that the client closed the connection.

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-Netflix_eureka-181-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.2879`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `added_service_orchestration_flow`
- Code excerpt:     private TimerTask getServiceUrlUpdateTask(final String zone) {\n        return new TimerTask() {\n            @Override\n            public void run() {\n                try {\n                    List<String> serviceUrlList = timedGetDiscoveryServiceUrls(zone);\n                    if (serviceUrlList.isEmpty()) {\n                        logger.warn("The service url list is empty");\n                        retu...[truncated]
- Comment excerpt: Gets the task that is responsible for fetching the eureka service Urls.

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-JodaOrg_joda_time-636-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.2756`
- Predicted doc_category: `testing_instructions`
- Predicted scenario_type: `changed_validation_max`
- Code excerpt:     public int getMaximumValue(PartialInstant instant, int[] values) {\n        return getWrappedField().getMaximumValue(instant, values) + 1;\n    }\n
- Comment excerpt: @return the maximum value

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-Netflix_eureka-351-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.2712`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `added_service_orchestration_flow`
- Code excerpt:     private void getAndStoreFullRegistry() throws Throwable {\n        long currentUpdateGeneration = fetchRegistryGeneration.get();\n\n        logger.info("Getting all instance registry info from the eureka server");\n\n        Applications apps = null;\n        if (shouldUseExperimentalTransport()) {\n            EurekaHttpResponse<Applications> httpResponse = clientConfig.getRegistryRefreshSingleVipAddress() == nu...[truncated]
- Comment excerpt: Gets the full registry information from the eureka server and stores it locally.

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-JodaOrg_joda_time-467-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.2562`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `changed_validation_max`
- Code excerpt:     public String toString() {\n        long millis = getMillis();\n        StringBuffer buf = new StringBuffer();\n        buf.append("PT");\n        FormatUtils.appendUnpaddedInteger(buf, millis / 1000);\n        long part = Math.abs(millis % 1000);\n        if (part > 0) {\n            buf.append('.');\n            FormatUtils.appendPaddedInteger(buf, part, 3);\n        }\n        buf.append('S');\n        return ...[truncated]
- Comment excerpt: @return the value as an ISO8601 string

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-JodaOrg_joda_time-994-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.2330`
- Predicted doc_category: `testing_instructions`
- Predicted scenario_type: `changed_validation_max`
- Code excerpt:         public YearMonth addWrapFieldToCopy(int valueToAdd) {\n            int[] newValues = iBase.getValues();\n            newValues = getField().addWrapField(iBase, iFieldIndex, newValues, valueToAdd);\n            return new YearMonth(iBase, newValues);\n        }\n
- Comment excerpt: Adds to the value of this field in a copy of this YearMonth wrapping within this field if the maximum value is reached.

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-JodaOrg_joda_time-979-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.2309`
- Predicted doc_category: `testing_instructions`
- Predicted scenario_type: `changed_testing_framework`
- Code excerpt:     public Object clone() {\n        throw ExceptionUtils.unsupportedInGwt();\n//        try {\n//            return super.clone();\n//        } catch (CloneNotSupportedException ex) {\n//            throw new InternalError("Clone error");\n//        }\n    }\n
- Comment excerpt: @return a clone of this object.

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-LawnchairLauncher_Lawnchair-42-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.2252`
- Predicted doc_category: `changelog`
- Predicted scenario_type: `removed_dto_model_field`
- Code excerpt:     private boolean onTouchForwarded(MotionEvent srcEvent) {\n        final View src = mSrcIcon;\n\n        final DeepShortcutsContainer dst = mLauncher.getOpenShortcutsContainer();\n        if (dst == null) {\n            return false;\n        }\n        if (!dst.isLaidOut()) {\n            return true;\n        }\n\n        // Convert event to destination-local coordinates.\n        final MotionEvent dstEvent = Mo...[truncated]
- Comment excerpt: @return true to continue forwarding motion events, false to cancel

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-JodaOrg_joda_time-979-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.2245`
- Predicted doc_category: `testing_instructions`
- Predicted scenario_type: `changed_testing_framework`
- Code excerpt:     public Object clone() {\n        throw ExceptionUtils.unsupportedInGwt();\n//        try {\n//            return super.clone();\n//        } catch (CloneNotSupportedException ex) {\n//            throw new InternalError("Clone error");\n//        }\n    }\n
- Comment excerpt: Clone this object.

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

## Median-Confidence False Positives

### deep-jit-OpenAPITools_openapi_generator-2540-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.1223`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `added_service_orchestration_flow`
- Code excerpt:   public Order placeOrder(Order body) throws ApiException {\n    ApiResponse<Order> resp = placeOrderWithHttpInfo(body);\n    return resp.getData();\n  }\n
- Comment excerpt: Place an order for a pet

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-JodaOrg_joda_time-1058-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.1222`
- Predicted doc_category: `testing_instructions`
- Predicted scenario_type: `changed_validation_max`
- Code excerpt:     public String print(ReadablePartial partial) {\n        StringBuilder builder = new StringBuilder(requirePrinter().estimatePrintedLength());\n        try {\n            printTo(builder, partial);\n        } catch (IOException e) {\n            // StringBuilder does not throw IOException\n        }\n        return builder.toString();\n    }\n
- Comment excerpt: Prints a ReadablePartial to a new String.

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-Netflix_eureka-360-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.1221`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `changelog_worthy_behavior_change`
- Code excerpt:     public EurekaClient getEurekaClient() {\n        return eurekaClient;\n    }\n
- Comment excerpt: Get the  EurekaClient implementation.

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-JodaOrg_joda_time-1015-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.1206`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `changed_validation_min`
- Code excerpt:     public static DateTimeFormatter time() {\n        return Constants.t;\n    }\n
- Comment excerpt: Returns a formatter for a two digit hour of day, two digit minute of hour, two digit second of minute, three digit fraction of second, and time zone offset (HH:mm:ss.SSSZZ).

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-JodaOrg_joda_time-786-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.1205`
- Predicted doc_category: `testing_instructions`
- Predicted scenario_type: `changed_testing_framework`
- Code excerpt:     public static DateTimeFieldType weekyear() {\n        return WEEKYEAR_TYPE;\n    }\n
- Comment excerpt: Get the year of a week based year field type.

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-JodaOrg_joda_time-553-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.1201`
- Predicted doc_category: `testing_instructions`
- Predicted scenario_type: `changed_testing_framework`
- Code excerpt:     public boolean undoChanges(Object savedState) {\n        if (savedState instanceof SavedState) {\n            if (((SavedState)savedState).revertState(this)) {\n                iSavedState = savedState;\n                return true;\n            }\n        }\n        return false;\n    }\n
- Comment excerpt: Undos any changes that were made to this bucket since the given state was saved.

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-JodaOrg_joda_time-903-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.1197`
- Predicted doc_category: `testing_instructions`
- Predicted scenario_type: `changed_testing_framework`
- Code excerpt:     public PeriodFormatterBuilder appendSeparator(String text, String finalText) {\n        return appendSeparator(text, finalText, null, true, true);\n    }\n
- Comment excerpt: @return this PeriodFormatterBuilder

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-OpenAPITools_openapi_generator-1910-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.1195`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `changed_test_command`
- Code excerpt:   public Boolean fakeOuterBooleanSerialize(Boolean body) throws ApiException {\n    return fakeOuterBooleanSerializeWithHttpInfo(body).getData();\n      }\n
- Comment excerpt: Test serialization of outer boolean types

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-OpenAPITools_openapi_generator-1795-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.1192`
- Predicted doc_category: `architecture_flow`
- Predicted scenario_type: `changed_test_command`
- Code excerpt:   public User getUserByName (String username) throws ApiException {\n    Object postBody = null;\n    byte[] postBinaryBody = null;\n    \n     // verify the required parameter 'username' is set\n     if (username == null) {\n        throw new ApiException(400, "Missing the required parameter 'username' when calling getUserByName");\n     }\n     \n    // create path and map variables\n    String path = "/user/{usern...[truncated]
- Comment excerpt: Get user by user name

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-JodaOrg_joda_time-1008-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.1184`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `changed_validation_max`
- Code excerpt:     public boolean equals(Object obj) {\n        if (this == obj) {\n            return true;\n        }\n        if (obj != null && getClass() == obj.getClass()) {\n            BasicChronology chrono = (BasicChronology) obj;\n            return getMinimumDaysInFirstWeek() == chrono.getMinimumDaysInFirstWeek() &&\n                    getZone().equals(chrono.getZone());\n        }\n        return false;\n    }\n
- Comment excerpt: @return true if equal

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

## Lowest-Confidence False Positives

### deep-jit-OpenAPITools_openapi_generator-2152-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.0688`
- Predicted doc_category: `architecture_flow`
- Predicted scenario_type: `changed_middleware_auth_flow`
- Code excerpt:     public Mono<Client> testClientModel(Client body) throws RestClientException {\n        Object postBody = body;\n        \n        // verify the required parameter 'body' is set\n        if (body == null) {\n            throw new HttpClientErrorException(HttpStatus.BAD_REQUEST, "Missing the required parameter 'body' when calling testClientModel");\n        }\n        \n        String path = UriComponentsBuilder.fr...[truncated]
- Comment excerpt: To test \&quot;client\&quot; model

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-Atmosphere_atmosphere-157-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.0749`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `changed_validation_max`
- Code excerpt:     public Action doCometSupport(HttpServletRequest req, HttpServletResponse res)\n            throws IOException, ServletException {\n        req.setAttribute(BROADCASTER_FACTORY, broadcasterFactory);\n        req.setAttribute(PROPERTY_USE_STREAM, useStreamForFlushingComments);\n        req.setAttribute(BROADCASTER_CLASS, broadcasterClassName);\n        req.setAttribute(SUPPORT_TRACKABLE, config.getInitParameter(SUP...[truncated]
- Comment excerpt: @return an  Action

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-JPressProjects_jpress-3-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.0789`
- Predicted doc_category: `configuration`
- Predicted scenario_type: `changed_testing_framework`
- Code excerpt: 	public static String moveFile(UploadFile uploadFile) {\n		if (uploadFile == null)\n			return null;\n\n		File file = uploadFile.getFile();\n		if (!file.exists()) {\n			return null;\n		}\n\n		String webRoot = PathKit.getWebRootPath();\n\n		String uuid = UUID.randomUUID().toString().replace("-", "");\n\n		StringBuilder newFileName = new StringBuilder(webRoot).append(File.separator).append("attachment")\n				.append(Fil...[truncated]
- Comment excerpt: @return new file relative path

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-HoraApps_LeafPic-13-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.0792`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `removed_endpoint`
- Code excerpt:   private static ArrayList<Uri> getTreeUris(Context context) {\n	ArrayList<Uri> uris = new ArrayList<Uri>();\n\n	Uri uri1 = getSharedPreferenceUri(context, R.string.preference_internal_uri_extsdcard_photos);\n	if (uri1 != null) uris.add(uri1);\n\n	return uris;\n  }\n
- Comment excerpt: @return The tree URIs.

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-JodaOrg_joda_time-691-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.0803`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `changed_testing_framework`
- Code excerpt:     public DurationType getDurationType(Object object, boolean precise) {\n        ReadableTimePeriod period = (ReadableTimePeriod) object;\n        if (precise) {\n            if (period.getDurationType().isPrecise()) {\n                return period.getDurationType();\n            } else {\n                return DurationType.getPreciseAllType();\n            }\n        }\n        return period.getDurationType();\n...[truncated]
- Comment excerpt: Selects a suitable duration type for the given object.

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-Atmosphere_atmosphere-531-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.0812`
- Predicted doc_category: `configuration`
- Predicted scenario_type: `removed_environment_variable`
- Code excerpt:     public Action doCometSupport(AtmosphereRequest req, AtmosphereResponse res) throws IOException, ServletException {\n\n        if (isDestroyed.get()) return Action.CANCELLED;\n\n        Action a = null;\n        try {\n            configureRequestResponse(req, res);\n            a = asyncSupport.service(req, res);\n        } catch (IllegalStateException ex) {\n            boolean isJBoss = ex.getMessage().startsWi...[truncated]
- Comment excerpt: @return an  Action

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-OpenAPITools_openapi_generator-2007-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.0817`
- Predicted doc_category: `architecture_flow`
- Predicted scenario_type: `removed_request_field`
- Code excerpt:     public ApiResponse<Void> createXmlItemWithHttpInfo(XmlItem xmlItem) throws ApiException {\n        okhttp3.Call localVarCall = createXmlItemValidateBeforeCall(xmlItem, null, null);\n        return localVarApiClient.execute(localVarCall);\n    }\n
- Comment excerpt: creates an XmlItem this route creates an XmlItem

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-OpenAPITools_openapi_generator-2545-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.0841`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `changed_testing_framework`
- Code excerpt:   public List<Pet> findPetsByTags(List<String> tags) throws ApiException {\n    Call call = findPetsByTagsCall(tags);\n    Type returnType = new TypeToken<List<Pet>>(){}.getType();\n    return apiClient.execute(call, returnType);\n  }\n
- Comment excerpt: Finds Pets by tags

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-JodaOrg_joda_time-644-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.0842`
- Predicted doc_category: `workflow_documentation`
- Predicted scenario_type: `changed_testing_framework`
- Code excerpt:         public TimeOfDay setCopy(int value) {\n            int[] newValues = iTimeOfDay.getValues();\n            newValues = getField().set(iTimeOfDay, iFieldIndex, newValues, value);\n            return new TimeOfDay(iTimeOfDay, newValues);\n        }\n
- Comment excerpt: @return a copy of the TimeOfDay with the field value changed

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

### deep-jit-JodaOrg_joda_time-713-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw label: `0`
- Mapped label: `False`
- Predicted label: `True`
- Confidence: `0.0853`
- Predicted doc_category: `configuration`
- Predicted scenario_type: `changed_testing_framework`
- Code excerpt:     public Property weekOfWeekyear() {\n        return new Property(this, getChronology().weekOfWeekyear());\n    }\n
- Comment excerpt: @return the week of a week based year property

- [ ] true false positive
- [ ] actually looks inconsistent
- [ ] label noise
- [ ] mapping bug
- [ ] insufficient context
- [ ] uncertain

