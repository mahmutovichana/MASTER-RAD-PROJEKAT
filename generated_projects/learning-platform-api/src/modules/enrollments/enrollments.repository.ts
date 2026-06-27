export type Enrollment = {
              id: string;
              name: string;
              status: "draft" | "active" | "archived";
              progressPercent: number;
            };

            const enrollments: Enrollment[] = [
              { id: "enrollment_1", name: "Enrollment", status: "active", progressPercent: 0 }
            ];

            export const enrollmentRepository = {
              list() {
                return enrollments;
              },
              create(input: Omit<Enrollment, "id">) {
                const saved = { id: `enrollment_${enrollments.length + 1}`, ...input };
                enrollments.push(saved);
                return saved;
              }
            };
