from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
from bson import ObjectId
from prometheus_client import start_http_server, Summary
import time
import os

app = FastAPI()

MONGODB_URL = os.getenv('MONGODB_URL')
print(MONGODB_URL)

client = MongoClient(MONGODB_URL)
db = client.quotes_db
collection = db.quotes

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

class Quote(BaseModel):
    text: str
    author: str

class QuoteInDB(Quote):
    id: str

@REQUEST_TIME.time()
@app.get("/quotes", response_model=List[QuoteInDB])
def get_quotes():
    quotes = list(collection.find())
    return [QuoteInDB(id=str(quote["_id"]), text=quote["text"], author=quote["author"]) for quote in quotes]

@REQUEST_TIME.time()
@app.post("/quotes", response_model=QuoteInDB)
def create_quote(quote: Quote):
    result = collection.insert_one(quote.dict())
    if result.inserted_id:
        return QuoteInDB(id=str(result.inserted_id), **quote.dict())
    raise HTTPException(status_code=500, detail="Quote could not be created")

@REQUEST_TIME.time()
@app.get("/quotes/{quote_id}", response_model=QuoteInDB)
def get_quote(quote_id: str):
    quote = collection.find_one({"_id": ObjectId(quote_id)})
    if quote:
        return QuoteInDB(id=str(quote["_id"]), text=quote["text"], author=quote["author"])
    raise HTTPException(status_code=404, detail="Quote not found")

@REQUEST_TIME.time()
@app.put("/quotes/{quote_id}", response_model=QuoteInDB)
def update_quote(quote_id: str, quote: Quote):
    result = collection.update_one({"_id": ObjectId(quote_id)}, {"$set": quote.dict()})
    if result.modified_count == 1:
        return QuoteInDB(id=quote_id, **quote.dict())
    raise HTTPException(status_code=404, detail="Quote not found")

@REQUEST_TIME.time()
@app.delete("/quotes/{quote_id}")
def delete_quote(quote_id: str):
    result = collection.delete_one({"_id": ObjectId(quote_id)})
    if result.deleted_count == 1:
        return {"message": "Quote deleted"}
    raise HTTPException(status_code=404, detail="Quote not found")

if __name__ == "__main__":
    start_http_server(8001)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
