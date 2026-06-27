import { Router } from "express";
            import { createSession, listSessions } from "./sessions.controller";

            export const sessionRouter = Router();

            sessionRouter.get("/", listSessions);
            sessionRouter.post("/", createSession);
