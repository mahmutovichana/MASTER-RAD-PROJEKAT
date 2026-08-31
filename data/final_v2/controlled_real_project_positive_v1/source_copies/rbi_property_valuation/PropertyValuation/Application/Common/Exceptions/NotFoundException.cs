namespace RBBH.CollateralAppraisal.Application.Common.Exceptions;

public class NotFoundException : Exception
{
    /// <summary>Mašinski čitljiv kod greške. Null ako nije definisan.</summary>
    public string? ErrorCode { get; }

    public NotFoundException(string name, object key, string? errorCode = null)
        : base($"Entity '{name}' with key '{key}' was not found.")
    {
        ErrorCode = errorCode;
    }

    public NotFoundException(string message, string? errorCode = null)
        : base(message)
    {
        ErrorCode = errorCode;
    }
}
