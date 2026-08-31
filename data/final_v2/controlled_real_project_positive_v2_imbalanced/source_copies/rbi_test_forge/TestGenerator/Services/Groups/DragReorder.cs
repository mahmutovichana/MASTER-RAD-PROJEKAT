namespace RBBH.TestAutomation.Api.Services.Groups;

/// <summary>
/// Čista (bez stanja) logika premještanja elementa u listi — odvojena od UI-a radi unit testiranja
/// drag&amp;drop reordera. Ne mutira ulaznu listu; vraća novu.
/// </summary>
public static class DragReorder
{
    /// <summary>
    /// Premješta element sa <paramref name="fromIndex"/> na <paramref name="toIndex"/> i vraća novu listu.
    ///
    /// Granični uslovi:
    ///   • <paramref name="fromIndex"/> van opsega [0, Count) → vraća nepromijenjenu kopiju (nema šta premjestiti).
    ///   • <paramref name="toIndex"/> se klampuje u [0, Count-1] — drop na kraj (index ≥ Count) ide na zadnju poziciju.
    ///   • <paramref name="fromIndex"/> jednak efektivnom odredištu → vraća nepromijenjenu kopiju (no-op).
    /// </summary>
    public static IReadOnlyList<T> Move<T>(IReadOnlyList<T> list, int fromIndex, int toIndex)
    {
        var result = new List<T>(list);

        if (fromIndex < 0 || fromIndex >= result.Count)
            return result;

        var target = Math.Clamp(toIndex, 0, result.Count - 1);
        if (fromIndex == target)
            return result;

        var item = result[fromIndex];
        result.RemoveAt(fromIndex);
        result.Insert(target, item);
        return result;
    }
}
