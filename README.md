# Warehouse & Inventory Management System

A RESTful API for managing warehouses, tracking inventory, and monitoring stock levels across multiple locations. This system helps logistics companies manage their product storage and movement efficiently.

## Features

- **Warehouse Management**: Add and list warehouses across different locations
- **Inventory Tracking**: Monitor products stored in warehouses with real-time stock levels
- **Stock Movements**: Track all product additions, removals, and transfers between warehouses
- **Historical Data**: Retrieve movement history for any product
- **Stock Alerts**: Automated system to flag products with low stock levels
- **Caching**: Efficient data retrieval using Redis for real-time stock information
- **Pagination**: Support for large data sets with limit and offset parameters

## Tech Stack

- **Backend**: Flask (Python 3.10)
- **Database**: MySQL 8.0
- **Caching**: Redis 7.0
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Migrations**: Flask-Migrate (Alembic)
- **Containerization**: Docker & Docker Compose

## Project Structure

```
flask-inventory-system/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── stock_movement.py
│   │   └── warehouse.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── alerts.py
│   │   ├── product_routes.py
│   │   └── warehouse_routes.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── cache.py
│   │   └── config.py
│   └── __init__.py
├── Dockerfile
├── docker-compose.yml
├── init.sql
├── requirements.txt
├── .env
├── README.md
└── run.py
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation & Setup

1. Clone the repository:
   ```
   git clone https://github.com/polukal/flask-inventory-system.git
   cd flask-inventory-system
   ```

2. Start the containerized application:
   ```
   docker-compose up --build
   ```

3. The API will be available at:
   ```
   http://localhost:5000
   ```

## API Documentation

For detailed API documentation, refer to [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

### Quick Reference

- **Warehouses**:
  - `GET /warehouses/` - List all warehouses
  - `POST /warehouses/` - Create new warehouse
  - `GET /warehouses/{id}` - Get warehouse details
  - `GET /warehouses/{id}/products` - List products in warehouse
  - `POST /warehouses/transfer` - Transfer products between warehouses

- **Products**:
  - `GET /products/` - List all products
  - `POST /products/` - Add new product
  - `GET /products/{id}` - Get product details
  - `GET /products/{id}/stock` - Get current stock level
  - `GET /products/{id}/movements` - Get movement history

- **Alerts**:
  - `GET /alerts/` - List products with low stock levels

## Database Schema

### Tables

1. **warehouse**
   - id (PK)
   - name (unique)
   - location
   - created_at
   - updated_at

2. **product**
   - id (PK)
   - name
   - description
   - sku (unique)
   - min_stock_level
   - warehouse_id (FK)
   - created_at
   - updated_at

3. **stock_movement**
   - id (PK)
   - product_id (FK)
   - source_warehouse_id (FK, nullable)
   - destination_warehouse_id (FK, nullable)
   - quantity
   - movement_type
   - timestamp

### Indexes

- warehouse(name)
- product(sku)
- product(warehouse_id)
- stock_movement(product_id)
- stock_movement(source_warehouse_id)
- stock_movement(destination_warehouse_id)
- stock_movement(timestamp)

## Caching Strategy

The system uses Redis for caching:

1. **Stock Levels**: Cached with key pattern `stock:{product_id}`
2. **Low Stock Alerts**: Stored in Redis set `low_stock_alerts`
3. **Product Details**: Cached with key pattern `product:{product_id}`
4. **Warehouse Details**: Cached with key pattern `warehouse:{warehouse_id}`

Cache is automatically updated when changes occur and falls back to database queries when cache misses happen.

## Testing

You can test the API using tools like Postman or curl:

```bash
# Example: Create a warehouse
curl -X POST http://localhost:5000/warehouses/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Main Warehouse","location":"Seattle, WA"}'

# Example: Get all warehouses
curl http://localhost:5000/warehouses/
```

## Contribution

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.