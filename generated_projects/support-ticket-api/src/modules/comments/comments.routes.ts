import { Router } from "express";
            import { createComment, listComments } from "./comments.controller";

            export const commentRouter = Router();

            commentRouter.get("/", listComments);
            commentRouter.post("/", createComment);
