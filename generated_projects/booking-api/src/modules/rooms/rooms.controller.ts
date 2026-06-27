import { Request, Response } from "express";
            import { createRoomSchema } from "./rooms.schema";
            import { roomService } from "./rooms.service";
            export function listRooms(_req: Request, res: Response) { res.status(200).json({ data: roomService.listRooms() }); }
            export function createRoom(req: Request, res: Response) {
              const input = createRoomSchema.parse(req.body);
              const result = roomService.createRoom(input);
              res.status(201).json({ data: result });
            }
