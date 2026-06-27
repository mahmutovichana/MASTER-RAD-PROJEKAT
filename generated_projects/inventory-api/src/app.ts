import express from "express";
        import { itemRouter } from "./modules/items/items.routes";
import { shipmentRouter } from "./modules/shipments/shipments.routes";

        export const app = express();

        app.use(express.json());
        app.use("/items", itemRouter);
app.use("/shipments", shipmentRouter);

        app.get("/health", (_req, res) => {
          res.status(200).json({ status: "ok" });
        });
