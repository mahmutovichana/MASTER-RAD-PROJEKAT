import { Request, Response } from "express";
            import { createProductSchema } from "./products.schema";
            import { productService } from "./products.service";
            export function listProducts(_req: Request, res: Response) { res.status(200).json({ data: productService.listProducts() }); }
            export function createProduct(req: Request, res: Response) {
              const input = createProductSchema.parse(req.body);
              const result = productService.createProduct(input);
              res.status(201).json({ data: result });
            }
