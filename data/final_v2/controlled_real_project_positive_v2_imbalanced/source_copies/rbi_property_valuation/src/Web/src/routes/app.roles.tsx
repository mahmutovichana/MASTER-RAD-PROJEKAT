import { createFileRoute } from "@tanstack/react-router";
import { RolesPage } from "@/features/roles/roles-page";
export const Route = createFileRoute("/app/roles")({ component: RolesPage });
