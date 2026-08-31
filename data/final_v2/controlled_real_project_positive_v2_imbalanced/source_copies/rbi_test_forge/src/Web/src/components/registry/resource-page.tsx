import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { AlertCircle, Copy, Download, KeyRound, Pencil, Play, Plus, Trash2 } from "lucide-react";
import { type FormEvent, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Heading, Text } from "@/components/ui/typography";
import { ResourceFormDialog } from "@/components/registry/resource-form-dialog";
import { ApiError, apiClient } from "@/lib/api/http-client";
import type { RegistryResource } from "@/lib/registry/resources";

type RecordValue = string | number | boolean | null | undefined | readonly unknown[] | Record<string, unknown>;
type DataRecord = Readonly<Record<string, RecordValue>>;

export function ResourcePage({ resource }: { readonly resource: RegistryResource }) {
  if (resource.key === "generator") return <GeneratorPage resource={resource} />;
  if (resource.key === "apiImport") return <ApiImportPage resource={resource} />;
  if (resource.key === "codeLists") return <CodeListsPage resource={resource} />;
  return <ManagementPage resource={resource} />;
}

function CodeListsPage({ resource }: { resource: RegistryResource }) {
  const { t } = useTranslation("registry");
  const client = useQueryClient();
  const [categoryId, setCategoryId] = useState("");
  const [error, setError] = useState<string>();
  const [editValue, setEditValue] = useState<DataRecord>();
  const categories = useQuery({ queryKey: ["code-list-categories"], queryFn: () => apiClient.get<DataRecord[]>("/api/frontend/code-lists") });
  const selectedId = categoryId || String(categories.data?.[0]?.["id"] ?? "");
  const values = useQuery({ queryKey: ["code-list-values", selectedId], queryFn: () => apiClient.get<DataRecord[]>(`/api/frontend/code-lists/${selectedId}/values`), enabled: Boolean(selectedId) });
  const save = useMutation({ mutationFn: (body: unknown) => editValue ? apiClient.put<void>(`/api/frontend/code-lists/${selectedId}/values/${String(editValue["id"])}`, { body }) : apiClient.post<void>(`/api/frontend/code-lists/${selectedId}/values`, { body }), onSuccess: async () => { setEditValue(undefined); await client.invalidateQueries({ queryKey: ["code-list-values", selectedId] }); }, onError: (value) => setError(errorMessage(value)) });
  const remove = useMutation({ mutationFn: (id: string) => apiClient.delete<void>(`/api/frontend/code-lists/${selectedId}/values/${id}`), onSuccess: async () => client.invalidateQueries({ queryKey: ["code-list-values", selectedId] }), onError: (value) => setError(errorMessage(value)) });
  function submit(event: FormEvent<HTMLFormElement>) { event.preventDefault(); setError(undefined); const data = new FormData(event.currentTarget); save.mutate({ name: String(data.get("name")).trim(), code: String(data.get("code") || "").trim() || null, order: Number(data.get("order")), active: data.get("active") === "on" }); }
  return <section><PageHeading resource={resource} />{categories.isError && <ErrorState message={errorMessage(categories.error)} retry={() => categories.refetch()} />}{categories.data && <><Label htmlFor="category" className="mt-7 block">{t("codeLists.category")}</Label><select id="category" value={selectedId} onChange={(event) => { setCategoryId(event.target.value); setEditValue(undefined); }} className="mt-2 h-11 w-full max-w-xl rounded-md border border-border-default bg-surface-default px-3 text-text-primary">{categories.data.map((category) => <option key={String(category["id"])} value={String(category["id"])}>{String(category["naziv"])}</option>)}</select><form key={String(editValue?.["id"] ?? "new")} onSubmit={submit} className="mt-6 grid gap-4 rounded-sm border border-border-subtle bg-surface-default p-5 sm:grid-cols-4"><Field name="name" label={t("fields.name")} defaultValue={String(editValue?.["naziv"] ?? "")} required maxLength={200} /><Field name="code" label={t("codeLists.code")} defaultValue={String(editValue?.["kod"] ?? editValue?.["sifra"] ?? "")} maxLength={100} /><Field name="order" label={t("codeLists.order")} type="number" defaultValue={String(editValue?.["redoslijed"] ?? 0)} min={0} max={10000} required /><label className="flex items-center gap-3 self-end pb-2 text-sm font-semibold"><input name="active" type="checkbox" defaultChecked={editValue?.["active"] === undefined ? true : Boolean(editValue["active"])} className="size-5 accent-[var(--color-rbi-yellow)]" />{t("codeLists.active")}</label><div className="flex gap-3 sm:col-span-4">{editValue && <Button type="button" variant="secondary" onClick={() => setEditValue(undefined)}>{t("actions.cancel")}</Button>}<Button type="submit" disabled={save.isPending}>{editValue ? <Pencil className="size-4" /> : <Plus className="size-4" />}{editValue ? t("actions.save") : t("codeLists.add")}</Button></div></form>{error && <ErrorBanner message={error} />}<div className="mt-5 overflow-x-auto rounded-sm border border-border-subtle bg-surface-default"><table className="w-full text-left text-sm"><thead className="bg-surface-subtle"><tr><th className="px-4 py-3">{t("fields.name")}</th><th className="px-4 py-3">{t("codeLists.code")}</th><th className="px-4 py-3">{t("codeLists.order")}</th><th className="px-4 py-3">{t("codeLists.active")}</th><th className="px-4 py-3 text-right">{t("actions.actions")}</th></tr></thead><tbody className="divide-y divide-border-subtle">{values.data?.map((value) => <tr key={String(value["id"])}><td className="px-4 py-3">{String(value["naziv"])}</td><td className="px-4 py-3">{formatValue(value["kod"] ?? value["sifra"])}</td><td className="px-4 py-3">{String(value["redoslijed"])}</td><td className="px-4 py-3">{formatValue(value["active"])}</td><td className="px-4 py-2"><div className="flex justify-end gap-1"><IconAction label={t("actions.edit")} onClick={() => setEditValue(value)}><Pencil /></IconAction><IconAction danger label={t("actions.delete")} onClick={() => remove.mutate(String(value["id"]))}><Trash2 /></IconAction></div></td></tr>)}</tbody></table>{values.isLoading && <LoadingState label={t("states.loading")} />}{values.data?.length === 0 && <EmptyState />}</div></>}</section>;
}

function ManagementPage({ resource }: { readonly resource: RegistryResource }) {
  const { t } = useTranslation("registry");
  const client = useQueryClient();
  const endpoint = resource.endpoint;
  const query = useQuery({
    queryKey: ["test-automation", resource.key],
    queryFn: () => apiClient.get<unknown>(endpoint!),
    enabled: Boolean(endpoint),
  });
  const records = useMemo(() => normalizeRecords(resource.key, query.data), [query.data, resource.key]);
  const [formOpen, setFormOpen] = useState(false);
  const [editRecord, setEditRecord] = useState<DataRecord>();
  const [deleteRecord, setDeleteRecord] = useState<DataRecord>();
  const [roleRecord, setRoleRecord] = useState<DataRecord>();
  const [operationError, setOperationError] = useState<string>();

  const remove = useMutation({
    mutationFn: (record: DataRecord) => apiClient.delete<void>(deletePath(resource.key, record)),
    onSuccess: async () => {
      setDeleteRecord(undefined);
      await client.invalidateQueries({ queryKey: ["test-automation", resource.key] });
    },
    onError: (error) => setOperationError(errorMessage(error)),
  });
  const action = useMutation({
    mutationFn: ({ record, actionName }: { record: DataRecord; actionName: "clone" | "run" }) =>
      apiClient.post<unknown>(`${endpoint}/${String(record["id"])}/${actionName}`),
    onSuccess: async () => client.invalidateQueries({ queryKey: ["test-automation"] }),
    onError: (error) => setOperationError(errorMessage(error)),
  });

  const canCreate = ["groups", "scenarios", "schedules", "apiKeys"].includes(resource.key);
  const canEdit = ["groups", "scenarios", "schedules"].includes(resource.key);
  const canDelete = ["groups", "scenarios", "schedules", "apiKeys"].includes(resource.key);
  const columns = tableColumns(resource.key, records);

  return (
    <section aria-labelledby={`${resource.key}-heading`}>
      <PageHeading resource={resource} />
      <div className="mt-6 flex flex-wrap items-center justify-between gap-3">
        <p className="text-sm text-text-secondary">{records.length} {t("records.count")}</p>
        {canCreate && <Button onClick={() => { setOperationError(undefined); setEditRecord(undefined); setFormOpen(true); }}><Plus className="size-4" />{t("actions.create")}</Button>}
      </div>
      {operationError && <ErrorBanner message={operationError} />}
      <div className="mt-4 overflow-hidden rounded-sm border border-border-subtle bg-surface-default">
        {query.isLoading && <LoadingState label={t("states.loading")} />}
        {query.isError && <ErrorState message={errorMessage(query.error)} retry={() => query.refetch()} />}
        {query.isSuccess && records.length === 0 && <EmptyState />}
        {query.isSuccess && records.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-surface-subtle text-text-secondary"><tr>
                {columns.map((column) => <th key={column} className="whitespace-nowrap px-4 py-3 font-semibold">{t(`columns.${column}` as never, { defaultValue: humanize(column) })}</th>)}
                {(canEdit || canDelete || resource.key === "scenarios" || resource.key === "users") && <th className="px-4 py-3 text-right font-semibold">{t("actions.actions")}</th>}
              </tr></thead>
              <tbody className="divide-y divide-border-subtle">
                {records.map((record, index) => <tr key={String(record["id"] ?? index)} className="hover:bg-surface-subtle">
                  {columns.map((column) => <td key={column} className="max-w-80 px-4 py-3 text-text-primary">{formatValue(record[column], t("values.yes"), t("values.no"))}</td>)}
                  {(canEdit || canDelete || resource.key === "scenarios" || resource.key === "users") && <td className="px-4 py-2"><div className="flex justify-end gap-1">
                    {resource.key === "groups" && <IconAction label={t("actions.run")} onClick={() => action.mutate({ record, actionName: "run" })}><Play /></IconAction>}
                    {resource.key === "schedules" && <IconAction label={t("actions.run")} onClick={() => action.mutate({ record, actionName: "run" })}><Play /></IconAction>}
                    {resource.key === "scenarios" && <><IconAction label={t("actions.run")} onClick={() => action.mutate({ record, actionName: "run" })}><Play /></IconAction><IconAction label={t("actions.clone")} onClick={() => action.mutate({ record, actionName: "clone" })}><Copy /></IconAction></>}
                    {resource.key === "users" && <IconAction label={t("actions.roles")} onClick={() => setRoleRecord(record)}><KeyRound /></IconAction>}
                    {canEdit && <IconAction label={t("actions.edit")} onClick={() => { setOperationError(undefined); setEditRecord(record); setFormOpen(true); }}><Pencil /></IconAction>}
                    {canDelete && <IconAction label={resource.key === "apiKeys" ? t("actions.revoke") : t("actions.delete")} danger onClick={() => setDeleteRecord(record)}><Trash2 /></IconAction>}
                  </div></td>}
                </tr>)}
              </tbody>
            </table>
          </div>
        )}
      </div>
      <ResourceFormDialog resource={resource} record={editRecord} open={formOpen} onOpenChange={(value) => { setFormOpen(value); if (!value) setEditRecord(undefined); }} onSaved={async () => {
        setEditRecord(undefined); await client.invalidateQueries({ queryKey: ["test-automation", resource.key] });
      }} />
      <RoleDialog record={roleRecord} open={Boolean(roleRecord)} onOpenChange={(value) => !value && setRoleRecord(undefined)} onSaved={async () => { setRoleRecord(undefined); await client.invalidateQueries({ queryKey: ["test-automation", "users"] }); }} />
      <AlertDialog open={Boolean(deleteRecord)} onOpenChange={(open) => !open && setDeleteRecord(undefined)}>
        <AlertDialogContent className="bg-surface-default text-text-primary">
          <AlertDialogHeader><AlertDialogTitle>{t("confirm.title")}</AlertDialogTitle><AlertDialogDescription>{t("confirm.delete")}</AlertDialogDescription></AlertDialogHeader>
          <AlertDialogFooter><AlertDialogCancel>{t("actions.cancel")}</AlertDialogCancel><AlertDialogAction onClick={() => deleteRecord && remove.mutate(deleteRecord)}>{t("actions.confirm")}</AlertDialogAction></AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </section>
  );
}

function RoleDialog({ record, open, onOpenChange, onSaved }: { record: DataRecord | undefined; open: boolean; onOpenChange: (open: boolean) => void; onSaved: () => void }) {
  const { t } = useTranslation("registry");
  const roles = useQuery({ queryKey: ["available-roles"], queryFn: () => apiClient.get<readonly string[]>("/api/frontend/users/roles"), enabled: open });
  const assigned = Array.isArray(record?.["roles"]) ? record["roles"].map(String) : [];
  const user = isRecord(record?.["user"]) ? record["user"] : undefined;
  const mutation = useMutation({ mutationFn: (selected: readonly string[]) => apiClient.put<void>(`/api/frontend/users/${String(user?.["id"])}/roles`, { body: { roles: selected } }), onSuccess: onSaved });
  function submit(event: FormEvent<HTMLFormElement>) { event.preventDefault(); const form = new FormData(event.currentTarget); mutation.mutate(form.getAll("roles").map(String)); }
  return <Dialog open={open} onOpenChange={onOpenChange}><DialogContent className="bg-surface-default text-text-primary sm:max-w-xl"><form onSubmit={submit}><DialogHeader><DialogTitle>{t("roles.title")}</DialogTitle><DialogDescription>{String(user?.["fullName"] ?? user?.["username"] ?? "")}</DialogDescription></DialogHeader><div className="mt-6 grid gap-3 sm:grid-cols-2">{roles.data?.map((role) => <label key={role} className="flex items-center gap-3 rounded-sm border border-border-subtle p-3 text-sm font-semibold"><input name="roles" value={role} type="checkbox" defaultChecked={assigned.includes(role)} className="size-5 accent-[var(--color-rbi-yellow)]" />{role}</label>)}</div>{mutation.isError && <ErrorBanner message={errorMessage(mutation.error)} />}<DialogFooter className="mt-7"><Button type="button" variant="secondary" onClick={() => onOpenChange(false)}>{t("actions.cancel")}</Button><Button type="submit" disabled={mutation.isPending}>{t("actions.save")}</Button></DialogFooter></form></DialogContent></Dialog>;
}

function GeneratorPage({ resource }: { resource: RegistryResource }) {
  const { t } = useTranslation("registry");
  const [files, setFiles] = useState<readonly { fileName: string; content: string }[]>([]);
  const [error, setError] = useState<string>();
  const mutation = useMutation({ mutationFn: (body: unknown) => apiClient.post<{ files: readonly { fileName: string; content: string }[] }>("/api/frontend/generator/rest", { body }), onSuccess: (value) => setFiles(value.files), onError: (value) => setError(errorMessage(value)) });
  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError(undefined); const data = new FormData(event.currentTarget);
    const className = String(data.get("className")).trim(); const route = String(data.get("route")).trim(); const body = String(data.get("body") || "").trim();
    if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(className)) { setError(t("generator.invalidClassName")); return; }
    if (!route.startsWith("/")) { setError(t("generator.invalidRoute")); return; }
    if (body) { try { JSON.parse(body); } catch { setError(t("generator.invalidJson")); return; } }
    mutation.mutate({ className, httpMethod: String(data.get("method")), routePath: route, expectedStatus: Number(data.get("status")), requestBodyJson: body || null, requiresAuth: data.get("auth") === "on" });
  }
  function download() {
    const blob = new Blob([files.map((file) => `// ${file.fileName}\n${file.content}`).join("\n\n")], { type: "text/plain;charset=utf-8" });
    const link = document.createElement("a"); link.href = URL.createObjectURL(blob); link.download = "generated-tests.txt"; link.click(); URL.revokeObjectURL(link.href);
  }
  return <section><PageHeading resource={resource} /><form onSubmit={submit} className="mt-8 grid gap-5 rounded-sm border border-border-subtle bg-surface-default p-6 sm:grid-cols-2"><div className="sm:col-span-2"><Heading level={2} size={2}>{t("generator.restTitle")}</Heading><Text tone="secondary" className="mt-1">{t("generator.restDescription")}</Text></div><Field name="className" label={t("generator.className")} placeholder="CreateCustomer" pattern="^[A-Za-z_][A-Za-z0-9_]*$" required /><NativeSelect name="method" label={t("fields.method")} options={["GET", "POST", "PUT", "PATCH", "DELETE"]} /><Field name="route" label={t("generator.route")} placeholder="/api/customers" pattern="^/.*" required /><Field name="status" label={t("fields.expectedStatus")} type="number" defaultValue="200" min={100} max={599} required /><Field name="body" label={t("fields.requestBody")} wide textarea /><label className="flex items-center gap-3 text-sm font-semibold"><input name="auth" type="checkbox" className="size-5 accent-[var(--color-rbi-yellow)]" />{t("generator.requiresAuth")}</label><div className="sm:col-span-2"><Button type="submit" disabled={mutation.isPending}>{t("generator.generate")}</Button></div></form>{error && <ErrorBanner message={error} />}{files.length > 0 && <GeneratedFiles files={files} onDownload={download} />}<ComponentProjectGenerator /></section>;
}

type ComponentSpec = DataRecord & { componentName: string };
type ComponentInfo = { filePath: string; isPage: boolean; spec: ComponentSpec };
type ProjectAnalysis = { components: ComponentInfo[]; warnings: string[]; pageCount: number; componentCount: number; totalRoutes: number; totalForms: number; totalHttpCalls: number };

function ComponentProjectGenerator() {
  const { t } = useTranslation("registry");
  const [analysis, setAnalysis] = useState<ProjectAnalysis>();
  const [selected, setSelected] = useState<ComponentInfo>();
  const [generated, setGenerated] = useState<readonly { fileName: string; content: string }[]>([]);
  const [error, setError] = useState<string>();
  const analyze = useMutation({ mutationFn: (files: readonly { relativePath: string; content: string }[]) => apiClient.post<ProjectAnalysis>("/api/frontend/generator/component/analyze", { body: { files } }), onSuccess: (value) => { setAnalysis(value); setSelected(value.components[0]); setGenerated([]); }, onError: (value) => setError(errorMessage(value)) });
  const generate = useMutation({ mutationFn: (framework: string) => apiClient.post<{ files: readonly { fileName: string; content: string }[] }>("/api/frontend/generator/component", { body: { framework, spec: selected?.spec } }), onSuccess: (value) => setGenerated(value.files), onError: (value) => setError(errorMessage(value)) });
  async function filesChanged(input?: FileList | null) {
    if (!input?.length) return;
    setError(undefined);
    const accepted = [...input].filter((file) => file.name.endsWith(".razor") || file.name.endsWith(".razor.cs"));
    if (accepted.length === 0) { setError(t("generator.componentInvalid")); return; }
    if (accepted.length > 250 || accepted.reduce((sum, file) => sum + file.size, 0) > 5_000_000) { setError(t("generator.componentTooLarge")); return; }
    analyze.mutate(await Promise.all(accepted.map(async (file) => ({ relativePath: file.webkitRelativePath || file.name, content: await file.text() }))));
  }
  function download() {
    const blob = new Blob([generated.map((file) => `// ${file.fileName}\n${file.content}`).join("\n\n")], { type: "text/plain;charset=utf-8" });
    const link = document.createElement("a"); link.href = URL.createObjectURL(blob); link.download = `${selected?.spec.componentName ?? "component"}-tests.txt`; link.click(); URL.revokeObjectURL(link.href);
  }
  return <div className="mt-8 rounded-sm border border-border-subtle bg-surface-default p-6"><Heading level={2} size={2}>{t("generator.componentTitle")}</Heading><Text tone="secondary" className="mt-1">{t("generator.componentDescription")}</Text><Label htmlFor="component-files" className="mt-5 block">{t("generator.componentFiles")}</Label><Input id="component-files" className="mt-2" type="file" accept=".razor,.cs" multiple onChange={(event) => filesChanged(event.target.files)} />{analyze.isPending && <LoadingState label={t("states.loading")} />}{error && <ErrorBanner message={error} />}{analysis && <><div className="mt-5 grid gap-3 sm:grid-cols-5">{[["pages",analysis.pageCount],["components",analysis.componentCount],["routes",analysis.totalRoutes],["forms",analysis.totalForms],["calls",analysis.totalHttpCalls]].map(([label,value]) => <div key={String(label)} className="rounded-sm bg-surface-subtle p-3"><p className="text-xs text-text-secondary">{t(`generator.metrics.${label}` as never)}</p><p className="mt-1 text-xl font-bold">{value}</p></div>)}</div><Label htmlFor="component-select" className="mt-5 block">{t("generator.componentSelect")}</Label><select id="component-select" className="mt-2 h-10 w-full rounded-md border border-border-default bg-surface-default px-3 text-sm text-text-primary" value={selected?.filePath} onChange={(event) => setSelected(analysis.components.find((item) => item.filePath === event.target.value))}>{analysis.components.map((item) => <option key={item.filePath} value={item.filePath}>{item.filePath}</option>)}</select><div className="mt-5 flex flex-wrap gap-3"><Button disabled={!selected || generate.isPending} onClick={() => generate.mutate("bunit")}>{t("generator.generateBunit")}</Button><Button variant="secondary" disabled={!selected || generate.isPending} onClick={() => generate.mutate("playwright")}>{t("generator.generatePlaywright")}</Button></div>{analysis.warnings.length > 0 && <ul className="mt-4 list-disc pl-5 text-sm text-feedback-warning">{analysis.warnings.map((warning) => <li key={warning}>{warning}</li>)}</ul>}</>}{generated.length > 0 && <GeneratedFiles files={generated} onDownload={download} />}</div>;
}

function GeneratedFiles({ files, onDownload }: { files: readonly { fileName: string; content: string }[]; onDownload: () => void }) { const { t } = useTranslation("registry"); return <div className="mt-6 rounded-sm border border-border-subtle bg-surface-default p-6"><div className="flex items-center justify-between gap-3"><h2 className="font-bold">{t("generator.result")}</h2><Button variant="secondary" onClick={onDownload}><Download className="size-4" />{t("actions.download")}</Button></div><div className="mt-4 flex flex-wrap gap-2">{files.map((file) => <span key={file.fileName} className="rounded-xs bg-surface-subtle px-3 py-2 font-mono text-xs">{file.fileName}</span>)}</div></div>; }

function ApiImportPage({ resource }: { resource: RegistryResource }) {
  const { t } = useTranslation("registry"); const [content, setContent] = useState(""); const [result, setResult] = useState<DataRecord>(); const [error, setError] = useState<string>();
  const mutation = useMutation({ mutationFn: () => apiClient.post<DataRecord>("/api/frontend/api-import/parse", { body: { content } }), onSuccess: setResult, onError: (value) => setError(errorMessage(value)) });
  async function fileChanged(file?: File) { if (!file) return; if (file.size > 5_000_000) { setError(t("apiImport.tooLarge")); return; } setContent(await file.text()); }
  return <section><PageHeading resource={resource} /><div className="mt-8 rounded-sm border border-border-subtle bg-surface-default p-6"><Label htmlFor="openapi-file">{t("apiImport.file")}</Label><Input id="openapi-file" className="mt-2" type="file" accept=".json,.yaml,.yml,application/json,text/yaml" onChange={(e) => fileChanged(e.target.files?.[0])} /><Label htmlFor="openapi-content" className="mt-5 block">{t("apiImport.content")}</Label><Textarea id="openapi-content" className="mt-2 min-h-64 font-mono" value={content} onChange={(e) => setContent(e.target.value)} /><Button className="mt-5" disabled={!content.trim() || mutation.isPending} onClick={() => mutation.mutate()}>{t("apiImport.analyze")}</Button></div>{error && <ErrorBanner message={error} />}{result && <div className="mt-6 rounded-sm border border-border-subtle bg-surface-default p-6"><h2 className="font-bold">{String(result["title"] ?? "API")}</h2><Text tone="secondary" className="mt-2">{formatValue(result["endpoints"])} · {formatValue(result["warnings"])}</Text></div>}</section>;
}

function PageHeading({ resource }: { resource: RegistryResource }) { const { t } = useTranslation("registry"); return <div><p className="text-eyebrow text-text-tertiary">{t(`areas.${resource.area}`)}</p><Heading level={1} size={4} className="mt-2">{t(`resources.${resource.key}.title` as never)}</Heading><Text tone="secondary" className="mt-2 max-w-prose">{t(`resources.${resource.key}.description` as never)}</Text></div>; }
function Field({ name, label, textarea, wide, ...props }: { name: string; label: string; textarea?: boolean; wide?: boolean } & React.InputHTMLAttributes<HTMLInputElement>) { return <div className={wide ? "sm:col-span-2" : ""}><Label htmlFor={name}>{label}</Label>{textarea ? <Textarea id={name} name={name} className="mt-2" /> : <Input id={name} name={name} className="mt-2" {...props} />}</div>; }
function NativeSelect({ name, label, options }: { name: string; label: string; options: readonly string[] }) { return <div><Label htmlFor={name}>{label}</Label><select id={name} name={name} className="mt-2 h-10 w-full rounded-md border border-border-default bg-surface-default px-3 text-sm text-text-primary">{options.map((option) => <option key={option} value={option}>{option}</option>)}</select></div>; }
function IconAction({ label, danger, onClick, children }: { label: string; danger?: boolean; onClick: () => void; children: React.ReactNode }) { return <Button variant="ghost" size="icon" className={danger ? "text-feedback-danger" : ""} aria-label={label} title={label} onClick={onClick}>{children}</Button>; }
function LoadingState({ label }: { label: string }) { return <div className="space-y-3 p-6" aria-label={label}>{[1,2,3,4].map((item) => <div key={item} className="h-10 animate-pulse rounded-xs bg-surface-muted" />)}</div>; }
function ErrorState({ message, retry }: { message: string; retry: () => void }) { const { t } = useTranslation("registry"); return <div className="flex flex-col items-center px-6 py-16 text-center"><AlertCircle className="size-8 text-feedback-danger" /><h2 className="mt-4 font-bold">{t("states.errorTitle")}</h2><Text tone="secondary" className="mt-2 max-w-prose">{message}</Text><Button className="mt-5" onClick={retry}>{t("actions.tryAgain")}</Button></div>; }
function EmptyState() { const { t } = useTranslation("registry"); return <div className="px-6 py-16 text-center"><h2 className="font-bold">{t("states.emptyTitle")}</h2><Text tone="secondary" className="mt-2">{t("states.emptyBody")}</Text></div>; }
function ErrorBanner({ message }: { message: string }) { return <div role="alert" className="mt-4 flex gap-3 rounded-sm border border-feedback-danger bg-feedback-danger-subtle p-4 text-sm text-feedback-danger"><AlertCircle className="size-5 shrink-0" />{message}</div>; }

function normalizeRecords(key: string, payload: unknown): DataRecord[] {
  if (isRecord(payload)) return [payload];
  if (!Array.isArray(payload)) return [];
  if (key === "groups") return payload.flatMap((node) => flattenGroup(node));
  return payload.map((item) => isRecord(item) ? item : ({ value: String(item) } as DataRecord));
}
function flattenGroup(value: unknown): DataRecord[] { if (!isRecord(value)) return []; const group = isRecord(value["group"]) ? value["group"] : value; const summary = isRecord(value["summary"]) ? value["summary"] : {}; const current = { ...group, ...summary } as DataRecord; const children = Array.isArray(value["children"]) ? value["children"].flatMap(flattenGroup) : []; return [current, ...children]; }
function isRecord(value: unknown): value is Record<string, RecordValue> { return typeof value === "object" && value !== null && !Array.isArray(value); }
function tableColumns(key: string, records: readonly DataRecord[]) { const preferred: Record<string, string[]> = { groups:["naziv","tag","scenarioCount","lastPassRate","activeScheduleCount"], scenarios:["naziv","tip","redoslijed","runSequentially"], schedules:["groupNaziv","cronExpression","isActive","timezone"], history:["groupName","state","passRate","totalCount","startedAt"], apiKeys:["name","prefix","isRevoked","expiresAt","createdAt"], users:["user","roles"], audit:["timestampUtc","eventType","username","ipAddress","failureReason"], codeLists:["naziv","slug","opis","active"] }; const available = new Set(records.flatMap((record) => Object.keys(record))); const selected = (preferred[key] ?? []).filter((column) => available.has(column)); return selected.length > 0 ? selected : [...available].filter((column) => column !== "id" && isReadable(records.find((r) => r[column] !== undefined)?.[column])).slice(0,6); }
function isReadable(value: RecordValue) { return value == null || ["string","number","boolean"].includes(typeof value) || Array.isArray(value); }
function humanize(value: string) { return value.replace(/([a-z])([A-Z])/g,"$1 $2").replaceAll("_"," ").replace(/^./,(letter) => letter.toUpperCase()); }
function formatValue(value: RecordValue, yes = "Da", no = "Ne"): string { if (value == null || value === "") return "—"; if (typeof value === "boolean") return value ? yes : no; if (Array.isArray(value)) return value.length === 0 ? "—" : value.map((item) => isRecord(item) ? String(item["name"] ?? item["naziv"] ?? "") : String(item)).filter(Boolean).join(", "); if (isRecord(value)) return String(value["username"] ?? value["fullName"] ?? value["naziv"] ?? "—"); if (typeof value === "string" && /^\d{4}-\d{2}-\d{2}T/.test(value)) return new Intl.DateTimeFormat(undefined,{dateStyle:"medium",timeStyle:"short"}).format(new Date(value)); return String(value); }
function errorMessage(error: unknown) { if (error instanceof ApiError) { const fields = Object.values(error.details ?? {}).flat(); return [error.message, ...fields].filter(Boolean).join(" "); } return error instanceof Error ? error.message : "Zahtjev nije moguće izvršiti."; }
function deletePath(key: string, record: DataRecord) { const id = String(record["id"]); return key === "apiKeys" ? `/api/frontend/api-keys/${id}` : `/api/frontend/${key.replace(/[A-Z]/g,(m) => `-${m.toLowerCase()}`)}/${id}`; }
