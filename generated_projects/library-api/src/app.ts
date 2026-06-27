import express from "express";
        import { bookRouter } from "./modules/books/books.routes";
import { loanRouter } from "./modules/loans/loans.routes";

        export const app = express();

        app.use(express.json());
        app.use("/books", bookRouter);
app.use("/loans", loanRouter);

        app.get("/health", (_req, res) => {
          res.status(200).json({ status: "ok" });
        });
