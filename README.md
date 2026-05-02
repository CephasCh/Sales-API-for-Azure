# Sales Data API for Postman Agent and Azure Streaming

This project is a local FastAPI service that is designed to be triggered from the Postman Agent application. The API runs on `127.0.0.1:8000`, and Postman sends requests to it to generate sales data or start streaming sales transactions into Azure services.

When the `/start_stream` endpoint is called from Postman, the application continuously creates random sales transactions, stores them in Azure Cosmos DB, and sends them to Azure Event Hub using the Kafka protocol.

## Features

- Generate random sales transactions with customer name, amount, location, and timestamp.
- Expose local REST API endpoints using FastAPI.
- Work with Postman Agent for local endpoint testing and execution.
- Start and stop automatic Azure data streaming from Postman requests.
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
- Postman Desktop Agent or Postman Agent application installed and running.
- An Azure Cosmos DB account.
- An Azure Event Hub namespace with Kafka enabled.
- A valid Event Hub connection string.
- Postman configured to call the local API endpoints.

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



## Running With Postman Agent

1. Start the server:

   ```powershell
   uvicorn main:app --reload
   ```

2. Open the Postman Agent application and make sure it is running.

3. In Postman, create a request to check that the local API is running:

   ```http
   GET http://127.0.0.1:8000/
   ```

4. To generate sample data only, send:

   ```http
   GET http://127.0.0.1:8000/generate_sales_data?records=5
   ```
<img width="1077" height="394" alt="image" src="https://github.com/user-attachments/assets/997eba55-4cf6-4ee5-aaab-385fce43119c" />


5. To start streaming data into Azure, send this request through Postman Agent:

   ```http
   POST http://127.0.0.1:8000/start_stream
   ```
<img width="1071" height="326" alt="image" src="https://github.com/user-attachments/assets/3dfedb8e-9086-4e53-8410-1062f3b35309" />

6. Keep the FastAPI terminal open. Watch the logs to confirm that records are being inserted into Cosmos DB and delivered to Event Hub.

7. To stop streaming, send this request through Postman Agent:

   ```http
   POST http://127.0.0.1:8000/stop_stream
   ```
<img width="1068" height="403" alt="image" src="https://github.com/user-attachments/assets/702c916e-7616-4d97-8036-148fab88990d" />

## How The Application Works

When the local FastAPI app starts, `main.py` calls `init_db()` from `cosmos_db.py`. This prepares the Cosmos DB database and container if they do not already exist.

The `/generate_sales_data` endpoint calls `generate_sales_data()` from `data_generator.py`. This returns random transaction data but does not save it to Azure.

The `/start_stream` endpoint is called from Postman Agent. It starts the async streaming loop from `event_streamer.py`. The loop keeps running until `/stop_stream` is called. During each loop cycle, the app creates a transaction, saves it to Cosmos DB, sends it to Azure Event Hub, and then waits 2 seconds before generating the next transaction.

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

### Postman cannot connect to 127.0.0.1

Check the following:

- The FastAPI server is running.
- The URL is exactly `http://127.0.0.1:8000`.
- Postman Agent is running.
- You are using `POST` for `/start_stream` and `/stop_stream`.

## Security Note

This project should not expose Azure credentials publicly. Before pushing to GitHub, remove hardcoded secrets and load them from environment variables instead.
