# Shared Components

This folder is for **reusable Blazor components** that you create for your application.

## 📁 Purpose

Place custom UI components here that will be used across multiple pages:
- Navigation components
- Form controls
- Data display components
- Modal dialogs
- Alerts and notifications

## 📝 Example Component

```razor
@* Shared/MyComponent.razor *@

<div class="my-component">
    <MudPaper Elevation="2" Class="pa-4">
        <MudText Typo="Typo.h6">@Title</MudText>
        @ChildContent
    </MudPaper>
</div>

@code {
    [Parameter]
    public string Title { get; set; } = "Default Title";

    [Parameter]
    public RenderFragment? ChildContent { get; set; }
}
```

## 🎯 Usage

```razor
@* In any page *@

<MyComponent Title="Hello">
    <MudText>Your content here</MudText>
</MyComponent>
```

## 💡 Tips

- Keep components focused on a single responsibility
- Use parameters for customization
- Consider using MudBlazor components as building blocks
- Document your components with XML comments
