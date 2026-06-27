import { Router } from "express";
            import { createTicket, listTickets } from "./tickets.controller";

            export const ticketRouter = Router();

            ticketRouter.get("/", listTickets);
            ticketRouter.post("/", createTicket);
