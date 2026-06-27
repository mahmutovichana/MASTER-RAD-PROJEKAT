# Support Ticket API API Reference

## Tickets

### GET /tickets

Returns all tickets.

### POST /tickets

Creates a ticket.

- `severity`: integer, minimum 1, maximum 5

## Comments

### GET /comments

Returns all comments.

### POST /comments

Creates a comment.

- `visibilityLevel`: integer, minimum 1, maximum 3
