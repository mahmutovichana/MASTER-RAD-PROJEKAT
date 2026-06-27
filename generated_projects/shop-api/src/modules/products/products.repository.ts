export type Product = { id: string; name: string; status: "draft" | "active" | "archived"; stock: number; };
            const products: Product[] = [{ id: "product_1", name: "Desk Lamp", status: "active", stock: 0 }];
            export const productRepository = {
              list() { return products; },
              create(input: Omit<Product, "id">) {
                const saved = { id: `product_${products.length + 1}`, ...input };
                products.push(saved);
                return saved;
              }
            };
