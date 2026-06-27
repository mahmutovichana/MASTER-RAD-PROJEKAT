import { loanRepository } from "./loans.repository";

            export const loanService = {
              listLoans() {
                return loanRepository.list();
              },
              createLoan(input: { name: string; status: "draft" | "active" | "archived"; loanDays: number }) {
                return loanRepository.create(input);
              }
            };
