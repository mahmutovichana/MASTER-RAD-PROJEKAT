export type Order = {
              id: string;
              name: string;
              status: "draft" | "active" | "archived";
              quantity: number;
            };

            const orders: Order[] = [
              { id: "order_1", name: "Order", status: "active", quantity: 1 }
            ];

            export const orderRepository = {
              list() {
                return orders;
              },
              create(input: Omit<Order, "id">) {
                const saved = { id: `order_${orders.length + 1}`, ...input };
                orders.push(saved);
                return saved;
              }
            };
