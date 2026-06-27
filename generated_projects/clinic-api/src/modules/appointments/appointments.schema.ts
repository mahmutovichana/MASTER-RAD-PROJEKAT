import { z } from "zod";
            export const createAppointmentSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              durationMinutes: z.number().int().min(10).max(180)
            });
