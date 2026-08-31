import { createFileRoute } from "@tanstack/react-router";
import { AppraisersPage } from "@/features/appraisers/appraisers-page";
export const Route = createFileRoute("/app/appraisers")({ component: AppraisersPage });
