import { z } from "zod";
            export const createCommentSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              visibilityLevel: z.number().int().min(1).max(3)
            });
