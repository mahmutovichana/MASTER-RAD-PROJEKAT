import {
  BookOpen,
  Bell,
  BriefcaseBusiness,
  ClipboardCheck,
  ClipboardList,
  FileClock,
  FileText,
  Gauge,
  HeartPulse,
  Landmark,
  ShieldCheck,
  UserRoundSearch,
  Users,
  type LucideIcon,
} from "lucide-react";

export interface RegistryResource {
  readonly key: string;
  readonly path: string;
  readonly endpoint?: string;
  readonly icon: LucideIcon;
  readonly area: "work" | "operations" | "administration";
}

export const registryResources: readonly RegistryResource[] = [
  { key: "dashboard", path: "/app", icon: Gauge, area: "work" },
  {
    key: "orders",
    path: "/app/orders",
    endpoint: "/api/orders",
    icon: ClipboardList,
    area: "work",
  },
  {
    key: "tasks",
    path: "/app/tasks",
    endpoint: "/api/tasks/my",
    icon: ClipboardCheck,
    area: "work",
  },
  {
    key: "protocol",
    path: "/app/protocol",
    endpoint: "/api/protocol/orders",
    icon: FileText,
    area: "operations",
  },
  {
    key: "notifications",
    path: "/app/notifications",
    endpoint: "/api/notifications/mine",
    icon: Bell,
    area: "operations",
  },
  {
    key: "appraisers",
    path: "/app/appraisers",
    endpoint: "/api/appraisers",
    icon: UserRoundSearch,
    area: "operations",
  },
  {
    key: "reports",
    path: "/app/reports",
    endpoint: "/api/reports/orders",
    icon: BriefcaseBusiness,
    area: "operations",
  },
  {
    key: "documents",
    path: "/app/documents",
    endpoint: "/api/shared-documents",
    icon: FileText,
    area: "operations",
  },
  { key: "users", path: "/app/users", endpoint: "/api/users", icon: Users, area: "administration" },
  {
    key: "roles",
    path: "/app/roles",
    endpoint: "/api/admin/roles",
    icon: ShieldCheck,
    area: "administration",
  },
  {
    key: "codeLists",
    path: "/app/code-lists",
    endpoint: "/api/admin/codebooks",
    icon: BookOpen,
    area: "administration",
  },
  {
    key: "audit",
    path: "/app/audit",
    endpoint: "/api/audit",
    icon: FileClock,
    area: "administration",
  },
  {
    key: "branches",
    path: "/app/branches",
    endpoint: "/api/branches",
    icon: Landmark,
    area: "administration",
  },
  { key: "health", path: "/app/health", icon: HeartPulse, area: "administration" },
];

export const resourcesBySlug = new Map(
  registryResources
    .filter((resource) => resource.path !== "/app")
    .map((resource) => [resource.path.split("/").at(-1)!, resource]),
);
