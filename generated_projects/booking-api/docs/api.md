# Booking API Documentation

## Rooms

            ### GET /rooms

            Returns all rooms.

            Response: `200 OK`

            ### POST /rooms

            Creates a room.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `capacity`: integer, minimum 1, maximum 200

            Response: `201 Created`
## Reservations

            ### GET /reservations

            Returns all reservations.

            Response: `200 OK`

            ### POST /reservations

            Creates a reservation.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `guestCount`: integer, minimum 1, maximum 12

            Response: `201 Created`
