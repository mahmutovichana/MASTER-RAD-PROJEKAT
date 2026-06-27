import { Router } from "express";
            import { createRoom, listRooms } from "./rooms.controller";

            export const roomRouter = Router();

            roomRouter.get("/", listRooms);
            roomRouter.post("/", createRoom);
