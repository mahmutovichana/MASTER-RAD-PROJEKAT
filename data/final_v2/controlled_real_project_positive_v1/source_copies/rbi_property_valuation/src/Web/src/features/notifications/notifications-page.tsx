import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Bell, Check, RefreshCw } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Heading, Text } from "@/components/ui/typography";
import { apiClient } from "@/lib/api/http-client";
import { useBusinessText } from "@/localization/use-business-text";
import { useState } from "react";
import { toast } from "sonner";
type Notice = Readonly<Record<string, unknown>>;
const get = (r: Notice, ...k: string[]) => k.map((x) => r[x]).find((v) => v != null);
async function load(unreadOnly: boolean): Promise<readonly Notice[]> {
  const raw = await apiClient.getLegacy<unknown>("/api/notifications/mine", {
    query: { page: 1, pageSize: 100, unreadOnly },
  });
  const root = (raw as Record<string, unknown>)?.["data"] ?? raw;
  const items = Array.isArray(root)
    ? root
    : ((root as Record<string, unknown>)?.["items"] ??
      (root as Record<string, unknown>)?.["Items"]);
  return Array.isArray(items) ? (items as Notice[]) : [];
}
export function NotificationsPage() {
  const bt = useBusinessText();
  const [unreadOnly, setUnreadOnly] = useState(false);
  const cache = useQueryClient();
  const query = useQuery({
    queryKey: ["notifications", unreadOnly],
    queryFn: () => load(unreadOnly),
  });
  const read = useMutation({
    mutationFn: (id: number) => apiClient.postLegacy(`/api/notifications/${id}/read`),
    onSuccess: async () => {
      toast.success(bt("Obavještenje je označeno kao pročitano.", "Notification marked as read."));
      await cache.invalidateQueries({ queryKey: ["notifications"] });
    },
    onError: (error) => toast.error(error.message),
  });
  return (
    <section className="min-w-0">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="text-eyebrow text-text-tertiary">{bt("Operacije", "Operations")}</p>
          <Heading level={1} size={4} className="mt-2">
            {bt("Obavještenja", "Notifications")}
          </Heading>
          <Text tone="secondary" className="mt-2">
            {bt(
              "Sistemske i workflow poruke namijenjene vašem profilu.",
              "System and workflow messages for your profile.",
            )}
          </Text>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button
            variant={unreadOnly ? "primary" : "secondary"}
            onClick={() => setUnreadOnly((value) => !value)}
          >
            {bt("Samo nepročitane", "Unread only")}
          </Button>
          <Button variant="secondary" onClick={() => query.refetch()}>
            <RefreshCw className="size-4" />
            {bt("Osvježi", "Refresh")}
          </Button>
        </div>
      </div>
      <div className="mt-7 grid gap-3">
        {query.data?.map((n, i) => {
          const id = Number(get(n, "id", "Id"));
          const isRead = Boolean(get(n, "isRead", "IsRead"));
          return (
            <article
              key={id || i}
              className={`rounded-sm border p-5 ${isRead ? "border-border-subtle bg-surface-default" : "border-border-brand bg-surface-brand-subtle"}`}
            >
              <div className="flex flex-wrap items-start gap-4 sm:flex-nowrap">
                <Bell className="mt-1 size-5 shrink-0" />
                <div className="min-w-0 flex-1">
                  <h2 className="font-bold">
                    {String(get(n, "title", "Title") ?? bt("Obavještenje", "Notification"))}
                  </h2>
                  <p className="mt-2 text-sm text-text-secondary">
                    {String(get(n, "message", "Message", "body", "Body") ?? "")}
                  </p>
                  <p className="mt-3 text-xs text-text-tertiary">
                    {String(get(n, "createdAt", "CreatedAt") ?? "")}
                  </p>
                </div>
                {!isRead && (
                  <Button size="sm" variant="secondary" onClick={() => read.mutate(id)}>
                    <Check className="size-4" />
                    {bt("Označi pročitano", "Mark as read")}
                  </Button>
                )}
              </div>
            </article>
          );
        })}
        {query.data?.length === 0 && (
          <p className="rounded-sm border border-border-subtle p-10 text-center">
            {bt("Nema obavještenja.", "No notifications.")}
          </p>
        )}
        {query.isError && <p className="text-feedback-danger">{query.error.message}</p>}
      </div>
    </section>
  );
}
