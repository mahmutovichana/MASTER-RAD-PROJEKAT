import { createFileRoute } from "@tanstack/react-router";
import { ReportsPage } from "@/features/common/reports-page";
export const Route = createFileRoute("/app/reports")({
  component: ReportsPage,
});
