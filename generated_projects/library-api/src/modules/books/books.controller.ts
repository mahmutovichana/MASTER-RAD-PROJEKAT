import { Request, Response } from "express";
            import { createBookSchema } from "./books.schema";
            import { bookService } from "./books.service";
            export function listBooks(_req: Request, res: Response) { res.status(200).json({ data: bookService.listBooks() }); }
            export function createBook(req: Request, res: Response) {
              const input = createBookSchema.parse(req.body);
              const result = bookService.createBook(input);
              res.status(201).json({ data: result });
            }
