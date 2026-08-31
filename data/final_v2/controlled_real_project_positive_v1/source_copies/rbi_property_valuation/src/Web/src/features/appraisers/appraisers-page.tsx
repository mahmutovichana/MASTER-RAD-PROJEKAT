import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Ban,
  BriefcaseBusiness,
  Download,
  Palmtree,
  Pencil,
  Plus,
  RefreshCw,
  Upload,
} from "lucide-react";
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
import type { components } from "@/lib/api/generated/api";
import { downloadAuthenticatedFile } from "@/lib/api/file-client";
import { apiClient } from "@/lib/api/http-client";

type Appraiser = Readonly<Record<string, unknown>>;
type Form = components["schemas"]["CreateAppraiserRequest"];
const empty: Form = {
  name: "",
  city: "",
  legalForm: "Individual",
  contactEmail: "",
  contactPhone: "",
  notes: "",
  supportedPropertyTypes: "",
  supportedCities: "",
  clientScope: "Sve",
};
const val = (r: Appraiser, ...keys: string[]) => keys.map((k) => r[k]).find((x) => x != null);
interface Filters {
  readonly search: string;
  readonly city: string;
  readonly onLeave: string;
  readonly blacklisted: string;
  readonly active: string;
}
async function list(filters: Filters): Promise<readonly Appraiser[]> {
  const raw = await apiClient.getLegacy<unknown>("/api/appraisers/", {
    query: {
      Search: filters.search || undefined,
      City: filters.city || undefined,
      OnLeave: filters.onLeave === "all" ? undefined : filters.onLeave === "true",
      Blacklisted: filters.blacklisted === "all" ? undefined : filters.blacklisted === "true",
      Active: filters.active === "all" ? undefined : filters.active === "true",
      PageSize: 100,
    },
  });
  const root = (raw as Record<string, unknown>)?.["data"] ?? raw;
  const items = Array.isArray(root)
    ? root
    : ((root as Record<string, unknown>)?.["items"] ??
      (root as Record<string, unknown>)?.["Items"]);
  return Array.isArray(items) ? (items as Appraiser[]) : [];
}
export function AppraisersPage() {
  const cache = useQueryClient();
  const [search, setSearch] = useState("");
  const [city, setCity] = useState("");
  const [onLeave, setOnLeave] = useState("all");
  const [blacklisted, setBlacklisted] = useState("all");
  const [active, setActive] = useState("true");
  const [importOpen, setImportOpen] = useState(false);
  const [importFile, setImportFile] = useState<File>();
  const [previewToken, setPreviewToken] = useState("");
  const [open, setOpen] = useState(false);
  const [editingId, setEditingId] = useState<number>();
  const [form, setForm] = useState<Form>(empty);
  const filters = { search, city, onLeave, blacklisted, active };
  const query = useQuery({
    queryKey: ["appraisers", filters],
    queryFn: () => list(filters),
  });
  const invalidate = () => cache.invalidateQueries({ queryKey: ["appraisers"] });
  const create = useMutation({
    mutationFn: () =>
      editingId
        ? apiClient.putLegacy(`/api/appraisers/${editingId}`, { body: form })
        : apiClient.postLegacy("/api/appraisers/", { body: form }),
    onSuccess: async () => {
      setOpen(false);
      setEditingId(undefined);
      setForm(empty);
      await invalidate();
    },
  });
  const openCreate = () => {
    setEditingId(undefined);
    setForm(empty);
    setOpen(true);
  };
  const openEdit = (appraiser: Appraiser) => {
    setEditingId(Number(val(appraiser, "id", "Id")));
    setForm({
      name: String(val(appraiser, "name", "Name") ?? ""),
      city: String(val(appraiser, "city", "City") ?? ""),
      legalForm: String(val(appraiser, "legalForm", "LegalForm") ?? "Individual"),
      contactEmail: String(val(appraiser, "contactEmail", "ContactEmail") ?? ""),
      contactPhone: String(val(appraiser, "contactPhone", "ContactPhone") ?? ""),
      notes: String(val(appraiser, "notes", "Notes") ?? ""),
      supportedPropertyTypes: String(
        val(appraiser, "supportedPropertyTypes", "SupportedPropertyTypes") ?? "",
      ),
      supportedCities: String(val(appraiser, "supportedCities", "SupportedCities") ?? ""),
      clientScope: String(val(appraiser, "clientScope", "ClientScope") ?? "Sve"),
    });
    setOpen(true);
  };
  const flag = useMutation({
    mutationFn: ({ id, suffix, value }: { id: number; suffix: string; value: boolean }) =>
      apiClient.postLegacy(`/api/appraisers/${id}/${suffix}`, { body: { value } }),
    onSuccess: invalidate,
  });
  const deactivate = useMutation({
    mutationFn: (id: number) => apiClient.deleteLegacy(`/api/appraisers/${id}`),
    onSuccess: invalidate,
  });
  const importPreview = useMutation({
    mutationFn: async () => {
      if (!importFile) throw new Error("Odaberite Excel datoteku.");
      const body = new FormData();
      body.append("file", importFile);
      const result = await apiClient.postLegacy<Appraiser>("/api/codebooks/import-export/preview", {
        query: { codebookType: "vjestaci", mode: 0 },
        body,
      });
      setPreviewToken(String(val(result, "previewToken", "PreviewToken") ?? ""));
      return result;
    },
  });
  const confirmImport = useMutation({
    mutationFn: () =>
      apiClient.postLegacy("/api/codebooks/import-export/confirm", {
        body: { previewToken },
      }),
    onSuccess: async () => {
      setImportOpen(false);
      setImportFile(undefined);
      setPreviewToken("");
      await invalidate();
    },
  });
  return (
    <section>
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-eyebrow text-text-tertiary">Operacije</p>
          <Heading level={1} size={4} className="mt-2">
            Vještaci
          </Heading>
          <Text tone="secondary" className="mt-2">
            Master podaci, dostupnost, opterećenje i blacklist status.
          </Text>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => setImportOpen(true)}>
            <Upload className="size-4" />
            Uvezi
          </Button>
          <Button
            variant="secondary"
            onClick={() =>
              downloadAuthenticatedFile(
                "/api/codebooks/import-export/export?codebookType=vjestaci&format=xlsx&includeInactive=true",
                "vjestaci.xlsx",
              )
            }
          >
            <Download className="size-4" />
            Izvezi
          </Button>
          <Button variant="secondary" onClick={() => query.refetch()}>
            <RefreshCw className="size-4" />
            Osvježi
          </Button>
          <Button onClick={openCreate}>
            <Plus className="size-4" />
            Novi vještak
          </Button>
        </div>
      </div>
      <div className="mt-6 grid gap-3 md:grid-cols-5">
        <Input
          placeholder="Pretraga po nazivu…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <Input placeholder="Grad" value={city} onChange={(e) => setCity(e.target.value)} />
        <FilterSelect label="Godišnji odmor" value={onLeave} onChange={setOnLeave} />
        <FilterSelect label="Crna lista" value={blacklisted} onChange={setBlacklisted} />
        <FilterSelect label="Aktivnost" value={active} onChange={setActive} />
      </div>
      <div className="mt-6 overflow-x-auto rounded-sm border border-border-subtle bg-surface-default">
        <table className="w-full text-left text-sm">
          <thead className="bg-surface-subtle">
            <tr>
              {[
                "Naziv",
                "Grad",
                "Tip",
                "Aktivne procjene",
                "GO",
                "Blacklist",
                "Aktivan",
                "Akcije",
              ].map((h) => (
                <th key={h} className="px-4 py-3">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle">
            {query.data?.map((a, i) => {
              const id = Number(val(a, "id", "Id"));
              const leave = Boolean(val(a, "isOnLeave", "IsOnLeave"));
              const black = Boolean(val(a, "isBlacklisted", "IsBlacklisted"));
              return (
                <tr key={id || i}>
                  <td className="px-4 py-3">
                    <b>{String(val(a, "name", "Name"))}</b>
                    <p className="text-xs text-text-tertiary">
                      {String(val(a, "contactEmail", "ContactEmail") ?? "")}
                    </p>
                  </td>
                  <td className="px-4 py-3">{String(val(a, "city", "City") ?? "—")}</td>
                  <td className="px-4 py-3">
                    {String(val(a, "legalFormLabel", "LegalForm") ?? "—")}
                  </td>
                  <td className="px-4 py-3">
                    {String(val(a, "activeAssignmentCount", "ActiveAssignmentCount") ?? 0)}
                  </td>
                  <td className="px-4 py-3">
                    <Button
                      size="icon"
                      variant="ghost"
                      onClick={() => flag.mutate({ id, suffix: "on-leave", value: !leave })}
                    >
                      <Palmtree
                        className={`size-4 ${leave ? "text-feedback-warning" : "text-text-tertiary"}`}
                      />
                    </Button>
                  </td>
                  <td className="px-4 py-3">
                    <Button
                      size="icon"
                      variant="ghost"
                      onClick={() => flag.mutate({ id, suffix: "blacklist", value: !black })}
                    >
                      <Ban
                        className={`size-4 ${black ? "text-feedback-danger" : "text-text-tertiary"}`}
                      />
                    </Button>
                  </td>
                  <td className="px-4 py-3">{val(a, "isActive", "IsActive") ? "Da" : "Ne"}</td>
                  <td className="px-4 py-3">
                    <div className="flex gap-1">
                      <Button size="icon" variant="ghost" title="Uredi" onClick={() => openEdit(a)}>
                        <Pencil className="size-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="secondary"
                        onClick={() => confirm("Deaktivirati vještaka?") && deactivate.mutate(id)}
                      >
                        Deaktiviraj
                      </Button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <Dialog
        open={open}
        onOpenChange={(next) => {
          setOpen(next);
          if (!next) setEditingId(undefined);
        }}
      >
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>{editingId ? "Uredi vještaka" : "Novi vještak"}</DialogTitle>
            <DialogDescription>
              Podaci se koriste kod automatskog i ručnog odabira.
            </DialogDescription>
          </DialogHeader>
          <form
            className="grid gap-4 sm:grid-cols-2"
            onSubmit={(e) => {
              e.preventDefault();
              create.mutate();
            }}
          >
            {fields.map(([k, l]) => (
              <label className="grid gap-1 text-sm font-semibold" key={k}>
                {l}
                <Input
                  required={k === "name" || k === "legalForm"}
                  value={String(form[k] ?? "")}
                  onChange={(e) => setForm({ ...form, [k]: e.target.value })}
                />
              </label>
            ))}
            <Button className="sm:col-span-2" type="submit">
              <BriefcaseBusiness className="size-4" />
              {editingId ? "Sačuvaj izmjene" : "Sačuvaj vještaka"}
            </Button>
          </form>
        </DialogContent>
      </Dialog>
      <Dialog open={importOpen} onOpenChange={setImportOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Uvoz vještaka</DialogTitle>
            <DialogDescription>
              Prvo se radi validacijski pregled, a podaci se upisuju tek nakon potvrde.
            </DialogDescription>
          </DialogHeader>
          <Input
            type="file"
            accept=".xlsx,.xls,.csv"
            onChange={(e) => setImportFile(e.target.files?.[0])}
          />
          {!previewToken ? (
            <Button
              onClick={() => importPreview.mutate()}
              disabled={!importFile || importPreview.isPending}
            >
              Pregledaj uvoz
            </Button>
          ) : (
            <div className="rounded-sm border border-feedback-success p-4">
              <p className="text-sm font-semibold">Datoteka je validirana i spremna za upis.</p>
              <Button
                className="mt-3"
                onClick={() => confirmImport.mutate()}
                disabled={confirmImport.isPending}
              >
                Potvrdi uvoz
              </Button>
            </div>
          )}
          {(importPreview.error || confirmImport.error) && (
            <p className="text-sm text-feedback-danger">
              {(importPreview.error ?? confirmImport.error)?.message}
            </p>
          )}
        </DialogContent>
      </Dialog>
    </section>
  );
}
const fields: readonly [keyof Form, string][] = [
  ["name", "Naziv"],
  ["city", "Grad"],
  ["legalForm", "Pravni oblik"],
  ["contactEmail", "E-mail"],
  ["contactPhone", "Telefon"],
  ["supportedPropertyTypes", "Tipovi nekretnina"],
  ["supportedCities", "Podržani gradovi"],
  ["clientScope", "Opseg klijenata"],
  ["notes", "Napomena"],
];

function FilterSelect({
  label,
  value,
  onChange,
}: {
  readonly label: string;
  readonly value: string;
  readonly onChange: (value: string) => void;
}) {
  return (
    <select
      aria-label={label}
      className="h-10 rounded-sm border border-border-subtle bg-surface-default px-3 text-sm"
      value={value}
      onChange={(event) => onChange(event.target.value)}
    >
      <option value="all">{label}: svi</option>
      <option value="true">{label}: da</option>
      <option value="false">{label}: ne</option>
    </select>
  );
}
