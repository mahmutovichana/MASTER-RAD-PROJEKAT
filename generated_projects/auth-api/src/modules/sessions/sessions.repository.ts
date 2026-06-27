export type Session = {
              id: string;
              name: string;
              status: "draft" | "active" | "archived";
              durationMinutes: number;
            };

            const sessions: Session[] = [
              { id: "session_1", name: "Session", status: "active", durationMinutes: 5 }
            ];

            export const sessionRepository = {
              list() {
                return sessions;
              },
              create(input: Omit<Session, "id">) {
                const saved = { id: `session_${sessions.length + 1}`, ...input };
                sessions.push(saved);
                return saved;
              }
            };
