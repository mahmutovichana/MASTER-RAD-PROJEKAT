window.tagDownloadTextFile = (fileName, contentType, content) => {
    const blob = new Blob([content], { type: contentType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = fileName;
    link.click();
    link.remove();

    URL.revokeObjectURL(url);
};
