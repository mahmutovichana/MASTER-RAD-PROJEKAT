# Billing API Documentation

## Invoices

            ### GET /invoices

            Returns all invoices.

            Response: `200 OK`

            ### POST /invoices

            Creates a invoice.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `lineCount`: integer, minimum 1, maximum 200

            Response: `201 Created`
## Payments

            ### GET /payments

            Returns all payments.

            Response: `200 OK`

            ### POST /payments

            Creates a payment.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `amountCents`: integer, minimum 100, maximum 100000

            Response: `201 Created`
