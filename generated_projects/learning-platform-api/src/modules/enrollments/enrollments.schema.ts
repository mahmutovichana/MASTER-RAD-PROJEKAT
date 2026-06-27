import { z } from "zod";
            export const createEnrollmentSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              progressPercent: z.number().int().min(0).max(100)
            });
