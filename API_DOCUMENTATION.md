# Inventory Management System API Documentation

## Overview

This RESTful API provides comprehensive warehouse and inventory management capabilities for a logistics company. It allows tracking products across multiple warehouses, managing stock movements, monitoring real-time stock levels, and receiving alerts for low stock levels.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, this API does not implement authentication. Authentication will be added in future releases.

## Common Response Formats

### Success Response

```json
{
  "message": "Operation successful",
  "data": { ... }
}
```

### Error Response

```json
{
  "error": "Error message",
  "details": { ... }
}
```

### Pagination Format

All endpoints that return lists support pagination:

```json
{
  "items": [ ... ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "pages": 10
  }
}
```

## Warehouses

### Add a New Warehouse

**POST** `/warehouses/`

Create a new warehouse in the system.

**Request Body**

| Field    | Type   | Description              | Required |
|----------|--------|--------------------------|----------|
| name     | string | Name of the warehouse    | Yes      |
| location | string | Location of the warehouse| Yes      |

**Example Request**

```json
{
  "name": "North Seattle Warehouse",
  "location": "Seattle, WA"
}
```

**Example Response**

```json
{
  "message": "Warehouse added successfully",
  "warehouse": {
    "id": 1,
    "name": "North Seattle Warehouse",
    "location": "Seattle, WA",
    "created_at": "2025-03-06T12:30:45.123456",
    "updated_at": "2025-03-06T12:30:45.123456"
  }
}
```

### List All Warehouses

**GET** `/warehouses/`

Retrieve a paginated list of all warehouses.

**Query Parameters**

| Parameter | Description                | Default |
|-----------|----------------------------|---------|
| page      | Page number to retrieve    | 1       |
| limit     | Number of items per page   | 10      |

**Example Response**

```json
{
  "items": [
    {
      "id": 1,
      "name": "North Seattle Warehouse",
      "location": "Seattle, WA",
      "created_at": "2025-03-06T12:30:45.123456",
      "updated_at": "2025-03-06T12:30:45.123456"
    },
    {
      "id": 2,
      "name": "South Portland Warehouse",
      "location": "Portland, OR",
      "created_at": "2025-03-06T12:35:22.123456",
      "updated_at": "2025-03-06T12:35:22.123456"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 2,
    "pages": 1
  }
}
```

### Get Warehouse Details

**GET** `/warehouses/{warehouse_id}`

Retrieve details of a specific warehouse.

**Example Response**

```json
{
  "id": 1,
  "name": "North Seattle Warehouse",
  "location": "Seattle, WA",
  "created_at": "2025-03-06T12:30:45.123456",
  "updated_at": "2025-03-06T12:30:45.123456"
}
```

### List Products in a Warehouse

**GET** `/warehouses/{warehouse_id}/products`

Retrieve a paginated list of products in a specific warehouse.

**Query Parameters**

| Parameter | Description              | Default |
|-----------|--------------------------|---------|
| page      | Page number to retrieve  | 1       |
| limit     | Number of items per page | 10      |

**Example Response**

```json
{
  "items": [
    {
      "id": 1,
      "name": "LED Monitor",
      "description": "27-inch LED Monitor",
      "sku": "MON-LED-27",
      "min_stock_level": 10,
      "warehouse_id": 1,
      "warehouse_name": "North Seattle Warehouse",
      "created_at": "2025-03-06T12:40:15.123456",
      "updated_at": "2025-03-06T12:40:15.123456"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "pages": 1
  }
}
```

### Transfer Products Between Warehouses

**POST** `/warehouses/transfer`

Transfer products from one warehouse to another.

**Request Body**

| Field                   | Type    | Description                     | Required |
|-------------------------|---------|---------------------------------|----------|
| product_id              | integer | ID of the product to transfer   | Yes      |
| source_warehouse_id     | integer | Source warehouse ID             | Yes      |
| destination_warehouse_id| integer | Destination warehouse ID        | Yes      |
| quantity                | integer | Quantity to transfer            | Yes      |

**Example Request**

```json
{
  "product_id": 1,
  "source_warehouse_id": 1,
  "destination_warehouse_id": 2,
  "quantity": 5
}
```

**Example Response**

```json
{
  "message": "Product transferred successfully",
  "movement": {
    "id": 1,
    "product_id": 1,
    "source_warehouse_id": 1,
    "destination_warehouse_id": 2,
    "quantity": 5,
    "timestamp": "2025-03-06T14:30:15.123456"
  }
}
```

## Products

### Add a New Product

**POST** `/products/`

Add a new product to a warehouse.

**Request Body**

| Field           | Type    | Description                   | Required |
|-----------------|---------|-------------------------------|----------|
| name            | string  | Name of the product           | Yes      |
| description     | string  | Description of the product    | No       |
| sku             | string  | Stock keeping unit            | No       |
| min_stock_level | integer | Minimum stock threshold       | No       |
| warehouse_id    | integer | ID of the warehouse           | Yes      |
| stock           | integer | Initial stock level           | No       |

**Example Request**

```json
{
  "name": "LED Monitor",
  "description": "27-inch LED Monitor",
  "sku": "MON-LED-27",
  "min_stock_level": 10,
  "warehouse_id": 1,
  "stock": 20
}
```

**Example Response**

```json
{
  "message": "Product added successfully",
  "product": {
    "id": 1,
    "name": "LED Monitor",
    "description": "27-inch LED Monitor",
    "sku": "MON-LED-27",
    "min_stock_level": 10,
    "warehouse_id": 1,
    "warehouse_name": "North Seattle Warehouse",
    "created_at": "2025-03-06T12:40:15.123456",
    "updated_at": "2025-03-06T12:40:15.123456"
  }
}
```

### List All Products

**GET** `/products/`

Retrieve a paginated list of all products.

**Query Parameters**

| Parameter    | Description                | Default |
|--------------|----------------------------|---------|
| page         | Page number to retrieve    | 1       |
| limit        | Number of items per page   | 10      |
| warehouse_id | Filter by warehouse ID     | None    |

**Example Response**

```json
{
  "items": [
    {
      "id": 1,
      "name": "LED Monitor",
      "description": "27-inch LED Monitor",
      "sku": "MON-LED-27",
      "min_stock_level": 10,
      "warehouse_id": 1,
      "warehouse_name": "North Seattle Warehouse",
      "created_at": "2025-03-06T12:40:15.123456",
      "updated_at": "2025-03-06T12:40:15.123456"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "pages": 1
  }
}
```

### Get Product Details

**GET** `/products/{product_id}`

Retrieve details of a specific product.

**Example Response**

```json
{
  "id": 1,
  "name": "LED Monitor",
  "description": "27-inch LED Monitor",
  "sku": "MON-LED-27",
  "min_stock_level": 10,
  "warehouse_id": 1,
  "warehouse_name": "North Seattle Warehouse",
  "created_at": "2025-03-06T12:40:15.123456",
  "updated_at": "2025-03-06T12:40:15.123456"
}
```

### Get Product Stock Level

**GET** `/products/{product_id}/stock`

Retrieve the current stock level of a product.

**Example Response**

```json
{
  "product_id": 1,
  "stock_level": 15
}
```

### Get Product Movement History

**GET** `/products/{product_id}/movements`

Retrieve the movement history of a product.

**Query Parameters**

| Parameter | Description              | Default |
|-----------|--------------------------|---------|
| page      | Page number to retrieve  | 1       |
| limit     | Number of items per page | 10      |

**Example Response**

```json
{
  "items": [
    {
      "id": 1,
      "movement_type": "addition",
      "quantity": 20,
      "source_warehouse_id": null,
      "source_warehouse_name": null,
      "destination_warehouse_id": 1,
      "destination_warehouse_name": "North Seattle Warehouse",
      "timestamp": "2025-03-06T10:15:30.123456"
    },
    {
      "id": 2,
      "movement_type": "transfer",
      "quantity": 5,
      "source_warehouse_id": 1,
      "source_warehouse_name": "North Seattle Warehouse",
      "destination_warehouse_id": 2,
      "destination_warehouse_name": "South Portland Warehouse",
      "timestamp": "2025-03-06T14:30:15.123456"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 2,
    "pages": 1
  }
}
```

## Stock Alerts

### List Low Stock Alerts

**GET** `/alerts/`

Retrieve a list of products with stock levels below their minimum threshold.

**Example Response**

```json
[
  {
    "id": 2,
    "name": "Wireless Keyboard",
    "sku": "KEY-WL-01",
    "min_stock_level": 15,
    "warehouse_id": 1,
    "warehouse_name": "North Seattle Warehouse"
  }
]
```

## Error Codes

| Status Code | Description                               |
|-------------|-------------------------------------------|
| 400         | Bad Request - Invalid input parameters    |
| 404         | Not Found - Resource does not exist       |
| 500         | Internal Server Error                     |

## Caching Behavior

- Stock levels are cached in Redis for fast retrieval
- If data is not found in Redis, it's fetched from the database and then cached
- Products with stock levels below their minimum threshold are automatically flagged in Redis
- These flags are used to quickly retrieve the list of products with low stock levels

## API Usage Examples

### Complete Workflow Example

1. Create a warehouse:
   ```
   POST /warehouses/
   {
     "name": "Main Warehouse",
     "location": "Seattle, WA"
   }
   ```

2. Create another warehouse:
   ```
   POST /warehouses/
   {
     "name": "Secondary Warehouse",
     "location": "Portland, OR"
   }
   ```

3. Add a product to the first warehouse:
   ```
   POST /products/
   {
     "name": "LED Monitor",
     "description": "27-inch LED Monitor",
     "sku": "MON-LED-27",
     "min_stock_level": 10,
     "warehouse_id": 1,
     "stock": 20
   }
   ```

4. Transfer products between warehouses:
   ```
   POST /warehouses/transfer
   {
     "product_id": 1,
     "source_warehouse_id": 1,
     "destination_warehouse_id": 2,
     "quantity": 5
   }
   ```

5. Check stock level:
   ```
   GET /products/1/stock
   ```

6. View product movement history:
   ```
   GET /products/1/movements
   ```

7. Add more products and check for alerts:
   ```
   POST /products/
   {
     "name": "Wireless Keyboard",
     "description": "Bluetooth wireless keyboard",
     "sku": "KEY-WL-01",
     "min_stock_level": 15,
     "warehouse_id": 1,
     "stock": 10
   }
   
   GET /alerts/
   ```