import json
import asyncio
import uuid
import random
import time
import confluent_kafka
from confluent_kafka import Producer
from data_generator import CUSTOMERS, LOCATIONS
from cosmos_db import insert_transaction

# Kafka-enabled Event Hub details
BOOTSTRAP_SERVERS = "your-eventhub-namespace.servicebus.windows.net:9093"
SASL_USERNAME = "$ConnectionString"
SASL_PASSWORD = "your-eventhub-connection-string"
TOPIC_NAME = "your-eventhub-name"

is_streaming = False

# Configure Kafka producer
producer_conf = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': SASL_USERNAME,
    'sasl.password': SASL_PASSWORD
}

producer = Producer(producer_conf)


def delivery_report(err, msg):
    """Callback when Kafka delivery completes."""
    if err is not None:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Delivered to {msg.topic()} [{msg.partition()}]")


async def send_to_eventhub(transaction):
    """Send transaction to Event Hub via Kafka interface"""
    producer.produce(
        TOPIC_NAME,
        key=str(transaction["id"]),
        value=json.dumps(transaction),
        callback=delivery_report
    )
    producer.flush()  # ensure delivery


async def start_streaming():
    """Continuously generate and stream random sales data"""
    global is_streaming
    is_streaming = True
    print("🚀 Streaming started using Kafka-enabled Event Hub.")

    while is_streaming:
        transaction = {
            "id": str(int(time.time() * 1000)),  # numeric ID
            "transaction_id": str(uuid.uuid4()),
            "customer_name": random.choice(CUSTOMERS),
            "amount": round(random.uniform(50, 5000), 2),
            "location": random.choice(LOCATIONS),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Store in Cosmos DB
        try:
            insert_transaction(transaction)
            print(f"💾 Saved to Cosmos DB: {transaction['id']}")
        except Exception as e:
            print(f"⚠️ Failed to insert into Cosmos DB: {e}")

        # Send to Kafka-enabled Event Hub
        asyncio.create_task(send_to_eventhub(transaction))

        await asyncio.sleep(2)


def stop_streaming():
    """Stop data streaming"""
    global is_streaming
    is_streaming = False
    print("🛑 Streaming stopped.")
