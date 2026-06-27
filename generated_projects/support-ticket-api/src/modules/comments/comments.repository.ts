export type Comment = {
              id: string;
              name: string;
              status: "draft" | "active" | "archived";
              visibilityLevel: number;
            };

            const comments: Comment[] = [
              { id: "comment_1", name: "Initial Reply", status: "active", visibilityLevel: 1 }
            ];

            export const commentRepository = {
              list() {
                return comments;
              },
              create(input: Omit<Comment, "id">) {
                const saved = { id: `comment_${comments.length + 1}`, ...input };
                comments.push(saved);
                return saved;
              }
            };
