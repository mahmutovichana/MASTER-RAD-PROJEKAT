import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowRight, Layers3 } from "lucide-react";
import { useTranslation } from "react-i18next";

import { Heading, Text } from "@/components/ui/typography";
import { registryResources } from "@/lib/registry/resources";

export const Route = createFileRoute("/app/")({ component: Dashboard });

function Dashboard() {
  const { t } = useTranslation("registry");
  const resources = registryResources.filter((item) => item.key !== "dashboard");
  return (
    <section>
      <div className="rounded-sm bg-surface-inverse p-6 text-text-inverse sm:p-10">
        <Layers3 className="size-8" />
        <p className="mt-6 text-eyebrow text-text-inverse-muted">{t("dashboard.eyebrow")}</p>
        <Heading level={1} size={5} className="mt-2 text-text-inverse">
          {t("dashboard.title")}
        </Heading>
        <Text className="mt-3 max-w-prose text-text-inverse-muted">
          {t("dashboard.description")}
        </Text>
      </div>
      <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {resources.map((resource) => (
          <Link
            key={resource.key}
            to={resource.path}
            className="group rounded-sm border border-border-subtle bg-surface-default p-5 transition hover:border-border-brand hover:shadow-sm"
          >
            <resource.icon className="size-5" />
            <h2 className="mt-5 font-bold">{t(`resources.${resource.key}.title` as never)}</h2>
            <p className="mt-2 line-clamp-2 text-sm text-text-secondary">
              {t(`resources.${resource.key}.description` as never)}
            </p>
            <span className="mt-5 flex items-center gap-2 text-sm font-semibold">
              {t("actions.open")}
              <ArrowRight className="size-4 transition-transform group-hover:translate-x-1" />
            </span>
          </Link>
        ))}
      </div>
    </section>
  );
}
