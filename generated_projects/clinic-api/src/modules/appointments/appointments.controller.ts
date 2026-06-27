import { Request, Response } from "express";
            import { createAppointmentSchema } from "./appointments.schema";
            import { appointmentService } from "./appointments.service";

            export function listAppointments(_req: Request, res: Response) {
              res.status(200).json({ data: appointmentService.listAppointments() });
            }

            export function createAppointment(req: Request, res: Response) {
              const input = createAppointmentSchema.parse(req.body);
              const result = appointmentService.createAppointment(input);
              res.status(201).json({ data: result });
            }
