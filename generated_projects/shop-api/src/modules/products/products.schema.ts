import { z } from "zod";
            export const createProductSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              stock: z.number().int().min(0).max(500)
            });
