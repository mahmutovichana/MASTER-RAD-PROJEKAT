import { Router } from "express";
            import { createAppointment, listAppointments } from "./appointments.controller";

            export const appointmentRouter = Router();

            appointmentRouter.get("/", listAppointments);
            appointmentRouter.post("/", createAppointment);
