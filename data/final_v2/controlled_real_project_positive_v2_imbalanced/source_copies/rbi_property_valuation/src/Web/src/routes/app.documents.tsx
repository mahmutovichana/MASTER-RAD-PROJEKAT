import { createFileRoute } from "@tanstack/react-router";
import { SharedDocumentsPage } from "@/features/documents/shared-documents-page";
export const Route = createFileRoute("/app/documents")({ component: SharedDocumentsPage });
