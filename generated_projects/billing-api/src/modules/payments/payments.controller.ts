import { Request, Response } from "express";
            import { createPaymentSchema } from "./payments.schema";
            import { paymentService } from "./payments.service";

            export function listPayments(_req: Request, res: Response) {
              res.status(200).json({ data: paymentService.listPayments() });
            }

            export function createPayment(req: Request, res: Response) {
              const input = createPaymentSchema.parse(req.body);
              const result = paymentService.createPayment(input);
              res.status(201).json({ data: result });
            }
