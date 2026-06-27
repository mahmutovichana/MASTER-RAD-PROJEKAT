import { Router } from "express";
            import { createProject, listProjects } from "./projects.controller";

            export const projectRouter = Router();

            projectRouter.get("/", listProjects);
            projectRouter.post("/", createProject);
