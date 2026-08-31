import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";
import { Copy, Plus, RefreshCw, Search, Send, Trash2 } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

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
import { profileList, useProfile } from "@/lib/auth/use-profile";
import { useBusinessText } from "@/localization/use-business-text";

import {
  cancelOrder,
  createOrder,
  listOrders,
  submitOrder,
  type CreateOrderRequest,
  type OrderRecord,
} from "./orders-api";

const emptyOrder: CreateOrderRequest = {
  clientName: "",
  clientType: "FL",
  clientIdentifier: "",
  collateralTypeId: 1,
  combinedCollateralTypeId: null,
  city: "",
  propertyAddress: "",
  branch: "",
  branchAddress: "",
  contactName: "",
  contactPhone: "",
  contactEmail: "",
  internalNote: "",
  deliveryContactName: "",
  amRecipientName: "",
};

export function OrdersPage() {
  const bt = useBusinessText();
  const navigate = useNavigate();
  const profile = useProfile();
  const permissions = profileList(profile.data, "permissions");
  const canCreate = permissions.includes("orders.create");
  const canSubmit = permissions.includes("orders.submit");
  const canCancel = permissions.includes("orders.cancel");
  const client = useQueryClient();
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [createOpen, setCreateOpen] = useState(false);
  const [detail, setDetail] = useState<OrderRecord>();
  const [form, setForm] = useState<CreateOrderRequest>(emptyOrder);
  const orders = useQuery({ queryKey: ["orders", search], queryFn: () => listOrders(search) });
  const collateralTypes = useQuery({
    queryKey: ["collateral-types"],
    queryFn: () => loadOptions("/api/codebooks/collateral-types"),
  });
  const combinedTypes = useQuery({
    queryKey: ["combined-collateral-types"],
    queryFn: () => loadOptions("/api/codebooks/combined-collateral-types"),
  });
  const cities = useQuery({
    queryKey: ["cities"],
    queryFn: () => loadOptions("/api/branches/cities", "name"),
  });
  const branches = useQuery({
    queryKey: ["branches"],
    queryFn: () => loadOptions("/api/branches/", "code"),
  });
  const selectedCityId = cities.data?.find((city) => city.value === form.city)?.id;
  const availableBranches = selectedCityId
    ? branches.data?.filter((branch) => branch.cityId === selectedCityId)
    : branches.data;
  const refresh = () => client.invalidateQueries({ queryKey: ["orders"] });
  const create = useMutation({
    mutationFn: createOrder,
    onSuccess: async () => {
      setCreateOpen(false);
      setForm(emptyOrder);
      await refresh();
      toast.success(bt("Nacrt narudžbe je kreiran.", "Order draft created."));
    },
    onError: (error) => toast.error(error.message),
  });
  const submit = useMutation({
    mutationFn: submitOrder,
    onSuccess: async () => {
      toast.success(bt("Narudžba je poslana.", "Order submitted."));
      await refresh();
    },
    onError: (error) => toast.error(error.message),
  });
  const cancel = useMutation({
    mutationFn: cancelOrder,
    onSuccess: async () => {
      toast.success(bt("Narudžba je otkazana.", "Order cancelled."));
      await refresh();
    },
    onError: (error) => toast.error(error.message),
  });

  const value = (row: OrderRecord, ...keys: string[]) =>
    keys.map((key) => row[key]).find((item) => item != null);
  const idOf = (row: OrderRecord) => Number(value(row, "id", "Id"));
  const visibleOrders = orders.data?.filter(
    (row) => !statusFilter || String(value(row, "status", "Status")) === statusFilter,
  );
  const cloneOrder = (row: OrderRecord) => {
    setForm({
      ...emptyOrder,
      ...Object.fromEntries(
        Object.keys(emptyOrder).map((key) => [
          key,
          value(row, key, key[0]!.toUpperCase() + key.slice(1)) ??
            emptyOrder[key as keyof CreateOrderRequest],
        ]),
      ),
      clientType: String(value(row, "clientType", "ClientType") ?? "FL"),
    } as CreateOrderRequest);
    setCreateOpen(true);
  };

  return (
    <section className="min-w-0">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-eyebrow text-text-tertiary">{bt("Radni proces", "Workflow")}</p>
          <Heading level={1} size={4} className="mt-2">
            {bt("Narudžbe procjene", "Appraisal orders")}
          </Heading>
          <Text tone="secondary" className="mt-2">
            {bt(
              "Kreiranje, pregled, slanje i upravljanje narudžbama procjene.",
              "Create, review, submit, and manage appraisal orders.",
            )}
          </Text>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => orders.refetch()}>
            <RefreshCw className="size-4" />
            {bt("Osvježi", "Refresh")}
          </Button>
          {canCreate && (
            <Button onClick={() => setCreateOpen(true)}>
              <Plus className="size-4" />
              {bt("Nova narudžba", "New order")}
            </Button>
          )}
        </div>
      </div>
      <div className="mt-6 flex max-w-3xl flex-wrap items-center gap-2">
        <Search className="size-4 text-text-tertiary" />
        <Input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder={bt("Broj, klijent, naslov ili grad…", "Number, client, title, or city…")}
        />
        <select
          className="h-10 min-w-44 rounded-sm border border-border-subtle bg-surface-default px-3"
          value={statusFilter}
          onChange={(event) => setStatusFilter(event.target.value)}
        >
          <option value="">{bt("Svi statusi", "All statuses")}</option>
          {[...new Set(orders.data?.map((row) => String(value(row, "status", "Status"))) ?? [])]
            .filter(Boolean)
            .map((status) => (
              <option key={status}>{status}</option>
            ))}
        </select>
      </div>
      <div className="mt-6 overflow-x-auto rounded-sm border border-border-subtle bg-surface-default">
        {orders.isLoading && <p className="p-8 text-text-secondary">Učitavanje narudžbi…</p>}
        {orders.isError && <p className="p-8 text-feedback-danger">{orders.error.message}</p>}
        {orders.data && (
          <table className="min-w-full text-left text-sm">
            <thead className="bg-surface-subtle text-text-secondary">
              <tr>
                {[
                  bt("Broj", "Number"),
                  bt("Klijent", "Client"),
                  bt("Grad", "City"),
                  bt("Status", "Status"),
                  bt("Kreirano", "Created"),
                  bt("Akcije", "Actions"),
                ].map((x) => (
                  <th className="px-4 py-3" key={x}>
                    {x}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle">
              {visibleOrders?.map((row, index) => {
                const status = String(value(row, "status", "Status") ?? "");
                const isDraft = status === "Draft" || status === "0";
                return (
                  <tr key={idOf(row) || index} className="hover:bg-surface-subtle">
                    <td className="px-4 py-3 font-bold">
                      <button onClick={() => setDetail(row)}>
                        {String(value(row, "orderNumber", "OrderNumber") ?? "—")}
                      </button>
                    </td>
                    <td className="px-4 py-3">
                      {String(value(row, "clientName", "ClientName") ?? "—")}
                    </td>
                    <td className="px-4 py-3">{String(value(row, "city", "City") ?? "—")}</td>
                    <td className="px-4 py-3">
                      {String(value(row, "simpleStatusLabel", "status", "Status") ?? "—")}
                    </td>
                    <td className="px-4 py-3">
                      {formatDate(value(row, "createdAt", "CreatedAt"))}
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center justify-end gap-1">
                        <Button
                          size="sm"
                          variant="secondary"
                          onClick={() =>
                            navigate({ to: "/app/orders/$id", params: { id: String(idOf(row)) } })
                          }
                        >
                          {bt("Detalji", "Details")}
                        </Button>
                        {canCreate && (
                          <Button
                            size="icon"
                            variant="ghost"
                            title={bt("Kloniraj", "Clone")}
                            aria-label={bt("Kloniraj narudžbu", "Clone order")}
                            onClick={() => cloneOrder(row)}
                          >
                            <Copy className="size-4" />
                          </Button>
                        )}
                        {isDraft && canSubmit && (
                          <Button
                            size="icon"
                            variant="ghost"
                            title={bt("Pošalji", "Submit")}
                            aria-label={bt("Pošalji narudžbu", "Submit order")}
                            onClick={() => submit.mutate(idOf(row))}
                          >
                            <Send className="size-4" />
                          </Button>
                        )}
                        {isDraft && canCancel && (
                          <Button
                            size="icon"
                            variant="ghost"
                            title={bt("Otkaži", "Cancel")}
                            aria-label={bt("Otkaži narudžbu", "Cancel order")}
                            onClick={() =>
                              confirm(bt("Otkazati narudžbu?", "Cancel this order?")) &&
                              cancel.mutate(idOf(row))
                            }
                          >
                            <Trash2 className="size-4" />
                          </Button>
                        )}
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
        {!orders.isLoading && !orders.isError && visibleOrders?.length === 0 && (
          <p className="p-8 text-center text-text-secondary">
            {bt("Nema narudžbi za odabrane filtere.", "No orders match the selected filters.")}
          </p>
        )}
      </div>
      <Dialog open={createOpen} onOpenChange={setCreateOpen}>
        <DialogContent className="max-h-[90vh] max-w-3xl overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Nova narudžba</DialogTitle>
            <DialogDescription>
              Unesite obavezne podatke. Narudžba se kreira kao nacrt.
            </DialogDescription>
          </DialogHeader>
          <form
            className="grid gap-4 sm:grid-cols-2"
            onSubmit={(e) => {
              e.preventDefault();
              create.mutate(form);
            }}
          >
            {fields.map(([key, label, type]) => (
              <label className="grid gap-1 text-sm font-semibold" key={key}>
                {label}
                {key === "clientType" ? (
                  <select
                    className="h-10 rounded-sm border border-border-subtle bg-surface-default px-3"
                    value={String(form.clientType ?? "FL")}
                    onChange={(event) => setForm({ ...form, clientType: event.target.value })}
                  >
                    <option value="FL">Fizičko lice</option>
                    <option value="PL">Pravno lice</option>
                  </select>
                ) : key === "collateralTypeId" ? (
                  <OptionSelect
                    required
                    options={collateralTypes.data}
                    value={form.collateralTypeId}
                    onChange={(value) => setForm({ ...form, collateralTypeId: Number(value) })}
                  />
                ) : key === "combinedCollateralTypeId" ? (
                  <OptionSelect
                    options={combinedTypes.data}
                    value={form.combinedCollateralTypeId ?? ""}
                    onChange={(value) =>
                      setForm({ ...form, combinedCollateralTypeId: value ? Number(value) : null })
                    }
                  />
                ) : key === "city" ? (
                  <OptionSelect
                    required
                    options={cities.data}
                    value={form.city}
                    onChange={(value) =>
                      setForm({ ...form, city: value, branch: "", branchAddress: "" })
                    }
                  />
                ) : key === "branch" ? (
                  <OptionSelect
                    required
                    options={availableBranches}
                    value={form.branch}
                    onChange={(value) => {
                      const selected = branches.data?.find((branch) => branch.value === value);
                      setForm({ ...form, branch: value, branchAddress: selected?.address ?? "" });
                    }}
                  />
                ) : (
                  <Input
                    required={required.has(key)}
                    type={type}
                    value={String(form[key] ?? "")}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        [key]: type === "number" ? Number(e.target.value) : e.target.value,
                      })
                    }
                  />
                )}
              </label>
            ))}
            <div className="sm:col-span-2 flex justify-end gap-2">
              <Button type="button" variant="secondary" onClick={() => setCreateOpen(false)}>
                Odustani
              </Button>
              <Button type="submit" disabled={create.isPending}>
                Kreiraj nacrt
              </Button>
            </div>
            {create.error && (
              <p className="sm:col-span-2 text-feedback-danger">{create.error.message}</p>
            )}
          </form>
        </DialogContent>
      </Dialog>
      <Dialog open={Boolean(detail)} onOpenChange={(open) => !open && setDetail(undefined)}>
        <DialogContent className="max-h-[85vh] max-w-2xl overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Detalji narudžbe</DialogTitle>
            <DialogDescription>Kompletan odgovor postojećeg API-ja.</DialogDescription>
          </DialogHeader>
          <dl className="grid gap-3 sm:grid-cols-2">
            {detail &&
              Object.entries(detail)
                .filter(([, v]) => v == null || ["string", "number", "boolean"].includes(typeof v))
                .map(([k, v]) => (
                  <div key={k} className="border-b border-border-subtle pb-2">
                    <dt className="text-xs font-bold uppercase text-text-tertiary">
                      {humanize(k)}
                    </dt>
                    <dd className="mt-1 break-words text-sm">{String(v ?? "—")}</dd>
                  </div>
                ))}
          </dl>
        </DialogContent>
      </Dialog>
    </section>
  );
}

const fields: readonly [keyof CreateOrderRequest, string, string][] = [
  ["clientName", "Naziv klijenta", "text"],
  ["clientType", "Tip klijenta (FL/PL)", "text"],
  ["clientIdentifier", "JMBG/ID broj", "text"],
  ["collateralTypeId", "Tip kolaterala ID", "number"],
  ["combinedCollateralTypeId", "Kombinovani tip kolaterala", "number"],
  ["city", "Grad", "text"],
  ["propertyAddress", "Adresa nekretnine", "text"],
  ["branch", "Poslovnica", "text"],
  ["branchAddress", "Adresa poslovnice", "text"],
  ["contactName", "Kontakt osoba", "text"],
  ["contactPhone", "Telefon", "tel"],
  ["contactEmail", "E-mail", "email"],
  ["deliveryContactName", "Osoba za dostavu", "text"],
  ["amRecipientName", "Account manager", "text"],
  ["internalNote", "Interna napomena", "text"],
];
const required = new Set<keyof CreateOrderRequest>([
  "clientName",
  "collateralTypeId",
  "city",
  "branch",
  "contactName",
  "contactPhone",
  "deliveryContactName",
  "amRecipientName",
]);
const humanize = (v: string) =>
  v.replace(/([a-z])([A-Z])/g, "$1 $2").replace(/^./, (x) => x.toUpperCase());
const formatDate = (v: unknown) =>
  v ? new Intl.DateTimeFormat("bs-BA").format(new Date(String(v))) : "—";

interface OptionItem {
  readonly value: string;
  readonly label: string;
  readonly id?: number | undefined;
  readonly cityId?: number | undefined;
  readonly address?: string | undefined;
}
async function loadOptions(path: string, valueField?: "name" | "code"): Promise<OptionItem[]> {
  const raw = await apiClient.getLegacy<unknown>(path);
  const envelope = raw as Readonly<Record<string, unknown>>;
  const root = envelope["data"] ?? raw;
  const source = Array.isArray(root)
    ? root
    : ((root as Readonly<Record<string, unknown>>)?.["items"] ??
      (root as Readonly<Record<string, unknown>>)?.["Items"]);
  if (!Array.isArray(source)) return [];
  return source.map((item) => {
    const row = item as Readonly<Record<string, unknown>>;
    const preferred =
      valueField === "name"
        ? (row["name"] ?? row["Name"])
        : valueField === "code"
          ? (row["code"] ?? row["Code"])
          : undefined;
    const id =
      preferred ??
      row["id"] ??
      row["Id"] ??
      row["code"] ??
      row["Code"] ??
      row["name"] ??
      row["Name"];
    const labelValue =
      row["label"] ??
      row["Label"] ??
      row["name"] ??
      row["Name"] ??
      row["city"] ??
      row["City"] ??
      id;
    return {
      value: String(id ?? ""),
      label: String(labelValue ?? ""),
      id: Number(row["id"] ?? row["Id"]) || undefined,
      cityId: Number(row["cityId"] ?? row["CityId"]) || undefined,
      address: String(row["address"] ?? row["Address"] ?? "") || undefined,
    };
  });
}
function OptionSelect({
  options,
  value,
  onChange,
  required = false,
}: {
  readonly options?: readonly OptionItem[] | undefined;
  readonly value: string | number;
  readonly onChange: (value: string) => void;
  readonly required?: boolean;
}) {
  return (
    <select
      required={required}
      className="h-10 rounded-sm border border-border-subtle bg-surface-default px-3"
      value={String(value)}
      onChange={(event) => onChange(event.target.value)}
    >
      <option value="">Odaberite…</option>
      {options?.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
}
