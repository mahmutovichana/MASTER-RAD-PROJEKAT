import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft, Download, FileText, Pencil, RefreshCw } from "lucide-react";
import { useState } from "react";

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
import { downloadAuthenticatedFile } from "@/lib/api/file-client";
import { apiClient } from "@/lib/api/http-client";
import { profileList, useProfile } from "@/lib/auth/use-profile";

import { getOrder, getOrderCollection, runOrderAction, type OrderRecord } from "./orders-api";
import { OrderDocumentsPanel } from "./order-documents-panel";
import { OrderEditDialog } from "./order-edit-dialog";
import { OpinionUpload } from "./opinion-upload";
import { OrderQuotesPanel } from "./order-quotes-panel";

interface Field {
  readonly key: string;
  readonly label: string;
  readonly type?: string;
  readonly required?: boolean;
}
interface Action {
  readonly suffix: string;
  readonly label: string;
  readonly danger?: boolean;
  readonly fields?: readonly Field[] | undefined;
  readonly capability?: string;
  readonly permission?: string;
  readonly roleStatus?: "appraiser-accept" | "appraiser-work" | "appraiser-original";
}
const actions: readonly Action[] = [
  { suffix: "submit", label: "Pošalji CA-u", capability: "canSubmit" },
  {
    suffix: "select-appraiser/auto",
    label: "Automatski odaberi vještaka",
    capability: "canSelectAppraiser",
  },
  {
    suffix: "select-appraiser/manual",
    label: "Ručno odaberi vještaka",
    capability: "canSelectAppraiser",
    fields: [{ key: "appraiserId", label: "ID vještaka", type: "number", required: true }],
  },
  { suffix: "send-to-appraiser", label: "Pošalji vještaku", capability: "canSendToAppraiser" },
  { suffix: "accept-by-appraiser", label: "Prihvati kao vještak", roleStatus: "appraiser-accept" },
  {
    suffix: "reject-by-appraiser",
    label: "Odbij kao vještak",
    danger: true,
    roleStatus: "appraiser-accept",
    fields: [
      { key: "reason", label: "Šifra razloga odbijanja", type: "number", required: true },
      { key: "comment", label: "Komentar" },
    ],
  },
  {
    suffix: "request-additional-payment",
    label: "Traži dodatnu uplatu",
    capability: "canRequestAdditionalPayment",
    fields: undefined,
  },
  {
    suffix: "confirm-additional-payment",
    label: "Potvrdi dodatnu uplatu",
    capability: "canCompleteAdditionalPayment",
  },
  {
    suffix: "submit-appraisal",
    label: "Predaj procjenu",
    roleStatus: "appraiser-work",
    fields: [{ key: "visitDate", label: "Datum posjete", type: "datetime-local" }],
  },
  {
    suffix: "request-correction",
    label: "Traži korekciju",
    capability: "canRequestCorrection",
    fields: [
      { key: "reasonCodeId", label: "Šifra razloga", type: "number", required: true },
      { key: "comment", label: "Komentar" },
    ],
  },
  {
    suffix: "submit-correction",
    label: "Predaj korekciju",
    capability: "canSubmitCorrection",
    fields: [{ key: "comment", label: "Komentar" }],
  },
  {
    suffix: "complete-review",
    label: "Završi pregled dokumentacije",
    capability: "canCompleteReview",
  },
  {
    suffix: "access-check/approve",
    label: "Potvrdi uredan pristup",
    capability: "canAccessCheck",
    fields: [{ key: "comment", label: "Komentar" }],
  },
  {
    suffix: "access-check/reject",
    label: "Traži dopunu pristupa",
    danger: true,
    capability: "canAccessCheck",
    fields: [{ key: "comment", label: "Obrazloženje", required: true }],
  },
  {
    suffix: "approve-final",
    label: "Odobri finalnu procjenu",
    capability: "canApproveFinal",
    fields: [{ key: "appraiserRating", label: "Ocjena vještaka (1–5)", type: "number" }],
  },
  {
    suffix: "return-for-rework",
    label: "Vrati na doradu",
    danger: true,
    capability: "canReturnForRework",
    fields: [
      { key: "category", label: "Kategorija", required: true },
      { key: "comment", label: "Komentar", required: true },
    ],
  },
  { suffix: "sign-consent", label: "Potpiši saglasnost", capability: "canSignConsent" },
  { suffix: "confirm-original", label: "Potvrdi original", capability: "canConfirmOriginal" },
  {
    suffix: "deliver-original",
    label: "Evidentiraj dostavu originala",
    roleStatus: "appraiser-original",
  },
  {
    suffix: "complete-signed-docs",
    label: "Završi potpisanu dokumentaciju",
    roleStatus: "appraiser-work",
  },
  {
    suffix: "remind-appraiser",
    label: "Pošalji podsjetnik vještaku",
    capability: "canRemindAppraiser",
  },
  {
    suffix: "quote-requests",
    label: "Pošalji zahtjeve za ponudu",
    capability: "canSendQuoteRequests",
    fields: [
      {
        key: "appraiserIds",
        label: "ID-evi vještaka (odvojeni zarezom)",
        type: "number-list",
        required: true,
      },
      { key: "deadline", label: "Rok za ponudu", type: "datetime-local", required: true },
    ],
  },
  {
    suffix: "quote-requests/thank-you",
    label: "Pošalji zahvalnice",
    capability: "canSendThankYou",
  },
  {
    suffix: "invoice/upload",
    label: "Poveži fakturu",
    capability: "canUploadInvoice",
    fields: [
      { key: "documentId", label: "ID uploadovanog dokumenta", type: "number", required: true },
    ],
  },
  {
    suffix: "invoice/send-for-payment",
    label: "Pošalji fakturu na plaćanje",
    capability: "canSendInvoiceForPayment",
  },
  {
    suffix: "invoice/confirm-paid",
    label: "Potvrdi plaćanje fakture",
    capability: "canConfirmInvoicePaid",
  },
  {
    suffix: "opinions/request",
    label: "Zatraži mišljenja CO i Pravne",
    permission: "opinions.request",
  },
  {
    suffix: "reject-order",
    label: "Odbij narudžbu",
    danger: true,
    fields: [
      { key: "reason", label: "Razlog", required: true },
      { key: "comment", label: "Komentar" },
    ],
  },
];

export function OrderDetailPage({ id }: { readonly id: number }) {
  const cache = useQueryClient();
  const [chosen, setChosen] = useState<Action>();
  const [payload, setPayload] = useState<Record<string, unknown>>({});
  const [editOpen, setEditOpen] = useState(false);
  const profile = useProfile();
  const detail = useQuery({ queryKey: ["orders", id], queryFn: () => getOrder(id) });
  const opinions = useQuery({
    queryKey: ["orders", id, "opinions"],
    queryFn: () => getOrderCollection(id, "opinions"),
  });
  const candidates = useQuery({
    queryKey: ["orders", id, "appraiser-candidates"],
    queryFn: () => getOrderCollection(id, "appraiser-candidates"),
    enabled: capabilityRecord(detail.data)["canSelectAppraiser"] === true,
  });
  const appraisalStatus = useQuery({
    queryKey: ["orders", id, "appraisal-status"],
    queryFn: () => apiClient.getLegacy<OrderRecord>(`/api/orders/${id}/appraisal-status`),
  });
  const invoiceStatus = useQuery({
    queryKey: ["orders", id, "invoice-status"],
    queryFn: () => apiClient.getLegacy<OrderRecord>(`/api/orders/${id}/invoice/status`),
    enabled: permissionsForProfile(profile.data).includes("invoice.view"),
  });
  const appraiserPackage = useQuery({
    queryKey: ["orders", id, "appraiser-package"],
    queryFn: () => apiClient.getLegacy<OrderRecord>(`/api/orders/${id}/appraiser-package`),
    enabled: false,
  });
  const mutation = useMutation({
    mutationFn: ({ suffix, body }: { suffix: string; body?: unknown }) =>
      runOrderAction(id, suffix, body),
    onSuccess: async () => {
      setChosen(undefined);
      setPayload({});
      await cache.invalidateQueries({ queryKey: ["orders"] });
    },
  });
  const execute = (action: Action) =>
    action.fields?.length
      ? setChosen(action)
      : confirm(`Izvršiti akciju „${action.label}”?`) && mutation.mutate({ suffix: action.suffix });
  const capabilities = capabilityRecord(detail.data);
  const roles = profileList(profile.data, "roles").map((role) => role.toLocaleLowerCase("bs"));
  const permissions = profileList(profile.data, "permissions");
  const status = label(detail.data, "status", "Status");
  const visibleActions = actions.filter(
    (action) =>
      isActionVisible(action, capabilities, roles, permissions, status) &&
      (action.suffix !== "opinions/request" || opinions.data?.length === 0),
  );
  const downloadFinal = async () => {
    const raw = await apiClient.getLegacy<OrderRecord>(`/api/orders/${id}/final-appraisal`);
    const item = (raw["data"] as OrderRecord | undefined) ?? raw;
    await downloadAuthenticatedFile(
      String(item["downloadUrl"] ?? item["DownloadUrl"]),
      String(item["originalFileName"] ?? item["OriginalFileName"] ?? `procjena-${id}.pdf`),
    );
  };
  return (
    <section>
      <a
        href="/app/orders"
        className="inline-flex items-center gap-2 text-sm font-semibold text-text-secondary"
      >
        <ArrowLeft className="size-4" />
        Nazad na narudžbe
      </a>
      <div className="mt-5 flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-eyebrow text-text-tertiary">Narudžba #{id}</p>
          <Heading level={1} size={4} className="mt-2">
            {label(detail.data, "title", "Title", "orderNumber", "OrderNumber")}
          </Heading>
          <Text tone="secondary" className="mt-2">
            {label(detail.data, "clientName", "ClientName")} ·{" "}
            {label(detail.data, "statusLabel", "StatusLabel", "status", "Status")}
          </Text>
        </div>
        <div className="flex gap-2">
          {capabilities["canEdit"] === true && (
            <Button variant="secondary" onClick={() => setEditOpen(true)}>
              <Pencil className="size-4" />
              Uredi nacrt
            </Button>
          )}
          {capabilities["canDownloadFinal"] === true && (
            <Button variant="secondary" onClick={downloadFinal}>
              <Download className="size-4" />
              Finalna procjena
            </Button>
          )}
          <Button variant="secondary" onClick={() => detail.refetch()}>
            <RefreshCw className="size-4" />
            Osvježi
          </Button>
        </div>
      </div>
      {detail.isError && <p className="mt-6 p-4 text-feedback-danger">{detail.error.message}</p>}
      {detail.data && (
        <>
          <div className="mt-7 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
            {primitive(detail.data).map(([k, v]) => (
              <div
                className="rounded-sm border border-border-subtle bg-surface-default p-4"
                key={k}
              >
                <p className="text-xs font-bold uppercase text-text-tertiary">{humanize(k)}</p>
                <p className="mt-2 break-words text-sm font-semibold">{String(v ?? "—")}</p>
              </div>
            ))}
          </div>
          <div className="mt-8">
            <Heading level={2} size={2}>
              Workflow akcije
            </Heading>
            <div className="mt-4 flex flex-wrap gap-2">
              {visibleActions.map((a) => (
                <Button
                  key={a.suffix}
                  variant={a.danger ? "destructive" : "secondary"}
                  onClick={() => execute(a)}
                  disabled={mutation.isPending}
                >
                  {a.label}
                </Button>
              ))}
            </div>
            {mutation.error && (
              <p className="mt-3 text-feedback-danger">{mutation.error.message}</p>
            )}
          </div>
        </>
      )}
      <div className="mt-8 grid gap-5 xl:grid-cols-3">
        <StatusPanel title="Status izrade procjene" data={appraisalStatus.data} />
        {invoiceStatus.isSuccess && (
          <StatusPanel title="Status fakture" data={invoiceStatus.data} />
        )}
        {hasAppraiser(detail.data) && (
          <AppraiserPackagePanel
            data={appraiserPackage.data}
            loading={appraiserPackage.isFetching}
            onLoad={() => appraiserPackage.refetch()}
          />
        )}
        <OrderDocumentsPanel
          orderId={id}
          canGenerate={capabilities["canGenerateDocuments"] === true}
        />
        <OrderQuotesPanel orderId={id} />
        <Related title="Mišljenja" rows={opinions.data} />
        {Boolean(opinions.data?.length) &&
          permissions.some(
            (permission) =>
              permission === "opinions.submit-co" || permission === "opinions.submit-legal",
          ) && <OpinionUpload orderId={id} permissions={permissions} />}
      </div>
      {detail.data && (
        <OrderEditDialog id={id} order={detail.data} open={editOpen} onOpenChange={setEditOpen} />
      )}
      <Dialog open={Boolean(chosen)} onOpenChange={(open) => !open && setChosen(undefined)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{chosen?.label}</DialogTitle>
            <DialogDescription>Unesite podatke potrebne za nastavak workflowa.</DialogDescription>
          </DialogHeader>
          <form
            className="grid gap-4"
            onSubmit={(e) => {
              e.preventDefault();
              if (chosen) mutation.mutate({ suffix: chosen.suffix, body: payload });
            }}
          >
            {chosen?.fields?.map((f) => (
              <label className="grid gap-1 text-sm font-semibold" key={f.key}>
                {f.label}
                {f.key === "appraiserId" || f.key === "appraiserIds" ? (
                  <select
                    className="h-10 w-full rounded-sm border border-border-subtle bg-surface-default px-3"
                    required={f.required}
                    multiple={f.key === "appraiserIds"}
                    onChange={(event) => {
                      const selected = Array.from(event.target.selectedOptions).map((option) =>
                        Number(option.value),
                      );
                      setPayload({
                        ...payload,
                        [f.key]: f.key === "appraiserIds" ? selected : selected[0],
                      });
                    }}
                  >
                    {f.key === "appraiserId" && <option value="">Odaberite vještaka</option>}
                    {candidates.data?.map((candidate, index) => {
                      const candidateId = label(
                        candidate,
                        "id",
                        "Id",
                        "appraiserId",
                        "AppraiserId",
                      );
                      const candidateName = label(
                        candidate,
                        "name",
                        "Name",
                        "appraiserName",
                        "AppraiserName",
                      );
                      const city = label(candidate, "city", "City");
                      return (
                        <option key={`${candidateId}-${index}`} value={candidateId}>
                          {candidateName} · {city}
                        </option>
                      );
                    })}
                  </select>
                ) : (
                  <Input
                    required={f.required}
                    type={f.type ?? "text"}
                    onChange={(e) =>
                      setPayload({
                        ...payload,
                        [f.key]:
                          f.type === "number"
                            ? Number(e.target.value)
                            : f.type === "number-list"
                              ? e.target.value.split(",").map(Number).filter(Number.isFinite)
                              : e.target.value,
                      })
                    }
                  />
                )}
              </label>
            ))}
            <Button type="submit">Potvrdi akciju</Button>
          </form>
        </DialogContent>
      </Dialog>
    </section>
  );
}
function Related({
  title,
  rows,
}: {
  readonly title: string;
  readonly rows?: readonly OrderRecord[] | undefined;
}) {
  return (
    <div className="rounded-sm border border-border-subtle bg-surface-default p-5">
      <div className="flex items-center gap-2">
        <FileText className="size-4" />
        <h2 className="font-bold">{title}</h2>
      </div>
      <p className="mt-4 text-sm text-text-secondary">
        {rows ? `${rows.length} zapisa` : "Učitavanje…"}
      </p>
      {rows?.slice(0, 5).map((r, i) => (
        <div className="mt-3 border-t border-border-subtle pt-3 text-xs" key={i}>
          {primitive(r)
            .slice(0, 3)
            .map(([k, v]) => (
              <p key={k}>
                <b>{humanize(k)}:</b> {String(v ?? "—")}
              </p>
            ))}
        </div>
      ))}
    </div>
  );
}
function StatusPanel({ title, data }: { readonly title: string; readonly data?: OrderRecord | undefined }) {
  const root = ((data?.["data"] as OrderRecord | undefined) ?? data) as OrderRecord | undefined;
  return (
    <div className="rounded-sm border border-border-subtle bg-surface-default p-5">
      <h2 className="font-bold">{title}</h2>
      <div className="mt-3 grid gap-2 text-xs">
        {root ? (
          primitive(root).map(([key, value]) => (
            <p key={key}>
              <b>{humanize(key)}:</b> {String(value ?? "—")}
            </p>
          ))
        ) : (
          <p className="text-text-secondary">Učitavanje…</p>
        )}
      </div>
    </div>
  );
}
function AppraiserPackagePanel({
  data,
  loading,
  onLoad,
}: {
  readonly data?: OrderRecord | undefined;
  readonly loading: boolean;
  readonly onLoad: () => void;
}) {
  const root = ((data?.["data"] as OrderRecord | undefined) ?? data) as OrderRecord | undefined;
  const documents = (root?.["documents"] ?? root?.["Documents"]) as OrderRecord[] | undefined;
  return (
    <div className="rounded-sm border border-border-subtle bg-surface-default p-5">
      <div className="flex items-center justify-between gap-3">
        <h2 className="font-bold">Paket za vještaka</h2>
        <Button size="sm" variant="secondary" onClick={onLoad} disabled={loading}>
          {data ? "Ažuriraj" : "Prikaži"}
        </Button>
      </div>
      {documents?.map((document, index) => {
        const url = label(document, "downloadUrl", "DownloadUrl");
        const name = label(
          document,
          "displayName",
          "DisplayName",
          "originalFileName",
          "OriginalFileName",
        );
        return (
          <button
            type="button"
            className="mt-3 block text-left text-sm font-semibold text-text-link hover:underline"
            key={index}
            onClick={() => downloadAuthenticatedFile(url, name)}
          >
            {name}
          </button>
        );
      })}
      {data && !documents?.length && (
        <p className="mt-3 text-sm text-text-secondary">Nema dokumenata.</p>
      )}
    </div>
  );
}
const primitive = (r: OrderRecord) =>
  Object.entries(r).filter(
    ([, v]) => v == null || ["string", "number", "boolean"].includes(typeof v),
  );
const humanize = (v: string) =>
  v
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replaceAll("_", " ")
    .replace(/^./, (x) => x.toUpperCase());
const label = (r: OrderRecord | undefined, ...keys: string[]) =>
  String(keys.map((k) => r?.[k]).find((v) => v != null) ?? "—");

function capabilityRecord(order: OrderRecord | undefined): Readonly<Record<string, unknown>> {
  if (!order) return {};
  const value = order["capabilities"] ?? order["Capabilities"];
  return typeof value === "object" && value !== null
    ? (value as Readonly<Record<string, unknown>>)
    : {};
}

const permissionsForProfile = (profile: Readonly<Record<string, unknown>> | undefined) =>
  profileList(profile, "permissions");

const hasAppraiser = (order: OrderRecord | undefined) =>
  Boolean(order?.["appraiserId"] ?? order?.["AppraiserId"]);

function isActionVisible(
  action: Action,
  capabilities: Readonly<Record<string, unknown>>,
  roles: readonly string[],
  permissions: readonly string[],
  status: string,
) {
  if (action.suffix === "reject-order") {
    return capabilities["canRejectOrder"] === true || capabilities["canAdminRejectOrder"] === true;
  }
  if (action.capability) return capabilities[action.capability] === true;
  if (action.permission) return permissions.includes(action.permission);
  if (!action.roleStatus) return true;
  const isAppraiser = roles.some((role) => role.includes("vjestak") || role.includes("vještak"));
  if (!isAppraiser) return false;
  if (action.roleStatus === "appraiser-accept") return status === "OrderSentToAppraiser";
  if (action.roleStatus === "appraiser-original") {
    return status === "ReadyForProcedure" || status === "COApproved";
  }
  return [
    "OrderSentToAppraiser",
    "AppraisalInProgress",
    "AdditionalPaymentCompleted",
    "AppraisalReturnedForRework",
  ].includes(status);
}
