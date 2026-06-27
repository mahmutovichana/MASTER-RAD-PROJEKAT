import { sessionRepository } from "./sessions.repository";

            export const sessionService = {
              listSessions() {
                return sessionRepository.list();
              },
              createSession(input: { name: string; status: "draft" | "active" | "archived"; durationMinutes: number }) {
                return sessionRepository.create(input);
              }
            };
