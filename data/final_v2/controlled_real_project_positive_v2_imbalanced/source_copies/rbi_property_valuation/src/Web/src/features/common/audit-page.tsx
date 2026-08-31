import { useQuery } from "@tanstack/react-query";
import { Download, Eye, RefreshCw, Search, X } from "lucide-react";
import { useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Heading, Text } from "@/components/ui/typography";
import { apiClient } from "@/lib/api/http-client";

type Row = Readonly<Record<string, unknown>>;
type Filters = {
  search: string;
  module: string;
  actorUsername: string;
  actorRole: string;
  status: string;
  severity: string;
  from: string;
  to: string;
};
const empty: Filters = {
  search: "",
  module: "",
  actorUsername: "",
  actorRole: "",
  status: "",
  severity: "",
  from: "",
  to: "",
};
const pick = (row: Row, ...keys: string[]) =>
  keys.map((key) => row[key]).find((value) => value != null);
const unwrap = (raw: unknown): Row[] => {
  const root = (raw as Row)?.["data"] ?? raw;
  const items = Array.isArray(root) ? root : ((root as Row)?.["items"] ?? (root as Row)?.["Items"]);
  return Array.isArray(items) ? (items as Row[]) : [];
};

export function AuditPage() {
  const [filters, setFilters] = useState<Filters>(empty);
  const [selected, setSelected] = useState<Row>();
  const query = useQuery({
    queryKey: ["audit", filters],
    queryFn: async () =>
      unwrap(
        await apiClient.getLegacy("/api/audit", {
          query: {
            Search: filters.search || undefined,
            Module: filters.module || undefined,
            ActorUsername: filters.actorUsername || undefined,
            ActorRole: filters.actorRole || undefined,
            Status: filters.status || undefined,
            Severity: filters.severity || undefined,
            From: filters.from || undefined,
            To: filters.to ? `${filters.to}T23:59:59` : undefined,
            PageSize: 5000,
          },
        }),
      ),
  });
  const columns = useMemo(
    () =>
      [
        "timestampUtc",
        "actorUsername",
        "activeRole",
        "action",
        "module",
        "entityDisplayName",
        "status",
        "severity",
      ] as const,
    [],
  );
  const update = (key: keyof Filters, value: string) =>
    setFilters((current) => ({ ...current, [key]: value }));
  const exportCsv = () => {
    const rows = query.data ?? [];
    const csv = [
      columns.join(";"),
      ...rows.map((row) =>
        columns
          .map(
            (column) =>
              `"${String(pick(row, column, column[0]!.toUpperCase() + column.slice(1)) ?? "").replaceAll('"', '""')}"`,
          )
          .join(";"),
      ),
    ].join("\r\n");
    const url = URL.createObjectURL(new Blob(["\ufeff", csv], { type: "text/csv" }));
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `audit-${new Date().toISOString().slice(0, 10)}.csv`;
    anchor.click();
    URL.revokeObjectURL(url);
  };
  return (
    <section className="min-w-0 overflow-hidden">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-eyebrow text-text-tertiary">Administracija</p>
          <Heading level={1} size={4} className="mt-2">
            Audit log
          </Heading>
          <Text tone="secondary" className="mt-2">
            Sigurnosni i poslovni događaji s akterom, aktivnom ulogom, vremenom i ishodom.
          </Text>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={exportCsv} disabled={!query.data?.length}>
            <Download className="size-4" />
            CSV
          </Button>
          <Button variant="secondary" onClick={() => query.refetch()}>
            <RefreshCw className="size-4" />
            Osvježi
          </Button>
        </div>
      </div>
      <div className="mt-6 grid min-w-0 gap-3 rounded-sm border border-border-subtle bg-surface-default p-4 md:grid-cols-2 xl:grid-cols-4">
        <label className="grid min-w-0 gap-1 text-xs font-semibold xl:col-span-2">
          Pretraga
          <div className="flex min-w-0 items-center gap-2">
            <Search className="size-4 text-text-tertiary" />
            <Input
              className="min-w-0 w-full"
              placeholder="Akcija, korisnik ili entitet…"
              value={filters.search}
              onChange={(event) => update("search", event.target.value)}
            />
          </div>
        </label>
        <Field
          label="Korisnik"
          value={filters.actorUsername}
          onChange={(value) => update("actorUsername", value)}
        />
        <Field
          label="Aktivna rola"
          value={filters.actorRole}
          onChange={(value) => update("actorRole", value)}
        />
        <Select
          label="Modul"
          value={filters.module}
          values={[
            "Users",
            "Roles",
            "Codebooks",
            "Security",
            "AppraisalOrders",
            "Documents",
            "System",
          ]}
          onChange={(value) => update("module", value)}
        />
        <Select
          label="Status"
          value={filters.status}
          values={["Success", "Failed", "Forbidden", "Conflict", "ValidationFailed", "SystemError"]}
          onChange={(value) => update("status", value)}
        />
        <Select
          label="Ozbiljnost"
          value={filters.severity}
          values={["Info", "Warning", "Security", "Critical"]}
          onChange={(value) => update("severity", value)}
        />
        <div className="grid min-w-0 grid-cols-1 gap-2 sm:grid-cols-2">
          <label className="grid min-w-0 gap-1 text-xs font-semibold">
            Od
            <Input
              className="min-w-0 w-full"
              type="date"
              value={filters.from}
              onChange={(event) => update("from", event.target.value)}
            />
          </label>
          <label className="grid min-w-0 gap-1 text-xs font-semibold">
            Do
            <Input
              type="date"
              min={filters.from}
              value={filters.to}
              onChange={(event) => update("to", event.target.value)}
            />
          </label>
        </div>
        <Button
          className="md:col-span-2 xl:col-span-4"
          variant="ghost"
          onClick={() => setFilters(empty)}
        >
          <X className="size-4" />
          Očisti filtere
        </Button>
      </div>
      <div className="mt-6 max-w-full overflow-x-auto rounded-sm border border-border-subtle bg-surface-default">
        <table className="min-w-max text-left text-sm">
          <thead className="bg-surface-subtle">
            <tr>
              {[
                "Vrijeme",
                "Korisnik",
                "Rola",
                "Akcija",
                "Modul",
                "Entitet",
                "Status",
                "Ozbiljnost",
                "Detalj",
              ].map((label) => (
                <th className="whitespace-nowrap px-4 py-3" key={label}>
                  {label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle">
            {query.data?.map((row, index) => (
              <tr key={index}>
                {columns.map((column) => (
                  <td className="max-w-64 truncate px-4 py-3" key={column}>
                    {column === "timestampUtc"
                      ? date(pick(row, column, "TimestampUtc"))
                      : String(
                          pick(row, column, column[0]!.toUpperCase() + column.slice(1)) ?? "—",
                        )}
                  </td>
                ))}
                <td className="px-4 py-3">
                  <Button size="icon" variant="ghost" onClick={() => setSelected(row)}>
                    <Eye className="size-4" />
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {!query.isLoading && !query.data?.length && (
          <p className="p-8 text-center text-text-secondary">Nema zapisa za odabrane filtere.</p>
        )}
      </div>
      <Dialog open={Boolean(selected)} onOpenChange={(open) => !open && setSelected(undefined)}>
        <DialogContent className="max-h-[85vh] max-w-2xl overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Detalj audit zapisa</DialogTitle>
            <DialogDescription>Neizmijenjeni podaci zabilježeni na backendu.</DialogDescription>
          </DialogHeader>
          <dl className="grid gap-3 sm:grid-cols-2">
            {Object.entries(selected ?? {}).map(([key, value]) => (
              <div className="border-b border-border-subtle pb-2" key={key}>
                <dt className="text-xs font-bold uppercase text-text-tertiary">
                  {key.replace(/([a-z])([A-Z])/g, "$1 $2")}
                </dt>
                <dd className="mt-1 break-words text-sm">
                  {typeof value === "object" ? JSON.stringify(value) : String(value ?? "—")}
                </dd>
              </div>
            ))}
          </dl>
        </DialogContent>
      </Dialog>
    </section>
  );
}
function Field({
  label,
  value,
  onChange,
}: {
  readonly label: string;
  readonly value: string;
  readonly onChange: (value: string) => void;
}) {
  return (
    <label className="grid min-w-0 gap-1 text-xs font-semibold">
      {label}
      <Input value={value} onChange={(event) => onChange(event.target.value)} />
    </label>
  );
}
function Select({
  label,
  value,
  values,
  onChange,
}: {
  readonly label: string;
  readonly value: string;
  readonly values: readonly string[];
  readonly onChange: (value: string) => void;
}) {
  return (
    <label className="grid min-w-0 gap-1 text-xs font-semibold">
      {label}
      <select
        className="h-10 min-w-0 max-w-full rounded-sm border border-border-subtle bg-surface-default px-3"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      >
        <option value="">Sve</option>
        {values.map((item) => (
          <option key={item}>{item}</option>
        ))}
      </select>
    </label>
  );
}
const date = (value: unknown) =>
  value
    ? new Intl.DateTimeFormat("bs-BA", { dateStyle: "short", timeStyle: "medium" }).format(
        new Date(String(value)),
      )
    : "—";
