import { invoiceRepository } from "./invoices.repository";

            export const invoiceService = {
              listInvoices() {
                return invoiceRepository.list();
              },
              createInvoice(input: { name: string; status: "draft" | "active" | "archived"; lineCount: number }) {
                return invoiceRepository.create(input);
              }
            };
