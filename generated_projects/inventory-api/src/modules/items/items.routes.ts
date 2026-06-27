import { Router } from "express";
            import { createItem, listItems } from "./items.controller";
            export const itemRouter = Router();
            itemRouter.get("/", listItems);
            itemRouter.post("/", createItem);
