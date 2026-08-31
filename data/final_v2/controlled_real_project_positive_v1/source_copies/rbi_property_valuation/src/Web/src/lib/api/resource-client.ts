import { ApiError, apiClient } from "./http-client";

export type ResourceRecord = Readonly<Record<string, unknown>>;

/**
 * One temporary boundary for the existing API's raw arrays and PagedResult<T>.
 * Feature screens never unwrap transport shapes themselves. Generated OpenAPI
 * clients can replace this generic reader feature by feature.
 */
export async function getResourceRecords(path: string): Promise<readonly ResourceRecord[]> {
  const payload = await apiClient.getLegacy<unknown>(path);
  const candidate = unwrapCollection(payload);

  if (!Array.isArray(candidate)) {
    throw new ApiError(
      502,
      { code: "unexpected_response_shape", message: "The API did not return a collection." },
      "resource-boundary",
    );
  }

  return candidate.filter(isRecord);
}

function unwrapCollection(payload: unknown): unknown {
  if (Array.isArray(payload)) return payload;
  if (!isRecord(payload)) return payload;

  for (const key of ["items", "data", "results", "value"] as const) {
    const candidate = payload[key];
    if (Array.isArray(candidate)) return candidate;
    if (isRecord(candidate)) {
      const nested = unwrapCollection(candidate);
      if (Array.isArray(nested)) return nested;
    }
  }

  return payload;
}

function isRecord(value: unknown): value is ResourceRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
