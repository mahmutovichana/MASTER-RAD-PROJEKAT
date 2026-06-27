export type Loan = {
              id: string;
              name: string;
              status: "draft" | "active" | "archived";
              loanDays: number;
            };

            const loans: Loan[] = [
              { id: "loan_1", name: "Loan", status: "active", loanDays: 1 }
            ];

            export const loanRepository = {
              list() {
                return loans;
              },
              create(input: Omit<Loan, "id">) {
                const saved = { id: `loan_${loans.length + 1}`, ...input };
                loans.push(saved);
                return saved;
              }
            };
