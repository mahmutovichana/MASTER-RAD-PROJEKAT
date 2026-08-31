import { apiClient } from "@/lib/api/http-client";
/** Neutral reference client using the generated OpenAPI contract directly. */
export type ExampleResponse = Readonly<Record<string, unknown>>;

export function fetchExample(signal?: AbortSignal) {
  return apiClient.get<ExampleResponse>("/api/example", { signal });
}
