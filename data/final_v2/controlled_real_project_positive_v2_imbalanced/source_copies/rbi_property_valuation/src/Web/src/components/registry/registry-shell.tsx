import { Link, Outlet, useRouterState } from "@tanstack/react-router";
import { LogOut, Menu, X } from "lucide-react";
import { useEffect, useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";

import { RbiLogo } from "@/components/brand/rbi-logo";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/design-system/theme/theme-toggle";
import { LanguageSwitcher } from "@/localization";
import { useBusinessText } from "@/localization/use-business-text";
import { registryResources } from "@/lib/registry/resources";
import { isAuthenticationConfigured, keycloak } from "@/lib/auth/keycloak";
import { profileList, useProfile } from "@/lib/auth/use-profile";
import { apiClient } from "@/lib/api/http-client";
import { clearActiveRole, getActiveRole, setActiveRole } from "@/lib/auth/active-role";

export function RegistryShell() {
  const { t } = useTranslation("registry");
  const bt = useBusinessText();
  const pathname = useRouterState({ select: (state) => state.location.pathname });
  const [open, setOpen] = useState(false);
  const cache = useQueryClient();
  const profile = useProfile();
  const roles = profileList(profile.data, "roles");
  const activeRole = getActiveRole() ?? roles[0] ?? "";
  useEffect(() => {
    if (!getActiveRole() && roles.length === 1 && roles[0]) setActiveRole(roles[0]);
  }, [roles]);
  const changeRole = useMutation({
    mutationFn: (role: string) =>
      apiClient.postLegacy("/api/me/active-role", { body: { roleCode: role } }),
    onSuccess: async (_result, role) => {
      setActiveRole(role);
      await cache.invalidateQueries();
      location.assign("/app");
    },
  });
  const modules = profileList(profile.data, "availableModules");
  const visibleResources = registryResources.filter((item) => isVisible(item.key, modules));

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
            {roles.length > 1 && (
              <label className="hidden items-center gap-2 text-xs font-semibold md:flex">
                {bt("Aktivna uloga", "Active role")}
                <select
                  className="h-9 max-w-52 rounded-sm border border-border-subtle bg-surface-default px-2"
                  value={activeRole}
                  disabled={changeRole.isPending}
                  onChange={(event) => changeRole.mutate(event.target.value)}
                >
                  {roles.map((role) => (
                    <option key={role}>{role}</option>
                  ))}
                </select>
              </label>
            )}
            <span className="hidden text-right text-xs text-text-secondary md:block">
              <b className="block text-text-primary">
                {String(profile.data?.["displayName"] ?? profile.data?.["DisplayName"] ?? "")}
              </b>
              {activeRole || roles.join(", ")}
            </span>
            <ThemeToggle />
            <LanguageSwitcher className="hidden sm:flex" />
            {isAuthenticationConfigured ? <Button
              variant="ghost"
              size="icon"
              title={t("shell.logout", { defaultValue: "Odjava" })}
              onClick={() => {
                clearActiveRole();
                keycloak.logout({ redirectUri: location.origin });
              }}
            >
              <LogOut className="size-4" />
            </Button> : null}
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
          {(["work", "operations", "administration"] as const).map((area) => (
            <div key={area} className="mb-6">
              <p className="px-3 text-eyebrow text-text-tertiary">{t(`areas.${area}`)}</p>
              <nav className="mt-2 space-y-1" aria-label={t(`areas.${area}`)}>
                {visibleResources
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

const moduleByResource: Readonly<Record<string, string>> = {
  orders: "orders",
  tasks: "tasks",
  notifications: "notifications",
  codeLists: "codebooks",
  audit: "audit",
  health: "health",
  users: "access-management",
  roles: "access-management",
  appraisers: "orders",
  protocol: "orders",
  reports: "orders",
  documents: "orders",
  branches: "orders",
};
function isVisible(key: string, modules: readonly string[]) {
  if (key === "dashboard" || modules.length === 0) return true;
  const required = moduleByResource[key];
  return !required || modules.includes(required);
}
