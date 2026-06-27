import { taskRepository } from "./tasks.repository";

            export const taskService = {
              listTasks() {
                return taskRepository.list();
              },
              createTask(input: { name: string; status: "draft" | "active" | "archived"; priority: number }) {
                return taskRepository.create(input);
              }
            };
