import { useEffect, useMemo, useRef, useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { updateOrder, type CreateOrderRequest, type OrderRecord } from "./orders-api";
const keys: readonly [keyof CreateOrderRequest, string][] = [
  ["clientName", "Naziv klijenta"],
  ["clientType", "Tip klijenta"],
  ["clientIdentifier", "JMBG/ID"],
  ["collateralTypeId", "Tip kolaterala ID"],
  ["combinedCollateralTypeId", "Kombinovani tip ID"],
  ["city", "Grad"],
  ["propertyAddress", "Adresa nekretnine"],
  ["branch", "Poslovnica"],
  ["branchAddress", "Adresa poslovnice"],
  ["contactName", "Kontakt osoba"],
  ["contactPhone", "Telefon"],
  ["contactEmail", "E-mail"],
  ["deliveryContactName", "Osoba za dostavu"],
  ["amRecipientName", "Account manager"],
  ["internalNote", "Interna napomena"],
];
const source = (r: OrderRecord, k: string) => r[k] ?? r[k[0]!.toUpperCase() + k.slice(1)];
function initial(r: OrderRecord): CreateOrderRequest {
  return {
    clientName: String(source(r, "clientName") ?? ""),
    clientType: String(source(r, "clientType") ?? "FL"),
    clientIdentifier: String(source(r, "clientIdentifier") ?? ""),
    collateralTypeId: Number(source(r, "collateralTypeId") ?? 1),
    combinedCollateralTypeId:
      source(r, "combinedCollateralTypeId") == null
        ? null
        : Number(source(r, "combinedCollateralTypeId")),
    city: String(source(r, "city") ?? ""),
    propertyAddress: String(source(r, "propertyAddress") ?? ""),
    branch: String(source(r, "branch") ?? ""),
    branchAddress: String(source(r, "branchAddress") ?? ""),
    contactName: String(source(r, "contactName") ?? ""),
    contactPhone: String(source(r, "contactPhone") ?? ""),
    contactEmail: String(source(r, "contactEmail") ?? ""),
    internalNote: String(source(r, "internalNote") ?? ""),
    deliveryContactName: String(source(r, "deliveryContactName") ?? ""),
    amRecipientName: String(source(r, "amRecipientName") ?? ""),
  };
}
export function OrderEditDialog({
  id,
  order,
  open,
  onOpenChange,
}: {
  readonly id: number;
  readonly order: OrderRecord;
  readonly open: boolean;
  readonly onOpenChange: (v: boolean) => void;
}) {
  const cache = useQueryClient();
  const seed = useMemo(() => initial(order), [order]);
  const [form, setForm] = useState(seed);
  const [dirty, setDirty] = useState(false);
  useEffect(() => {
    setForm(seed);
    setDirty(false);
  }, [seed]);
  const save = useMutation({
    mutationFn: () => updateOrder(id, form),
    onSuccess: async () => {
      setDirty(false);
      await cache.invalidateQueries({ queryKey: ["orders", id] });
    },
  });
  const saveRef = useRef(save.mutate);
  saveRef.current = save.mutate;
  useEffect(() => {
    if (!open || !dirty) return;
    const timer = setTimeout(() => saveRef.current(), 1500);
    return () => clearTimeout(timer);
  }, [form, dirty, open]);
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-h-[90vh] max-w-3xl overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Uredi nacrt narudžbe</DialogTitle>
          <DialogDescription>
            Promjene se automatski čuvaju nakon kratke pauze. Backend dozvoljava izmjene samo dok je
            narudžba nacrt.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 sm:grid-cols-2">
          {keys.map(([k, l]) => (
            <label className="grid gap-1 text-sm font-bold" key={k}>
              {l}
              <Input
                type={k.toLowerCase().includes("id") ? "number" : "text"}
                value={String(form[k] ?? "")}
                onChange={(e) => {
                  const numeric = k.toLowerCase().includes("id");
                  setForm({
                    ...form,
                    [k]: numeric
                      ? e.target.value
                        ? Number(e.target.value)
                        : null
                      : e.target.value,
                  });
                  setDirty(true);
                }}
              />
            </label>
          ))}
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-text-secondary">
            {save.isPending
              ? "Čuvanje…"
              : save.isSuccess && !dirty
                ? "Sve promjene su sačuvane"
                : dirty
                  ? "Nesačuvane promjene"
                  : ""}
          </span>
          <div className="flex gap-2">
            <Button variant="secondary" onClick={() => onOpenChange(false)}>
              Zatvori
            </Button>
            <Button onClick={() => save.mutate()} disabled={save.isPending || !dirty}>
              Sačuvaj sada
            </Button>
          </div>
        </div>
        {save.error && <p className="text-feedback-danger">{save.error.message}</p>}
      </DialogContent>
    </Dialog>
  );
}
