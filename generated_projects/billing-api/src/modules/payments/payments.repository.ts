export type Payment = {
              id: string;
              name: string;
              status: "draft" | "active" | "archived";
              amountCents: number;
            };

            const payments: Payment[] = [
              { id: "payment_1", name: "Card Payment", status: "active", amountCents: 100 }
            ];

            export const paymentRepository = {
              list() {
                return payments;
              },
              create(input: Omit<Payment, "id">) {
                const saved = { id: `payment_${payments.length + 1}`, ...input };
                payments.push(saved);
                return saved;
              }
            };
