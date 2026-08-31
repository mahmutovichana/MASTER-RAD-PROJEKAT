import { createFileRoute } from "@tanstack/react-router";
import { ProtocolPage } from "@/features/common/protocol-page";
export const Route = createFileRoute("/app/protocol")({
  component: ProtocolPage,
});
