import { useQuery } from "@tanstack/react-query";
import { AlertCircle, RefreshCw } from "lucide-react";
import { useTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";
import { Heading, Text } from "@/components/ui/typography";
import { getResourceRecords } from "@/lib/api/resource-client";
import type { RegistryResource } from "@/lib/registry/resources";

export function ResourcePage({ resource }: { readonly resource: RegistryResource }) {
  const { t } = useTranslation("registry");
  const query = useQuery({
    queryKey: ["registry", resource.key],
    queryFn: () => getResourceRecords(resource.endpoint!),
    enabled: Boolean(resource.endpoint),
  });
  const records = query.data ?? [];
  const firstRecord = records[0];
  const columns = firstRecord
    ? Object.keys(firstRecord)
        .filter((key) => isReadable(firstRecord[key]))
        .slice(0, 6)
    : [];

  return (
    <section aria-labelledby={`${resource.key}-heading`}>
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-eyebrow text-text-tertiary">{t(`areas.${resource.area}`)}</p>
          <Heading level={1} size={4} id={`${resource.key}-heading`} className="mt-2">
            {t(`resources.${resource.key}.title` as never)}
          </Heading>
          <Text tone="secondary" className="mt-2 max-w-prose">
            {t(`resources.${resource.key}.description` as never)}
          </Text>
        </div>
        <Button variant="secondary" onClick={() => query.refetch()} disabled={query.isFetching}>
          <RefreshCw className={`size-4 ${query.isFetching ? "animate-spin" : ""}`} />
          {t("actions.refresh")}
        </Button>
      </div>
      <div className="mt-8 overflow-hidden rounded-sm border border-border-subtle bg-surface-default">
        {!resource.endpoint && (
          <div className="px-6 py-14 sm:px-10">
            <div className="max-w-2xl">
              <p className="text-eyebrow text-text-tertiary">{t("states.integrationEyebrow")}</p>
              <h2 className="mt-3 text-xl font-bold text-text-primary">
                {t("states.integrationTitle")}
              </h2>
              <Text tone="secondary" className="mt-3">
                {t("states.integrationBody")}
              </Text>
              <code className="mt-5 block rounded-xs bg-surface-sunken p-4 font-mono text-xs text-text-secondary">
                {t(`resources.${resource.key}.plannedEndpoint` as never)}
              </code>
            </div>
          </div>
        )}
        {query.isLoading && (
          <div className="space-y-3 p-6" aria-label={t("states.loading")}>
            {[1, 2, 3, 4].map((item) => (
              <div key={item} className="h-10 animate-pulse rounded-xs bg-surface-muted" />
            ))}
          </div>
        )}
        {query.isError && (
          <div className="flex flex-col items-center px-6 py-16 text-center">
            <AlertCircle className="size-8 text-feedback-danger" />
            <h2 className="mt-4 font-bold">{t("states.errorTitle")}</h2>
            <Text tone="secondary" className="mt-2 max-w-prose">
              {t("states.errorBody")}
            </Text>
            <Button className="mt-5" onClick={() => query.refetch()}>
              {t("actions.tryAgain")}
            </Button>
          </div>
        )}
        {query.isSuccess && records.length === 0 && (
          <div className="px-6 py-16 text-center">
            <h2 className="font-bold">{t("states.emptyTitle")}</h2>
            <Text tone="secondary" className="mt-2">
              {t("states.emptyBody")}
            </Text>
          </div>
        )}
        {query.isSuccess && records.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-surface-subtle text-text-secondary">
                <tr>
                  {columns.map((column) => (
                    <th key={column} className="whitespace-nowrap px-4 py-3 font-semibold">
                      {humanize(column)}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-border-subtle">
                {records.map((record, index) => (
                  <tr
                    key={String(record["id"] ?? record["Id"] ?? index)}
                    className="hover:bg-surface-subtle"
                  >
                    {columns.map((column) => (
                      <td key={column} className="max-w-72 truncate px-4 py-3 text-text-primary">
                        {formatValue(record[column])}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
}

function isReadable(value: unknown) {
  return value == null || ["string", "number", "boolean"].includes(typeof value);
}
function humanize(value: string) {
  return value
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replaceAll("_", " ")
    .replace(/^./, (letter) => letter.toUpperCase());
}
function formatValue(value: unknown) {
  if (value == null || value === "") return "—";
  if (typeof value === "boolean") return value ? "Da" : "Ne";
  return String(value);
}
