export type Book = { id: string; name: string; status: "draft" | "active" | "archived"; copyCount: number; };
            const books: Book[] = [{ id: "book_1", name: "Clean Architecture", status: "active", copyCount: 1 }];
            export const bookRepository = {
              list() { return books; },
              create(input: Omit<Book, "id">) {
                const saved = { id: `book_${books.length + 1}`, ...input };
                books.push(saved);
                return saved;
              }
            };
