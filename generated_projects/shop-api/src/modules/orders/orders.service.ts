import { orderRepository } from "./orders.repository";
            export const orderService = {
              listOrders() { return orderRepository.list(); },
              createOrder(input: { name: string; status: "draft" | "active" | "archived"; quantity: number }) {
                return orderRepository.create(input);
              }
            };
