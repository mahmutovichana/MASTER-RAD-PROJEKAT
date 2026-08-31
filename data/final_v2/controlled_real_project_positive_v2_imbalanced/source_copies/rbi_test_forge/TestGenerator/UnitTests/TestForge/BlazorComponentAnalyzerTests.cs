using RBBH.TestAutomation.Core.Generation;
using Xunit;

namespace UnitTests.TestForge;

public class BlazorComponentAnalyzerTests
{
    private const string SampleRazor = """
        @page "/grupe"
        @page "/grupe/{GroupId:guid}"
        @attribute [Authorize]
        @rendermode InteractiveServer
        @inject IGroupService GroupSvc

        <EditForm Model="@_form" OnValidSubmit="HandleSave">
            <DataAnnotationsValidator />
            <ValidationSummary />
            <InputText @bind-Value="_form.Naziv" />
            <InputNumber @bind-Value="_form.Prioritet" />
            <button type="submit">Spremi</button>
            <button type="button" @onclick="HandleDelete">Obriši</button>
        </EditForm>

        @code {
            [Parameter] public Guid   GroupId { get; set; }
            [Parameter] public string Title   { get; set; } = "";
            [Parameter] public EventCallback          OnSave   { get; set; }
            [Parameter] public EventCallback<Guid>    OnDelete { get; set; }

            private async Task HandleSave()   { await GroupSvc.CreateAsync(null!, "", ""); }
            private void       HandleDelete() { }

            private async Task LoadData()
            {
                var items = await _http.GetFromJsonAsync<List<object>>("api/groups");
            }
        }
        """;

    [Fact]
    public void Analyze_ParsesTwoPageRoutes()
    {
        var spec = BlazorComponentAnalyzer.Analyze("Grupe", SampleRazor);

        Assert.Equal(2, spec.Routes.Count);
        Assert.Equal("/grupe", spec.Routes[0].Route);
        Assert.Equal("/grupe/{GroupId:guid}", spec.Routes[1].Route);
    }

    [Fact]
    public void Analyze_ParsesRegularParameters()
    {
        var spec = BlazorComponentAnalyzer.Analyze("Grupe", SampleRazor);

        Assert.Equal(2, spec.Parameters.Count);
        Assert.Contains(spec.Parameters, p => p.Name == "GroupId" && p.Type == "Guid");
        Assert.Contains(spec.Parameters, p => p.Name == "Title"   && p.Type == "string");
    }

    [Fact]
    public void Analyze_ParsesEventCallbacks()
    {
        var spec = BlazorComponentAnalyzer.Analyze("Grupe", SampleRazor);

        Assert.Equal(2, spec.EventCallbacks.Count);
        Assert.Contains(spec.EventCallbacks, e => e.Name == "OnSave"   && e.GenericArg == "");
        Assert.Contains(spec.EventCallbacks, e => e.Name == "OnDelete" && e.GenericArg == "Guid");
    }

    [Fact]
    public void Analyze_ParsesOnClickHandlers()
    {
        var spec = BlazorComponentAnalyzer.Analyze("Grupe", SampleRazor);

        Assert.Single(spec.OnClickHandlers);
        Assert.Equal("HandleDelete", spec.OnClickHandlers[0].MethodName);
    }

    [Fact]
    public void Analyze_DetectsHttpCall()
    {
        var spec = BlazorComponentAnalyzer.Analyze("Grupe", SampleRazor);

        Assert.Single(spec.HttpCalls);
        Assert.Equal("GetFromJsonAsync", spec.HttpCalls[0].ClientMethod);
    }

    [Fact]
    public void Analyze_DetectsEditFormWithInputsAndValidation()
    {
        var spec = BlazorComponentAnalyzer.Analyze("Grupe", SampleRazor);

        Assert.Single(spec.Forms);
        Assert.True(spec.Forms[0].HasValidationSummary);
        Assert.Contains("InputText",   spec.Forms[0].InputTypes);
        Assert.Contains("InputNumber", spec.Forms[0].InputTypes);
    }

    [Fact]
    public void Analyze_ComponentWithNoFeatures_ReturnsEmptyCollections()
    {
        const string minimal = """
            @page "/test"
            <h1>Hello</h1>
            """;

        var spec = BlazorComponentAnalyzer.Analyze("Test", minimal);

        Assert.Single(spec.Routes);
        Assert.Empty(spec.Parameters);
        Assert.Empty(spec.EventCallbacks);
        Assert.Empty(spec.OnClickHandlers);
        Assert.Empty(spec.HttpCalls);
        Assert.Empty(spec.Forms);
    }
}
