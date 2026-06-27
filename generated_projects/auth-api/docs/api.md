# Auth API API Reference

## Users

### GET /users

Returns all users.

### POST /users

Creates a user.

- `loginAttempts`: integer, minimum 0, maximum 10

## Sessions

### GET /sessions

Returns all sessions.

### POST /sessions

Creates a session.

- `durationMinutes`: integer, minimum 5, maximum 480
