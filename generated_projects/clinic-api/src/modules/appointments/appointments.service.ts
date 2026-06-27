import { appointmentRepository } from "./appointments.repository";

            export const appointmentService = {
              listAppointments() {
                return appointmentRepository.list();
              },
              createAppointment(input: { name: string; status: "draft" | "active" | "archived"; durationMinutes: number }) {
                return appointmentRepository.create(input);
              }
            };
