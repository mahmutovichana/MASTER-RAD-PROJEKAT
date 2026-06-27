import { z } from "zod";

            export const createOrderSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              quantity: z.number().int().min(1).max(25)
            });
