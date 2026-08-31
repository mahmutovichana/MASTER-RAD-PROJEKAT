import {
  BookOpen,
  Boxes,
  CalendarClock,
  FileClock,
  FileCode2,
  Gauge,
  History,
  Import,
  KeyRound,
  ShieldCheck,
  TestTube2,
  UserRound,
  Users,
  type LucideIcon,
} from "lucide-react";

export interface RegistryResource {
  readonly key: string;
  readonly path: string;
  readonly endpoint?: string;
  readonly icon: LucideIcon;
  readonly area: "testing" | "administration";
}

export const registryResources: readonly RegistryResource[] = [
  { key: "dashboard", path: "/app", icon: Gauge, area: "testing" },
  { key: "profile", path: "/app/profile", endpoint: "/api/frontend/profile", icon: UserRound, area: "testing" },
  { key: "scenarios", path: "/app/scenarios", endpoint: "/api/frontend/scenarios", icon: TestTube2, area: "testing" },
  { key: "groups", path: "/app/groups", endpoint: "/api/frontend/groups", icon: Boxes, area: "testing" },
  { key: "generator", path: "/app/generator", icon: FileCode2, area: "testing" },
  { key: "apiImport", path: "/app/api-import", icon: Import, area: "testing" },
  { key: "schedules", path: "/app/schedules", endpoint: "/api/frontend/schedules", icon: CalendarClock, area: "testing" },
  { key: "history", path: "/app/history", endpoint: "/api/frontend/history", icon: History, area: "testing" },
  { key: "users", path: "/app/users", endpoint: "/api/frontend/users", icon: Users, area: "administration" },
  { key: "roles", path: "/app/roles", endpoint: "/api/frontend/users/roles", icon: ShieldCheck, area: "administration" },
  { key: "apiKeys", path: "/app/api-keys", endpoint: "/api/frontend/api-keys", icon: KeyRound, area: "administration" },
  { key: "codeLists", path: "/app/code-lists", endpoint: "/api/frontend/code-lists", icon: BookOpen, area: "administration" },
  { key: "audit", path: "/app/audit", endpoint: "/api/frontend/audit", icon: FileClock, area: "administration" },
];

export const resourcesBySlug = new Map(
  registryResources
    .filter((resource) => resource.path !== "/app")
    .map((resource) => [resource.path.split("/").at(-1)!, resource]),
);
