export interface ApiFailure {
  readonly code: string;
  readonly message: string;
  readonly details?: Readonly<Record<string, readonly string[]>> | null | undefined;
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

import { runtimeConfig } from "../../runtime-config";

export const apiBaseUrl: string = runtimeConfig.API_BASE_URL?.replace(/\/$/, "") ?? "";

const REQUEST_TIMEOUT_MS = 20_000;
let csrfTokenPromise: Promise<string> | undefined;
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
  getLegacy<T>(path: string, options?: ApiRequestOptions): Promise<T>;
  post<T>(path: string, options?: ApiBodyRequestOptions): Promise<T>;
  put<T>(path: string, options?: ApiBodyRequestOptions): Promise<T>;
  patch<T>(path: string, options?: ApiBodyRequestOptions): Promise<T>;
  delete<T>(path: string, options?: ApiBodyRequestOptions): Promise<T>;
}

function asRecord(value: unknown): Record<string, unknown> | undefined {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : undefined;
}

function toFailure(body: unknown, fallback: string): ApiFailure {
  const value = asRecord(body);
  const errors = asRecord(value?.["errors"]);
  const details = errors
    ? Object.fromEntries(
        Object.entries(errors).map(([key, messages]) => [
          key,
          Array.isArray(messages) ? messages.map(String) : [String(messages)],
        ]),
      )
    : undefined;
  const detail = typeof value?.["detail"] === "string" ? value["detail"] : undefined;
  const title = typeof value?.["title"] === "string" ? value["title"] : undefined;
  const message = typeof value?.["message"] === "string" ? value["message"] : detail ?? title ?? fallback;
  return { code: typeof value?.["code"] === "string" ? value["code"] : "request_failed", message, details };
}

async function getCsrfToken(): Promise<string> {
  csrfTokenPromise ??= fetch(`${apiBaseUrl}/api/security/csrf`, {
    credentials: "include",
    headers: { accept: "application/json" },
  }).then(async (response) => {
    const body: unknown = await response.json().catch(() => undefined);
    const token = asRecord(body)?.["token"];
    if (!response.ok || typeof token !== "string" || !token) {
      csrfTokenPromise = undefined;
      throw new ApiError(response.status, toFailure(body, "Sigurni token zahtjeva nije dostupan."), "unknown");
    }
    return token;
  });
  return csrfTokenPromise;
}

export function createApiClient(): ApiClient {
  async function request<T>(
    method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE",
    path: string,
    options: ApiBodyRequestOptions = {},
  ): Promise<T> {
    const controller = new AbortController();
    const abort = () => controller.abort(options.signal?.reason);
    const timeout = setTimeout(() => controller.abort(new Error("Request timed out")), options.timeoutMs ?? REQUEST_TIMEOUT_MS);
    options.signal?.addEventListener("abort", abort, { once: true });

    try {
      const isFormData = options.body instanceof FormData;
      const headers: Record<string, string> = { accept: "application/json", ...options.headers };
      if (options.body !== undefined && !isFormData) headers["content-type"] = "application/json";
      if (method !== "GET") headers["X-CSRF-TOKEN"] = await getCsrfToken();
      const init: RequestInit = { method, credentials: "include", headers, signal: controller.signal };
      if (options.body !== undefined)
        init.body = isFormData ? options.body : JSON.stringify(options.body);

      const response = await fetch(buildUrl(path, options.query), init);
      const body: unknown = response.status === 204 ? undefined : await response.json().catch(() => undefined);
      if (!response.ok) {
        const failure = toFailure(body, "Zahtjev nije moguće izvršiti.");
        const traceId = response.headers.get("x-correlation-id") ?? String(asRecord(body)?.["traceId"] ?? "unknown");
        throw new ApiError(response.status, failure, traceId);
      }
      return body as T;
    } finally {
      clearTimeout(timeout);
      options.signal?.removeEventListener("abort", abort);
    }
  }

  return {
    get: (path, options) => request("GET", path, options),
    getLegacy: (path, options) => request("GET", path, options),
    post: (path, options) => request("POST", path, options),
    put: (path, options) => request("PUT", path, options),
    patch: (path, options) => request("PATCH", path, options),
    delete: (path, options) => request("DELETE", path, options),
  };
}

export const apiClient: ApiClient = createApiClient();
