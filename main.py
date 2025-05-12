from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from typing import List
from src.Controllers import messagesController
from src.Controllers import documentsController
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

#test api
@app.get("/")
async def root():
    return {"message": "Hello World"}
#test api
@app.get("/document")
async def get_document():
    return "hello world"

#send document to the chatbot (one at a time if use raptor for mor efficiently)
@app.post("/document")
async def get_document(request:ListDocuments):
    try:
        result = documentsController.get_documents(request.documents)
    except Exception as e:
        return {"e" : str(e)}
    return "upload successfully"

@app.post("/message")

#send message to the chatbot and then receive message back from chatbot
async def get_message(request: Message):
    try:
        result = messagesController.receive_messages(request.message)
    except Exception as e:
        return {"error": str(e)}
    return result