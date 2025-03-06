-- Initialize database schema
CREATE DATABASE IF NOT EXISTS inventory;
USE inventory;

-- Warehouses table
CREATE TABLE IF NOT EXISTS warehouse (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    location VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_warehouse_name (name)
);

-- Products table
CREATE TABLE IF NOT EXISTS product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    sku VARCHAR(50) UNIQUE,
    min_stock_level INT DEFAULT 10,
    warehouse_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (warehouse_id) REFERENCES warehouse(id),
    INDEX idx_product_sku (sku),
    INDEX idx_product_warehouse (warehouse_id)
);

-- Stock Movements table
CREATE TABLE IF NOT EXISTS stock_movement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    source_warehouse_id INT,
    destination_warehouse_id INT,
    quantity INT NOT NULL,
    movement_type VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (source_warehouse_id) REFERENCES warehouse(id),
    FOREIGN KEY (destination_warehouse_id) REFERENCES warehouse(id),
    INDEX idx_movement_product (product_id),
    INDEX idx_movement_source (source_warehouse_id),
    INDEX idx_movement_destination (destination_warehouse_id),
    INDEX idx_movement_timestamp (timestamp)
);

-- Insert some sample data
INSERT INTO warehouse (name, location) VALUES 
('Main Warehouse', 'Seattle, WA'),
('Distribution Center', 'Portland, OR');