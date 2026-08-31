import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Download, RefreshCw, Send } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Heading, Text } from "@/components/ui/typography";
import { downloadAuthenticatedFile } from "@/lib/api/file-client";
import { apiClient } from "@/lib/api/http-client";

type Row = Readonly<Record<string, unknown>>;
const pick = (row: Row, ...keys: string[]) =>
  keys.map((key) => row[key]).find((value) => value != null);
const unwrap = (raw: unknown): Row[] => {
  const root = (raw as Row)?.["data"] ?? raw;
  const items = Array.isArray(root) ? root : ((root as Row)?.["items"] ?? (root as Row)?.["Items"]);
  return Array.isArray(items) ? (items as Row[]) : [];
};

export function ReportsPage() {
  const cache = useQueryClient();
  const [endDate, setEndDate] = useState("");
  const [asOfDate, setAsOfDate] = useState("");
  const [option, setOption] = useState(1);
  const [minDays, setMinDays] = useState(5);
  const orders = useQuery({
    queryKey: ["reports", "orders", endDate],
    queryFn: async () =>
      unwrap(
        await apiClient.getLegacy("/api/reports/orders", {
          query: { format: "json", endDate: endDate || undefined },
        }),
      ),
  });
  const reminders = useQuery({
    queryKey: ["reports", "reminders", minDays],
    queryFn: async () =>
      unwrap(
        await apiClient.getLegacy("/api/reports/appraiser-reminders/", {
          query: { minBusinessDaysOverdue: minDays, pageSize: 200 },
        }),
      ),
  });
  const send = useMutation({
    mutationFn: (orderId: number) =>
      apiClient.postLegacy(`/api/reports/appraiser-reminders/${orderId}/send`),
    onSuccess: () => cache.invalidateQueries({ queryKey: ["reports", "reminders"] }),
  });
  return (
    <section>
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-eyebrow text-text-tertiary">Analitika</p>
          <Heading level={1} size={4} className="mt-2">
            Izvještaji
          </Heading>
          <Text tone="secondary" className="mt-2">
            Operativni pregled, Excel izvještaji koncentracije i rokova te podsjetnici vještacima.
          </Text>
        </div>
        <Button
          variant="secondary"
          onClick={() => {
            orders.refetch();
            reminders.refetch();
          }}
        >
          <RefreshCw className="size-4" />
          Osvježi
        </Button>
      </div>
      <div className="mt-7 grid gap-4 lg:grid-cols-2">
        <div className="rounded-sm border border-border-subtle bg-surface-default p-5">
          <h2 className="font-bold">Vremena obrade narudžbi</h2>
          <label className="mt-4 grid gap-1 text-sm font-semibold">
            Presjek do datuma
            <Input
              type="date"
              value={endDate}
              onChange={(event) => setEndDate(event.target.value)}
            />
          </label>
          <Button
            className="mt-3"
            variant="secondary"
            onClick={() =>
              downloadAuthenticatedFile(
                `/api/reports/orders?format=xlsx${endDate ? `&endDate=${endDate}` : ""}`,
                "vremena-obrade.xlsx",
              )
            }
          >
            <Download className="size-4" />
            Preuzmi Excel
          </Button>
          <Button
            className="mt-3 ml-2"
            variant="secondary"
            onClick={() =>
              downloadAuthenticatedFile(
                `/api/reports/timeline${endDate ? `?endDate=${endDate}` : ""}`,
                "vremenska-linija-narudzbi.xlsx",
              )
            }
          >
            <Download className="size-4" />
            Detaljna vremenska linija
          </Button>
        </div>
        <div className="rounded-sm border border-border-subtle bg-surface-default p-5">
          <h2 className="font-bold">Koncentracija vještaka</h2>
          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            <label className="grid gap-1 text-sm font-semibold">
              Opcija
              <select
                className="h-10 rounded-sm border border-border-subtle bg-surface-default px-3"
                value={option}
                onChange={(event) => setOption(Number(event.target.value))}
              >
                {[1, 2, 3, 4, 5].map((value) => (
                  <option key={value} value={value}>
                    Opcija {value}
                  </option>
                ))}
              </select>
            </label>
            <label className="grid gap-1 text-sm font-semibold">
              Datum presjeka
              <Input
                type="date"
                value={asOfDate}
                onChange={(event) => setAsOfDate(event.target.value)}
              />
            </label>
          </div>
          <Button
            className="mt-3"
            variant="secondary"
            onClick={() =>
              downloadAuthenticatedFile(
                `/api/reports/concentration?option=${option}${asOfDate ? `&asOfDate=${asOfDate}` : ""}`,
                "koncentracija-vjestaka.xlsx",
              )
            }
          >
            <Download className="size-4" />
            Preuzmi Excel
          </Button>
        </div>
      </div>
      <div className="mt-6 rounded-sm border border-border-subtle bg-surface-default p-5">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h2 className="font-bold">Zakašnjele procjene</h2>
            <p className="text-sm text-text-secondary">
              Narudžbe za koje je moguće poslati podsjetnik vještaku.
            </p>
          </div>
          <label className="grid gap-1 text-xs font-semibold">
            Minimalno radnih dana
            <Input
              className="w-32"
              type="number"
              min={1}
              value={minDays}
              onChange={(event) => setMinDays(Number(event.target.value))}
            />
          </label>
        </div>
        <div className="mt-4 divide-y divide-border-subtle">
          {reminders.data?.map((row, index) => {
            const orderId = Number(pick(row, "orderId", "OrderId", "id", "Id"));
            return (
              <div
                className="flex flex-wrap items-center justify-between gap-3 py-3"
                key={orderId || index}
              >
                <div>
                  <p className="font-semibold">
                    {String(
                      pick(row, "orderNumber", "OrderNumber", "clientName", "ClientName") ??
                        `Narudžba #${orderId}`,
                    )}
                  </p>
                  <p className="text-xs text-text-secondary">
                    {String(pick(row, "appraiserName", "AppraiserName") ?? "—")} ·{" "}
                    {String(pick(row, "businessDaysOverdue", "BusinessDaysOverdue") ?? "—")} radnih
                    dana
                  </p>
                </div>
                <Button
                  size="sm"
                  variant="secondary"
                  disabled={send.isPending}
                  onClick={() => send.mutate(orderId)}
                >
                  <Send className="size-4" />
                  Pošalji podsjetnik
                </Button>
              </div>
            );
          })}
          {!reminders.isLoading && !reminders.data?.length && (
            <p className="py-4 text-sm text-text-secondary">Nema zakašnjelih procjena.</p>
          )}
        </div>
      </div>
      <div className="mt-6 overflow-x-auto rounded-sm border border-border-subtle bg-surface-default">
        <table className="w-full text-left text-sm">
          <thead className="bg-surface-subtle">
            <tr>
              {["Narudžba", "Klijent", "Status", "Kreirano", "Poslano", "Završeno"].map((label) => (
                <th className="px-4 py-3" key={label}>
                  {label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle">
            {orders.data?.map((row, index) => (
              <tr key={index}>
                <td className="px-4 py-3 font-semibold">
                  {String(pick(row, "orderNumber", "OrderNumber") ?? "—")}
                </td>
                <td className="px-4 py-3">
                  {String(pick(row, "clientName", "ClientName") ?? "—")}
                </td>
                <td className="px-4 py-3">
                  {String(pick(row, "statusLabel", "StatusLabel", "status", "Status") ?? "—")}
                </td>
                <td className="px-4 py-3">{formatDate(pick(row, "createdAt", "CreatedAt"))}</td>
                <td className="px-4 py-3">
                  {formatDate(pick(row, "sentAt", "SentAt", "submittedAt", "SubmittedAt"))}
                </td>
                <td className="px-4 py-3">{formatDate(pick(row, "completedAt", "CompletedAt"))}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
const formatDate = (value: unknown) =>
  value ? new Intl.DateTimeFormat("bs-BA").format(new Date(String(value))) : "—";
