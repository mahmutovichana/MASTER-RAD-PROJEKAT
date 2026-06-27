import { Request, Response } from "express";
            import { createTaskSchema } from "./tasks.schema";
            import { taskService } from "./tasks.service";

            export function listTasks(_req: Request, res: Response) {
              res.status(200).json({ data: taskService.listTasks() });
            }

            export function createTask(req: Request, res: Response) {
              const input = createTaskSchema.parse(req.body);
              const result = taskService.createTask(input);
              res.status(201).json({ data: result });
            }
