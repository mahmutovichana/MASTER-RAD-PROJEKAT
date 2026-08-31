import { useQuery } from "@tanstack/react-query";
import { Download, RefreshCw, Search } from "lucide-react";
import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Heading, Text } from "@/components/ui/typography";
import { apiClient } from "@/lib/api/http-client";
type Row = Readonly<Record<string, unknown>>;
function unwrap(raw: unknown): Row[] {
  const root = (raw as Row)?.["data"] ?? raw;
  const value = Array.isArray(root)
    ? root
    : ((root as Row)?.["items"] ?? (root as Row)?.["Items"] ?? (root as Row)?.["results"]);
  return Array.isArray(value) ? (value as Row[]) : [];
}
export function RecordsPage({
  title,
  description,
  endpoint,
  area = "Operacije",
}: {
  readonly title: string;
  readonly description: string;
  readonly endpoint: string;
  readonly area?: string;
}) {
  const [search, setSearch] = useState("");
  const query = useQuery({
    queryKey: [endpoint],
    queryFn: async () => unwrap(await apiClient.getLegacy(endpoint, { query: { PageSize: 250 } })),
  });
  const filtered = useMemo(
    () =>
      query.data?.filter((r) =>
        JSON.stringify(r).toLocaleLowerCase("bs").includes(search.toLocaleLowerCase("bs")),
      ) ?? [],
    [query.data, search],
  );
  const columns = useMemo(() => {
    const first = filtered[0];
    return first
      ? Object.keys(first)
          .filter((k) => {
            const v = first[k];
            return v == null || ["string", "number", "boolean"].includes(typeof v);
          })
          .slice(0, 10)
      : [];
  }, [filtered]);
  const exportCsv = () => {
    const csv = [
      columns.join(";"),
      ...filtered.map((r) =>
        columns.map((c) => `"${String(r[c] ?? "").replaceAll('"', '""')}"`).join(";"),
      ),
    ].join("\r\n");
    const url = URL.createObjectURL(new Blob(["\ufeff", csv], { type: "text/csv" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = `${title.toLowerCase().replaceAll(" ", "-")}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };
  return (
    <section>
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-eyebrow text-text-tertiary">{area}</p>
          <Heading level={1} size={4} className="mt-2">
            {title}
          </Heading>
          <Text tone="secondary" className="mt-2">
            {description}
          </Text>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => query.refetch()}>
            <RefreshCw className="size-4" />
            Osvježi
          </Button>
          <Button variant="secondary" onClick={exportCsv} disabled={!filtered.length}>
            <Download className="size-4" />
            CSV
          </Button>
        </div>
      </div>
      <div className="mt-6 flex max-w-md items-center gap-2">
        <Search className="size-4 text-text-tertiary" />
        <Input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Filtriraj prikazane rezultate…"
        />
      </div>
      {query.isError && <p className="mt-6 text-feedback-danger">{query.error.message}</p>}
      <div className="mt-6 overflow-x-auto rounded-sm border border-border-subtle bg-surface-default">
        <table className="w-full text-left text-sm">
          <thead className="bg-surface-subtle">
            <tr>
              {columns.map((c) => (
                <th className="whitespace-nowrap px-4 py-3" key={c}>
                  {human(c)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle">
            {filtered.map((r, i) => (
              <tr key={String(r["id"] ?? r["Id"] ?? i)}>
                {columns.map((c) => (
                  <td className="max-w-80 truncate px-4 py-3" title={String(r[c] ?? "")} key={c}>
                    {format(r[c])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        {query.isLoading && <p className="p-8">Učitavanje…</p>}
        {!query.isLoading && !filtered.length && (
          <p className="p-8 text-center text-text-secondary">Nema podataka za prikaz.</p>
        )}
      </div>
    </section>
  );
}
const human = (v: string) =>
  v
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replaceAll("_", " ")
    .replace(/^./, (x) => x.toUpperCase());
const format = (v: unknown) =>
  v == null || v === "" ? "—" : typeof v === "boolean" ? (v ? "Da" : "Ne") : String(v);
