import { z } from "zod";
            export const createTaskSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              priority: z.number().int().min(1).max(5)
            });
