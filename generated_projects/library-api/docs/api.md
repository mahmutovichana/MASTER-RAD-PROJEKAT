# Library API Documentation

## Books

            ### GET /books

            Returns all books.

            Response: `200 OK`

            ### POST /books

            Creates a book.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `copyCount`: integer, minimum 1, maximum 20

            Response: `201 Created`
## Loans

            ### GET /loans

            Returns all loans.

            Response: `200 OK`

            ### POST /loans

            Creates a loan.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `loanDays`: integer, minimum 1, maximum 60

            Response: `201 Created`
