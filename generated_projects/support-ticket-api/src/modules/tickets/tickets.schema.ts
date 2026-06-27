import { z } from "zod";
            export const createTicketSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              severity: z.number().int().min(1).max(5)
            });
