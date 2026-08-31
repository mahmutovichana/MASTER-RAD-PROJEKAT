namespace RBBH.TestAutomation.Api.DTO;

/// <summary>
/// Example Data Transfer Object
/// Create your DTOs here to match backend API models
/// </summary>
public class ExampleDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
}

/// <summary>
/// Example request model
/// </summary>
public class CreateExampleRequest
{
    public string Name { get; set; } = string.Empty;
}

/// <summary>
/// Example response model
/// </summary>
public class ExampleResponse
{
    public bool Success { get; set; }
    public string Message { get; set; } = string.Empty;
    public ExampleDto? Data { get; set; }
}
