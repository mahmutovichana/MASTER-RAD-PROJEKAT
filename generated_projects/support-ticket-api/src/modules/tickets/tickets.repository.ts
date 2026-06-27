export type Ticket = {
              id: string;
              name: string;
              status: "draft" | "active" | "archived";
              severity: number;
            };

            const tickets: Ticket[] = [
              { id: "ticket_1", name: "Login Issue", status: "active", severity: 1 }
            ];

            export const ticketRepository = {
              list() {
                return tickets;
              },
              create(input: Omit<Ticket, "id">) {
                const saved = { id: `ticket_${tickets.length + 1}`, ...input };
                tickets.push(saved);
                return saved;
              }
            };
