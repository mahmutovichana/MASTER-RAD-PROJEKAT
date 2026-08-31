import { useMutation, useQuery } from "@tanstack/react-query";
import { AlertCircle, Check, Copy } from "lucide-react";
import { type FormEvent, useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ApiError, apiClient } from "@/lib/api/http-client";
import type { RegistryResource } from "@/lib/registry/resources";

type RecordValue = string | number | boolean | null | undefined | readonly unknown[] | Record<string, unknown>;
type KnownFields = {
  readonly id?: RecordValue; readonly naziv?: RecordValue; readonly name?: RecordValue;
  readonly opis?: RecordValue; readonly boja?: RecordValue; readonly tag?: RecordValue;
  readonly prioritet?: RecordValue; readonly tip?: RecordValue; readonly groupId?: RecordValue;
  readonly runSequentially?: RecordValue; readonly rest?: RecordValue; readonly ui?: RecordValue;
  readonly blazor?: RecordValue; readonly cronExpression?: RecordValue; readonly timezone?: RecordValue;
  readonly isActive?: RecordValue; readonly expiresAt?: RecordValue;
};
type NestedFields = Record<string, unknown> & {
  id?: unknown; naziv?: unknown; name?: unknown; group?: unknown; children?: unknown;
  metoda?: unknown; url?: unknown; ocekivaniStatus?: unknown; requestBody?: unknown;
  headeri?: unknown; responseAsserti?: unknown; urlStranice?: unknown; koraci?: unknown;
  componentName?: unknown; razorContent?: unknown; rawKey?: unknown;
};
export type ResourceRecord = Readonly<Record<string, RecordValue>> & KnownFields;
type GroupOption = { id: string; name: string };
type ScenarioType = "Rest" | "Ui" | "Blazor";

export function ResourceFormDialog({
  resource,
  record,
  open,
  onOpenChange,
  onSaved,
}: {
  resource: RegistryResource;
  record: ResourceRecord | undefined;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSaved: () => void | Promise<void>;
}) {
  const { t } = useTranslation("registry");
  const [clientError, setClientError] = useState<string>();
  const [createdSecret, setCreatedSecret] = useState<string>();
  const [copied, setCopied] = useState(false);
  const isEditing = Boolean(record?.id);
  const details = useQuery({
    queryKey: ["test-automation", resource.key, "detail", record?.id],
    queryFn: () => apiClient.get<ResourceRecord>(`${resource.endpoint}/${String(record?.id)}`),
    enabled: open && isEditing && resource.key === "scenarios",
  });
  const groups = useQuery({
    queryKey: ["test-automation", "groups", "form-options"],
    queryFn: () => apiClient.get<unknown>("/api/frontend/groups"),
    enabled: open && (resource.key === "scenarios" || resource.key === "schedules"),
  });
  const groupOptions = useMemo(() => flattenGroupOptions(groups.data), [groups.data]);
  const initial = details.data ?? record;
  const mutation = useMutation({
    mutationFn: (body: unknown) => isEditing
      ? apiClient.put<void>(`${resource.endpoint}/${String(record?.id)}`, { body })
      : apiClient.post<unknown>(resource.endpoint!, { body }),
    onSuccess: async (response) => {
      await onSaved();
      const result = object(response);
      if (resource.key === "apiKeys" && typeof result?.rawKey === "string") {
        setCreatedSecret(result.rawKey);
      } else {
        onOpenChange(false);
      }
    },
  });

  useEffect(() => {
    if (open) { setClientError(undefined); setCreatedSecret(undefined); setCopied(false); }
  }, [open, record?.id]);

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setClientError(undefined);
    const result = buildPayload(resource.key, new FormData(event.currentTarget));
    if (result.error) {
      setClientError(result.error);
      return;
    }
    mutation.mutate(result.body);
  }

  const title = isEditing ? t("forms.editTitle") : t(`forms.${resource.key}.title` as never);
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-h-[calc(100vh-2rem)] overflow-y-auto bg-surface-raised text-text-primary sm:max-w-5xl">
        {createdSecret ? <div>
          <DialogHeader><DialogTitle>{t("apiKeys.createdTitle")}</DialogTitle><DialogDescription>{t("apiKeys.createdDescription")}</DialogDescription></DialogHeader>
          <div className="mt-6 rounded-sm border border-feedback-success bg-feedback-success-subtle p-4">
            <code className="block break-all text-sm text-text-primary">{createdSecret}</code>
            <Button type="button" variant="secondary" className="mt-4" onClick={async () => { await navigator.clipboard.writeText(createdSecret); setCopied(true); }}>
              {copied ? <Check className="size-4" /> : <Copy className="size-4" />}{copied ? t("apiKeys.copied") : t("apiKeys.copy")}
            </Button>
          </div>
          <DialogFooter className="mt-7"><Button type="button" onClick={() => onOpenChange(false)}>{t("actions.confirm")}</Button></DialogFooter>
        </div> : <form key={`${resource.key}-${String(record?.id ?? "new")}-${String(details.data?.id ?? "")}`} onSubmit={submit}>
          <DialogHeader>
            <DialogTitle>{title}</DialogTitle>
            <DialogDescription>{t(`forms.${resource.key}.description` as never)}</DialogDescription>
          </DialogHeader>
          {details.isLoading ? (
            <p className="mt-6 text-sm text-text-secondary">{t("states.loading")}</p>
          ) : (
            <div className="mt-6 grid gap-x-5 gap-y-4 md:grid-cols-2">
              <ResourceFields resourceKey={resource.key} initial={initial} groups={groupOptions} />
            </div>
          )}
          {(clientError || mutation.isError || details.isError || groups.isError) && (
            <ErrorBanner message={clientError ?? readableError(mutation.error ?? details.error ?? groups.error)} />
          )}
          <DialogFooter className="mt-7">
            <Button type="button" variant="secondary" onClick={() => onOpenChange(false)}>{t("actions.cancel")}</Button>
            <Button type="submit" disabled={mutation.isPending || details.isLoading || groups.isLoading}>
              {mutation.isPending ? t("states.saving") : t("actions.save")}
            </Button>
          </DialogFooter>
        </form>}
      </DialogContent>
    </Dialog>
  );
}

function ResourceFields({ resourceKey, initial, groups }: { resourceKey: string; initial: ResourceRecord | undefined; groups: GroupOption[] }) {
  if (resourceKey === "groups") return <GroupFields initial={initial} />;
  if (resourceKey === "scenarios") return <ScenarioFields initial={initial} groups={groups} />;
  if (resourceKey === "schedules") return <ScheduleFields initial={initial} groups={groups} />;
  return <ApiKeyFields initial={initial} />;
}

function GroupFields({ initial }: { initial: ResourceRecord | undefined }) {
  const { t } = useTranslation("registry");
  return <>
    <Field name="name" label={t("fields.name")} defaultValue={text(initial?.naziv)} required maxLength={200} autoFocus />
    <Field name="priority" label={t("fields.priority")} type="number" defaultValue={text(initial?.prioritet, "50")} required min={0} max={1000} />
    <Field name="description" label={t("fields.description")} defaultValue={text(initial?.opis)} textarea wide maxLength={1000} />
    <Field name="color" label={t("fields.color")} type="color" defaultValue={text(initial?.boja, "#ffdd00")} />
    <NativeSelect name="tag" label={t("fields.tag")} defaultValue={text(initial?.tag, "Smoke")} options={[
      ["Smoke", t("values.groupTypes.smoke")], ["Regression", t("values.groupTypes.regression")], ["Full", t("values.groupTypes.full")],
    ]} />
  </>;
}

function ScenarioFields({ initial, groups }: { initial: ResourceRecord | undefined; groups: GroupOption[] }) {
  const { t } = useTranslation("registry");
  const initialType = (text(initial?.tip, "Rest") as ScenarioType);
  const [type, setType] = useState<ScenarioType>(initialType);
  useEffect(() => setType(initialType), [initialType, initial?.id]);
  const rest = object(initial?.rest);
  const ui = object(initial?.ui);
  const blazor = object(initial?.blazor);
  return <>
    <Field name="name" label={t("fields.name")} defaultValue={text(initial?.naziv)} required maxLength={200} autoFocus />
    <NativeSelect name="groupId" label={t("fields.group")} defaultValue={text(initial?.groupId)} required placeholder={t("fields.selectGroup")} options={groups.map((group) => [group.id, group.name])} />
    <NativeSelect name="scenarioType" label={t("fields.scenarioType")} defaultValue={type} onChange={(value) => setType(value as ScenarioType)} options={[
      ["Rest", "REST API"], ["Ui", t("values.scenarioTypes.ui")], ["Blazor", "Blazor / bUnit"],
    ]} />
    <BooleanField name="runSequentially" label={t("fields.runSequentially")} defaultChecked={Boolean(initial?.runSequentially)} />
    <Field name="description" label={t("fields.description")} defaultValue={text(initial?.opis)} textarea wide maxLength={1000} />
    {type === "Rest" && <>
      <NativeSelect name="method" label={t("fields.method")} defaultValue={text(rest?.metoda, "Get")} options={["Get", "Post", "Put", "Patch", "Delete"].map((value) => [value, value.toUpperCase()])} />
      <Field name="url" label="URL" defaultValue={text(rest?.url)} placeholder="https://api.example.com/items ili {{baseUrl}}/items" required maxLength={2000} />
      <Field name="expectedStatus" label={t("fields.expectedStatus")} type="number" defaultValue={text(rest?.ocekivaniStatus, "200")} required min={100} max={599} />
      <Field name="requestBody" label={t("fields.requestBody")} defaultValue={text(rest?.requestBody)} textarea wide placeholder={'{"name":"value"}'} />
      <Field name="headers" label={t("fields.headersJson")} defaultValue={json(rest?.headeri)} textarea wide placeholder={'[{"kljuc":"Authorization","vrijednost":"Bearer {{token}}"}]'} />
      <Field name="assertions" label={t("fields.assertionsJson")} defaultValue={json(rest?.responseAsserti)} textarea wide placeholder={'[{"jsonPutanja":"$.id","ocekivanaVrijednost":"1"}]'} />
    </>}
    {type === "Ui" && <>
      <Field name="pageUrl" label={t("fields.pageUrl")} defaultValue={text(ui?.urlStranice)} required wide placeholder="{{baseUrl}}/customers" />
      <Field name="steps" label={t("fields.stepsJson")} defaultValue={json(ui?.koraci)} textarea wide required placeholder={'[{"akcija":"Klik","selektor":"#save","vrijednost":null,"ocekivaniTekst":null}]'} />
    </>}
    {type === "Blazor" && <>
      <Field name="componentName" label={t("fields.componentName")} defaultValue={text(blazor?.componentName)} required maxLength={200} />
      <Field name="razorContent" label={t("fields.razorContent")} defaultValue={text(blazor?.razorContent)} textarea wide required />
    </>}
  </>;
}

function ScheduleFields({ initial, groups }: { initial: ResourceRecord | undefined; groups: GroupOption[] }) {
  const { t } = useTranslation("registry");
  return <>
    <NativeSelect name="groupId" label={t("fields.group")} defaultValue={text(initial?.groupId)} required placeholder={t("fields.selectGroup")} options={groups.map((group) => [group.id, group.name])} disabled={Boolean(initial?.id)} />
    <Field name="cronExpression" label={t("fields.cron")} defaultValue={text(initial?.cronExpression, "0 8 * * 1-5")} required pattern="^\\s*\\S+\\s+\\S+\\s+\\S+\\s+\\S+\\s+\\S+\\s*$" />
    <NativeSelect name="timezone" label={t("fields.timezone")} defaultValue={text(initial?.timezone, "Europe/Sarajevo")} options={[
      ["Europe/Sarajevo", "Europe/Sarajevo"], ["UTC", "UTC"], ["Europe/Vienna", "Europe/Vienna"],
    ]} />
    <BooleanField name="active" label={t("fields.activeSchedule")} defaultChecked={initial?.isActive === undefined ? true : Boolean(initial.isActive)} />
  </>;
}

function ApiKeyFields({ initial }: { initial: ResourceRecord | undefined }) {
  const { t } = useTranslation("registry");
  const tomorrow = new Date(Date.now() + 86_400_000).toISOString().slice(0, 10);
  return <>
    <Field name="name" label={t("fields.name")} defaultValue={text(initial?.name)} required maxLength={120} autoFocus />
    <Field name="expiresAt" label={t("fields.expiresAt")} type="date" defaultValue={text(initial?.expiresAt).slice(0, 10)} min={tomorrow} />
  </>;
}

function Field({ name, label, textarea, wide, defaultValue, ...props }: { name: string; label: string; textarea?: boolean; wide?: boolean; defaultValue?: string } & Omit<React.InputHTMLAttributes<HTMLInputElement>, "defaultValue">) {
  return <div className={wide ? "md:col-span-2" : ""}>
    <Label htmlFor={name}>{label}{props.required ? " *" : ""}</Label>
    {textarea
      ? <Textarea id={name} name={name} className="mt-2 min-h-24" defaultValue={defaultValue} required={props.required} maxLength={props.maxLength} />
      : <Input id={name} name={name} className="mt-2" defaultValue={defaultValue} {...props} />}
  </div>;
}

function NativeSelect({ name, label, options, defaultValue, placeholder, required, disabled, onChange }: { name: string; label: string; options: readonly (readonly [string, string])[]; defaultValue?: string; placeholder?: string; required?: boolean; disabled?: boolean; onChange?: (value: string) => void }) {
  return <div>
    <Label htmlFor={name}>{label}{required ? " *" : ""}</Label>
    <select id={name} name={name} defaultValue={defaultValue ?? ""} required={required} disabled={disabled} onChange={(event) => onChange?.(event.target.value)} className="mt-2 h-10 w-full rounded-md border border-border-default bg-surface-raised px-3 text-sm text-text-primary disabled:bg-surface-muted disabled:text-text-secondary">
      {placeholder && <option value="">{placeholder}</option>}
      {options.map(([value, text]) => <option key={value} value={value}>{text}</option>)}
    </select>
    {disabled && <input type="hidden" name={name} value={defaultValue} />}
  </div>;
}

function BooleanField({ name, label, defaultChecked }: { name: string; label: string; defaultChecked: boolean }) {
  return <label className="flex min-h-10 items-center gap-3 self-end rounded-md border border-border-default bg-surface-raised px-4 py-2 text-sm font-semibold">
    <input name={name} type="checkbox" defaultChecked={defaultChecked} className="size-5 accent-[var(--color-rbi-yellow)]" />{label}
  </label>;
}

function buildPayload(key: string, data: FormData): { body?: unknown; error?: string } {
  const name = value(data, "name").trim();
  if ((key === "groups" || key === "scenarios" || key === "apiKeys") && !name) return { error: "Naziv je obavezan." };
  if (key === "groups") return { body: { naziv: name, opis: optional(data, "description"), boja: value(data, "color") || "#ffdd00", tag: value(data, "tag"), prioritet: number(data, "priority"), parentGroupId: null } };
  if (key === "schedules") {
    if (!value(data, "groupId")) return { error: "Odaberite grupu testova." };
    return { body: { groupId: value(data, "groupId"), cronExpression: value(data, "cronExpression").trim(), timezone: value(data, "timezone"), isActive: data.get("active") === "on" } };
  }
  if (key === "apiKeys") return { body: { name, expiresAt: optional(data, "expiresAt") } };

  const groupId = value(data, "groupId");
  if (!groupId) return { error: "Scenarij mora biti dodijeljen grupi." };
  const tip = value(data, "scenarioType") as ScenarioType;
  const common = { groupId, naziv: name, opis: optional(data, "description"), tip, runSequentially: data.get("runSequentially") === "on" };
  if (tip === "Rest") {
    const url = value(data, "url").trim();
    if (!isEndpointUrl(url)) return { error: "Unesite ispravan HTTP(S) URL ili adresu koja počinje sa {{baseUrl}}." };
    const requestBody = optional(data, "requestBody");
    if (requestBody && !isJson(requestBody)) return { error: "Tijelo zahtjeva mora biti ispravan JSON." };
    const headers = parseArray(data, "headers", "Headeri"); if (headers.error) return headers;
    const assertions = parseArray(data, "assertions", "Provjere odgovora"); if (assertions.error) return assertions;
    return { body: { ...common, rest: { metoda: value(data, "method"), url, headeri: headers.body, requestBody, ocekivaniStatus: number(data, "expectedStatus"), responseAsserti: assertions.body }, ui: null, blazor: null } };
  }
  if (tip === "Ui") {
    const pageUrl = value(data, "pageUrl").trim();
    if (!isEndpointUrl(pageUrl)) return { error: "Unesite ispravan URL stranice ili adresu koja počinje sa {{baseUrl}}." };
    const steps = parseArray(data, "steps", "Koraci"); if (steps.error) return steps;
    if ((steps.body as unknown[]).length === 0) return { error: "Dodajte najmanje jedan UI korak." };
    return { body: { ...common, rest: null, ui: { urlStranice: pageUrl, koraci: steps.body }, blazor: null } };
  }
  const componentName = value(data, "componentName").trim();
  const razorContent = value(data, "razorContent").trim();
  if (!componentName || !razorContent) return { error: "Naziv komponente i Razor sadržaj su obavezni." };
  return { body: { ...common, rest: null, ui: null, blazor: { componentName, razorContent } } };
}

function parseArray(data: FormData, key: string, label: string): { body?: unknown[]; error?: string } {
  const raw = value(data, key).trim();
  if (!raw) return { body: [] };
  try { const parsed: unknown = JSON.parse(raw); return Array.isArray(parsed) ? { body: parsed } : { error: `${label} moraju biti JSON lista.` }; }
  catch { return { error: `${label} nisu ispravan JSON.` }; }
}
function isJson(value: string) { try { JSON.parse(value); return true; } catch { return false; } }
function isEndpointUrl(value: string) { if (value.startsWith("{{baseUrl}}")) return value.length > 11; try { const url = new URL(value); return url.protocol === "http:" || url.protocol === "https:"; } catch { return false; } }
function value(data: FormData, key: string) { return String(data.get(key) ?? ""); }
function optional(data: FormData, key: string) { return value(data, key).trim() || null; }
function number(data: FormData, key: string) { return Number(value(data, key)); }
function object(value: unknown): NestedFields | undefined { return typeof value === "object" && value !== null && !Array.isArray(value) ? value as NestedFields : undefined; }
function text(value: unknown, fallback = "") { return value == null ? fallback : String(value); }
function json(value: unknown) { return Array.isArray(value) && value.length > 0 ? JSON.stringify(value, null, 2) : ""; }
function flattenGroupOptions(payload: unknown): GroupOption[] {
  if (!Array.isArray(payload)) return [];
  return payload.flatMap((entry) => {
    const node = object(entry); const group = object(node?.group) ?? node; const children = Array.isArray(node?.children) ? flattenGroupOptions(node?.children) : [];
    return group?.id ? [{ id: String(group.id), name: String(group.naziv ?? group.name ?? group.id) }, ...children] : children;
  });
}
function readableError(error: unknown) { if (error instanceof ApiError) return [error.message, ...Object.values(error.details ?? {}).flat()].filter(Boolean).join(" "); return error instanceof Error ? error.message : "Zahtjev nije moguće izvršiti."; }
function ErrorBanner({ message }: { message: string }) { return <div role="alert" className="mt-5 flex gap-3 rounded-sm border border-feedback-danger bg-feedback-danger-subtle p-4 text-sm text-feedback-danger"><AlertCircle className="size-5 shrink-0" />{message}</div>; }
