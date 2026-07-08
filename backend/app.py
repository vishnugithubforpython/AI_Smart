from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import QuestionRequest
from router import process_query

app = FastAPI()

chat_history = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():

    return {
        "message": "Welcome to AI Smart!"
    }


@app.post("/ask")
def ask(request: QuestionRequest):

    query = request.question

    answer, sources = process_query(
        query,
        chat_history
    )

    chat_history.append({
        "user": query,
        "assistant": answer
    })

    return {
        "answer": answer,
        "sources": sources
    }