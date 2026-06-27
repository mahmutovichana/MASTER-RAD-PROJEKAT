import express from "express";
        import { ticketRouter } from "./modules/tickets/tickets.routes";
import { commentRouter } from "./modules/comments/comments.routes";

        export const app = express();

        app.use(express.json());
        app.use("/tickets", ticketRouter);
app.use("/comments", commentRouter);

        app.get("/health", (_req, res) => {
          res.status(200).json({ status: "ok" });
        });
