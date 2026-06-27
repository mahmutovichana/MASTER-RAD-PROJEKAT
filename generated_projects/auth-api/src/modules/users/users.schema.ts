import { z } from "zod";
            export const createUserSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              loginAttempts: z.number().int().min(0).max(10)
            });
