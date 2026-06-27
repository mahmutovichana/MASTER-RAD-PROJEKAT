import { Request, Response } from "express";
            import { createOrderSchema } from "./orders.schema";
            import { orderService } from "./orders.service";
            export function listOrders(_req: Request, res: Response) { res.status(200).json({ data: orderService.listOrders() }); }
            export function createOrder(req: Request, res: Response) {
              const input = createOrderSchema.parse(req.body);
              const result = orderService.createOrder(input);
              res.status(201).json({ data: result });
            }
