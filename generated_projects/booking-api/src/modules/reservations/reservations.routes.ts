import { Router } from "express";
            import { createReservation, listReservations } from "./reservations.controller";

            export const reservationRouter = Router();

            reservationRouter.get("/", listReservations);
            reservationRouter.post("/", createReservation);
