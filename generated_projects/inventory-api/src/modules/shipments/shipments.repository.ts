export type Shipment = { id: string; name: string; status: "draft" | "active" | "archived"; packageCount: number; };
            const shipments: Shipment[] = [{ id: "shipment_1", name: "Inbound Shipment", status: "active", packageCount: 1 }];
            export const shipmentRepository = {
              list() { return shipments; },
              create(input: Omit<Shipment, "id">) {
                const saved = { id: `shipment_${shipments.length + 1}`, ...input };
                shipments.push(saved);
                return saved;
              }
            };
