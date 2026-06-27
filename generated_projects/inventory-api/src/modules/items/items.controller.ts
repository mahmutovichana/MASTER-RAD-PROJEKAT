import { Request, Response } from "express";
            import { createItemSchema } from "./items.schema";
            import { itemService } from "./items.service";

            export function listItems(_req: Request, res: Response) {
              res.status(200).json({ data: itemService.listItems() });
            }

            export function createItem(req: Request, res: Response) {
              const input = createItemSchema.parse(req.body);
              const result = itemService.createItem(input);
              res.status(201).json({ data: result });
            }
