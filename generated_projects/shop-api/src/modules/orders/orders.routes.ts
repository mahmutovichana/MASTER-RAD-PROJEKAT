import { Router } from "express";
            import { createOrder, listOrders } from "./orders.controller";

            export const orderRouter = Router();

            orderRouter.get("/", listOrders);
            orderRouter.post("/", createOrder);
