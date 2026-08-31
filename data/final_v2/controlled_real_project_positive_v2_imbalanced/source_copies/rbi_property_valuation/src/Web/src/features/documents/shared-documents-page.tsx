import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Download, FileUp, Trash2 } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Heading, Text } from "@/components/ui/typography";
import { downloadAuthenticatedFile } from "@/lib/api/file-client";
import { apiClient } from "@/lib/api/http-client";
type Row = Readonly<Record<string, unknown>>;
const pick = (r: Row, ...k: string[]) => k.map((x) => r[x]).find((v) => v != null);
async function load(): Promise<Row[]> {
  const raw = await apiClient.getLegacy<unknown>("/api/shared-documents/");
  const root = (raw as Row)?.["data"] ?? raw;
  return Array.isArray(root) ? (root as Row[]) : [];
}
export function SharedDocumentsPage() {
  const cache = useQueryClient();
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState("Ostalo");
  const query = useQuery({ queryKey: ["shared-documents"], queryFn: load });
  const refresh = () => cache.invalidateQueries({ queryKey: ["shared-documents"] });
  const upload = useMutation({
    mutationFn: (file: File) => {
      const body = new FormData();
      body.append("file", file);
      body.append("title", title);
      body.append("category", category);
      return apiClient.postLegacy("/api/shared-documents/", { body });
    },
    onSuccess: refresh,
  });
  const remove = useMutation({
    mutationFn: (id: number) => apiClient.deleteLegacy(`/api/shared-documents/${id}`),
    onSuccess: refresh,
  });
  return (
    <section>
      <div>
        <p className="text-eyebrow text-text-tertiary">Operacije</p>
        <Heading level={1} size={4} className="mt-2">
          Zajednički dokumenti
        </Heading>
        <Text tone="secondary" className="mt-2">
          Cjenovnici, obrasci i zajednička dokumentacija dostupna učesnicima procesa.
        </Text>
      </div>
      <div className="mt-6 flex flex-wrap items-end gap-3 rounded-sm border border-border-subtle bg-surface-default p-5">
        <label className="grid gap-1 text-sm font-bold">
          Naslov
          <Input value={title} onChange={(e) => setTitle(e.target.value)} />
        </label>
        <label className="grid gap-1 text-sm font-bold">
          Kategorija
          <Input value={category} onChange={(e) => setCategory(e.target.value)} />
        </label>
        <label className="inline-flex h-10 cursor-pointer items-center gap-2 rounded-sm bg-surface-brand px-4 text-sm font-bold text-text-on-brand">
          <FileUp className="size-4" />
          Dodaj dokument
          <input
            className="sr-only"
            type="file"
            onChange={(e) => {
              const f = e.target.files?.[0];
              if (f && title) upload.mutate(f);
            }}
          />
        </label>
      </div>
      <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        {query.data?.map((d, i) => {
          const id = Number(pick(d, "id", "Id"));
          const name = String(
            pick(d, "fileName", "FileName", "title", "Title") ?? `dokument-${id}`,
          );
          return (
            <article
              className="rounded-sm border border-border-subtle bg-surface-default p-5"
              key={id || i}
            >
              <h2 className="font-bold">{String(pick(d, "title", "Title") ?? name)}</h2>
              <p className="mt-2 text-xs text-text-tertiary">
                {String(pick(d, "category", "Category") ?? "—")}
              </p>
              <div className="mt-4 flex gap-2">
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={() =>
                    downloadAuthenticatedFile(`/api/shared-documents/${id}/download`, name)
                  }
                >
                  <Download className="size-4" />
                  Preuzmi
                </Button>
                <Button
                  size="icon"
                  variant="ghost"
                  onClick={() => confirm("Obrisati dokument?") && remove.mutate(id)}
                >
                  <Trash2 className="size-4" />
                </Button>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}
