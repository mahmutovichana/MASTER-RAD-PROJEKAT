import { Router } from "express";
            import { createUser, listUsers } from "./users.controller";
            export const userRouter = Router();
            userRouter.get("/", listUsers);
            userRouter.post("/", createUser);
