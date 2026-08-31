using RBBH.TestAutomation.Api.DTO;

namespace RBBH.TestAutomation.Api.Services.Groups;

/// <summary>
/// Čista (bez I/O) izgradnja stabla grupa iz ravne liste. Potpuno unit-testabilno.
///
/// Pravila:
///   • Root su grupe bez parenta ILI siročad (parent ne postoji u listi) — siroče se
///     tretira kao root da ne nestane iz prikaza (vidljivost &gt; tiho odbacivanje).
///   • Sortiranje na svakom nivou: <c>Prioritet</c> opadajuće, pa <c>Naziv</c> (case-insensitive).
///   • Grupa bez sažetka u mapi dobije prazan <see cref="GroupSummaryDto"/> (defanzivno).
///   • Ciklus u parent-lancu (A→B→A) ili samo-referenca (A→A): takve grupe nisu dostupne
///     ni iz jednog root-a i inače bi tiho nestale — tretiraju se kao root, a rekurzija je
///     zaštićena od beskonačne petlje (svaka grupa se posjeti najviše jednom).
/// Hijerarhija je u praksi ≤2 nivoa, ali izgradnja je rekurzivna pa radi za bilo koju dubinu.
/// </summary>
public static class GroupTreeBuilder
{
    /// <summary>
    /// Gradi stablo iz <paramref name="groups"/> uz pred-izračunate <paramref name="summaries"/> (id → sažetak).
    /// </summary>
    public static IReadOnlyList<GroupTreeNodeDto> Build(
        IReadOnlyList<GroupDto> groups,
        IReadOnlyDictionary<Guid, GroupSummaryDto> summaries)
    {
        var idSet = new HashSet<Guid>(groups.Count);
        foreach (var g in groups)
            idSet.Add(g.Id);

        var childrenByParent = groups
            .Where(g => g.ParentGroupId is Guid pid && idSet.Contains(pid))
            .GroupBy(g => g.ParentGroupId!.Value)
            .ToDictionary(grp => grp.Key, grp => (IReadOnlyList<GroupDto>)grp.ToList());

        GroupSummaryDto SummaryFor(Guid id) =>
            summaries.TryGetValue(id, out var s) ? s : new GroupSummaryDto(0, null, null, 0);

        // Cycle-guard: grupa posjećena jednom se ne ulazi ponovo (spriječava beskonačnu
        // rekurziju kod ciklusa/samo-reference i osigurava da se svaka pojavi tačno jednom).
        var visited = new HashSet<Guid>(groups.Count);

        IReadOnlyList<GroupTreeNodeDto> BuildNodes(IEnumerable<GroupDto> level)
        {
            var nodes = new List<GroupTreeNodeDto>();
            foreach (var g in level
                         .OrderByDescending(x => x.Prioritet)
                         .ThenBy(x => x.Naziv, StringComparer.OrdinalIgnoreCase))
            {
                if (!visited.Add(g.Id))
                    continue; // već posjećen — dio ciklusa, ne ulazi ponovo

                var children = childrenByParent.TryGetValue(g.Id, out var kids)
                    ? BuildNodes(kids)
                    : (IReadOnlyList<GroupTreeNodeDto>)[];

                nodes.Add(new GroupTreeNodeDto(g, SummaryFor(g.Id), children));
            }

            return nodes;
        }

        var roots = groups.Where(g => g.ParentGroupId is not Guid pid || !idSet.Contains(pid));
        var tree = BuildNodes(roots).ToList();

        // Grupe zarobljene u ciklusu nisu dostupne iz nijednog root-a — dodaj ih kao root
        // da ostanu vidljive (vidljivost > tiho odbacivanje).
        var unreached = groups.Where(g => !visited.Contains(g.Id)).ToList();
        if (unreached.Count > 0)
            tree.AddRange(BuildNodes(unreached));

        return tree;
    }
}
