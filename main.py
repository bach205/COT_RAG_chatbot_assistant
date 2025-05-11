from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.model.retrieval import indexing
from src.model.graph import graph 
from typing import List
import asyncio
from dotenv import load_dotenv


load_dotenv()

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

@app.get("/document")
async def get_document():
    return "hello world"

@app.post("/document")
async def get_document(request:ListDocuments):
    try:
        asyncio.create_task(await indexing.add_documents(request.documents))
    except Exception as e:
        return {"error": str(e)}
    return "upload successfully"

@app.post("/message")
async def get_message(request: Message):
    try:
        a = graph.invoke({"question" : request.message})
    except Exception as e:
        return {"error": str(e)}
    return a