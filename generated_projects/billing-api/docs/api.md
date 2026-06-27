# Billing API API Reference

## Invoices

### GET /invoices

Returns all invoices.

### POST /invoices

Creates a invoice.

- `lineCount`: integer, minimum 1, maximum 200

## Payments

### GET /payments

Returns all payments.

### POST /payments

Creates a payment.

- `amountCents`: integer, minimum 100, maximum 100000
