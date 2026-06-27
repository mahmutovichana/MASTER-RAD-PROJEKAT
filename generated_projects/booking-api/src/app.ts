import express from "express";
        import { roomRouter } from "./modules/rooms/rooms.routes";
import { reservationRouter } from "./modules/reservations/reservations.routes";

        export const app = express();

        app.use(express.json());
        app.use("/rooms", roomRouter);
app.use("/reservations", reservationRouter);

        app.get("/health", (_req, res) => {
          res.status(200).json({ status: "ok" });
        });
