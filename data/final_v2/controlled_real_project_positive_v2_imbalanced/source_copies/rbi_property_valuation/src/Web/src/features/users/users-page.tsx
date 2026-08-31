import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  ArrowRightLeft,
  Download,
  Plus,
  RefreshCw,
  ShieldMinus,
  UserCheck,
  UserX,
} from "lucide-react";
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
import { useBusinessText } from "@/localization/use-business-text";
type User = Readonly<Record<string, unknown>>;
const pick = (u: User, ...k: string[]) => k.map((x) => u[x]).find((v) => v != null);
async function load(search: string): Promise<readonly User[]> {
  const raw = await apiClient.getLegacy<unknown>("/api/users", {
    query: { Search: search || undefined, Page: 1, PageSize: 100 },
  });
  const root = (raw as Record<string, unknown>)?.["data"] ?? raw;
  const items = Array.isArray(root)
    ? root
    : ((root as Record<string, unknown>)?.["items"] ??
      (root as Record<string, unknown>)?.["Items"]);
  return Array.isArray(items) ? (items as User[]) : [];
}
export function UsersPage() {
  const bt = useBusinessText();
  const cache = useQueryClient();
  const [search, setSearch] = useState("");
  const [roleUser, setRoleUser] = useState<User>();
  const [role, setRole] = useState("");
  const [transferSource, setTransferSource] = useState<User>();
  const [transferTargetId, setTransferTargetId] = useState("");
  const [transferReason, setTransferReason] = useState("");
  const query = useQuery({ queryKey: ["users", search], queryFn: () => load(search) });
  const roleDefinitions = useQuery({
    queryKey: ["role-definitions", "active"],
    queryFn: async () => {
      const raw = await apiClient.getLegacy<unknown>("/api/admin/roles/", {
        query: { IsActive: true, PageSize: 100 },
      });
      const root = (raw as User)?.["data"] ?? raw;
      const items = Array.isArray(root) ? root : (root as User)?.["items"];
      return Array.isArray(items) ? (items as User[]) : [];
    },
  });
  const refresh = () => cache.invalidateQueries({ queryKey: ["users"] });
  const status = useMutation({
    mutationFn: ({ id, suspend }: { id: string; suspend: boolean }) =>
      apiClient.postLegacy(
        `/api/users/${id}/${suspend ? "suspend" : "reactivate"}`,
        suspend ? { body: { reason: prompt("Razlog suspenzije:") ?? "" } } : {},
      ),
    onSuccess: async () => {
      toast.success(bt("Status korisnika je ažuriran.", "User status updated."));
      await refresh();
    },
    onError: (error) => toast.error(error.message),
  });
  const roleMutation = useMutation({
    mutationFn: ({ id, remove }: { id: string; remove: boolean }) =>
      apiClient.postLegacy(`/api/roles/${remove ? "remove" : "assign"}`, {
        body: { userId: id, roleName: role },
      }),
    onSuccess: async () => {
      setRoleUser(undefined);
      setRole("");
      await refresh();
      toast.success(bt("Uloga je ažurirana.", "Role assignment updated."));
    },
    onError: (error) => toast.error(error.message),
  });
  const transfer = useMutation({
    mutationFn: () =>
      apiClient.postLegacy("/api/roles/transfer-admin", {
        body: {
          sourceUserId: String(pick(transferSource ?? {}, "id", "Id", "userId", "UserId")),
          targetUserId: transferTargetId,
          reason: transferReason,
        },
      }),
    onSuccess: async () => {
      setTransferSource(undefined);
      setTransferTargetId("");
      setTransferReason("");
      await refresh();
      toast.success(bt("Administratorska uloga je prenesena.", "Administrator role transferred."));
    },
    onError: (error) => toast.error(error.message),
  });
  return (
    <section className="min-w-0">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="text-eyebrow text-text-tertiary">
            {bt("Administracija", "Administration")}
          </p>
          <Heading level={1} size={4} className="mt-2">
            {bt("Korisnici i pristupi", "Users and access")}
          </Heading>
          <Text tone="secondary" className="mt-2">
            {bt(
              "Keycloak korisnici, status naloga i poslovne uloge.",
              "Keycloak users, account status, and business roles.",
            )}
          </Text>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button variant="secondary" onClick={() => exportUsers(query.data ?? [])}>
            <Download className="size-4" />
            {bt("Izvezi CSV", "Export CSV")}
          </Button>
          <Button variant="secondary" onClick={() => query.refetch()}>
            <RefreshCw className="size-4" />
            {bt("Osvježi", "Refresh")}
          </Button>
        </div>
      </div>
      <Input
        className="mt-6 max-w-md"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder={bt("Korisničko ime, ime ili e-mail…", "Username, name, or email…")}
      />
      <div className="mt-6 max-w-full overflow-x-auto rounded-sm border border-border-subtle bg-surface-default">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-surface-subtle">
            <tr>
              {[
                bt("Korisnik", "User"),
                bt("E-mail", "Email"),
                bt("Uloge", "Roles"),
                bt("Status", "Status"),
                bt("Akcije", "Actions"),
              ].map((x) => (
                <th className="px-4 py-3" key={x}>
                  {x}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle">
            {query.data?.map((u, i) => {
              const id = String(pick(u, "id", "Id", "userId", "UserId"));
              const active = pick(u, "isActive", "IsActive", "enabled", "Enabled") !== false;
              const roles = pick(u, "roles", "Roles");
              return (
                <tr key={id || i}>
                  <td className="px-4 py-3">
                    <b>
                      {String(pick(u, "displayName", "DisplayName", "username", "Username") ?? "—")}
                    </b>
                    <p className="text-xs text-text-tertiary">
                      {String(pick(u, "username", "Username") ?? "")}
                    </p>
                  </td>
                  <td className="px-4 py-3">{String(pick(u, "email", "Email") ?? "—")}</td>
                  <td className="px-4 py-3">
                    {Array.isArray(roles) ? roles.join(", ") : String(roles ?? "—")}
                  </td>
                  <td className="px-4 py-3">{active ? "Aktivan" : "Suspendovan"}</td>
                  <td className="px-4 py-3">
                    <div className="flex items-center justify-end gap-1">
                      <Button
                        size="icon"
                        variant="ghost"
                        title={active ? "Suspenduj" : "Reaktiviraj"}
                        onClick={() => status.mutate({ id, suspend: active })}
                      >
                        {active ? <UserX className="size-4" /> : <UserCheck className="size-4" />}
                      </Button>
                      <Button
                        size="icon"
                        variant="ghost"
                        title="Dodijeli rolu"
                        onClick={() => setRoleUser(u)}
                      >
                        <Plus className="size-4" />
                      </Button>
                      <Button
                        size="icon"
                        variant="ghost"
                        title="Ukloni rolu"
                        onClick={() => {
                          setRoleUser(u);
                          setRole(Array.isArray(roles) ? String(roles[0] ?? "") : "");
                        }}
                      >
                        <ShieldMinus className="size-4" />
                      </Button>
                      <Button
                        size="icon"
                        variant="ghost"
                        title="Prenesi administratorsku ulogu"
                        onClick={() => setTransferSource(u)}
                      >
                        <ArrowRightLeft className="size-4" />
                      </Button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {query.isLoading && (
          <p className="p-8 text-center text-text-secondary">
            {bt("Učitavanje korisnika…", "Loading users…")}
          </p>
        )}
        {query.isError && (
          <p className="p-8 text-center text-feedback-danger">{query.error.message}</p>
        )}
        {!query.isLoading && !query.isError && !query.data?.length && (
          <p className="p-8 text-center text-text-secondary">
            {bt("Nema korisnika za prikaz.", "No users to display.")}
          </p>
        )}
      </div>
      <Dialog open={Boolean(roleUser)} onOpenChange={(o) => !o && setRoleUser(undefined)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{bt("Upravljanje ulogom", "Manage role")}</DialogTitle>
            <DialogDescription>
              Dodjela i uklanjanje se provjeravaju na backendu i evidentiraju u auditu.
            </DialogDescription>
          </DialogHeader>
          <label className="grid gap-1 text-sm font-bold">
            Naziv role
            <Input
              list="role-definitions"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              placeholder="npr. KolateralAdministrator"
            />
            <datalist id="role-definitions">
              {roleDefinitions.data?.map((item, index) => (
                <option key={index} value={String(pick(item, "name", "Name") ?? "")} />
              ))}
            </datalist>
          </label>
          <div className="flex justify-end gap-2">
            <Button
              variant="destructive"
              disabled={!role}
              onClick={() =>
                roleUser &&
                roleMutation.mutate({
                  id: String(pick(roleUser, "id", "Id", "userId", "UserId")),
                  remove: true,
                })
              }
            >
              Ukloni
            </Button>
            <Button
              disabled={!role}
              onClick={() =>
                roleUser &&
                roleMutation.mutate({
                  id: String(pick(roleUser, "id", "Id", "userId", "UserId")),
                  remove: false,
                })
              }
            >
              Dodijeli
            </Button>
          </div>
        </DialogContent>
      </Dialog>
      <Dialog
        open={Boolean(transferSource)}
        onOpenChange={(next) => !next && setTransferSource(undefined)}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Prijenos administratorske uloge</DialogTitle>
            <DialogDescription>
              Backend prvo dodjeljuje administratorsku ulogu ciljnom korisniku, a tek zatim je
              uklanja izvornom korisniku.
            </DialogDescription>
          </DialogHeader>
          <label className="grid gap-1 text-sm font-bold">
            Ciljni korisnik
            <select
              className="h-11 rounded-sm border border-border-subtle bg-surface-default px-3"
              value={transferTargetId}
              onChange={(event) => setTransferTargetId(event.target.value)}
            >
              <option value="">Odaberite korisnika…</option>
              {query.data
                ?.filter(
                  (item) =>
                    String(pick(item, "id", "Id", "userId", "UserId")) !==
                    String(pick(transferSource ?? {}, "id", "Id", "userId", "UserId")),
                )
                .map((item, index) => (
                  <option key={index} value={String(pick(item, "id", "Id", "userId", "UserId"))}>
                    {String(pick(item, "displayName", "DisplayName", "username", "Username"))}
                  </option>
                ))}
            </select>
          </label>
          <label className="grid gap-1 text-sm font-bold">
            Razlog
            <Input
              value={transferReason}
              onChange={(event) => setTransferReason(event.target.value)}
            />
          </label>
          <Button
            disabled={!transferTargetId || !transferReason || transfer.isPending}
            onClick={() => transfer.mutate()}
          >
            Potvrdi prijenos
          </Button>
        </DialogContent>
      </Dialog>
    </section>
  );
}

function exportUsers(users: readonly User[]) {
  const lines = [
    ["Korisničko ime", "Prikazno ime", "E-mail", "Role", "Status"],
    ...users.map((user) => {
      const roles = pick(user, "roles", "Roles");
      return [
        pick(user, "username", "Username"),
        pick(user, "displayName", "DisplayName"),
        pick(user, "email", "Email"),
        Array.isArray(roles) ? roles.join("; ") : roles,
        pick(user, "isActive", "IsActive", "enabled", "Enabled") !== false
          ? "Aktivan"
          : "Suspendovan",
      ];
    }),
  ];
  downloadCsv("korisnici.csv", lines);
}

function downloadCsv(name: string, rows: readonly (readonly unknown[])[]) {
  const csv = rows
    .map((row) => row.map((value) => `"${String(value ?? "").replaceAll('"', '""')}"`).join(","))
    .join("\r\n");
  const url = URL.createObjectURL(new Blob(["\uFEFF", csv], { type: "text/csv;charset=utf-8" }));
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = name;
  anchor.click();
  URL.revokeObjectURL(url);
}
