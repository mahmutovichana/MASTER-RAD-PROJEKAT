export type Room = {
              id: string;
              name: string;
              status: "draft" | "active" | "archived";
              capacity: number;
            };

            const rooms: Room[] = [
              { id: "room_1", name: "Blue Room", status: "active", capacity: 1 }
            ];

            export const roomRepository = {
              list() {
                return rooms;
              },
              create(input: Omit<Room, "id">) {
                const saved = { id: `room_${rooms.length + 1}`, ...input };
                rooms.push(saved);
                return saved;
              }
            };
