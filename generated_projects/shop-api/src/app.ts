import express from "express";
        import { productRouter } from "./modules/products/products.routes";
import { orderRouter } from "./modules/orders/orders.routes";

        export const app = express();

        app.use(express.json());
        app.use("/products", productRouter);
app.use("/orders", orderRouter);

        app.get("/health", (_req, res) => {
          res.status(200).json({ status: "ok" });
        });
