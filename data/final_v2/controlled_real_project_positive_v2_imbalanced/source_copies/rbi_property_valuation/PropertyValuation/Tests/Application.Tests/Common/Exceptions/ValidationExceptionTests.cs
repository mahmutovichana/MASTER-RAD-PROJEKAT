using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Models;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Common.Exceptions;

public sealed class ValidationExceptionTests
{
    [Fact]
    public void DefaultConstructor_HasEmptyErrorsAndDefaultMessage()
    {
        var ex = new ValidationException();

        Assert.Empty(ex.Errors);
        Assert.Null(ex.FieldErrors);
        Assert.Equal("One or more validation failures have occurred.", ex.Message);
    }

    [Fact]
    public void DictionaryConstructor_StoresProvidedErrors()
    {
        var errors = new Dictionary<string, string[]>
        {
            ["clientName"] = ["Ime klijenta je obavezno."]
        };

        var ex = new ValidationException(errors);

        Assert.Same(errors, ex.Errors);
        Assert.Null(ex.FieldErrors);
    }

    [Fact]
    public void FieldAndErrorConstructor_WrapsSingleErrorInDictionary()
    {
        var ex = new ValidationException("clientName", "Ime klijenta je obavezno.");

        var messages = Assert.Single(ex.Errors);
        Assert.Equal("clientName", messages.Key);
        Assert.Equal("Ime klijenta je obavezno.", Assert.Single(messages.Value));
        Assert.Null(ex.FieldErrors);
    }

    [Fact]
    public void FieldErrorsConstructor_StoresFieldErrorsAndEmptyErrorsDictionary()
    {
        var fieldErrors = new List<ValidationFieldError>
        {
            new("jmbg", "INVALID_JMBG_LENGTH", "JMBG mora sadržavati tačno 13 cifara.")
        };

        var ex = new ValidationException(fieldErrors);

        Assert.Empty(ex.Errors);
        Assert.Same(fieldErrors, ex.FieldErrors);
    }
}
