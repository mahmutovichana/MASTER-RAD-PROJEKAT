import { Router } from "express";
            import { createPayment, listPayments } from "./payments.controller";
            export const paymentRouter = Router();
            paymentRouter.get("/", listPayments);
            paymentRouter.post("/", createPayment);
