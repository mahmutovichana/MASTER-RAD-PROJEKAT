import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Download, KeyRound, Pencil, Plus, Power, RefreshCw, Trash2, X } from "lucide-react";
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
type Row = Readonly<Record<string, unknown>>;
const pick = (r: Row, ...k: string[]) => k.map((x) => r[x]).find((v) => v != null);
const rows = (raw: unknown) => {
  const root = (raw as Row)?.["data"] ?? raw;
  const value = Array.isArray(root) ? root : ((root as Row)?.["items"] ?? (root as Row)?.["Items"]);
  return Array.isArray(value) ? (value as Row[]) : [];
};
export function RolesPage() {
  const cache = useQueryClient();
  const [open, setOpen] = useState(false);
  const [editingId, setEditingId] = useState<number>();
  const [role, setRole] = useState({ name: "", displayName: "", description: "" });
  const [permissionRole, setPermissionRole] = useState<Row>();
  const [permissionId, setPermissionId] = useState("");
  const query = useQuery({
    queryKey: ["role-definitions"],
    queryFn: async () => rows(await apiClient.getLegacy("/api/admin/roles/")),
  });
  const permissions = useQuery({
    queryKey: ["permissions"],
    queryFn: async () => rows(await apiClient.getLegacy("/api/admin/permissions/")),
  });
  const roleDetail = useQuery({
    queryKey: ["role-definition", pick(permissionRole ?? {}, "id", "Id")],
    queryFn: () =>
      apiClient.getLegacy<Row>(
        `/api/admin/roles/${Number(pick(permissionRole ?? {}, "id", "Id"))}`,
      ),
    enabled: Boolean(permissionRole),
  });
  const refresh = () => cache.invalidateQueries({ queryKey: ["role-definitions"] });
  const action = useMutation({
    mutationFn: ({
      method,
      url,
      body,
    }: {
      method: "post" | "put" | "delete";
      url: string;
      body?: unknown;
    }) =>
      method === "delete"
        ? apiClient.deleteLegacy(url)
        : method === "put"
          ? apiClient.putLegacy(url, { body })
          : apiClient.postLegacy(url, body ? { body } : {}),
    onSuccess: async () => {
      setOpen(false);
      setEditingId(undefined);
      setPermissionRole(undefined);
      await refresh();
    },
  });
  const openCreate = () => {
    setEditingId(undefined);
    setRole({ name: "", displayName: "", description: "" });
    setOpen(true);
  };
  const openEdit = (item: Row) => {
    setEditingId(Number(pick(item, "id", "Id")));
    setRole({
      name: String(pick(item, "name", "Name") ?? ""),
      displayName: String(pick(item, "displayName", "DisplayName") ?? ""),
      description: String(pick(item, "description", "Description") ?? ""),
    });
    setOpen(true);
  };
  return (
    <section>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-eyebrow text-text-tertiary">Administracija</p>
          <Heading level={1} size={4} className="mt-2">
            Role i permissioni
          </Heading>
          <Text tone="secondary" className="mt-2">
            Definicije poslovnih uloga sinhronizovane s Keycloak realmom.
          </Text>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => exportRoles(query.data ?? [])}>
            <Download className="size-4" />
            Export CSV
          </Button>
          <Button variant="secondary" onClick={() => query.refetch()}>
            <RefreshCw className="size-4" />
            Osvježi
          </Button>
          <Button onClick={openCreate}>
            <Plus className="size-4" />
            Nova rola
          </Button>
        </div>
      </div>
      <div className="mt-6 rounded-sm border border-border-subtle bg-surface-default p-5">
        <h2 className="font-bold">Centralni katalog permissiona</h2>
        <p className="mt-1 text-sm text-text-secondary">
          Sve dozvole koje se mogu dodijeliti poslovnim rolama, grupisane prema backend modulu.
        </p>
        <div className="mt-4 flex flex-wrap gap-2">
          {permissions.data?.map((permission, index) => (
            <span
              className="rounded-full border border-border-subtle bg-surface-subtle px-3 py-1 text-xs"
              key={index}
              title={String(pick(permission, "description", "Description") ?? "")}
            >
              {String(pick(permission, "module", "Module") ?? "Opšte")} ·{" "}
              {String(
                pick(permission, "displayName", "DisplayName", "name", "Name", "code", "Code"),
              )}
            </span>
          ))}
        </div>
      </div>
      <div className="mt-7 overflow-x-auto rounded-sm border border-border-subtle bg-surface-default">
        <table className="w-full text-left text-sm">
          <thead className="bg-surface-subtle">
            <tr>
              {["Naziv", "Prikazni naziv", "Opis", "Tip", "Status", "Akcije"].map((h) => (
                <th className="px-4 py-3" key={h}>
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle">
            {query.data?.map((r, i) => {
              const id = Number(pick(r, "id", "Id"));
              const active = pick(r, "isActive", "IsActive") !== false;
              return (
                <tr key={id || i}>
                  <td className="px-4 py-3 font-bold">{String(pick(r, "name", "Name"))}</td>
                  <td className="px-4 py-3">
                    {String(pick(r, "displayName", "DisplayName") ?? "—")}
                  </td>
                  <td className="px-4 py-3">
                    {String(pick(r, "description", "Description") ?? "—")}
                  </td>
                  <td className="px-4 py-3">
                    {pick(r, "isSystem", "IsSystem") ? "Sistemska" : "Custom"}
                  </td>
                  <td className="px-4 py-3">{active ? "Aktivna" : "Neaktivna"}</td>
                  <td className="px-4 py-3">
                    <div className="flex gap-1">
                      <Button size="icon" variant="ghost" title="Uredi" onClick={() => openEdit(r)}>
                        <Pencil className="size-4" />
                      </Button>
                      <Button
                        size="icon"
                        variant="ghost"
                        title="Dodaj permission"
                        onClick={() => setPermissionRole(r)}
                      >
                        <KeyRound className="size-4" />
                      </Button>
                      <Button
                        size="icon"
                        variant="ghost"
                        title={active ? "Deaktiviraj" : "Aktiviraj"}
                        onClick={() =>
                          action.mutate({
                            method: "post",
                            url: `/api/admin/roles/${id}/${active ? "deactivate" : "activate"}`,
                          })
                        }
                      >
                        <Power className="size-4" />
                      </Button>
                      <Button
                        size="icon"
                        variant="ghost"
                        title="Obriši"
                        onClick={() =>
                          confirm("Obrisati custom rolu?") &&
                          action.mutate({ method: "delete", url: `/api/admin/roles/${id}` })
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
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{editingId ? "Uredi poslovnu rolu" : "Nova poslovna rola"}</DialogTitle>
            <DialogDescription>
              Rola će biti kreirana u aplikaciji i sinhronizovana u Keycloak.
            </DialogDescription>
          </DialogHeader>
          <form
            className="grid gap-3"
            onSubmit={(e) => {
              e.preventDefault();
              action.mutate({
                method: editingId ? "put" : "post",
                url: editingId ? `/api/admin/roles/${editingId}` : "/api/admin/roles/",
                body: editingId
                  ? { displayName: role.displayName, description: role.description }
                  : role,
              });
            }}
          >
            {Object.entries(role).map(([k, v]) => (
              <label className="grid gap-1 text-sm font-bold" key={k}>
                {k}
                <Input
                  required={k !== "description"}
                  disabled={Boolean(editingId) && k === "name"}
                  value={v}
                  onChange={(e) => setRole({ ...role, [k]: e.target.value })}
                />
              </label>
            ))}
            <Button type="submit">Kreiraj rolu</Button>
          </form>
        </DialogContent>
      </Dialog>
      <Dialog
        open={Boolean(permissionRole)}
        onOpenChange={(o) => !o && setPermissionRole(undefined)}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Dodaj permission</DialogTitle>
            <DialogDescription>Odaberite permission iz centralnog kataloga.</DialogDescription>
          </DialogHeader>
          <select
            className="h-11 rounded-sm border border-border-subtle bg-surface-default px-3"
            value={permissionId}
            onChange={(e) => setPermissionId(e.target.value)}
          >
            <option value="">Odaberite…</option>
            {permissions.data?.map((p, i) => (
              <option key={i} value={String(pick(p, "id", "Id"))}>
                {String(pick(p, "displayName", "DisplayName", "name", "Name", "code", "Code"))}
              </option>
            ))}
          </select>
          <Button
            disabled={!permissionId}
            onClick={() =>
              permissionRole &&
              action.mutate({
                method: "post",
                url: `/api/admin/roles/${Number(pick(permissionRole, "id", "Id"))}/permissions`,
                body: { permissionDefinitionId: Number(permissionId) },
              })
            }
          >
            Dodaj permission
          </Button>
          <div className="divide-y divide-border-subtle rounded-sm border border-border-subtle">
            {assignedPermissions(roleDetail.data).map((permission, index) => {
              const permissionIdValue = Number(
                pick(permission, "id", "Id", "permissionDefinitionId"),
              );
              return (
                <div
                  className="flex items-center justify-between gap-3 p-3 text-sm"
                  key={permissionIdValue || index}
                >
                  <span>
                    {String(
                      pick(
                        permission,
                        "displayName",
                        "DisplayName",
                        "name",
                        "Name",
                        "code",
                        "Code",
                      ) ?? permissionIdValue,
                    )}
                  </span>
                  <Button
                    size="icon"
                    variant="ghost"
                    title="Ukloni permission"
                    onClick={() =>
                      action.mutate({
                        method: "delete",
                        url: `/api/admin/roles/${Number(pick(permissionRole ?? {}, "id", "Id"))}/permissions/${permissionIdValue}`,
                      })
                    }
                  >
                    <X className="size-4" />
                  </Button>
                </div>
              );
            })}
          </div>
        </DialogContent>
      </Dialog>
    </section>
  );
}
function assignedPermissions(detail: Row | undefined): Row[] {
  if (!detail) return [];
  const root = (detail["data"] as Row | undefined) ?? detail;
  const value = root["permissions"] ?? root["Permissions"];
  return Array.isArray(value) ? (value as Row[]) : [];
}

function exportRoles(roles: readonly Row[]) {
  const rows = [
    ["Naziv", "Prikazni naziv", "Opis", "Tip", "Status", "Broj permissiona"],
    ...roles.map((role) => [
      pick(role, "name", "Name"),
      pick(role, "displayName", "DisplayName"),
      pick(role, "description", "Description"),
      pick(role, "isSystem", "IsSystem") ? "Sistemska" : "Custom",
      pick(role, "isActive", "IsActive") !== false ? "Aktivna" : "Neaktivna",
      pick(role, "permissionCount", "PermissionCount") ?? 0,
    ]),
  ];
  const csv = rows
    .map((row) => row.map((value) => `"${String(value ?? "").replaceAll('"', '""')}"`).join(","))
    .join("\r\n");
  const url = URL.createObjectURL(new Blob(["\uFEFF", csv], { type: "text/csv;charset=utf-8" }));
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "role.csv";
  anchor.click();
  URL.revokeObjectURL(url);
}
