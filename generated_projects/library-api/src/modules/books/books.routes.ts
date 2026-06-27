import { Router } from "express";
            import { createBook, listBooks } from "./books.controller";

            export const bookRouter = Router();

            bookRouter.get("/", listBooks);
            bookRouter.post("/", createBook);
