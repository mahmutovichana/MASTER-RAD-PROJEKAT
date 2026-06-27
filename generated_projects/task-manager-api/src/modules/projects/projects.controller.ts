import { Request, Response } from "express";
            import { createProjectSchema } from "./projects.schema";
            import { projectService } from "./projects.service";

            export function listProjects(_req: Request, res: Response) {
              res.status(200).json({ data: projectService.listProjects() });
            }

            export function createProject(req: Request, res: Response) {
              const input = createProjectSchema.parse(req.body);
              const result = projectService.createProject(input);
              res.status(201).json({ data: result });
            }
