import { useMutation, useQueryClient } from "@tanstack/react-query";
import { FileUp } from "lucide-react";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { apiClient } from "@/lib/api/http-client";
export function OpinionUpload({
  orderId,
  permissions,
}: {
  readonly orderId: number;
  readonly permissions: readonly string[];
}) {
  const cache = useQueryClient();
  const allowedTypes = [
    permissions.includes("opinions.submit-co") && { value: "CO", label: "Kolateral oficir" },
    permissions.includes("opinions.submit-legal") && { value: "Pravna", label: "Pravna služba" },
  ].filter(Boolean) as { value: string; label: string }[];
  const [type, setType] = useState(allowedTypes[0]?.value ?? "CO");
  const [comment, setComment] = useState("");
  const upload = useMutation({
    mutationFn: (file: File) => {
      const body = new FormData();
      body.append("file", file);
      body.append("comment", comment);
      return apiClient.postLegacy(`/api/orders/${orderId}/opinions/${type}`, { body });
    },
    onSuccess: () => cache.invalidateQueries({ queryKey: ["orders", orderId, "opinions"] }),
  });
  return (
    <div className="rounded-sm border border-border-subtle bg-surface-default p-5">
      <h2 className="font-bold">Dodaj mišljenje</h2>
      <select
        className="mt-4 h-10 w-full rounded-sm border border-border-subtle bg-surface-default px-3"
        value={type}
        onChange={(e) => setType(e.target.value)}
      >
        {allowedTypes.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      <Input
        className="mt-3"
        placeholder="Komentar (opcionalno)"
        value={comment}
        onChange={(e) => setComment(e.target.value)}
      />
      <label className="mt-3 inline-flex h-10 cursor-pointer items-center gap-2 rounded-sm bg-surface-brand px-4 text-sm font-bold text-text-on-brand">
        <FileUp className="size-4" />
        Odaberi PDF
        <input
          className="sr-only"
          type="file"
          accept="application/pdf"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) upload.mutate(f);
          }}
        />
      </label>
      {upload.error && <p className="mt-2 text-sm text-feedback-danger">{upload.error.message}</p>}
    </div>
  );
}
