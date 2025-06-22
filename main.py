from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict
from utils import chat_with_model
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Student Tutor Chatbot")

# In-memory chat sessions
chat_sessions: Dict[str, list] = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())

    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    chat_sessions[session_id].append({"role": "user", "content": req.message})

    response = await chat_with_model(chat_sessions[session_id])

    chat_sessions[session_id].append({"role": "assistant", "content": response})

    return {
        "session_id": session_id,
        "response": response
    }

@app.get("/")
def root():
    return {"message": "Student Chatbot API is running"}
