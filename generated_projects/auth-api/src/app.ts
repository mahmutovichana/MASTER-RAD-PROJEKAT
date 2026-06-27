import express from "express";
        import { userRouter } from "./modules/users/users.routes";
import { sessionRouter } from "./modules/sessions/sessions.routes";

        export const app = express();

        app.use(express.json());
        app.use("/users", userRouter);
app.use("/sessions", sessionRouter);

        app.get("/health", (_req, res) => {
          res.status(200).json({ status: "ok" });
        });
