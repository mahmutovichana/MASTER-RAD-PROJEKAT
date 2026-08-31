import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Check, Send } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { apiClient } from "@/lib/api/http-client";

import { getOrderCollection, type OrderRecord } from "./orders-api";

const pick = (row: OrderRecord, ...keys: string[]) =>
  keys.map((key) => row[key]).find((value) => value != null);

export function OrderQuotesPanel({ orderId }: { readonly orderId: number }) {
  const cache = useQueryClient();
  const [respondingId, setRespondingId] = useState<number>();
  const [offeredPrice, setOfferedPrice] = useState("");
  const [offeredDays, setOfferedDays] = useState("");
  const query = useQuery({
    queryKey: ["orders", orderId, "quotes"],
    queryFn: () => getOrderCollection(orderId, "quote-requests"),
  });
  const refresh = () => cache.invalidateQueries({ queryKey: ["orders", orderId, "quotes"] });
  const respond = useMutation({
    mutationFn: (quoteId: number) =>
      apiClient.postLegacy(`/api/orders/${orderId}/quote-requests/${quoteId}/respond`, {
        body: { offeredPrice: Number(offeredPrice), offeredDays: Number(offeredDays) },
      }),
    onSuccess: async () => {
      setRespondingId(undefined);
      setOfferedPrice("");
      setOfferedDays("");
      await refresh();
    },
  });
  const accept = useMutation({
    mutationFn: (quoteId: number) =>
      apiClient.postLegacy(`/api/orders/${orderId}/quote-requests/${quoteId}/accept`),
    onSuccess: refresh,
  });

  return (
    <div className="rounded-sm border border-border-subtle bg-surface-default p-5">
      <h2 className="font-bold">Ponude vještaka</h2>
      <div className="mt-4 divide-y divide-border-subtle">
        {query.data?.map((quote, index) => {
          const id = Number(pick(quote, "id", "Id"));
          const status = String(pick(quote, "status", "Status") ?? "—");
          return (
            <div className="py-3" key={id || index}>
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div>
                  <p className="font-semibold">
                    {String(pick(quote, "appraiserName", "AppraiserName") ?? `Ponuda #${id}`)}
                  </p>
                  <p className="text-xs text-text-secondary">
                    {status} · {String(pick(quote, "offeredPrice", "OfferedPrice") ?? "—")} KM ·{" "}
                    {String(pick(quote, "offeredDays", "OfferedDays") ?? "—")} dana
                  </p>
                </div>
                <div className="flex gap-1">
                  <Button size="sm" variant="secondary" onClick={() => setRespondingId(id)}>
                    <Send className="size-4" />
                    Odgovori
                  </Button>
                  <Button
                    size="sm"
                    disabled={status.toLowerCase() !== "responded" || accept.isPending}
                    onClick={() => accept.mutate(id)}
                  >
                    <Check className="size-4" />
                    Prihvati
                  </Button>
                </div>
              </div>
              {respondingId === id && (
                <form
                  className="mt-3 grid gap-2 sm:grid-cols-[1fr_1fr_auto]"
                  onSubmit={(event) => {
                    event.preventDefault();
                    respond.mutate(id);
                  }}
                >
                  <Input
                    required
                    min="0"
                    step="0.01"
                    type="number"
                    placeholder="Cijena (KM)"
                    value={offeredPrice}
                    onChange={(event) => setOfferedPrice(event.target.value)}
                  />
                  <Input
                    required
                    min="1"
                    type="number"
                    placeholder="Broj dana"
                    value={offeredDays}
                    onChange={(event) => setOfferedDays(event.target.value)}
                  />
                  <Button type="submit" disabled={respond.isPending}>
                    Pošalji
                  </Button>
                </form>
              )}
            </div>
          );
        })}
        {!query.isLoading && !query.data?.length && (
          <p className="py-4 text-sm text-text-secondary">Nema zahtjeva za ponudu.</p>
        )}
      </div>
    </div>
  );
}
