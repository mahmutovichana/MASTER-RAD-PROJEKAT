import { getAccessToken } from "../auth/keycloak";
import { getActiveRole } from "../auth/active-role";
import { runtimeConfig } from "../../runtime-config";

/** One wire format for every successful and failed application API response. */
export interface ApiEnvelope<T> {
  readonly success: boolean;
  readonly data: T | null;
  readonly error: ApiFailure | null;
  readonly traceId: string;
}

export interface ApiFailure {
  readonly code: string;
  readonly message: string;
  readonly details?: Readonly<Record<string, readonly string[]>> | null;
}

export class ApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly traceId: string;
  readonly details?: ApiFailure["details"];

  constructor(status: number, failure: ApiFailure, traceId: string) {
    super(failure.message);
    this.name = "ApiError";
    this.status = status;
    this.code = failure.code;
    this.traceId = traceId;
    this.details = failure.details;
  }
}

export const apiBaseUrl: string = runtimeConfig.API_BASE_URL?.replace(/\/$/, "") ?? "";

const REQUEST_TIMEOUT_MS = 15_000;
export type QueryValue = string | number | boolean | undefined | null;

export interface ApiRequestOptions {
  readonly query?: Readonly<Record<string, QueryValue>> | undefined;
  readonly signal?: AbortSignal | undefined;
  readonly timeoutMs?: number | undefined;
  readonly headers?: Readonly<Record<string, string>> | undefined;
}

export interface ApiBodyRequestOptions extends ApiRequestOptions {
  readonly body?: unknown | undefined;
}

export function buildUrl(path: string, query?: ApiRequestOptions["query"]): string {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(query ?? {})) {
    if (value === undefined || value === null || value === "") continue;
    params.set(key, String(value));
  }
  const search = params.toString();
  return `${apiBaseUrl}${path}${search ? `?${search}` : ""}`;
}

export interface ApiClient {
  get<T>(path: string, options?: ApiRequestOptions): Promise<T>;
  /** Temporary bridge for controllers not yet migrated to ApiEnvelope<T>. */
  getLegacy<T>(path: string, options?: ApiRequestOptions): Promise<T>;
  postLegacy<T>(path: string, options?: ApiBodyRequestOptions): Promise<T>;
  putLegacy<T>(path: string, options?: ApiBodyRequestOptions): Promise<T>;
  deleteLegacy<T>(path: string, options?: ApiBodyRequestOptions): Promise<T>;
  post<T>(path: string, options?: ApiBodyRequestOptions): Promise<T>;
  put<T>(path: string, options?: ApiBodyRequestOptions): Promise<T>;
  patch<T>(path: string, options?: ApiBodyRequestOptions): Promise<T>;
  delete<T>(path: string, options?: ApiBodyRequestOptions): Promise<T>;
}

function isEnvelope<T>(body: unknown): body is ApiEnvelope<T> {
  if (!body || typeof body !== "object") return false;
  const value = body as Partial<ApiEnvelope<T>>;
  return typeof value.success === "boolean" && typeof value.traceId === "string";
}

export function createApiClient(): ApiClient {
  async function request<T>(
    method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE",
    path: string,
    options: ApiBodyRequestOptions = {},
    envelopeRequired = true,
  ): Promise<T> {
    const controller = new AbortController();
    const abort = () => controller.abort(options.signal?.reason);
    const timeout = setTimeout(
      () => controller.abort(new Error("Request timed out")),
      options.timeoutMs ?? REQUEST_TIMEOUT_MS,
    );
    options.signal?.addEventListener("abort", abort, { once: true });

    const isFormData = options.body instanceof FormData;
    const headers: Record<string, string> = { accept: "application/json", ...options.headers };
    const accessToken = await getAccessToken();
    if (accessToken) headers["authorization"] = `Bearer ${accessToken}`;
    const activeRole = getActiveRole();
    if (activeRole) headers["X-Active-Role"] = activeRole;
    if (options.body !== undefined && !isFormData) headers["content-type"] = "application/json";
    // Keycloak access tokens are attached explicitly and are not ambient browser
    // credentials, so these API calls are not vulnerable to cookie-based CSRF.

    try {
      const requestBody =
        options.body === undefined
          ? undefined
          : isFormData
            ? options.body
            : JSON.stringify(options.body);
      const init: RequestInit = {
        method,
        credentials: "include",
        headers,
        signal: controller.signal,
      };
      if (requestBody !== undefined) init.body = requestBody;
      const response = await fetch(buildUrl(path, options.query), init);

      const body: unknown =
        response.status === 204 ? null : await response.json().catch(() => null);
      if (!envelopeRequired) {
        if (!response.ok) {
          throw new ApiError(
            response.status,
            { code: "legacy_request_failed", message: "The legacy service request failed." },
            response.headers.get("x-correlation-id") ?? "unknown",
          );
        }
        return body as T;
      }
      if (!isEnvelope<T>(body)) {
        throw new ApiError(
          response.status,
          { code: "invalid_response", message: "The server returned an invalid response." },
          response.headers.get("x-correlation-id") ?? "unknown",
        );
      }
      if (!response.ok || !body.success || body.data === null) {
        throw new ApiError(
          response.status,
          body.error ?? { code: "request_failed", message: "The request could not be completed." },
          body.traceId,
        );
      }
      return body.data;
    } finally {
      clearTimeout(timeout);
      options.signal?.removeEventListener("abort", abort);
    }
  }

  return {
    get: (path, options) => request("GET", path, options),
    getLegacy: (path, options) => request("GET", path, options, false),
    postLegacy: (path, options) => request("POST", path, options, false),
    putLegacy: (path, options) => request("PUT", path, options, false),
    deleteLegacy: (path, options) => request("DELETE", path, options, false),
    post: (path, options) => request("POST", path, options),
    put: (path, options) => request("PUT", path, options),
    patch: (path, options) => request("PATCH", path, options),
    delete: (path, options) => request("DELETE", path, options),
  };
}

export const apiClient: ApiClient = createApiClient();
