# Support Ticket API Documentation

## Tickets

            ### GET /tickets

            Returns all tickets.

            Response: `200 OK`

            ### POST /tickets

            Creates a ticket.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `severity`: integer, minimum 1, maximum 5

            Response: `201 Created`
## Comments

            ### GET /comments

            Returns all comments.

            Response: `200 OK`

            ### POST /comments

            Creates a comment.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `visibilityLevel`: integer, minimum 1, maximum 3

            Response: `201 Created`
