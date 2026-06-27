import { z } from "zod";
            export const createBookSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              copyCount: z.number().int().min(1).max(20)
            });
