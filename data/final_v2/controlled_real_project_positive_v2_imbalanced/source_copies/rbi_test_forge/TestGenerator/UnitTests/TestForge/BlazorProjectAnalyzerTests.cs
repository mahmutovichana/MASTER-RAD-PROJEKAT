using RBBH.TestAutomation.Core.Generation;
using Xunit;

namespace UnitTests.TestForge;

public class BlazorProjectAnalyzerTests
{
    // Stranica sa svim karakteristikama koje pokrivaju Acceptance Criteria
    // (@page rute, [Parameter], EventCallback, @onclick, HttpClient, EditForm + ValidationSummary).
    private const string GrupePage = """
        @page "/grupe"
        @page "/grupe/{GroupId:guid}"
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
            [Parameter] public EventCallback       OnSave   { get; set; }
            [Parameter] public EventCallback<Guid> OnDelete { get; set; }

            private async Task HandleSave()   { await GroupSvc.CreateAsync(null!, "", ""); }
            private void       HandleDelete() { }

            private async Task LoadData()
            {
                var items = await _http.GetFromJsonAsync<List<object>>("api/groups");
            }
        }
        """;

    // Druga, jednostavna stranica — samo ruta.
    private const string HomePage = """
        @page "/"
        <h1>Početna</h1>
        """;

    // Obična komponenta — nema @page (dakle nije stranica), ali ima [Parameter].
    private const string StatusBadgeComponent = """
        <span class="badge">@Text</span>
        @code {
            [Parameter] public string Text { get; set; } = "";
        }
        """;

    private static BlazorProjectAnalysis AnalyzeSample() =>
        BlazorProjectAnalyzer.Analyze(
        [
            new BlazorRazorFile("Components/Pages/Grupe.razor", GrupePage),
            new BlazorRazorFile("Components/Pages/Home.razor",  HomePage),
            new BlazorRazorFile("Components/Shared/StatusBadge.razor", StatusBadgeComponent),
        ]);

    [Fact]
    public void Analyze_ListsAllPagesAndComponents()
    {
        var result = AnalyzeSample();

        Assert.Equal(3, result.Components.Count);
        Assert.Equal(2, result.PageCount);       // Grupe + Home imaju @page
        Assert.Equal(1, result.ComponentCount);  // StatusBadge nema @page
    }

    [Fact]
    public void Analyze_DerivesComponentNameFromFileName()
    {
        var result = AnalyzeSample();

        Assert.Contains(result.Components, c => c.Spec.ComponentName == "Grupe");
        Assert.Contains(result.Components, c => c.Spec.ComponentName == "Home");
        Assert.Contains(result.Components, c => c.Spec.ComponentName == "StatusBadge");
    }

    [Fact]
    public void Analyze_OrdersPagesBeforeComponents()
    {
        var result = AnalyzeSample();

        // Stranice (IsPage) moraju doći prije običnih komponenti.
        Assert.True(result.Components[0].IsPage);
        Assert.True(result.Components[1].IsPage);
        Assert.False(result.Components[^1].IsPage);
        Assert.Equal("StatusBadge", result.Components[^1].Spec.ComponentName);
    }

    [Fact]
    public void Analyze_DetectsAllRoutesPerComponent() // AC: @page direktive i rute
    {
        var grupe = AnalyzeSample().Components.Single(c => c.Spec.ComponentName == "Grupe");

        Assert.Equal(2, grupe.Spec.Routes.Count);
        Assert.Equal("/grupe", grupe.Spec.Routes[0].Route);
        Assert.Equal("/grupe/{GroupId:guid}", grupe.Spec.Routes[1].Route);
    }

    [Fact]
    public void Analyze_DetectsParameters() // AC: [Parameter] atributi
    {
        var grupe = AnalyzeSample().Components.Single(c => c.Spec.ComponentName == "Grupe");

        Assert.Contains(grupe.Spec.Parameters, p => p.Name == "GroupId" && p.Type == "Guid");
        Assert.Contains(grupe.Spec.Parameters, p => p.Name == "Title" && p.Type == "string");
    }

    [Fact]
    public void Analyze_DetectsEventCallbacksAndOnClick() // AC: EventCallback + button interakcije
    {
        var grupe = AnalyzeSample().Components.Single(c => c.Spec.ComponentName == "Grupe");

        Assert.Contains(grupe.Spec.EventCallbacks, e => e.Name == "OnSave" && e.GenericArg == "");
        Assert.Contains(grupe.Spec.EventCallbacks, e => e.Name == "OnDelete" && e.GenericArg == "Guid");
        Assert.Contains(grupe.Spec.OnClickHandlers, h => h.MethodName == "HandleDelete");
    }

    [Fact]
    public void Analyze_DetectsHttpCalls() // AC: HttpClient pozivi (za mockovanje)
    {
        var grupe = AnalyzeSample().Components.Single(c => c.Spec.ComponentName == "Grupe");

        Assert.Contains(grupe.Spec.HttpCalls, h => h.ClientMethod == "GetFromJsonAsync");
        Assert.True(AnalyzeSample().TotalHttpCalls >= 1);
    }

    [Fact]
    public void Analyze_DetectsForms() // AC: EditForm, InputText, ValidationSummary
    {
        var result = AnalyzeSample();
        var grupe = result.Components.Single(c => c.Spec.ComponentName == "Grupe");

        Assert.Single(grupe.Spec.Forms);
        Assert.True(grupe.Spec.Forms[0].HasValidationSummary);
        Assert.Contains("InputText", grupe.Spec.Forms[0].InputTypes);
        Assert.Contains("InputNumber", grupe.Spec.Forms[0].InputTypes);
        Assert.Equal(1, result.TotalForms);
    }

    [Fact]
    public void Analyze_PreservesRawContentForSaving()
    {
        var home = AnalyzeSample().Components.Single(c => c.Spec.ComponentName == "Home");

        Assert.Equal(HomePage, home.RawContent);
    }

    [Fact]
    public void Analyze_MergesCodeBehind_DetectsParametersFromRazorCs()
    {
        // Parametri deklarisani u .razor.cs code-behindu moraju biti detektovani nakon spajanja.
        const string razor = """
            @page "/profil"
            <h1>Profil</h1>
            """;
        const string codeBehind = """
            namespace App;
            public partial class Profil
            {
                [Parameter] public string Username { get; set; } = "";
                [Parameter] public EventCallback OnLogout { get; set; }
            }
            """;

        var result = BlazorProjectAnalyzer.Analyze(
        [
            new BlazorRazorFile("Pages/Profil.razor", razor),
            new BlazorRazorFile("Pages/Profil.razor.cs", codeBehind),
        ]);

        var profil = Assert.Single(result.Components);
        Assert.Equal("Profil", profil.Spec.ComponentName);
        Assert.Contains(profil.Spec.Parameters, p => p.Name == "Username");
        Assert.Contains(profil.Spec.EventCallbacks, e => e.Name == "OnLogout");
    }

    [Fact]
    public void Analyze_SkipsEmptyRazorFile_AddsWarning()
    {
        var result = BlazorProjectAnalyzer.Analyze(
        [
            new BlazorRazorFile("Pages/Home.razor", HomePage),
            new BlazorRazorFile("Pages/Prazna.razor", "   "),
        ]);

        Assert.Single(result.Components);
        Assert.Contains(result.Warnings, w => w.Contains("Prazna.razor"));
    }

    [Fact]
    public void Analyze_NoRazorFiles_ReturnsWarningAndEmptyList()
    {
        var result = BlazorProjectAnalyzer.Analyze(
        [
            new BlazorRazorFile("README.md", "# Projekt"),
            new BlazorRazorFile("Program.cs", "// kod"),
        ]);

        Assert.Empty(result.Components);
        Assert.NotEmpty(result.Warnings);
    }

    [Fact]
    public void Analyze_EmptyCollection_ReturnsWarning()
    {
        var result = BlazorProjectAnalyzer.Analyze([]);

        Assert.Empty(result.Components);
        Assert.NotEmpty(result.Warnings);
    }

    [Fact]
    public void Analyze_DuplicateRazorPaths_KeepsBothWithoutThrowing()
    {
        // Rubni slučaj: dva .razor fajla s istom putanjom (npr. loše spakovan ZIP).
        // Analyzer ne smije baciti; oba se pojave (bez tihog gubljenja komponente).
        var result = BlazorProjectAnalyzer.Analyze(
        [
            new BlazorRazorFile("Components/Pages/Home.razor", HomePage),
            new BlazorRazorFile("Components/Pages/Home.razor", HomePage),
        ]);

        Assert.Equal(2, result.Components.Count);
        Assert.All(result.Components, c => Assert.Equal("Home", c.Spec.ComponentName));
    }

    [Fact]
    public void Analyze_ContentWithBom_IsAnalyzedNotSkipped()
    {
        // BOM na početku sadržaja ne smije biti tretiran kao prazan fajl.
        var withBom = "﻿" + HomePage;
        var result = BlazorProjectAnalyzer.Analyze(
        [
            new BlazorRazorFile("Components/Pages/Home.razor", withBom),
        ]);

        var component = Assert.Single(result.Components);
        Assert.Equal("Home", component.Spec.ComponentName);
        Assert.True(component.IsPage); // @page "/" i dalje detektovan
    }
}
