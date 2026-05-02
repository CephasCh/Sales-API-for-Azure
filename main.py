from fastapi import FastAPI
from data_generator import generate_sales_data
from event_streamer import start_streaming, stop_streaming
from cosmos_db import init_db
import asyncio

app = FastAPI(title="Sales Data API with Azure Integration", version="3.0")

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
def home():
    return {"message": "Welcome to the Azure Sales Data Generator API!"}

@app.get("/generate_sales_data")
def get_sales_data(records: int = 1):
    return [generate_sales_data() for _ in range(records)]

@app.post("/start_stream")
async def start_stream():
    asyncio.create_task(start_streaming())
    return {"message": "Automatic data streaming to Event Hub and Cosmos DB started."}

@app.post("/stop_stream")
def stop_stream():
    stop_streaming()
    return {"message": "Automatic data streaming stopped."}
