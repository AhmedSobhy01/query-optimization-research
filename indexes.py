indexes = {
	  "Default": [],
    
		"BTree_Index": [
        "CREATE INDEX idx_customers_email ON customers(email);",  
        "CREATE INDEX idx_products_category ON products(category);",  
        "CREATE INDEX idx_orders_customer_id ON orders(customer_id);",
        "CREATE INDEX idx_order_items_order_id ON order_items(order_id);",
    ],

    "Hash_Index": [
        "CREATE INDEX idx_customers_email_hash ON customers USING HASH (email);",  
				"CREATE INDEX idx_orders_order_id_hash ON orders USING HASH (order_id);",  
    ],

    "Composite_Index": [
        "CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);",  
        "CREATE INDEX idx_order_items_product_quantity ON order_items(product_id, quantity);",  
    ],

    "Unique_Index": [
        "CREATE UNIQUE INDEX idx_customers_unique_email ON customers(email);",  
        "CREATE UNIQUE INDEX idx_order_items_unique ON order_items(order_id, product_id);",  
    ],

    "Full_Text_Index": [
        "CREATE INDEX idx_products_description_gin ON products USING gin(to_tsvector('english', product_name));",  # Full-text index on product_name
    ],

    "Clustered_Index": [
        "CLUSTER orders USING idx_orders_customer_id;",
    ],
}
