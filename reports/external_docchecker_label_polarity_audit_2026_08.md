# External DocChecker / Deep-JIT Label Polarity Audit 2026-08

## Summary

- Processed sample: `data/external/docchecker_binary_sample_500.jsonl`
- Raw files used: `data\external\raw\deep_jit_inconsistency\Return\test.json`, `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw label column used: `label`
- Raw label values observed in sample: `0`=250, `1`=250
- Mapping used by adapter: raw `1` -> `docs_update_required=true`; raw `0` -> `docs_update_required=false`.
- Repository evidence: Deep-JIT is explicitly an inconsistency detection dataset; DocChecker says its Just-In-Time task determines whether a comment is semantically out of sync with code and returns `Inconsistent!` or `Consistent!`.
- Documentation caveat: the GitHub README pages confirm the task semantics, but the Deep-JIT README does not explicitly define the numeric polarity of the downloaded `label` field.
- Current certainty: polarity is plausible and the sampled examples are consistent with `1=inconsistent/update-required`, `0=consistent/no-update`, but numeric polarity should still be manually verified against the paper or original preprocessing code before thesis-level claims.
- Signs of reversal: no obvious reversal in sampled examples; raw label `1` examples usually show old comments updated to match code changes, while raw label `0` examples usually keep the same comment.

Sources: https://github.com/panthap2/deep-jit-inconsistency-detection and https://github.com/FSoft-AI4Code/DocChecker

## Raw Positive Examples

### deep-jit-2dxgujun_AndroidTagGroup-0-2552

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw id: `2dxgujun_AndroidTagGroup-0-2552`
- Raw label: `1`
- Mapped docs_update_required: `True`
- Old code excerpt: protected TagView getInputTag() {\n    if (isAppendMode) {\n        final int inputTagIndex = getChildCount() - NUM;\n        TagView inputTag = (TagView) getChildAt(inputTagIndex);\n        if (inputTag != null && inputTag.mState == TagView.STATE_INPUT) {\n            return inputTag;\n        } else {\n            return null;\n        }\n    } else {\n        return null;\n    }\n}
- New code excerpt: public String getInputTag() {\n    final TagView inputTagView = getInputTagView();\n    if (inputTagView != null) {\n        return inputTagView.getText().toString();\n    }\n    return null;\n}
- Old comment excerpt: @return The INPUT state tag or null if none.
- New comment excerpt: @return the INPUT state tag view or null if not exists

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-54-Associations-FirstSentence

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw id: `Atmosphere_atmosphere-54-Associations-FirstSentence`
- Raw label: `1`
- Mapped docs_update_required: `True`
- Old code excerpt:     public HttpServletRequest getRequest() {\n        return atmosphereRequest;\n    }\n
- New code excerpt:     public AtmosphereRequest getRequest() {\n        return atmosphereRequest;\n    }\n\n
- Old comment excerpt: Return the associated  HttpServletRequest
- New comment excerpt: Return the associated  AtmosphereRequest

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-1-1471

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw id: `Atmosphere_atmosphere-1-1471`
- Raw label: `1`
- Mapped docs_update_required: `True`
- Old code excerpt: public AsyncSupport newCometSupport(final Class<? extends AsyncSupport> targetClass) {\n    try {\n        return (AsyncSupport) targetClass.getDeclaredConstructor(new Class[] { AtmosphereConfig.class }).newInstance(config);\n    } catch (final Exception e) {\n        logger.error(STR, targetClass, e);\n        logger.error(STR);\n        return new BlockingIOCometSupport(config);\n    }\n}
- New code excerpt: public AsyncSupport newCometSupport(final Class<? extends AsyncSupport> targetClass) {\n    try {\n        return (AsyncSupport) targetClass.getDeclaredConstructor(new Class[] { AtmosphereConfig.class }).newInstance(config);\n    } catch (final Exception e) {\n        logger.warn(STR, targetClass, e);\n        return null;\n    }\n}
- Old comment excerpt: @return an instance of the specified class
- New comment excerpt: @return an instance of the specified class or null if the class cannot be instantiated

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-79-Associations-FirstSentence

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw id: `Atmosphere_atmosphere-79-Associations-FirstSentence`
- Raw label: `1`
- Mapped docs_update_required: `True`
- Old code excerpt:     public static MetaBroadcaster metaBroadcaster() {\n        return metaBroadcaster;\n    }\n
- New code excerpt:     public static DefaultMetaBroadcaster metaBroadcaster() {\n        return metaBroadcaster;\n    }\n\n
- Old comment excerpt: Return the  org.atmosphere.cpr.MetaBroadcaster
- New comment excerpt: Return the  DefaultMetaBroadcaster

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-5-1472

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw id: `Atmosphere_atmosphere-5-1472`
- Raw label: `1`
- Mapped docs_update_required: `True`
- Old code excerpt: public String getInitParameter(String name) {\n    try {\n        return framework.getServletConfig().getInitParameter(name);\n    } catch (Throwable ex) {\n        return null;\n    }\n}
- New code excerpt: public String getInitParameter(String name) {\n    try {\n        String value = framework.getServletConfig().getInitParameter(name);\n        if (value == null && useServletContextParameters) {\n            value = framework.getServletContext().getInitParameter(name);\n        }\n        return value;\n    } catch (Throwable ex) {\n        return null;\n    }\n}
- Old comment excerpt: @return the list of init params defined in web.xml or application.xml
- New comment excerpt: @return the value for the init parameter if defined

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-857-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw id: `Atmosphere_atmosphere-857-FirstSentence-0`
- Raw label: `1`
- Mapped docs_update_required: `True`
- Old code excerpt:     protected WebSocket doWebSocketConnect(final HttpServletRequest request, final String protocol) {\n        logger.info("WebSocket upgrade requested");\n\n        return new WebSocket() {\n            private WebSocketProcessor webSocketProcessor;\n\n            @Override\n            public void onConnect(WebSocket.Outbound outbound) {\n                webSocketProcessor = new WebSocketProcessor(AtmosphereServlet...[truncated]
- New code excerpt:     public WebSocket doWebSocketConnect(final HttpServletRequest request, final String protocol) {\n        logger.info("WebSocket upgrade requested");\n\n        return new JettyWebSocketListener(request,this);\n    }\n
- Old comment excerpt: Jetty 7 and up WebSocket support.
- New comment excerpt: Jetty 7.2 & 8.0.0-M1/M2and up WebSocket support.

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-54-3693

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw id: `Atmosphere_atmosphere-54-3693`
- Raw label: `1`
- Mapped docs_update_required: `True`
- Old code excerpt: public HttpServletRequest getRequest() {\n    return atmosphereRequest;\n}
- New code excerpt: public AtmosphereRequest getRequest() {\n    return atmosphereRequest;\n}
- Old comment excerpt: @return the associated {@link HttpServletRequest}
- New comment excerpt: @return the associated {@link AtmosphereRequest}

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-859-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw id: `Atmosphere_atmosphere-859-FirstSentence-0`
- Raw label: `1`
- Mapped docs_update_required: `True`
- Old code excerpt:     public WebSocket doWebSocketConnect(final HttpServletRequest request, final String protocol) {\n        logger.info("WebSocket upgrade requested");\n\n        return new JettyWebSocketHandler(request,this, webSocketProcessorClassName);\n    }\n
- New code excerpt:     protected WebSocket doWebSocketConnect(final HttpServletRequest request, final String protocol) {\n        logger.info("WebSocket upgrade requested");\n\n        return new WebSocket() {\n            private WebSocketProcessor webSocketProcessor;\n\n            @Override\n            public void onConnect(WebSocket.Outbound outbound) {\n                webSocketProcessor = new WebSocketProcessor(AtmosphereServlet...[truncated]
- Old comment excerpt: Jetty 7.2 & 8.0.0-M1/M2and up WebSocket support.
- New comment excerpt: Jetty 7 and up WebSocket support.

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-6-1473

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw id: `Atmosphere_atmosphere-6-1473`
- Raw label: `1`
- Mapped docs_update_required: `True`
- Old code excerpt: public String getInitParameter(String name) {\n    try {\n        return framework.getServletConfig().getInitParameter(name);\n    } catch (Throwable ex) {\n        return null;\n    }\n}
- New code excerpt: public String getInitParameter(String name) {\n    try {\n        String value = framework.getServletConfig().getInitParameter(name);\n        if (value == null) {\n            value = framework.getServletContext().getInitParameter(name);\n        }\n        return value;\n    } catch (Throwable ex) {\n        return null;\n    }\n}
- Old comment excerpt: @return the list of init params defined in web.xml or application.xml
- New comment excerpt: @return the value for the init parameter if defined

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-861-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw id: `Atmosphere_atmosphere-861-FirstSentence-0`
- Raw label: `1`
- Mapped docs_update_required: `True`
- Old code excerpt:     public Action doCometSupport(AtmosphereRequest req, AtmosphereResponse res) throws IOException, ServletException {\n        req.setAttribute(BROADCASTER_FACTORY, broadcasterFactory);\n        req.setAttribute(PROPERTY_USE_STREAM, useStreamForFlushingComments);\n        req.setAttribute(BROADCASTER_CLASS, broadcasterClassName);\n        req.setAttribute(ATMOSPHERE_CONFIG, config);\n\n        Action a = null;\n    ...[truncated]
- New code excerpt:     public Action doCometSupport(AtmosphereRequest req, AtmosphereResponse res) throws IOException, ServletException {\n        req.setAttribute(BROADCASTER_FACTORY, broadcasterFactory);\n        req.setAttribute(PROPERTY_USE_STREAM, useStreamForFlushingComments);\n        req.setAttribute(BROADCASTER_CLASS, broadcasterClassName);\n        req.setAttribute(ATMOSPHERE_CONFIG, config);\n\n        Action a = null;\n    ...[truncated]
- Old comment excerpt: Invoke the proprietary  CometSupport
- New comment excerpt: Invoke the proprietary  AsyncSupport

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise


## Raw Negative Examples

### deep-jit-Atmosphere_atmosphere-157-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw id: `Atmosphere_atmosphere-157-ConstrainedReturn-0`
- Raw label: `0`
- Mapped docs_update_required: `False`
- Old code excerpt:     public Action doCometSupport(HttpServletRequest req, HttpServletResponse res)\n            throws IOException, ServletException {\n        req.setAttribute(BROADCASTER_FACTORY, broadcasterFactory);\n        req.setAttribute(PROPERTY_USE_STREAM, useStreamForFlushingComments);\n        req.setAttribute(BROADCASTER_CLASS, broadcasterClassName);\n        req.setAttribute(SUPPORT_TRACKABLE, config.getInitParameter(SUP...[truncated]
- New code excerpt:     public Action doCometSupport(HttpServletRequest req, HttpServletResponse res)\n            throws IOException, ServletException {\n        req.setAttribute(BROADCASTER_FACTORY, broadcasterFactory);\n        req.setAttribute(PROPERTY_USE_STREAM, useStreamForFlushingComments);\n        req.setAttribute(BROADCASTER_CLASS, broadcasterClassName);\n        req.setAttribute(SUPPORT_TRACKABLE, config.getInitParameter(SUP...[truncated]
- Old comment excerpt: @return an  Action
- New comment excerpt: @return an  Action

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-542-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw id: `Atmosphere_atmosphere-542-FirstSentence-0`
- Raw label: `0`
- Mapped docs_update_required: `False`
- Old code excerpt:     protected DefaultMetaBroadcaster flushCache() {\n        if (cache != null) cache.flushCache();\n        return this;\n    }\n
- New code excerpt:     protected MetaBroadcaster flushCache() {\n        if (cache != null) cache.flushCache();\n        return this;\n    }\n
- Old comment excerpt: Flush the cached messages.
- New comment excerpt: Flush the cached messages.

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-531-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw id: `Atmosphere_atmosphere-531-ConstrainedReturn-0`
- Raw label: `0`
- Mapped docs_update_required: `False`
- Old code excerpt:     public Action doCometSupport(AtmosphereRequest req, AtmosphereResponse res) throws IOException, ServletException {\n        Action a = null;\n        try {\n            configureRequestResponse(req, res);\n            a = asyncSupport.service(req, res);\n        } catch (IllegalStateException ex) {\n            boolean isJBoss = ex.getMessage().startsWith("JBoss failed");\n            if (ex.getMessage() != null ...[truncated]
- New code excerpt:     public Action doCometSupport(AtmosphereRequest req, AtmosphereResponse res) throws IOException, ServletException {\n\n        if (isDestroyed.get()) return Action.CANCELLED;\n\n        Action a = null;\n        try {\n            configureRequestResponse(req, res);\n            a = asyncSupport.service(req, res);\n        } catch (IllegalStateException ex) {\n            boolean isJBoss = ex.getMessage().startsWi...[truncated]
- Old comment excerpt: @return an  Action
- New comment excerpt: @return an  Action

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-608-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw id: `Atmosphere_atmosphere-608-FirstSentence-0`
- Raw label: `0`
- Mapped docs_update_required: `False`
- Old code excerpt:     public List<ResourceFilter> create(AbstractMethod am) {\n        LinkedList<ResourceFilter> list = new LinkedList<ResourceFilter>();\n\n        if (logger.isLoggable(Level.FINE)) {\n            for (Annotation a : am.getAnnotations()) {\n                logger.log(Level.FINE, "AtmosphereFilter processing annotation: " + a);\n            }\n        }\n\n        if (am.isAnnotationPresent(Broadcast.class)) {\n\n   ...[truncated]
- New code excerpt:     public List<ResourceFilter> create(AbstractMethod am) {\n        LinkedList<ResourceFilter> list = new LinkedList<ResourceFilter>();\n        Filter f;\n        if (logger.isLoggable(Level.FINE)) {\n            for (Annotation a : am.getAnnotations()) {\n                logger.log(Level.FINE, "AtmosphereFilter processing annotation: " + a);\n            }\n        }\n\n        if (SuspendResponse.class.isAssignab...[truncated]
- Old comment excerpt: Create a  ResourceFilter which contains the information about the annotation being processed.
- New comment excerpt: Create a  ResourceFilter which contains the information about the annotation being processed.

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-622-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw id: `Atmosphere_atmosphere-622-ConstrainedReturn-0`
- Raw label: `0`
- Mapped docs_update_required: `False`
- Old code excerpt:     public List<ResourceFilter> create(AbstractMethod am) {\n        LinkedList<ResourceFilter> list = new LinkedList<ResourceFilter>();\n        Filter f;\n\n        if (logger.isDebugEnabled()) {\n            for (Annotation annotation : am.getAnnotations()) {\n                logger.debug("AtmosphereFilter processing annotation: {}", annotation);\n            }\n        }\n\n        if (SuspendResponse.class.isAss...[truncated]
- New code excerpt:     public List<ResourceFilter> create(AbstractMethod am) {\n        LinkedList<ResourceFilter> list = new LinkedList<ResourceFilter>();\n        Filter f;\n\n        if (logger.isDebugEnabled()) {\n            for (Annotation annotation : am.getAnnotations()) {\n                logger.debug("AtmosphereFilter processing annotation: {}", annotation);\n            }\n        }\n\n        if (am.getMethod() == null) {\n...[truncated]
- Old comment excerpt: @return a List of  ResourceFilter to invoke.
- New comment excerpt: @return a List of  ResourceFilter to invoke.

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-626-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw id: `Atmosphere_atmosphere-626-FirstSentence-0`
- Raw label: `0`
- Mapped docs_update_required: `False`
- Old code excerpt:     public CometSupport defaultCometSupport(final boolean preferBlocking) {\n        if (!preferBlocking && testClassExists(SERVLET_30)) {\n            return new Servlet30CometSupport(config);\n        } else {\n            return new BlockingIOCometSupport(config);\n        }\n    }\n
- New code excerpt:     public CometSupport defaultCometSupport(final boolean preferBlocking) {\n        if (!preferBlocking && testClassExists(SERVLET_30)) {\n            if (detectWebSocketPresent().size() > 0) {\n                return new Servlet30CometSupportWithWebSocket(config);\n            }\n            return new Servlet30CometSupport(config);\n        } else {\n            return new BlockingIOCometSupport(config);\n        ...[truncated]
- Old comment excerpt: This method is used to determine the default CometSupport if all else fails
- New comment excerpt: This method is used to determine the default CometSupport if all else fails

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-628-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw id: `Atmosphere_atmosphere-628-ConstrainedReturn-0`
- Raw label: `0`
- Mapped docs_update_required: `False`
- Old code excerpt:     public Action doCometSupport(HttpServletRequest req, HttpServletResponse res)\n            throws IOException, ServletException {\n        req.setAttribute(BROADCASTER_FACTORY, broadcasterFactory);\n        req.setAttribute(PROPERTY_USE_STREAM, useStreamForFlushingComments);\n        req.setAttribute(BROADCASTER_CLASS, broadcasterClassName);\n        req.setAttribute(SUPPORT_TRACKABLE, config.getInitParameter(SUP...[truncated]
- New code excerpt:     public Action doCometSupport(HttpServletRequest req, HttpServletResponse res)\n            throws IOException, ServletException {\n        req.setAttribute(BROADCASTER_FACTORY, broadcasterFactory);\n        req.setAttribute(PROPERTY_USE_STREAM, useStreamForFlushingComments);\n        req.setAttribute(BROADCASTER_CLASS, broadcasterClassName);\n        req.setAttribute(SUPPORT_TRACKABLE, config.getInitParameter(SUP...[truncated]
- Old comment excerpt: @return an  Action
- New comment excerpt: @return an  Action

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-630-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw id: `Atmosphere_atmosphere-630-FirstSentence-0`
- Raw label: `0`
- Mapped docs_update_required: `False`
- Old code excerpt:         public ContainerResponse filter(final ContainerRequest request, final ContainerResponse response) {\n            if (response.getMappedThrowable() != null) {\n                return response;\n            }\n\n            AtmosphereResource<HttpServletRequest, HttpServletResponse> r =\n                    (AtmosphereResource<HttpServletRequest, HttpServletResponse>) servletReq\n                            .ge...[truncated]
- New code excerpt:         public ContainerResponse filter(final ContainerRequest request, final ContainerResponse response) {\n            if (response.getMappedThrowable() != null) {\n                return response;\n            }\n\n            AtmosphereResource<HttpServletRequest, HttpServletResponse> r =\n                    (AtmosphereResource<HttpServletRequest, HttpServletResponse>) servletReq\n                            .ge...[truncated]
- Old comment excerpt: Configure the  AtmosphereResourceEvent state (suspend, resume, broadcast) based on the annotation the web application has used.
- New comment excerpt: Configure the  AtmosphereResourceEvent state (suspend, resume, broadcast) based on the annotation the web application has used.

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-631-ConstrainedReturn-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Return\test.json`
- Raw id: `Atmosphere_atmosphere-631-ConstrainedReturn-0`
- Raw label: `0`
- Mapped docs_update_required: `False`
- Old code excerpt:         public ContainerResponse filter(final ContainerRequest request, final ContainerResponse response) {\n            if (response.getMappedThrowable() != null) {\n                return response;\n            }\n\n            AtmosphereResource<HttpServletRequest, HttpServletResponse> r =\n                    (AtmosphereResource<HttpServletRequest, HttpServletResponse>) servletReq\n                            .ge...[truncated]
- New code excerpt:         public ContainerResponse filter(final ContainerRequest request, final ContainerResponse response) {\n            if (response.getMappedThrowable() != null) {\n                return response;\n            }\n\n            AtmosphereResource<HttpServletRequest, HttpServletResponse> r =\n                    (AtmosphereResource<HttpServletRequest, HttpServletResponse>) servletReq\n                            .ge...[truncated]
- Old comment excerpt: @return the  ContainerResponse
- New comment excerpt: @return the  ContainerResponse

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

### deep-jit-Atmosphere_atmosphere-639-FirstSentence-0

- Raw source file: `data\external\raw\deep_jit_inconsistency\Summary\test.json`
- Raw id: `Atmosphere_atmosphere-639-FirstSentence-0`
- Raw label: `0`
- Mapped docs_update_required: `False`
- Old code excerpt:     public Action doCometSupport(AtmosphereRequest req, AtmosphereResponse res) throws IOException, ServletException {\n        req.setAttribute(BROADCASTER_FACTORY, broadcasterFactory);\n        req.setAttribute(PROPERTY_USE_STREAM, useStreamForFlushingComments);\n        req.setAttribute(BROADCASTER_CLASS, broadcasterClassName);\n        req.setAttribute(ATMOSPHERE_CONFIG, config);\n\n        AtmosphereRequest r = ...[truncated]
- New code excerpt:     public Action doCometSupport(AtmosphereRequest req, AtmosphereResponse res) throws IOException, ServletException {\n        req.setAttribute(BROADCASTER_FACTORY, broadcasterFactory);\n        req.setAttribute(PROPERTY_USE_STREAM, useStreamForFlushingComments);\n        req.setAttribute(BROADCASTER_CLASS, broadcasterClassName);\n        req.setAttribute(ATMOSPHERE_CONFIG, config);\n\n        AtmosphereRequest r = ...[truncated]
- Old comment excerpt: Invoke the proprietary  CometSupport
- New comment excerpt: Invoke the proprietary  CometSupport

- [ ] mapping looks correct
- [ ] mapping questionable
- [ ] label polarity unclear
- [ ] possible dataset noise

