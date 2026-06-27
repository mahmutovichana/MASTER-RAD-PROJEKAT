import { Request, Response } from "express";
            import { createReservationSchema } from "./reservations.schema";
            import { reservationService } from "./reservations.service";
            export function listReservations(_req: Request, res: Response) { res.status(200).json({ data: reservationService.listReservations() }); }
            export function createReservation(req: Request, res: Response) {
              const input = createReservationSchema.parse(req.body);
              const result = reservationService.createReservation(input);
              res.status(201).json({ data: result });
            }
