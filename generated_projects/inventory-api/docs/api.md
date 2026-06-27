# Inventory API API Reference

## Items

### GET /items

Returns all items.

### POST /items

Creates a item.

- `reorderPoint`: integer, minimum 0, maximum 1000

## Shipments

### GET /shipments

Returns all shipments.

### POST /shipments

Creates a shipment.

- `packageCount`: integer, minimum 1, maximum 100
