import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Download, Pencil, Plus, Power, RefreshCw, Trash2, Upload } from "lucide-react";
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
import { apiClient } from "@/lib/api/http-client";
import { downloadAuthenticatedFile } from "@/lib/api/file-client";
type Row = Readonly<Record<string, unknown>>;
const pick = (r: Row, ...k: string[]) => k.map((x) => r[x]).find((v) => v != null);
const unwrap = (raw: unknown) => {
  const root = (raw as Row)?.["data"] ?? raw;
  const items = Array.isArray(root) ? root : ((root as Row)?.["items"] ?? (root as Row)?.["Items"]);
  return Array.isArray(items) ? (items as Row[]) : [];
};
export function CodebooksPage() {
  const cache = useQueryClient();
  const [selected, setSelected] = useState<string>();
  const [bookOpen, setBookOpen] = useState(false);
  const [valueOpen, setValueOpen] = useState(false);
  const [editingBook, setEditingBook] = useState(false);
  const [editingValueId, setEditingValueId] = useState<number>();
  const [importFile, setImportFile] = useState<File>();
  const [previewToken, setPreviewToken] = useState("");
  const [importOpen, setImportOpen] = useState(false);
  const [book, setBook] = useState({ code: "", name: "", description: "", category: "" });
  const [value, setValue] = useState({ code: "", label: "", description: "", sortOrder: 0 });
  const books = useQuery({
    queryKey: ["codebooks"],
    queryFn: async () => unwrap(await apiClient.getLegacy("/api/admin/codebooks/")),
  });
  const values = useQuery({
    queryKey: ["codebooks", selected, "values"],
    queryFn: async () => unwrap(await apiClient.getLegacy(`/api/codebooks/${selected}/values`)),
    enabled: Boolean(selected),
  });
  const refresh = () => cache.invalidateQueries({ queryKey: ["codebooks"] });
  const mutate = useMutation({
    mutationFn: ({
      url,
      method,
      body,
    }: {
      url: string;
      method: "post" | "put" | "delete";
      body?: unknown;
    }) =>
      method === "delete"
        ? apiClient.deleteLegacy(url)
        : method === "put"
          ? apiClient.putLegacy(url, { body })
          : apiClient.postLegacy(url, body ? { body } : {}),
    onSuccess: async () => {
      setBookOpen(false);
      setValueOpen(false);
      setEditingBook(false);
      setEditingValueId(undefined);
      await refresh();
    },
  });
  const importPreview = useMutation({
    mutationFn: async () => {
      const data = new FormData();
      if (!importFile || !selected) throw new Error("Odaberite šifarnik i datoteku.");
      data.append("file", importFile);
      const result = await apiClient.postLegacy<Row>("/api/codebooks/import-export/preview", {
        query: { codebookType: selected, mode: 0 },
        body: data,
      });
      setPreviewToken(String(pick(result, "previewToken", "PreviewToken") ?? ""));
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
      await refresh();
    },
  });
  const editBook = (row: Row) => {
    setBook({
      code: String(pick(row, "code", "Code") ?? ""),
      name: String(pick(row, "name", "Name") ?? ""),
      description: String(pick(row, "description", "Description") ?? ""),
      category: String(pick(row, "category", "Category") ?? ""),
    });
    setEditingBook(true);
    setBookOpen(true);
  };
  const editValue = (row: Row) => {
    setEditingValueId(Number(pick(row, "id", "Id")));
    setValue({
      code: String(pick(row, "code", "Code") ?? ""),
      label: String(pick(row, "label", "Label") ?? ""),
      description: String(pick(row, "description", "Description") ?? ""),
      sortOrder: Number(pick(row, "sortOrder", "SortOrder") ?? 0),
    });
    setValueOpen(true);
  };
  return (
    <section className="min-w-0">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="text-eyebrow text-text-tertiary">Administracija</p>
          <Heading level={1} size={4} className="mt-2">
            Šifarnici
          </Heading>
          <Text tone="secondary" className="mt-2">
            Kontejneri i vrijednosti centralnih poslovnih šifarnika.
          </Text>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button variant="secondary" onClick={() => books.refetch()}>
            <RefreshCw className="size-4" />
            Osvježi
          </Button>
          <Button
            onClick={() => {
              setEditingBook(false);
              setBook({ code: "", name: "", description: "", category: "" });
              setBookOpen(true);
            }}
          >
            <Plus className="size-4" />
            Novi šifarnik
          </Button>
        </div>
      </div>
      <div className="mt-7 grid min-w-0 gap-6 xl:grid-cols-[minmax(18rem,22rem)_minmax(0,1fr)]">
        <div className="min-w-0 rounded-sm border border-border-subtle bg-surface-default p-3">
          {books.data?.map((b, i) => {
            const code = String(pick(b, "code", "Code"));
            const active = pick(b, "isActive", "IsActive") !== false;
            return (
              <div
                key={code || i}
                className={`mb-1 grid min-w-0 grid-cols-[minmax(0,1fr)_auto] items-center gap-2 rounded-sm p-2 text-left ${selected === code ? "bg-surface-brand text-text-on-brand" : "hover:bg-surface-subtle"}`}
              >
                <button
                  type="button"
                  className="grid min-w-0 gap-1 text-left"
                  onClick={() => setSelected(code)}
                >
                  <span className="min-w-0">
                    <b className="block break-words">{String(pick(b, "name", "Name"))}</b>
                    <small className="block break-all opacity-70">{code}</small>
                  </span>
                  <span className="text-xs opacity-80">{active ? "Aktivan" : "Neaktivan"}</span>
                </button>
                <span className="flex shrink-0 items-center gap-1">
                  <Button
                    size="icon"
                    variant="ghost"
                    title="Uredi šifarnik"
                    onClick={(event) => {
                      event.stopPropagation();
                      editBook(b);
                    }}
                  >
                    <Pencil className="size-4" />
                  </Button>
                  <Button
                    size="icon"
                    variant="ghost"
                    title={active ? "Deaktiviraj" : "Aktiviraj"}
                    onClick={(event) => {
                      event.stopPropagation();
                      mutate.mutate({
                        url: `/api/admin/codebooks/${code}/${active ? "deactivate" : "activate"}`,
                        method: "post",
                      });
                    }}
                  >
                    <Power className="size-4" />
                  </Button>
                  <Button
                    size="icon"
                    variant="ghost"
                    title="Obriši šifarnik"
                    onClick={(event) => {
                      event.stopPropagation();
                      if (confirm("Obrisati šifarnik?"))
                        mutate.mutate({ url: `/api/admin/codebooks/${code}`, method: "delete" });
                    }}
                  >
                    <Trash2 className="size-4" />
                  </Button>
                </span>
              </div>
            );
          })}
        </div>
        <div className="min-w-0 rounded-sm border border-border-subtle bg-surface-default p-5">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h2 className="font-bold">Vrijednosti {selected ?? ""}</h2>
            {selected && (
              <div className="flex flex-wrap gap-2">
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={() =>
                    downloadAuthenticatedFile(
                      `/api/codebooks/import-export/export?codebookType=${encodeURIComponent(selected)}&format=xlsx&includeInactive=true`,
                      `${selected}.xlsx`,
                    )
                  }
                >
                  <Download className="size-4" />
                  Izvoz
                </Button>
                <Button size="sm" variant="secondary" onClick={() => setImportOpen(true)}>
                  <Upload className="size-4" />
                  Uvoz
                </Button>
                <Button
                  size="sm"
                  onClick={() => {
                    setEditingValueId(undefined);
                    setValue({ code: "", label: "", description: "", sortOrder: 0 });
                    setValueOpen(true);
                  }}
                >
                  <Plus className="size-4" />
                  Nova vrijednost
                </Button>
              </div>
            )}
          </div>
          {!selected && <p className="mt-8 text-center text-text-secondary">Odaberite šifarnik.</p>}
          <div className="mt-4 divide-y divide-border-subtle">
            {values.data?.map((v, i) => {
              const id = Number(pick(v, "id", "Id"));
              const active = pick(v, "isActive", "IsActive") !== false;
              return (
                <div key={id || i} className="flex items-center justify-between gap-3 py-3">
                  <div>
                    <b>{String(pick(v, "label", "Label"))}</b>
                    <p className="text-xs text-text-tertiary">{String(pick(v, "code", "Code"))}</p>
                  </div>
                  <div className="flex gap-1">
                    <Button size="icon" variant="ghost" title="Uredi" onClick={() => editValue(v)}>
                      <Pencil className="size-4" />
                    </Button>
                    <Button
                      size="icon"
                      variant="ghost"
                      onClick={() =>
                        mutate.mutate({
                          url: `/api/codebooks/${selected}/values/${id}/${active ? "deactivate" : "activate"}`,
                          method: "post",
                          body: active ? { reason: "Administrativna izmjena" } : undefined,
                        })
                      }
                    >
                      <Power className="size-4" />
                    </Button>
                    <Button
                      size="icon"
                      variant="ghost"
                      onClick={() =>
                        confirm("Obrisati vrijednost?") &&
                        mutate.mutate({
                          url: `/api/codebooks/${selected}/values/${id}`,
                          method: "delete",
                        })
                      }
                    >
                      <Trash2 className="size-4" />
                    </Button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
      <Dialog open={bookOpen} onOpenChange={setBookOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{editingBook ? "Uredi šifarnik" : "Novi šifarnik"}</DialogTitle>
            <DialogDescription>Kod mora biti jedinstven.</DialogDescription>
          </DialogHeader>
          <form
            className="grid gap-3"
            onSubmit={(e) => {
              e.preventDefault();
              mutate.mutate({
                url: editingBook ? `/api/admin/codebooks/${book.code}` : "/api/admin/codebooks/",
                method: editingBook ? "put" : "post",
                body: editingBook
                  ? { name: book.name, description: book.description, category: book.category }
                  : book,
              });
            }}
          >
            {Object.entries(book).map(([k, v]) => (
              <label className="grid gap-1 text-sm font-bold" key={k}>
                {k}
                <Input
                  required={k === "code" || k === "name"}
                  disabled={editingBook && k === "code"}
                  value={v}
                  onChange={(e) => setBook({ ...book, [k]: e.target.value })}
                />
              </label>
            ))}
            <Button type="submit">Sačuvaj</Button>
          </form>
        </DialogContent>
      </Dialog>
      <Dialog open={valueOpen} onOpenChange={setValueOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{editingValueId ? "Uredi vrijednost" : "Nova vrijednost"}</DialogTitle>
            <DialogDescription>Vrijednost se dodaje u {selected}.</DialogDescription>
          </DialogHeader>
          <form
            className="grid gap-3"
            onSubmit={(e) => {
              e.preventDefault();
              mutate.mutate({
                url: `/api/codebooks/${selected}/values${editingValueId ? `/${editingValueId}` : ""}`,
                method: editingValueId ? "put" : "post",
                body: editingValueId
                  ? {
                      label: value.label,
                      description: value.description,
                      sortOrder: value.sortOrder,
                    }
                  : value,
              });
            }}
          >
            {Object.entries(value).map(([k, v]) => (
              <label className="grid gap-1 text-sm font-bold" key={k}>
                {k}
                <Input
                  required={k === "code" || k === "label"}
                  disabled={Boolean(editingValueId) && k === "code"}
                  type={k === "sortOrder" ? "number" : "text"}
                  value={v}
                  onChange={(e) =>
                    setValue({
                      ...value,
                      [k]: k === "sortOrder" ? Number(e.target.value) : e.target.value,
                    })
                  }
                />
              </label>
            ))}
            <Button type="submit">Sačuvaj vrijednost</Button>
          </form>
        </DialogContent>
      </Dialog>
      <Dialog open={importOpen} onOpenChange={setImportOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Uvoz šifarnika</DialogTitle>
            <DialogDescription>
              Prvo pregledajte validaciju; upis se izvršava tek nakon potvrde.
            </DialogDescription>
          </DialogHeader>
          <Input
            type="file"
            accept=".csv,.xlsx"
            onChange={(event) => setImportFile(event.target.files?.[0])}
          />
          {importPreview.data && (
            <pre className="max-h-64 overflow-auto rounded-sm bg-surface-subtle p-3 text-xs">
              {JSON.stringify(importPreview.data, null, 2)}
            </pre>
          )}
          {importPreview.error && (
            <p className="text-sm text-feedback-danger">{importPreview.error.message}</p>
          )}
          <div className="flex justify-end gap-2">
            <Button
              variant="secondary"
              disabled={!importFile || importPreview.isPending}
              onClick={() => importPreview.mutate()}
            >
              Pregled uvoza
            </Button>
            <Button
              disabled={!previewToken || confirmImport.isPending}
              onClick={() => confirmImport.mutate()}
            >
              Potvrdi uvoz
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </section>
  );
}
