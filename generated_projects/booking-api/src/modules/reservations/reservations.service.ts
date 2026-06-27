import { reservationRepository } from "./reservations.repository";
            export const reservationService = {
              listReservations() { return reservationRepository.list(); },
              createReservation(input: { name: string; status: "draft" | "active" | "archived"; guestCount: number }) {
                return reservationRepository.create(input);
              }
            };
