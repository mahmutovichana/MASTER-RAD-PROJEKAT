# Auth API Documentation

## Users

            ### GET /users

            Returns all users.

            Response: `200 OK`

            ### POST /users

            Creates a user.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `loginAttempts`: integer, minimum 0, maximum 10

            Response: `201 Created`
## Sessions

            ### GET /sessions

            Returns all sessions.

            Response: `200 OK`

            ### POST /sessions

            Creates a session.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `durationMinutes`: integer, minimum 5, maximum 480

            Response: `201 Created`
