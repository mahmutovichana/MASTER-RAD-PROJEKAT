import { z } from "zod";
            export const createShipmentSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              packageCount: z.number().int().min(1).max(100)
            });
