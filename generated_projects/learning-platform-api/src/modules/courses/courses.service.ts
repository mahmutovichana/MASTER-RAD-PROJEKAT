import { courseRepository } from "./courses.repository";
            export const courseService = {
              listCourses() { return courseRepository.list(); },
              createCourse(input: { name: string; status: "draft" | "active" | "archived"; lessonCount: number }) {
                return courseRepository.create(input);
              }
            };
