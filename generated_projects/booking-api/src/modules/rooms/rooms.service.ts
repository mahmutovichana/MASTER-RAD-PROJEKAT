import { roomRepository } from "./rooms.repository";
            export const roomService = {
              listRooms() { return roomRepository.list(); },
              createRoom(input: { name: string; status: "draft" | "active" | "archived"; capacity: number }) {
                return roomRepository.create(input);
              }
            };
