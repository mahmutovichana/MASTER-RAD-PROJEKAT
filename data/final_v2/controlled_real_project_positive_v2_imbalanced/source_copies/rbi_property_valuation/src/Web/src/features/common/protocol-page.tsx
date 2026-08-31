import { useQuery } from "@tanstack/react-query";
import { Eye, RefreshCw, Search } from "lucide-react";
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
const pick = (row: Row, ...keys: string[]) =>
  keys.map((key) => row[key]).find((value) => value != null);
const unwrap = (raw: unknown): Row[] => {
  const root = (raw as Row)?.["data"] ?? raw;
  const items = Array.isArray(root) ? root : ((root as Row)?.["items"] ?? (root as Row)?.["Items"]);
  return Array.isArray(items) ? (items as Row[]) : [];
};

export function ProtocolPage() {
  const [search, setSearch] = useState("");
  const [selectedId, setSelectedId] = useState<number>();
  const query = useQuery({
    queryKey: ["protocol"],
    queryFn: async () =>
      unwrap(await apiClient.getLegacy("/api/protocol/orders", { query: { PageSize: 250 } })),
  });
  const detail = useQuery({
    queryKey: ["protocol", selectedId],
    queryFn: async () => apiClient.getLegacy<Row>(`/api/protocol/orders/${selectedId}`),
    enabled: Boolean(selectedId),
  });
  const rows = useMemo(
    () =>
      query.data?.filter((row) =>
        JSON.stringify(row).toLocaleLowerCase("bs").includes(search.toLocaleLowerCase("bs")),
      ) ?? [],
    [query.data, search],
  );
  return (
    <section>
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-eyebrow text-text-tertiary">Operacije</p>
          <Heading level={1} size={4} className="mt-2">
            Protokol narudžbi
          </Heading>
          <Text tone="secondary" className="mt-2">
            Evidencija prijema, otpreme, odgovornih osoba i potpunog kretanja svake narudžbe.
          </Text>
        </div>
        <Button variant="secondary" onClick={() => query.refetch()}>
          <RefreshCw className="size-4" />
          Osvježi
        </Button>
      </div>
      <div className="mt-6 flex max-w-md items-center gap-2">
        <Search className="size-4 text-text-tertiary" />
        <Input
          placeholder="Broj protokola, narudžba ili klijent…"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
      </div>
      <div className="mt-6 overflow-x-auto rounded-sm border border-border-subtle bg-surface-default">
        <table className="w-full text-left text-sm">
          <thead className="bg-surface-subtle">
            <tr>
              {[
                "Broj protokola",
                "Narudžba",
                "Klijent",
                "Zaprimljeno",
                "Poslano",
                "Status",
                "Detalji",
              ].map((label) => (
                <th className="px-4 py-3" key={label}>
                  {label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle">
            {rows.map((row, index) => {
              const id = Number(pick(row, "orderId", "OrderId", "id", "Id"));
              return (
                <tr key={id || index}>
                  <td className="px-4 py-3 font-semibold">
                    {String(pick(row, "protocolNumber", "ProtocolNumber") ?? "—")}
                  </td>
                  <td className="px-4 py-3">
                    {String(pick(row, "orderNumber", "OrderNumber") ?? id)}
                  </td>
                  <td className="px-4 py-3">
                    {String(pick(row, "clientName", "ClientName") ?? "—")}
                  </td>
                  <td className="px-4 py-3">
                    {date(pick(row, "receivedAt", "ReceivedAt", "createdAt", "CreatedAt"))}
                  </td>
                  <td className="px-4 py-3">{date(pick(row, "sentAt", "SentAt"))}</td>
                  <td className="px-4 py-3">
                    {String(pick(row, "statusLabel", "StatusLabel", "status", "Status") ?? "—")}
                  </td>
                  <td className="px-4 py-3">
                    <Button
                      size="icon"
                      variant="ghost"
                      title="Otvori detalje"
                      onClick={() => setSelectedId(id)}
                    >
                      <Eye className="size-4" />
                    </Button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {!query.isLoading && !rows.length && (
          <p className="p-8 text-center text-text-secondary">Nema protokolarnih zapisa.</p>
        )}
      </div>
      <Dialog open={Boolean(selectedId)} onOpenChange={(open) => !open && setSelectedId(undefined)}>
        <DialogContent className="max-h-[85vh] max-w-2xl overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Detalj protokola</DialogTitle>
            <DialogDescription>Potpuna evidencija za odabranu narudžbu.</DialogDescription>
          </DialogHeader>
          {detail.isLoading ? (
            <p>Učitavanje…</p>
          ) : (
            <dl className="grid gap-3 sm:grid-cols-2">
              {Object.entries((detail.data?.["data"] as Row | undefined) ?? detail.data ?? {}).map(
                ([key, value]) => (
                  <div className="border-b border-border-subtle pb-2" key={key}>
                    <dt className="text-xs font-bold uppercase text-text-tertiary">{human(key)}</dt>
                    <dd className="mt-1 break-words text-sm">{format(value)}</dd>
                  </div>
                ),
              )}
            </dl>
          )}
        </DialogContent>
      </Dialog>
    </section>
  );
}
const date = (value: unknown) =>
  value
    ? new Intl.DateTimeFormat("bs-BA", { dateStyle: "medium", timeStyle: "short" }).format(
        new Date(String(value)),
      )
    : "—";
const human = (value: string) =>
  value.replace(/([a-z])([A-Z])/g, "$1 $2").replace(/^./, (char) => char.toUpperCase());
const format = (value: unknown) =>
  value == null ? "—" : typeof value === "object" ? JSON.stringify(value) : String(value);
