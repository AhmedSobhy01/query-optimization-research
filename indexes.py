indexes = {
    "no_indexes": [],
    "single_column_indexes": [
        "CREATE INDEX idx_customers_email ON customers (email);",
        "CREATE INDEX idx_products_category ON products (category);",
        "CREATE INDEX idx_customers_created_date ON customers (created_date);", 
        "CREATE INDEX idx_orders_order_date ON orders (order_date);",
        
    ],
    "composite_indexes": [
        "CREATE INDEX idx_orders_customer_order_date ON orders (customer_id, order_date);",
        "CREATE INDEX idx_order_items_order_product ON order_items (order_id, product_id);",
        "CREATE INDEX idx_products_category_price ON products (category, price);",
    ],
    "partial_indexes": [
        "CREATE INDEX idx_products_expensive ON products (price) WHERE price > 500;",
        "CREATE INDEX idx_orders_recent ON orders (order_date) WHERE order_date > '2020-01-01';",
    ],
    "expression_indexes": [
        "CREATE INDEX idx_customers_lower_name ON customers (LOWER(customer_name));",
        "CREATE INDEX idx_products_category_name ON products ((category || ' ' || product_name));",
    ],
    "covering_indexes": [
        "CREATE INDEX idx_orders_order_date_total_amount ON orders (order_date) INCLUDE (total_amount);",
        "CREATE INDEX idx_order_items_product_id_quantity ON order_items (product_id) INCLUDE (quantity);",
    ],
}
