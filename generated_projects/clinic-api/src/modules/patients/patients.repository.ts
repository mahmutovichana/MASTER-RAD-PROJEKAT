export type Patient = {
              id: string;
              name: string;
              status: "draft" | "active" | "archived";
              riskScore: number;
            };

            const patients: Patient[] = [
              { id: "patient_1", name: "Alex Patient", status: "active", riskScore: 0 }
            ];

            export const patientRepository = {
              list() {
                return patients;
              },
              create(input: Omit<Patient, "id">) {
                const saved = { id: `patient_${patients.length + 1}`, ...input };
                patients.push(saved);
                return saved;
              }
            };
