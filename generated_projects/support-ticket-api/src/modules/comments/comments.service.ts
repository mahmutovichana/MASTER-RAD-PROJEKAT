import { commentRepository } from "./comments.repository";

            export const commentService = {
              listComments() {
                return commentRepository.list();
              },
              createComment(input: { name: string; status: "draft" | "active" | "archived"; visibilityLevel: number }) {
                return commentRepository.create(input);
              }
            };
