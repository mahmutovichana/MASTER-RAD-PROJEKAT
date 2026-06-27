export type Invoice = { id: string; name: string; status: "draft" | "active" | "archived"; lineCount: number; };
            const invoices: Invoice[] = [{ id: "invoice_1", name: "January Invoice", status: "active", lineCount: 1 }];
            export const invoiceRepository = {
              list() { return invoices; },
              create(input: Omit<Invoice, "id">) {
                const saved = { id: `invoice_${invoices.length + 1}`, ...input };
                invoices.push(saved);
                return saved;
              }
            };
