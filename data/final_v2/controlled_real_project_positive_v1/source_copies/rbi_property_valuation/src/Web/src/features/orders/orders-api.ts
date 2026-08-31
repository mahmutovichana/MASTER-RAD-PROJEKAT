import type { components } from "@/lib/api/generated/api";
import { apiClient } from "@/lib/api/http-client";

export type CreateOrderRequest = components["schemas"]["CreateOrderRequest"];
export type OrderRecord = Readonly<Record<string, unknown>>;

function record(value: unknown): OrderRecord | undefined {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as OrderRecord)
    : undefined;
}

function unwrap(value: unknown): unknown {
  const item = record(value);
  return item?.["data"] ?? value;
}

export async function listOrders(search = ""): Promise<readonly OrderRecord[]> {
  const response = await apiClient.getLegacy<unknown>("/api/orders", {
    query: { Search: search || undefined, PageSize: 100 },
  });
  const payload = unwrap(response);
  if (Array.isArray(payload))
    return payload.filter((item): item is OrderRecord => Boolean(record(item)));
  const body = record(payload);
  const items = body?.["items"] ?? body?.["Items"];
  return Array.isArray(items)
    ? items.filter((item): item is OrderRecord => Boolean(record(item)))
    : [];
}

export async function getOrder(id: number): Promise<OrderRecord> {
  const response = unwrap(await apiClient.getLegacy<unknown>(`/api/orders/${id}/detail`));
  const result = record(response);
  if (!result) throw new Error("API nije vratio detalje narudžbe.");
  return result;
}

export const createOrder = (body: CreateOrderRequest) =>
  apiClient.postLegacy<unknown>("/api/orders", { body });
export const updateOrder = (id: number, body: CreateOrderRequest) =>
  apiClient.putLegacy<unknown>(`/api/orders/${id}`, { body });
export const submitOrder = (id: number) =>
  apiClient.postLegacy<unknown>(`/api/orders/${id}/submit`);
export const cancelOrder = (id: number) => apiClient.deleteLegacy<unknown>(`/api/orders/${id}`);

export async function getOrderCollection(
  id: number,
  suffix: string,
): Promise<readonly OrderRecord[]> {
  const payload = unwrap(await apiClient.getLegacy<unknown>(`/api/orders/${id}/${suffix}`));
  if (Array.isArray(payload))
    return payload.filter((item): item is OrderRecord => Boolean(record(item)));
  const body = record(payload);
  const items = body?.["items"] ?? body?.["Items"] ?? body?.["documents"] ?? body?.["Documents"];
  return Array.isArray(items)
    ? items.filter((item): item is OrderRecord => Boolean(record(item)))
    : [];
}

export const runOrderAction = (id: number, suffix: string, body?: unknown) =>
  apiClient.postLegacy<unknown>(`/api/orders/${id}/${suffix}`, body === undefined ? {} : { body });

export function uploadOrderDocuments(orderId: number, documentTypeId: number, files: FileList) {
  const body = new FormData();
  Array.from(files).forEach((file) => body.append("files", file));
  return apiClient.postLegacy(`/api/orders/${orderId}/documents`, {
    query: { documentTypeId },
    body,
  });
}

export function replaceOrderDocument(documentId: number, file: File) {
  const body = new FormData();
  body.append("file", file);
  return apiClient.postLegacy(`/api/documents/${documentId}/versions`, { body });
}

export const deactivateDocument = (id: number, reason: string) =>
  apiClient.postLegacy(`/api/documents/${id}/deactivate`, { body: { reason } });
export const reactivateDocument = (id: number) =>
  apiClient.postLegacy(`/api/documents/${id}/reactivate`);
export const deleteDocument = (id: number) => apiClient.deleteLegacy(`/api/documents/${id}`);
