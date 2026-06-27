import { z } from "zod";

            export const createCourseSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              lessonCount: z.number().int().min(1).max(80)
            });
