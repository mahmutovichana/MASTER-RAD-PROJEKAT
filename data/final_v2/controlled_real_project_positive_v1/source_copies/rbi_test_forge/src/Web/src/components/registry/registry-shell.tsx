import { Link, Outlet, useRouterState } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { LogIn, LogOut, Menu, X } from "lucide-react";
import { useState } from "react";
import { useTranslation } from "react-i18next";

import { RbiLogo } from "@/components/brand/rbi-logo";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/design-system/theme/theme-toggle";
import { apiClient } from "@/lib/api/http-client";
import { registryResources } from "@/lib/registry/resources";
import { LanguageSwitcher } from "@/localization";

interface CurrentUser {
  readonly fullName: string;
  readonly roles: readonly string[];
  readonly isAuthenticated: boolean;
}

export function RegistryShell() {
  const { t } = useTranslation("registry");
  const pathname = useRouterState({ select: (state) => state.location.pathname });
  const [open, setOpen] = useState(false);
  const profile = useQuery({
    queryKey: ["current-user"],
    queryFn: () => apiClient.get<CurrentUser>("/api/frontend/profile"),
    retry: false,
  });

  return (
    <div className="min-h-screen bg-surface text-text-primary">
      <header className="glass-strong sticky top-0 z-40 border-b border-border-subtle">
        <div className="flex h-16 w-full items-center gap-4 px-4 lg:px-6">
          <Link
            to="/app"
            className="flex min-w-0 items-center gap-3"
            aria-label={t("shell.homeLabel")}
          >
            <RbiLogo variant="bankMono" className="h-9 w-auto dark:hidden" />
            <RbiLogo variant="bankYellowInverse" className="hidden h-9 w-auto dark:block" />
            <span className="hidden truncate border-l border-border-subtle pl-3 text-sm font-bold sm:block">
              {t("shell.product")}
            </span>
          </Link>
          <div className="ml-auto flex items-center gap-2">
            <LanguageSwitcher />
            <ThemeToggle />
            {profile.data?.isAuthenticated ? (
              <a href="/authentication/logout" className="hidden min-h-9 items-center gap-2 rounded-sm px-3 text-sm font-semibold text-text-secondary hover:bg-surface-muted hover:text-text-primary md:flex" title={profile.data.roles.join(", ")}>
                <span className="max-w-40 truncate">{profile.data.fullName}</span><LogOut className="size-4" />
              </a>
            ) : profile.isError ? (
              <a href="/authentication/login?returnUrl=/app" className="hidden min-h-9 items-center gap-2 rounded-sm px-3 text-sm font-semibold text-text-secondary hover:bg-surface-muted hover:text-text-primary md:flex">
                <LogIn className="size-4" />{t("shell.login")}
              </a>
            ) : null}
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={() => setOpen((value) => !value)}
              aria-label={t("shell.menu")}
            >
              {open ? <X /> : <Menu />}
            </Button>
          </div>
        </div>
      </header>

      <div className="grid w-full lg:grid-cols-[17rem_minmax(0,1fr)]">
        <aside
          className={`${open ? "block" : "hidden"} border-r border-border-subtle bg-surface-subtle p-4 lg:block lg:min-h-[calc(100vh-4rem)]`}
        >
          {(["testing", "administration"] as const).map((area) => (
            <div key={area} className="mb-6">
              <p className="px-3 text-eyebrow text-text-tertiary">{t(`areas.${area}`)}</p>
              <nav className="mt-2 space-y-1" aria-label={t(`areas.${area}`)}>
                {registryResources
                  .filter((item) => item.area === area)
                  .map((item) => {
                    const active =
                      item.path === "/app"
                        ? pathname === item.path
                        : pathname.startsWith(item.path);
                    return (
                      <Link
                        key={item.key}
                        to={item.path}
                        onClick={() => setOpen(false)}
                        className={`flex min-h-11 items-center gap-3 rounded-sm px-3 py-2 text-sm font-medium transition-colors ${active ? "bg-surface-brand text-text-on-brand" : "text-text-secondary hover:bg-surface-muted hover:text-text-primary"}`}
                      >
                        <item.icon className="size-4 shrink-0" aria-hidden="true" />
                        {t(`resources.${item.key}.title` as never)}
                      </Link>
                    );
                  })}
              </nav>
            </div>
          ))}
        </aside>
        <main id="main-content" className="min-w-0 px-4 py-8 lg:px-10 lg:py-10">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
