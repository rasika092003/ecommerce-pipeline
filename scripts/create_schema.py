from sqlalchemy import create_engine, text

import os

engine = create_engine(
    f"postgresql://postgres:{os.environ.get('DB_PASSWORD', 'your_password_here')}@localhost:5432/ecommerce_db"
)


schema_sql = """
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    city VARCHAR(100),
    country VARCHAR(100),
    signup_date DATE
);

CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200),
    category_id INT REFERENCES categories(id),
    price NUMERIC(10,2),
    stock_qty INT
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    order_date TIMESTAMP,
    status VARCHAR(50),
    total_amount NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    quantity INT,
    unit_price NUMERIC(10,2)
);
"""

with engine.connect() as conn:
    conn.execute(text(schema_sql))
    conn.commit()
    print("All tables created successfully!")
