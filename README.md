# Sales Data API with Azure Integration

This project is a FastAPI-based sales data generator that creates random sales transactions and streams them into Azure services. It can generate sample sales records through an API endpoint, continuously stream records to Azure Event Hub using the Kafka protocol, and store streamed transactions in Azure Cosmos DB.

## Features

- Generate random sales transactions with customer name, amount, location, and timestamp.
- Expose REST API endpoints using FastAPI.
- Start and stop automatic data streaming from API calls.
- Send generated transactions to Azure Event Hub using Kafka.
- Store generated transactions in Azure Cosmos DB.
- Test endpoints easily using Postman or the FastAPI Swagger UI.

## Project Structure

```text
sales_api_app/
|-- main.py              # FastAPI application and API routes
|-- data_generator.py    # Random sales transaction generator
|-- event_streamer.py    # Streaming logic for Event Hub and Cosmos DB
|-- cosmos_db.py         # Cosmos DB connection and insert logic
|-- requirements.txt     # Python package dependencies
`-- commands.txt         # Optional command notes
```

## Prerequisites

Before running the project, make sure you have:

- Python 3.10 or later installed.
- An Azure Cosmos DB account.
- An Azure Event Hub namespace with Kafka enabled.
- A valid Event Hub connection string.
- Postman, if you want to test the endpoints manually.

## Install Dependencies

Open a terminal inside the project folder:

```powershell
cd "E:\projects\BD IA3\sales_api_app"
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\activate
```

Install the required packages:

```powershell
pip install -r requirements.txt
```

This project also uses `confluent_kafka` in `event_streamer.py`, so install it if it is not already installed:

```powershell
pip install confluent-kafka
```

## Azure Configuration

The project uses Azure Cosmos DB and Azure Event Hub credentials in:

- `cosmos_db.py`
- `event_streamer.py`

Update these values before running the streaming endpoint:

```python
COSMOS_URI = "your-cosmos-db-uri"
COSMOS_KEY = "your-cosmos-db-key"
DATABASE_NAME = "SalesDatabase"
CONTAINER_NAME = "Transactions"
```

For Event Hub Kafka streaming, update:

```python
BOOTSTRAP_SERVERS = "your-eventhub-namespace.servicebus.windows.net:9093"
SASL_USERNAME = "$ConnectionString"
SASL_PASSWORD = "your-eventhub-connection-string"
TOPIC_NAME = "your-eventhub-name"
```

Important: do not commit real Azure keys or connection strings to GitHub. Use environment variables or a `.env` file for production or shared repositories.

## Run The FastAPI Server

Start the API server with Uvicorn:

```powershell
uvicorn main:app --reload
```

If the server starts successfully, you should see output showing that Uvicorn is running on:

```text
http://127.0.0.1:8000
```

You can also open the FastAPI Swagger documentation in your browser:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Home Endpoint

```http
GET http://127.0.0.1:8000/
```

Returns a welcome message.

Example response:

```json
{
  "message": "Welcome to the Azure Sales Data Generator API!"
}
```

### Generate Sales Data

```http
GET http://127.0.0.1:8000/generate_sales_data?records=5
```

Generates random sales records without sending them to Azure.

Example response:

```json
[
  {
    "id": "1730342455123",
    "customer_name": "Alice",
    "amount": 2450.75,
    "location": "New York",
    "timestamp": "2025-10-31 10:30:55"
  }
]
```

### Start Streaming Data To Azure

Use this endpoint in Postman to start automatic streaming:

```http
POST http://127.0.0.1:8000/start_stream
```

No request body is required.

Example response:

```json
{
  "message": "Automatic data streaming to Event Hub and Cosmos DB started."
}
```

After this endpoint is called, the application starts generating one sales transaction every 2 seconds. Each transaction is inserted into Cosmos DB and sent to Azure Event Hub.

### Stop Streaming Data

Use this endpoint to stop the automatic streaming loop:

```http
POST http://127.0.0.1:8000/stop_stream
```

No request body is required.

Example response:

```json
{
  "message": "Automatic data streaming stopped."
}
```

## Testing With Postman

1. Start the server:

   ```powershell
   uvicorn main:app --reload
   ```

2. Open Postman.

3. To check that the API is running, send:

   ```http
   GET http://127.0.0.1:8000/
   ```

4. To generate sample data only, send:

   ```http
   GET http://127.0.0.1:8000/generate_sales_data?records=5
   ```

5. To start streaming data into Azure, send:

   ```http
   POST http://127.0.0.1:8000/start_stream
   ```

6. Watch the terminal logs to confirm that records are being inserted into Cosmos DB and delivered to Event Hub.

7. To stop streaming, send:

   ```http
   POST http://127.0.0.1:8000/stop_stream
   ```

## How The Application Works

When the FastAPI app starts, `main.py` calls `init_db()` from `cosmos_db.py`. This prepares the Cosmos DB database and container if they do not already exist.

The `/generate_sales_data` endpoint calls `generate_sales_data()` from `data_generator.py`. This returns random transaction data but does not save it to Azure.

The `/start_stream` endpoint starts the async streaming loop from `event_streamer.py`. The loop keeps running until `/stop_stream` is called. During each loop cycle, the app creates a transaction, saves it to Cosmos DB, sends it to Azure Event Hub, and then waits 2 seconds before generating the next transaction.

## Troubleshooting

### ModuleNotFoundError: No module named 'confluent_kafka'

Install the missing package:

```powershell
pip install confluent-kafka
```

### Server is not starting

Make sure you are inside the project folder and the virtual environment is activated:

```powershell
.venv\Scripts\activate
uvicorn main:app --reload
```

### Postman returns Method Not Allowed

The streaming endpoints use `POST`, not `GET`.

Use:

```http
POST http://127.0.0.1:8000/start_stream
POST http://127.0.0.1:8000/stop_stream
```

### Data is not appearing in Azure

Check the following:

- Cosmos DB URI and key are correct.
- Event Hub connection string is correct.
- Event Hub name matches `TOPIC_NAME`.
- Event Hub has Kafka enabled.
- Your network allows outbound connections to Azure.
- The terminal logs do not show authentication or delivery errors.

## Security Note

This project should not expose Azure credentials publicly. Before pushing to GitHub, remove hardcoded secrets and load them from environment variables instead.
