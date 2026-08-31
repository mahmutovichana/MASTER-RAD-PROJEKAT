using RBBH.TestAutomation.Api.Services.Groups;

namespace UnitTests.Grupe;

/// <summary>
/// Unit testovi za <see cref="DragReorder.Move{T}"/> — čista logika premještanja iza drag&amp;drop reordera (AC2).
/// </summary>
public class DragReorderTests
{
    private static readonly string[] Base = ["A", "B", "C"];

    [Theory]
    [InlineData(0, 2, new[] { "B", "C", "A" })] // pomjeri prvi na kraj
    [InlineData(2, 0, new[] { "C", "A", "B" })] // pomjeri zadnji na početak
    [InlineData(0, 1, new[] { "B", "A", "C" })] // pomjeri za jedno mjesto dolje
    [InlineData(1, 1, new[] { "A", "B", "C" })] // isti indeks → no-op
    [InlineData(0, 99, new[] { "B", "C", "A" })] // toIndex iznad opsega → klamp na kraj
    [InlineData(5, 0, new[] { "A", "B", "C" })] // fromIndex van opsega → no-op
    [InlineData(0, -5, new[] { "A", "B", "C" })] // toIndex < 0 klamp na 0, from==target → no-op
    public void Move_WhenGivenIndices_ProducesExpectedOrder(int from, int to, string[] expected)
    {
        var result = DragReorder.Move(Base, from, to);
        Assert.Equal(expected, result);
    }

    [Fact]
    public void Move_WhenCalled_DoesNotMutateInputList()
    {
        var input = new List<string> { "A", "B", "C" };
        _ = DragReorder.Move(input, 0, 2);
        Assert.Equal(["A", "B", "C"], input);
    }

    [Fact]
    public void Move_WhenEmptyList_ReturnsEmpty()
    {
        var result = DragReorder.Move(Array.Empty<int>(), 0, 0);
        Assert.Empty(result);
    }
}
