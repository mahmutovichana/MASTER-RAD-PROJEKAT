export type Reservation = {
              id: string;
              name: string;
              status: "draft" | "active" | "archived";
              guestCount: number;
            };

            const reservations: Reservation[] = [
              { id: "reservation_1", name: "Morning Booking", status: "active", guestCount: 1 }
            ];

            export const reservationRepository = {
              list() {
                return reservations;
              },
              create(input: Omit<Reservation, "id">) {
                const saved = { id: `reservation_${reservations.length + 1}`, ...input };
                reservations.push(saved);
                return saved;
              }
            };
