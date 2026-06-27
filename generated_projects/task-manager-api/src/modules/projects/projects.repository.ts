export type Project = {
              id: string;
              name: string;
              status: "draft" | "active" | "archived";
              memberLimit: number;
            };

            const projects: Project[] = [
              { id: "project_1", name: "Launch Plan", status: "active", memberLimit: 1 }
            ];

            export const projectRepository = {
              list() {
                return projects;
              },
              create(input: Omit<Project, "id">) {
                const saved = { id: `project_${projects.length + 1}`, ...input };
                projects.push(saved);
                return saved;
              }
            };
