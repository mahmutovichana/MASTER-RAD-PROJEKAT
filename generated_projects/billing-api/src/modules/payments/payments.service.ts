import { paymentRepository } from "./payments.repository";

            export const paymentService = {
              listPayments() {
                return paymentRepository.list();
              },
              createPayment(input: { name: string; status: "draft" | "active" | "archived"; amountCents: number }) {
                return paymentRepository.create(input);
              }
            };
