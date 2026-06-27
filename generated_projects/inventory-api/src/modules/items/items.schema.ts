import { z } from "zod";

            export const createItemSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              reorderPoint: z.number().int().min(0).max(1000)
            });
