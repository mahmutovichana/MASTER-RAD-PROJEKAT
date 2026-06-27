import { productRepository } from "./products.repository";

            export const productService = {
              listProducts() {
                return productRepository.list();
              },
              createProduct(input: { name: string; status: "draft" | "active" | "archived"; stock: number }) {
                return productRepository.create(input);
              }
            };
