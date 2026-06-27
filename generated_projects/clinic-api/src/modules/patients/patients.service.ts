import { patientRepository } from "./patients.repository";

            export const patientService = {
              listPatients() {
                return patientRepository.list();
              },
              createPatient(input: { name: string; status: "draft" | "active" | "archived"; riskScore: number }) {
                return patientRepository.create(input);
              }
            };
