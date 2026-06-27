# Shop API API Reference

## Products

### GET /products

Returns all products.

### POST /products

Creates a product.

- `stock`: integer, minimum 0, maximum 500

## Orders

### GET /orders

Returns all orders.

### POST /orders

Creates a order.

- `quantity`: integer, minimum 1, maximum 25
