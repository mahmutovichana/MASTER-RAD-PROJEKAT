# Booking API API Reference

## Rooms

### GET /rooms

Returns all rooms.

### POST /rooms

Creates a room.

- `capacity`: integer, minimum 1, maximum 200

## Reservations

### GET /reservations

Returns all reservations.

### POST /reservations

Creates a reservation.

- `guestCount`: integer, minimum 1, maximum 12
