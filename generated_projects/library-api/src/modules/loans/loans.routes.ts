import { Router } from "express";
            import { createLoan, listLoans } from "./loans.controller";
            export const loanRouter = Router();
            loanRouter.get("/", listLoans);
            loanRouter.post("/", createLoan);
