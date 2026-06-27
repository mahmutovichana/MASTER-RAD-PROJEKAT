import { Router } from "express";
            import { createShipment, listShipments } from "./shipments.controller";
            export const shipmentRouter = Router();
            shipmentRouter.get("/", listShipments);
            shipmentRouter.post("/", createShipment);
