from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import indexing
from typing import List
import asyncio

class Message(BaseModel):
    message: str

class ListDocuments(BaseModel):
    documents: list[str]

app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/")
async def request_message(msg: Message):
    return {msg.message}

@app.get("/document")
async def get_document():
    return "hello world"

@app.post("/document")
async def get_document(request:ListDocuments):
    asyncio.create_task(indexing.add_documents(request.documents))
    return "upload successfully"