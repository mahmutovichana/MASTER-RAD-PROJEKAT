namespace RBBH.TestAutomation.Core.Generation;

public sealed record BlazorPageRoute(string Route);

public sealed record BlazorParameter(string Name, string Type);

public sealed record BlazorEventCallback(string Name, string GenericArg);

public sealed record BlazorOnClickHandler(string MethodName);

public sealed record BlazorHttpCall(string ClientMethod, string UrlFragment);

public sealed record BlazorForm(IReadOnlyList<string> InputTypes, bool HasValidationSummary);

public sealed record BlazorComponentSpec(
    string                            ComponentName,
    IReadOnlyList<BlazorPageRoute>    Routes,
    IReadOnlyList<BlazorParameter>    Parameters,
    IReadOnlyList<BlazorEventCallback> EventCallbacks,
    IReadOnlyList<BlazorOnClickHandler> OnClickHandlers,
    IReadOnlyList<BlazorHttpCall>     HttpCalls,
    IReadOnlyList<BlazorForm>         Forms
);
