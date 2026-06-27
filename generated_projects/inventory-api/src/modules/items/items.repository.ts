export type Item = { id: string; name: string; status: "draft" | "active" | "archived"; reorderPoint: number; };
            const items: Item[] = [{ id: "item_1", name: "USB Cable", status: "active", reorderPoint: 0 }];
            export const itemRepository = {
              list() { return items; },
              create(input: Omit<Item, "id">) {
                const saved = { id: `item_${items.length + 1}`, ...input };
                items.push(saved);
                return saved;
              }
            };
