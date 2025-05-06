from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from chatbot.chain import get_response 

app = FastAPI()

# CORS (so frontend like React can access it)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or list your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input schema
class ChatRequest(BaseModel):
    question: str

# Output route
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    response = get_response(request.question)
    return {"response": response}
