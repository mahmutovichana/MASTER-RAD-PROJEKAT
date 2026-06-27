import { Request, Response } from "express";
            import { createInvoiceSchema } from "./invoices.schema";
            import { invoiceService } from "./invoices.service";

            export function listInvoices(_req: Request, res: Response) {
              res.status(200).json({ data: invoiceService.listInvoices() });
            }

            export function createInvoice(req: Request, res: Response) {
              const input = createInvoiceSchema.parse(req.body);
              const result = invoiceService.createInvoice(input);
              res.status(201).json({ data: result });
            }
