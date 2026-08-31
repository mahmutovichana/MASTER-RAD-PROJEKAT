import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { CheckCircle2, Clock3, RefreshCw } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Heading, Text } from "@/components/ui/typography";
import { apiClient } from "@/lib/api/http-client";
import { useBusinessText } from "@/localization/use-business-text";

type Task = Readonly<Record<string, unknown>>;
const pick = (row: Task, ...keys: string[]) => keys.map((k) => row[k]).find((v) => v != null);
async function loadTasks(): Promise<readonly Task[]> {
  const raw = await apiClient.getLegacy<unknown>("/api/tasks/my", { query: { pageSize: 100 } });
  const root = (raw as Record<string, unknown>)?.["data"] ?? raw;
  const items = Array.isArray(root)
    ? root
    : ((root as Record<string, unknown>)?.["items"] ??
      (root as Record<string, unknown>)?.["Items"]);
  return Array.isArray(items) ? (items as Task[]) : [];
}

export function TasksPage() {
  const bt = useBusinessText();
  const cache = useQueryClient();
  const query = useQuery({ queryKey: ["tasks"], queryFn: loadTasks });
  const accept = useMutation({
    mutationFn: (id: number) => apiClient.postLegacy(`/api/tasks/${id}/accept`),
    onSuccess: async () => {
      toast.success(bt("Zadatak je prihvaćen.", "Task accepted."));
      await cache.invalidateQueries({ queryKey: ["tasks"] });
    },
    onError: (error) => toast.error(error.message),
  });
  return (
    <section className="min-w-0">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="text-eyebrow text-text-tertiary">{bt("Radni proces", "Workflow")}</p>
          <Heading level={1} size={4} className="mt-2">
            {bt("Moji zadaci", "My tasks")}
          </Heading>
          <Text tone="secondary" className="mt-2">
            {bt(
              "Zadaci dodijeljeni vama ili vašoj aktivnoj ulozi.",
              "Tasks assigned to you or your active role.",
            )}
          </Text>
        </div>
        <Button variant="secondary" onClick={() => query.refetch()}>
          <RefreshCw className="size-4" />
          {bt("Osvježi", "Refresh")}
        </Button>
      </div>
      <div className="mt-7 grid gap-3">
        {query.isLoading && <p>{bt("Učitavanje…", "Loading…")}</p>}
        {query.isError && <p className="text-feedback-danger">{query.error.message}</p>}
        {query.data?.length === 0 && (
          <div className="rounded-sm border border-border-subtle bg-surface-default p-10 text-center">
            <CheckCircle2 className="mx-auto size-8 text-feedback-success" />
            <h2 className="mt-3 font-bold">{bt("Nema otvorenih zadataka", "No open tasks")}</h2>
          </div>
        )}
        {query.data?.map((task, index) => {
          const id = Number(pick(task, "id", "Id"));
          const orderId = Number(pick(task, "orderId", "OrderId"));
          const locked = Boolean(pick(task, "isLocked", "IsLocked"));
          return (
            <article
              className="rounded-sm border border-border-subtle bg-surface-default p-5"
              key={id || index}
            >
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div className="min-w-0">
                  <h2 className="font-bold">{String(pick(task, "title", "Title") ?? "Zadatak")}</h2>
                  <p className="mt-1 text-sm text-text-secondary">
                    {String(pick(task, "orderTitle", "OrderTitle") ?? "")}
                  </p>
                  <div className="mt-3 flex flex-wrap gap-4 text-xs text-text-tertiary">
                    <span>#{String(pick(task, "orderNumber", "OrderNumber") ?? orderId)}</span>
                    <span className="inline-flex gap-1">
                      <Clock3 className="size-3" />
                      {String(pick(task, "dueDate", "DueDate") ?? bt("Bez roka", "No due date"))}
                    </span>
                  </div>
                </div>
                <div className="flex flex-wrap gap-2">
                  <Button
                    variant="secondary"
                    onClick={() => location.assign(`/app/orders/${orderId}`)}
                  >
                    {bt("Otvori narudžbu", "Open order")}
                  </Button>
                  {!locked && (
                    <Button onClick={() => accept.mutate(id)} disabled={accept.isPending}>
                      {bt("Prihvati zadatak", "Accept task")}
                    </Button>
                  )}
                </div>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}
