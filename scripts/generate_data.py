from faker import Faker
from sqlalchemy import create_engine
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker()
import os

engine = create_engine(
    f"postgresql://postgres:{os.environ.get('DB_PASSWORD', 'your_password_here')}@localhost:5432/ecommerce_db"
)


##Categories 
categories = [
    {"id": i+1, "name": name}
    for i, name in enumerate([
        "Electronics", "Clothing", "Books",
        "Home & Garden", "Sports", "Toys"
    ])
]
pd.DataFrame(categories).to_sql(
    "categories", engine, if_exists="append", index = False
)
print("Categories Inserted.")


##---Customers (10,000)---
customers = []
for i in range (1, 10001):
    customers.append({
        "name": fake.name(),
        "email": fake.unique.email(),
        "city": fake.city(),
        "country": fake.country(),
        "signup_date": fake.date_between(
            start_date="-3y", end_date="today"
        )

    })
pd.DataFrame(customers).to_sql(
    "customers", engine, if_exists="append",
    index=False, chunksize=500
)   
print("Customers Inserted") 

# --- Products (500) ---
products = []
for i in range(1, 501):
    products.append({
        "name": fake.bs().title(),
        "category_id": random.randint(1, 6),
        "price": round(random.uniform(5.0, 999.0), 2),
        "stock_qty": random.randint(0, 500)
    })
pd.DataFrame(products).to_sql(
    "products", engine, if_exists="append",
    index=False, chunksize=100
)
print("Products inserted.")

# --- Orders + Order Items (50,000 orders) ---
orders = []
order_items = []
order_id = 1

for i in range(1, 50001):
    order_date = fake.date_time_between(
        start_date="-2y", end_date="now"
    )
    status = random.choice([
        "completed", "completed", "completed",
        "pending", "cancelled", "refunded"
    ])
    num_items = random.randint(1, 5)
    total = 0
    items = []
    for _ in range(num_items):
        product_id = random.randint(1, 500)
        qty = random.randint(1, 4)
        price = round(random.uniform(5.0, 999.0), 2)
        total += qty * price
        items.append({
            "order_id": order_id,
            "product_id": product_id,
            "quantity": qty,
            "unit_price": price
        })
    orders.append({
        "customer_id": random.randint(1, 10000),
        "order_date": order_date,
        "status": status,
        "total_amount": round(total, 2)
    })
    order_items.extend(items)
    order_id += 1

pd.DataFrame(orders).to_sql(
    "orders", engine, if_exists="append",
    index=False, chunksize=500
)
print("Orders inserted.")

pd.DataFrame(order_items).to_sql(
    "order_items", engine, if_exists="append",
    index=False, chunksize=1000
)
print("Order items inserted.")
print("Data generation complete!")
