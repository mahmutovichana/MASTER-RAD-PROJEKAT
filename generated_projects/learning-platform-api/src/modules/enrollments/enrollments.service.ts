import { enrollmentRepository } from "./enrollments.repository";
            export const enrollmentService = {
              listEnrollments() { return enrollmentRepository.list(); },
              createEnrollment(input: { name: string; status: "draft" | "active" | "archived"; progressPercent: number }) {
                return enrollmentRepository.create(input);
              }
            };
