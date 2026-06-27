import { Router } from "express";
            import { createInvoice, listInvoices } from "./invoices.controller";
            export const invoiceRouter = Router();
            invoiceRouter.get("/", listInvoices);
            invoiceRouter.post("/", createInvoice);
