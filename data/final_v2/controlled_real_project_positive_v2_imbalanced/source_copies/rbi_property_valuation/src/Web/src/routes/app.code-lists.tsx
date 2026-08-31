import { createFileRoute } from "@tanstack/react-router";
import { CodebooksPage } from "@/features/codebooks/codebooks-page";
export const Route = createFileRoute("/app/code-lists")({ component: CodebooksPage });
