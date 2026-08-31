// testforgeDownload — inicira download ZIP blob-a u browseru putem data URL-a.
// Poziva se iz Blazor Server komponente putem JS Interop (IJSRuntime.InvokeVoidAsync).
window.testforgeDownload = function (filename, base64) {
    const link = document.createElement('a');
    link.href = 'data:application/zip;base64,' + base64;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};
