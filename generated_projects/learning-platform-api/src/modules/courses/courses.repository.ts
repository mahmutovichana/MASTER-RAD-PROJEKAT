export type Course = { id: string; name: string; status: "draft" | "active" | "archived"; lessonCount: number; };
            const courses: Course[] = [{ id: "course_1", name: "Intro to APIs", status: "active", lessonCount: 1 }];
            export const courseRepository = {
              list() { return courses; },
              create(input: Omit<Course, "id">) {
                const saved = { id: `course_${courses.length + 1}`, ...input };
                courses.push(saved);
                return saved;
              }
            };
