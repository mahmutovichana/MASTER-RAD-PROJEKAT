import express from "express";
        import { taskRouter } from "./modules/tasks/tasks.routes";
import { projectRouter } from "./modules/projects/projects.routes";

        export const app = express();

        app.use(express.json());
        app.use("/tasks", taskRouter);
app.use("/projects", projectRouter);

        app.get("/health", (_req, res) => {
          res.status(200).json({ status: "ok" });
        });
