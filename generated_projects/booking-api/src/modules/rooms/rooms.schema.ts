import { z } from "zod";
            export const createRoomSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              capacity: z.number().int().min(1).max(200)
            });
