import { Request, Response } from "express";
            import { createLoanSchema } from "./loans.schema";
            import { loanService } from "./loans.service";

            export function listLoans(_req: Request, res: Response) {
              res.status(200).json({ data: loanService.listLoans() });
            }

            export function createLoan(req: Request, res: Response) {
              const input = createLoanSchema.parse(req.body);
              const result = loanService.createLoan(input);
              res.status(201).json({ data: result });
            }
