from azure.cosmos import CosmosClient, PartitionKey, exceptions

# Replace with your Cosmos DB credentials
# Replace with your Cosmos DB credentials
COSMOS_URI = "your-cosmos-db-uri"
COSMOS_KEY = "your-cosmos-db-key"
DATABASE_NAME = "SalesDatabase"
CONTAINER_NAME = "Transactions"


client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)

def init_db():
    try:
        database = client.create_database_if_not_exists(DATABASE_NAME)
        database.create_container_if_not_exists(
            id=CONTAINER_NAME,
            partition_key=PartitionKey(path="/transaction_id"),
            offer_throughput=400
        )
        print("✅ Cosmos DB ready.")
    except exceptions.CosmosHttpResponseError as e:
        print(f"❌ Error creating Cosmos DB: {e}")

def insert_transaction(data: dict):
    try:
        database = client.get_database_client(DATABASE_NAME)
        container = database.get_container_client(CONTAINER_NAME)
        container.create_item(data)
        print(f"💾 Saved to Cosmos DB: {data['transaction_id']}")
    except Exception as e:
        print(f"❌ Failed to insert: {e}")
