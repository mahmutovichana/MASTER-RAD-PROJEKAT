import { useQuery } from "@tanstack/react-query";
import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowRight, Bell, ClipboardCheck, ClipboardList, UserRoundSearch } from "lucide-react";
import { Heading, Text } from "@/components/ui/typography";
import { apiClient } from "@/lib/api/http-client";
import { profileList, useProfile } from "@/lib/auth/use-profile";
export const Route = createFileRoute("/app/")({ component: Dashboard });
type Obj = Readonly<Record<string, unknown>>;
const data = (raw: unknown) => ((raw as Obj)?.["data"] ?? raw) as Obj;
const count = (v: unknown) =>
  Array.isArray(v)
    ? v.length
    : Number(
        (v as Obj)?.["totalCount"] ??
          (v as Obj)?.["TotalCount"] ??
          (v as Obj)?.["total"] ??
          (v as Obj)?.["Total"] ??
          (v as Obj)?.["count"] ??
          0,
      );
function Dashboard() {
  const profile = useProfile();
  const summary = useQuery({
    queryKey: ["dashboard", "orders"],
    queryFn: async () => data(await apiClient.getLegacy("/api/orders/summary")),
  });
  const tasks = useQuery({
    queryKey: ["dashboard", "tasks"],
    queryFn: async () =>
      data(await apiClient.getLegacy("/api/tasks/my", { query: { pageSize: 100 } })),
  });
  const unread = useQuery({
    queryKey: ["dashboard", "notifications"],
    queryFn: async () => data(await apiClient.getLegacy("/api/notifications/unread-count")),
  });
  const cards = [
    {
      label: "Ukupno narudžbi",
      value: count(summary.data),
      icon: ClipboardList,
      to: "/app/orders",
    },
    {
      label: "Moji otvoreni zadaci",
      value: count(tasks.data),
      icon: ClipboardCheck,
      to: "/app/tasks",
    },
    {
      label: "Nepročitane obavijesti",
      value: count(unread.data),
      icon: Bell,
      to: "/app/notifications",
    },
    {
      label: "Aktivne role",
      value: profileList(profile.data, "roles").length,
      icon: UserRoundSearch,
      to: "/app/users",
    },
  ] as const;
  return (
    <section>
      <div className="rounded-sm bg-surface-inverse p-7 text-text-inverse sm:p-10">
        <p className="text-eyebrow text-text-inverse-muted">Digitalizacija procjene nekretnine</p>
        <Heading level={1} size={5} className="mt-2 text-text-inverse">
          Dobro došli,{" "}
          {String(profile.data?.["displayName"] ?? profile.data?.["DisplayName"] ?? "korisniče")}
        </Heading>
        <Text className="mt-3 max-w-prose text-text-inverse-muted">
          Radni prostor je prilagođen vašim rolama i permissionima. Izaberite karticu za nastavak
          rada.
        </Text>
      </div>
      <div className="mt-7 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {cards.map((c) => (
          <Link
            key={c.label}
            to={c.to}
            className="rounded-sm border border-border-subtle bg-surface-default p-5 hover:border-border-brand"
          >
            <c.icon className="size-5" />
            <p className="mt-5 text-3xl font-bold">{c.value}</p>
            <p className="mt-1 text-sm text-text-secondary">{c.label}</p>
            <span className="mt-4 inline-flex items-center gap-2 text-sm font-semibold">
              Otvori <ArrowRight className="size-4" />
            </span>
          </Link>
        ))}
      </div>
      <div className="mt-7 rounded-sm border border-border-subtle bg-surface-default p-6">
        <h2 className="font-bold">Vaš pristup</h2>
        <p className="mt-2 text-sm text-text-secondary">
          Role: {profileList(profile.data, "roles").join(", ") || "Nije dodijeljena"}
        </p>
        <p className="mt-1 text-sm text-text-secondary">
          Dostupni moduli:{" "}
          {profileList(profile.data, "availableModules").join(", ") || "Osnovni pristup"}
        </p>
      </div>
    </section>
  );
}
