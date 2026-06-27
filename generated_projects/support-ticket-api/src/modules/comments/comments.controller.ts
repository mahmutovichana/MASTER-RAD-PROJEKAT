import { Request, Response } from "express";
            import { createCommentSchema } from "./comments.schema";
            import { commentService } from "./comments.service";
            export function listComments(_req: Request, res: Response) { res.status(200).json({ data: commentService.listComments() }); }
            export function createComment(req: Request, res: Response) {
              const input = createCommentSchema.parse(req.body);
              const result = commentService.createComment(input);
              res.status(201).json({ data: result });
            }
