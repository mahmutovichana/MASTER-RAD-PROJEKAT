import { Request, Response } from "express";
            import { createSessionSchema } from "./sessions.schema";
            import { sessionService } from "./sessions.service";
            export function listSessions(_req: Request, res: Response) { res.status(200).json({ data: sessionService.listSessions() }); }
            export function createSession(req: Request, res: Response) {
              const input = createSessionSchema.parse(req.body);
              const result = sessionService.createSession(input);
              res.status(201).json({ data: result });
            }
