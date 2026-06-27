import { shipmentRepository } from "./shipments.repository";

            export const shipmentService = {
              listShipments() {
                return shipmentRepository.list();
              },
              createShipment(input: { name: string; status: "draft" | "active" | "archived"; packageCount: number }) {
                return shipmentRepository.create(input);
              }
            };
