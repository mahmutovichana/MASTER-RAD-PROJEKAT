import { z } from "zod";
            export const createProjectSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              memberLimit: z.number().int().min(1).max(50)
            });
