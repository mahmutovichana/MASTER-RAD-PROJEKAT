using System.Text.RegularExpressions;

namespace RBBH.TestAutomation.Core.Generation;

/// <summary>
/// Regex-based parser za .razor sadržaj — bez Roslyn ovisnosti.
/// Pokriva standardne Blazor obrasce dovoljno dobro za generisanje bUnit templatea.
/// </summary>
public static class BlazorComponentAnalyzer
{
    // @page "/ruta" ili @page "/ruta/{Id:guid}"
    private static readonly Regex PageRx = new(
        @"@page\s+""([^""]+)""",
        RegexOptions.Multiline | RegexOptions.Compiled);

    // [Parameter] public EventCallback<T>? Name  ili  EventCallback Name
    private static readonly Regex EventCallbackRx = new(
        @"\[Parameter\]\s+public\s+EventCallback(?:<([^>]+)>)?\s+(\w+)",
        RegexOptions.Singleline | RegexOptions.Compiled);

    // [Parameter] public SomeType Name { — ne smije uhvatiti EventCallback (excluded via negativni lookahead)
    private static readonly Regex ParameterRx = new(
        @"\[Parameter\]\s+public\s+(?!EventCallback)(\w[\w?<>, \[\]]*?)\s+(\w+)\s*\{",
        RegexOptions.Singleline | RegexOptions.Compiled);

    // @onclick="MethodName" ili @onclick="@MethodName" — ne hvata lambde
    private static readonly Regex OnClickRx = new(
        @"@onclick=""@?(\w+)""",
        RegexOptions.Compiled);

    // GetFromJsonAsync<T>("url"), PostAsJsonAsync("url"), itd.
    // Podržava nested generike poput <List<object>> jednim nivoom ugniježđenja.
    private static readonly Regex HttpRx = new(
        @"\b(GetFromJsonAsync|PostAsJsonAsync|PutAsJsonAsync|GetAsync|PostAsync|PutAsync|PatchAsync|DeleteAsync|SendAsync)\s*(?:<(?:[^<>]|<[^<>]*>)*>)?\s*\(\s*(?:\$?""([^""]*)""|[^,)]+)",
        RegexOptions.Compiled);

    // <InputText, <InputDate, <InputNumber, <InputSelect, <InputTextArea, <InputCheckbox
    private static readonly Regex InputRx = new(
        @"<(InputText|InputDate|InputNumber|InputSelect|InputTextArea|InputCheckbox|InputRadio)\b",
        RegexOptions.Compiled);

    private static readonly Regex EditFormRx  = new(@"<EditForm\b",        RegexOptions.Compiled);
    private static readonly Regex ValidationRx = new(@"<ValidationSummary\b", RegexOptions.Compiled);

    public static BlazorComponentSpec Analyze(string componentName, string razorContent)
    {
        var routes = PageRx.Matches(razorContent)
            .Select(m => new BlazorPageRoute(m.Groups[1].Value))
            .ToList();

        var eventCallbacks = EventCallbackRx.Matches(razorContent)
            .Select(m => new BlazorEventCallback(m.Groups[2].Value, m.Groups[1].Value))
            .ToList();

        var ecNames = new HashSet<string>(eventCallbacks.Select(e => e.Name));

        var parameters = ParameterRx.Matches(razorContent)
            .Select(m => new BlazorParameter(m.Groups[2].Value, m.Groups[1].Value.Trim()))
            .Where(p => !ecNames.Contains(p.Name))
            .ToList();

        // Dedupliciraj @onclick handlere (isti handler na više elemenata → jedan test)
        var onClickHandlers = OnClickRx.Matches(razorContent)
            .Select(m => m.Groups[1].Value)
            .Distinct()
            .Select(name => new BlazorOnClickHandler(name))
            .ToList();

        var httpCalls = HttpRx.Matches(razorContent)
            .Select(m => new BlazorHttpCall(m.Groups[1].Value, m.Groups[2].Value))
            .ToList();

        List<BlazorForm> forms = [];
        var editFormCount = EditFormRx.Matches(razorContent).Count;
        if (editFormCount > 0)
        {
            var inputTypes = InputRx.Matches(razorContent)
                .Select(m => m.Groups[1].Value)
                .Distinct()
                .ToList();
            var hasValidation = ValidationRx.IsMatch(razorContent);
            forms.Add(new BlazorForm(inputTypes, hasValidation));
        }

        return new BlazorComponentSpec(
            componentName,
            routes,
            parameters,
            eventCallbacks,
            onClickHandlers,
            httpCalls,
            forms);
    }
}
