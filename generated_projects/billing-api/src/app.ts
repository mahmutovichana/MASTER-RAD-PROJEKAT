import express from "express";
        import { invoiceRouter } from "./modules/invoices/invoices.routes";
import { paymentRouter } from "./modules/payments/payments.routes";

        export const app = express();

        app.use(express.json());
        app.use("/invoices", invoiceRouter);
app.use("/payments", paymentRouter);

        app.get("/health", (_req, res) => {
          res.status(200).json({ status: "ok" });
        });
