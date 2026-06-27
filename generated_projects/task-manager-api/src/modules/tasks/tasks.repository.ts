export type Task = {
              id: string;
              name: string;
              status: "draft" | "active" | "archived";
              priority: number;
            };

            const tasks: Task[] = [
              { id: "task_1", name: "Write Brief", status: "active", priority: 1 }
            ];

            export const taskRepository = {
              list() {
                return tasks;
              },
              create(input: Omit<Task, "id">) {
                const saved = { id: `task_${tasks.length + 1}`, ...input };
                tasks.push(saved);
                return saved;
              }
            };
