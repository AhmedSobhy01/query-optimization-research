queries = {
    "query_1": """

SELECT * FROM customers

WHERE created_date > '2023-01-01';

""",
    "query_2": """

SELECT * FROM products

WHERE category = 'Electronics';

""",
    "query_3": """

SELECT category, AVG(price) AS average_price

FROM products

GROUP BY category;

""",

    "query_4": """

SELECT o.order_id, o.order_date, o.total_amount

FROM orders o

JOIN customers c ON o.customer_id = c.customer_id

WHERE c.email = 'john.doe@example.com';

""",
    "query_5": """

SELECT o.order_id, p.product_name, oi.quantity, oi.unit_price

FROM orders o

JOIN order_items oi ON o.order_id = oi.order_id

JOIN products p ON oi.product_id = p.product_id

WHERE o.order_date BETWEEN '2022-01-01' AND '2022-12-31';

""",

    "query_6": """

SELECT p.product_id, p.product_name, SUM(oi.quantity) AS total_quantity_sold

FROM products p

JOIN order_items oi ON p.product_id = oi.product_id

GROUP BY p.product_id, p.product_name

HAVING SUM(oi.quantity) > 10000

ORDER BY total_quantity_sold DESC;

""",
    "query_7": """

SELECT p.product_id, p.product_name

FROM products p

LEFT JOIN order_items oi ON p.product_id = oi.product_id

WHERE oi.product_id IS NULL;

""",
}
