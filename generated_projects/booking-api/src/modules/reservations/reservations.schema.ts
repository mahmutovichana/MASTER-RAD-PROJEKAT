import { z } from "zod";

            export const createReservationSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              guestCount: z.number().int().min(1).max(12)
            });
