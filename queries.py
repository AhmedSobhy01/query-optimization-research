queries = {
    "Q1": """
    SELECT 
        c.customer_id, 
        c.customer_name, 
        COUNT(DISTINCT o.order_id) as total_orders,
        SUM(oi.quantity * oi.unit_price) as total_spend
    FROM 
        customers c
    JOIN 
        orders o ON c.customer_id = o.customer_id
    JOIN 
        order_items oi ON o.order_id = oi.order_id
    GROUP BY 
        c.customer_id, c.customer_name
    ORDER BY 
        total_spend DESC
    LIMIT 100;
    """,
    
    "Q2": """
    WITH CustomerProductRanking AS (
        SELECT 
            o.customer_id,
            oi.product_id,
            SUM(oi.quantity) as total_purchased,
            RANK() OVER (PARTITION BY o.customer_id ORDER BY SUM(oi.quantity) DESC) as product_rank
        FROM 
            orders o
        JOIN 
            order_items oi ON o.order_id = oi.order_id
        GROUP BY 
            o.customer_id, oi.product_id
    )
    SELECT 
        c.customer_name,
        p.product_name,
        cpr.total_purchased
    FROM 
        CustomerProductRanking cpr
    JOIN 
        customers c ON cpr.customer_id = c.customer_id
    JOIN 
        products p ON cpr.product_id = p.product_id
    WHERE 
        cpr.product_rank <= 3;
    """,
    
    "Q3": """
    SELECT 
        p.product_name,
        p.price
    FROM 
        products p
    WHERE 
        p.price > (SELECT AVG(price) FROM products)
    AND EXISTS (
        SELECT 1 
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        WHERE oi.product_id = p.product_id 
        AND o.order_date >= (CURRENT_DATE - INTERVAL '6 months')
    );
    """,
    
    "Q4": """
    SELECT 
        EXTRACT(YEAR FROM o.order_date) as order_year,
        p.category,
        COUNT(DISTINCT o.customer_id) as unique_customers,
        SUM(oi.quantity * oi.unit_price) as total_revenue
    FROM 
        orders o
    JOIN 
        order_items oi ON o.order_id = oi.order_id
    JOIN 
        products p ON oi.product_id = p.product_id
    GROUP BY 
        order_year, p.category
    HAVING 
        SUM(oi.quantity * oi.unit_price) > 10000
    ORDER BY 
        total_revenue DESC;
    """,
    
    "Q5": """
    WITH RECURSIVE CustomerNetwork AS (
        SELECT 
            customer_id, 
            customer_name,
            0 as depth
        FROM 
            customers
        
        UNION
        
        SELECT 
            c.customer_id, 
            c.customer_name, 
            cn.depth + 1
        FROM 
            customers c
        CROSS JOIN 
            CustomerNetwork cn
        WHERE 
            cn.depth < 3
    )
    SELECT COUNT(*) FROM CustomerNetwork;
    """,
    
    "Q6": """
    WITH CustomerSpending AS (
        SELECT 
            o.customer_id, 
            SUM(oi.quantity * oi.unit_price) as total_spend
        FROM 
            orders o
        JOIN 
            order_items oi ON o.order_id = oi.order_id
        GROUP BY 
            o.customer_id
    )
    SELECT 
        customer_id, 
        total_spend,
        NTILE(4) OVER (ORDER BY total_spend) as spend_quartile
    FROM 
        CustomerSpending
    ORDER BY 
        total_spend DESC;
    """,
    
    "Q7": """
    SELECT 
        DATE_TRUNC('month', o.order_date) as order_month,
        COUNT(DISTINCT o.customer_id) as active_customers,
        SUM(oi.quantity * oi.unit_price) as monthly_revenue
    FROM 
        orders o
    JOIN 
        order_items oi ON o.order_id = oi.order_id
    GROUP BY 
        order_month
    ORDER BY 
        order_month;
    """,
    
    "Q8": """
    SELECT 
        p.product_name,
        p.price,
        sq.avg_order_quantity
    FROM 
        products p
    JOIN (
            SELECT 
                oi.product_id,
                AVG(oi.quantity) AS avg_order_quantity
            FROM 
                order_items oi
            GROUP BY 
                oi.product_id
    )   sq ON p.product_id = sq.product_id
    JOIN 
        orders o ON o.order_id = oi.order_id
    WHERE 
        p.price > 100
    ORDER BY 
        sq.avg_order_quantity DESC;
    """,
    
    "Q9": """
    SELECT 
        p.category,
        SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date) = 1 THEN oi.quantity * oi.unit_price ELSE 0 END) as Jan_sales,
        SUM(CASE WHEN EXTRACT(MONTH FROM o.order_date) = 2 THEN oi.quantity * oi.unit_price ELSE 0 END) as Feb_sales
    FROM 
        orders o
    JOIN 
        order_items oi ON o.order_id = oi.order_id
    JOIN 
        products p ON oi.product_id = p.product_id
    GROUP BY 
        p.category;
    """,
    
    "Q10": """
    SELECT 
        c.customer_name, 
        COUNT(o.order_id) as order_count
    FROM 
        customers c
    JOIN 
        orders o ON c.customer_id = o.customer_id
    WHERE 
        c.customer_name LIKE '%John%Smith%'
    GROUP BY 
        c.customer_id
    ORDER BY 
        order_count DESC;
    """
}

# each query and potential category in analysis
# Q1: Join / Aggregation , function( list of the first hundred customers by their total spend)
# Q2: Window Function and Ranking, function( list of the top 3 products by total quantity purchased for each customer)
# Q3: Subquery, function( list of products that have a price greater than the average product price and have been purchased in the last 6 months)
# Q4: Group By / Having with joins, function( list of product categories with total revenue greater than $10,000, ordered by total revenue AND counts unique customers :))
# Q5: Recursive CTE, function( count of customers within 3 degrees of separation from each customer)
# Q6: Window Function, function( list of customers with their total spend and quartile of spend)
# Q7: Time based aggregation, function( monthly active customers and revenue for each month)
# Q8: Joins with subqueries, function( list of products with price greater than $100 ordered by average order quantity)
# Q9: Group By with case, function( total sales for each product category in January and February)
# Q10: String matching, function( count of orders for customers with the name John Smith)

# I tried to be as diverse as possible with the queries, some of them do overlap, but i think it was necessary for complexity and we can now argue that these types of queries are very common in the data analysis world, so they are not dummy queries.
# 4 and 5 are entirely chatgpt :D