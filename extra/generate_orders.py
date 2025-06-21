from faker import Faker
import random
import csv
from datetime import datetime

fake = Faker()
Faker.seed(42)

NUM_ORDERS = 1000


def generate_order():
    return {
        "order_id": fake.uuid4(),
        "customer_name": fake.name(),
        "email": fake.email(),
        "product": fake.word(
            ext_word_list=["Laptop", "Mobile", "Tablet", "Monitor", "Keyboard", "Mouse"]
        ),
        "category": fake.word(ext_word_list=["Electronics", "Accessories"]),
        "price": round(random.uniform(1000, 50000), 2),
        "quantity": random.randint(1, 5),
        "order_date": fake.date_between(start_date="-1y", end_date="today").strftime(
            "%Y-%m-%d"
        ),
        "country": fake.country(),
    }


# Output CSV
output_file = "raw_orders.csv"

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "order_id",
            "customer_name",
            "email",
            "product",
            "category",
            "price",
            "quantity",
            "order_date",
            "country",
        ],
    )
    writer.writeheader()

    for _ in range(NUM_ORDERS):
        writer.writerow(generate_order())

print(f"{NUM_ORDERS} fake orders written to {output_file}")
