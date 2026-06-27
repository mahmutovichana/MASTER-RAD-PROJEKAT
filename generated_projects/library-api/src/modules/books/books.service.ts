import { bookRepository } from "./books.repository";
            export const bookService = {
              listBooks() { return bookRepository.list(); },
              createBook(input: { name: string; status: "draft" | "active" | "archived"; copyCount: number }) {
                return bookRepository.create(input);
              }
            };
