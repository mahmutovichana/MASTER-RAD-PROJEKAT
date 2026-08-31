using System.Text.Json;

namespace RBBH.TestAutomation.Api.Services.Run;

/// <summary>
/// Minimalni JSONPath evaluator za REST assert-e. Podržava:
///   <c>$.prop</c>, <c>$.a.b</c>, <c>$[0]</c>, <c>$[0].id</c>, <c>$.data[2].naziv</c>.
/// Ne podržava wildcard/filtere/rekurziju — dovoljno za status/body provjere scenarija.
/// </summary>
public static class JsonPathEvaluator
{
    /// <summary>
    /// Evaluira <paramref name="path"/> nad JSON tekstom. Vraća <c>true</c> i stringifikovanu
    /// vrijednost ako putanja postoji; <c>false</c> ako JSON nije validan ili putanja ne postoji.
    /// </summary>
    public static bool TryEvaluate(string json, string path, out string? value)
    {
        value = null;

        JsonDocument doc;
        try { doc = JsonDocument.Parse(json); }
        catch (JsonException) { return false; }

        using (doc)
        {
            var current = doc.RootElement;

            foreach (var seg in Tokenize(path))
            {
                if (seg.IsIndex)
                {
                    if (current.ValueKind != JsonValueKind.Array ||
                        seg.Index < 0 || seg.Index >= current.GetArrayLength())
                        return false;

                    current = current[seg.Index];
                }
                else
                {
                    if (current.ValueKind != JsonValueKind.Object ||
                        !current.TryGetProperty(seg.Name!, out var next))
                        return false;

                    current = next;
                }
            }

            value = Stringify(current);
            return true;
        }
    }

    private readonly record struct Segment(bool IsIndex, int Index, string? Name);

    private static IEnumerable<Segment> Tokenize(string path)
    {
        var i = 0;
        if (i < path.Length && path[i] == '$') i++;   // vodeći $

        while (i < path.Length)
        {
            var c = path[i];

            if (c == '.') { i++; continue; }

            if (c == '[')
            {
                var end = path.IndexOf(']', i);
                if (end < 0) yield break;

                var inner = path.Substring(i + 1, end - i - 1).Trim().Trim('\'', '"');
                if (int.TryParse(inner, out var idx))
                    yield return new Segment(true, idx, null);
                else
                    yield return new Segment(false, 0, inner);   // ['prop']

                i = end + 1;
            }
            else
            {
                var start = i;
                while (i < path.Length && path[i] != '.' && path[i] != '[') i++;
                yield return new Segment(false, 0, path[start..i]);
            }
        }
    }

    private static string Stringify(JsonElement el) => el.ValueKind switch
    {
        JsonValueKind.String => el.GetString() ?? "",
        JsonValueKind.Number => el.GetRawText(),
        JsonValueKind.True   => "true",
        JsonValueKind.False  => "false",
        JsonValueKind.Null   => "null",
        _                    => el.GetRawText(),   // objekti/nizovi → sirovi JSON
    };
}
