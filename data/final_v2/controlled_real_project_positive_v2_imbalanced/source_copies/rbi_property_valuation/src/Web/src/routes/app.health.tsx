import { createFileRoute } from "@tanstack/react-router";
import { HealthPage } from "@/features/health/health-page";
export const Route = createFileRoute("/app/health")({ component: HealthPage });
