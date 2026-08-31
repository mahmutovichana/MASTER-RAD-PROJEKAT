import { useQuery } from "@tanstack/react-query";
import { CheckCircle2, RefreshCw, XCircle } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Heading, Text } from "@/components/ui/typography";
import { apiBaseUrl } from "@/lib/api/http-client";

const checks = [
  { key: "api", label: "API", path: "/api/health" },
  { key: "db", label: "SQL Server", path: "/api/health/db" },
  { key: "storage", label: "Skladište dokumenata", path: "/api/health/storage" },
  { key: "auth", label: "Keycloak", path: "/api/health/auth" },
] as const;

async function checkHealth() {
  return Promise.all(
    checks.map(async (check) => {
      try {
        const response = await fetch(`${apiBaseUrl}${check.path}`);
        return { ...check, ok: response.ok, status: response.status };
      } catch {
        return { ...check, ok: false, status: 0 };
      }
    }),
  );
}

export function HealthPage() {
  const query = useQuery({
    queryKey: ["health"],
    queryFn: checkHealth,
    refetchInterval: 30_000,
  });
  return (
    <section>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-eyebrow text-text-tertiary">Administracija</p>
          <Heading level={1} size={4} className="mt-2">
            Zdravlje sistema
          </Heading>
          <Text tone="secondary" className="mt-2">
            Lokalna provjera API-ja i njegovih ključnih zavisnosti.
          </Text>
        </div>
        <Button variant="secondary" onClick={() => query.refetch()}>
          <RefreshCw className="size-4" />
          Provjeri
        </Button>
      </div>
      <div className="mt-7 grid gap-4 sm:grid-cols-2">
        {query.data?.map((check) => (
          <article
            className="flex items-center gap-4 rounded-sm border border-border-subtle bg-surface-default p-6"
            key={check.key}
          >
            {check.ok ? (
              <CheckCircle2 className="size-7 text-feedback-success" />
            ) : (
              <XCircle className="size-7 text-feedback-danger" />
            )}
            <div>
              <h2 className="font-bold">{check.label}</h2>
              <p className="text-sm text-text-secondary">
                {check.ok ? "Dostupno" : `Nedostupno (${check.status || "network"})`}
              </p>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
