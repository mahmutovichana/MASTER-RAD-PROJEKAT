import { z } from "zod";

            export const createSessionSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              durationMinutes: z.number().int().min(5).max(480)
            });
