import random
import time

# ✅ Define sample customer and location lists
CUSTOMERS = [
    "Alice", "Bob", "Charlie", "Diana", "Ethan",
    "Fiona", "George", "Hannah", "Isaac", "Julia"
]

LOCATIONS = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Seattle", "Miami", "Dallas", "San Francisco", "Boston"
]

def generate_sales_data():
    """Generate a random sales transaction"""
    transaction = {
        "id": str(int(time.time() * 1000)),  # Numeric ID
        "customer_name": random.choice(CUSTOMERS),
        "amount": round(random.uniform(50, 5000), 2),
        "location": random.choice(LOCATIONS),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    return transaction
