import { z } from "zod";

            export const createPatientSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              riskScore: z.number().int().min(0).max(10)
            });
