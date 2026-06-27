import { z } from "zod";

            export const createInvoiceSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              lineCount: z.number().int().min(1).max(200)
            });
