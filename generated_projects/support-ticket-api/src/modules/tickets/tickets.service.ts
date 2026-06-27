import { ticketRepository } from "./tickets.repository";

            export const ticketService = {
              listTickets() {
                return ticketRepository.list();
              },
              createTicket(input: { name: string; status: "draft" | "active" | "archived"; severity: number }) {
                return ticketRepository.create(input);
              }
            };
