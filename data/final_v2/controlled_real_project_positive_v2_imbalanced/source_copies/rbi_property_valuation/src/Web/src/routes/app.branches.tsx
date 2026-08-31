import { createFileRoute } from "@tanstack/react-router";
import { RecordsPage } from "@/features/common/records-page";
export const Route = createFileRoute("/app/branches")({
  component: () => (
    <RecordsPage
      title="Poslovnice"
      description="Referentni pregled poslovnica i pripadajućih gradova."
      endpoint="/api/branches/"
      area="Administracija"
    />
  ),
});
