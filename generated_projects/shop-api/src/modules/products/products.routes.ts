import { Router } from "express";
            import { createProduct, listProducts } from "./products.controller";
            export const productRouter = Router();
            productRouter.get("/", listProducts);
            productRouter.post("/", createProduct);
