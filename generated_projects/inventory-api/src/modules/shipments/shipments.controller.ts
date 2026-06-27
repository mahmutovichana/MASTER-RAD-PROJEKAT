import { Request, Response } from "express";
            import { createShipmentSchema } from "./shipments.schema";
            import { shipmentService } from "./shipments.service";

            export function listShipments(_req: Request, res: Response) {
              res.status(200).json({ data: shipmentService.listShipments() });
            }

            export function createShipment(req: Request, res: Response) {
              const input = createShipmentSchema.parse(req.body);
              const result = shipmentService.createShipment(input);
              res.status(201).json({ data: result });
            }
