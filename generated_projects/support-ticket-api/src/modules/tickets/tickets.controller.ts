import { Request, Response } from "express";
            import { createTicketSchema } from "./tickets.schema";
            import { ticketService } from "./tickets.service";
            export function listTickets(_req: Request, res: Response) { res.status(200).json({ data: ticketService.listTickets() }); }
            export function createTicket(req: Request, res: Response) {
              const input = createTicketSchema.parse(req.body);
              const result = ticketService.createTicket(input);
              res.status(201).json({ data: result });
            }
