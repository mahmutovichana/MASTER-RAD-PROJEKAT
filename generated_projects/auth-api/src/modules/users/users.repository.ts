export type User = {
              id: string;
              name: string;
              status: "draft" | "active" | "archived";
              loginAttempts: number;
            };

            const users: User[] = [
              { id: "user_1", name: "Pat User", status: "active", loginAttempts: 0 }
            ];

            export const userRepository = {
              list() {
                return users;
              },
              create(input: Omit<User, "id">) {
                const saved = { id: `user_${users.length + 1}`, ...input };
                users.push(saved);
                return saved;
              }
            };
