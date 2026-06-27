export type Appointment = { id: string; name: string; status: "draft" | "active" | "archived"; durationMinutes: number; };
            const appointments: Appointment[] = [{ id: "appointment_1", name: "Checkup", status: "active", durationMinutes: 10 }];
            export const appointmentRepository = {
              list() { return appointments; },
              create(input: Omit<Appointment, "id">) {
                const saved = { id: `appointment_${appointments.length + 1}`, ...input };
                appointments.push(saved);
                return saved;
              }
            };
