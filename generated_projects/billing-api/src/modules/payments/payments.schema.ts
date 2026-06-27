import { z } from "zod";
            export const createPaymentSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              amountCents: z.number().int().min(100).max(100000)
            });
