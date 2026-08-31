import { createFileRoute } from "@tanstack/react-router";
import { AuditPage } from "@/features/common/audit-page";
export const Route = createFileRoute("/app/audit")({
  component: AuditPage,
});
