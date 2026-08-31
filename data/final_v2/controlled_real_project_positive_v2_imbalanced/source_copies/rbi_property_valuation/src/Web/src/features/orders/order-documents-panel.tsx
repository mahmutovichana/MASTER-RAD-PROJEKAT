import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Download, FilePlus2, FileUp, Power, RefreshCw, Trash2 } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { downloadAuthenticatedFile } from "@/lib/api/file-client";
import { apiClient } from "@/lib/api/http-client";

import {
  deactivateDocument,
  deleteDocument,
  getOrderCollection,
  reactivateDocument,
  replaceOrderDocument,
  uploadOrderDocuments,
  type OrderRecord,
} from "./orders-api";
const pick = (r: OrderRecord, ...keys: string[]) => keys.map((k) => r[k]).find((v) => v != null);
export function OrderDocumentsPanel({
  orderId,
  canGenerate = false,
}: {
  readonly orderId: number;
  readonly canGenerate?: boolean;
}) {
  const cache = useQueryClient();
  const [typeId, setTypeId] = useState(1);
  const query = useQuery({
    queryKey: ["orders", orderId, "documents"],
    queryFn: () => getOrderCollection(orderId, "documents"),
  });
  const documentTypes = useQuery({
    queryKey: ["codebook", "tipovi_dokumenata", "active"],
    queryFn: async () => {
      const raw = await apiClient.getLegacy<unknown>(
        "/api/codebooks/tipovi_dokumenata/values/active",
      );
      const root = (raw as OrderRecord)?.["data"] ?? raw;
      return Array.isArray(root) ? (root as OrderRecord[]) : [];
    },
  });
  const refresh = () => cache.invalidateQueries({ queryKey: ["orders", orderId, "documents"] });
  const upload = useMutation({
    mutationFn: (files: FileList) => uploadOrderDocuments(orderId, typeId, files),
    onSuccess: refresh,
  });
  const action = useMutation({
    mutationFn: ({ kind, id }: { kind: string; id: number }) =>
      kind === "delete"
        ? deleteDocument(id)
        : kind === "activate"
          ? reactivateDocument(id)
          : deactivateDocument(id, prompt("Razlog deaktivacije:") ?? ""),
    onSuccess: refresh,
  });
  const replace = useMutation({
    mutationFn: ({ id, file }: { id: number; file: File }) => replaceOrderDocument(id, file),
    onSuccess: refresh,
  });
  const generate = useMutation({
    mutationFn: () =>
      apiClient.postLegacy(`/api/orders/${orderId}/documents/generate`, {
        body: { iznos: null, zkOznaka: null },
      }),
    onSuccess: refresh,
  });
  return (
    <div className="rounded-sm border border-border-subtle bg-surface-default p-5 xl:col-span-3">
      <h2 className="font-bold">Dokumenti narudžbe</h2>
      <div className="mt-4 flex flex-wrap items-end gap-3">
        <label className="grid gap-1 text-xs font-bold">
          Tip dokumenta
          <select
            className="h-10 min-w-56 rounded-sm border border-border-subtle bg-surface-default px-3 text-sm"
            value={typeId}
            onChange={(event) => setTypeId(Number(event.target.value))}
          >
            {documentTypes.data?.map((type, index) => (
              <option key={index} value={Number(pick(type, "id", "Id"))}>
                {String(pick(type, "label", "Label", "code", "Code"))}
              </option>
            ))}
          </select>
        </label>
        <label className="inline-flex h-10 cursor-pointer items-center gap-2 rounded-sm bg-surface-brand px-4 text-sm font-bold text-text-on-brand">
          <FileUp className="size-4" />
          Dodaj PDF
          <input
            className="sr-only"
            type="file"
            accept="application/pdf"
            multiple
            onChange={(e) => e.target.files?.length && upload.mutate(e.target.files)}
          />
        </label>
        {canGenerate && (
          <Button
            variant="secondary"
            disabled={generate.isPending}
            onClick={() => generate.mutate()}
          >
            <FilePlus2 className="size-4" />
            Generiši dokumente
          </Button>
        )}
        <Button variant="ghost" onClick={() => query.refetch()}>
          <RefreshCw className="size-4" />
          Osvježi
        </Button>
      </div>
      {upload.error && <p className="mt-2 text-feedback-danger">{upload.error.message}</p>}
      <div className="mt-5 overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead>
            <tr>
              {["Naziv", "Tip", "Verzija", "Aktivan", "Akcije"].map((x) => (
                <th className="border-b border-border-subtle p-3" key={x}>
                  {x}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {query.data?.map((d, i) => {
              const id = Number(pick(d, "id", "Id"));
              const active = Boolean(pick(d, "isActive", "IsActive"));
              const name = String(
                pick(d, "fileName", "FileName", "name", "Name") ?? `dokument-${id}`,
              );
              return (
                <tr key={id || i}>
                  <td className="p-3 font-semibold">{name}</td>
                  <td className="p-3">
                    {String(
                      pick(
                        d,
                        "documentTypeLabel",
                        "DocumentTypeLabel",
                        "documentType",
                        "DocumentType",
                      ) ?? "—",
                    )}
                  </td>
                  <td className="p-3">{String(pick(d, "version", "Version") ?? "—")}</td>
                  <td className="p-3">{active ? "Da" : "Ne"}</td>
                  <td className="p-3">
                    <div className="flex gap-1">
                      <Button
                        size="icon"
                        variant="ghost"
                        title="Preuzmi"
                        onClick={() =>
                          downloadAuthenticatedFile(`/api/documents/${id}/download`, name)
                        }
                      >
                        <Download className="size-4" />
                      </Button>
                      <label
                        className="inline-flex size-10 cursor-pointer items-center justify-center rounded-sm hover:bg-surface-subtle"
                        title="Nova verzija"
                      >
                        <FileUp className="size-4" />
                        <input
                          className="sr-only"
                          type="file"
                          accept="application/pdf"
                          onChange={(event) => {
                            const file = event.target.files?.[0];
                            if (file) replace.mutate({ id, file });
                          }}
                        />
                      </label>
                      <Button
                        size="icon"
                        variant="ghost"
                        title={active ? "Deaktiviraj" : "Aktiviraj"}
                        onClick={() =>
                          action.mutate({ kind: active ? "deactivate" : "activate", id })
                        }
                      >
                        <Power className="size-4" />
                      </Button>
                      <Button
                        size="icon"
                        variant="ghost"
                        title="Obriši"
                        onClick={() =>
                          confirm("Obrisati dokument?") && action.mutate({ kind: "delete", id })
                        }
                      >
                        <Trash2 className="size-4" />
                      </Button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
