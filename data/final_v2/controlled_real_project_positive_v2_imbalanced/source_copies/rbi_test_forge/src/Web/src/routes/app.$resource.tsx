import { createFileRoute, notFound } from "@tanstack/react-router";

import { ResourcePage } from "@/components/registry/resource-page";
import { resourcesBySlug } from "@/lib/registry/resources";

export const Route = createFileRoute("/app/$resource")({
  component: ResourceRoute,
});

function ResourceRoute() {
  const { resource: slug } = Route.useParams();
  const resource = resourcesBySlug.get(slug);
  if (!resource) throw notFound();
  return <ResourcePage resource={resource} />;
}
