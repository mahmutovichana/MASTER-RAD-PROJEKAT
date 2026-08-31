import { createFileRoute } from "@tanstack/react-router";

import { OrderDetailPage } from "@/features/orders/order-detail-page";

export const Route = createFileRoute("/app/orders_/$id")({ component: OrderRoute });

function OrderRoute() {
  const { id } = Route.useParams();
  return <OrderDetailPage id={Number(id)} />;
}
