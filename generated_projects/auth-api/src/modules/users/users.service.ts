import { userRepository } from "./users.repository";

            export const userService = {
              listUsers() {
                return userRepository.list();
              },
              createUser(input: { name: string; status: "draft" | "active" | "archived"; loginAttempts: number }) {
                return userRepository.create(input);
              }
            };
