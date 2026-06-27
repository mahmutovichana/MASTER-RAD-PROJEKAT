import { itemRepository } from "./items.repository";

            export const itemService = {
              listItems() {
                return itemRepository.list();
              },
              createItem(input: { name: string; status: "draft" | "active" | "archived"; reorderPoint: number }) {
                return itemRepository.create(input);
              }
            };
