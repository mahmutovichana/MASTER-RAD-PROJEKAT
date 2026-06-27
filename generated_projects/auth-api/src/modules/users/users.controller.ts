import { Request, Response } from "express";
            import { createUserSchema } from "./users.schema";
            import { userService } from "./users.service";
            export function listUsers(_req: Request, res: Response) { res.status(200).json({ data: userService.listUsers() }); }
            export function createUser(req: Request, res: Response) {
              const input = createUserSchema.parse(req.body);
              const result = userService.createUser(input);
              res.status(201).json({ data: result });
            }
