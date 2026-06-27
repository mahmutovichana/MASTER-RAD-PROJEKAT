# Inventory API Documentation

## Items

            ### GET /items

            Returns all items.

            Response: `200 OK`

            ### POST /items

            Creates a item.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `reorderPoint`: integer, minimum 0, maximum 1000

            Response: `201 Created`
## Shipments

            ### GET /shipments

            Returns all shipments.

            Response: `200 OK`

            ### POST /shipments

            Creates a shipment.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `packageCount`: integer, minimum 1, maximum 100

            Response: `201 Created`
