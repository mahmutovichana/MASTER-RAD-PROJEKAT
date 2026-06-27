import { z } from "zod";

            export const createLoanSchema = z.object({
              name: z.string().min(2),
              status: z.enum(["draft", "active", "archived"]),
              loanDays: z.number().int().min(1).max(60)
            });
