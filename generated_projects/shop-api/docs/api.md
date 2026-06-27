# Shop API Documentation

## Products

            ### GET /products

            Returns all products.

            Response: `200 OK`

            ### POST /products

            Creates a product.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `stock`: integer, minimum 0, maximum 500

            Response: `201 Created`
## Orders

            ### GET /orders

            Returns all orders.

            Response: `200 OK`

            ### POST /orders

            Creates a order.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `quantity`: integer, minimum 1, maximum 25

            Response: `201 Created`
