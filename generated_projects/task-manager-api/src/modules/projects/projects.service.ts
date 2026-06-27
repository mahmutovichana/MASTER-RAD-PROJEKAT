import { projectRepository } from "./projects.repository";

            export const projectService = {
              listProjects() {
                return projectRepository.list();
              },
              createProject(input: { name: string; status: "draft" | "active" | "archived"; memberLimit: number }) {
                return projectRepository.create(input);
              }
            };
