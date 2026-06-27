# Library API API Reference

## Books

### GET /books

Returns all books.

### POST /books

Creates a book.

- `copyCount`: integer, minimum 1, maximum 20

## Loans

### GET /loans

Returns all loans.

### POST /loans

Creates a loan.

- `loanDays`: integer, minimum 1, maximum 60
