from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from upload import router as upload_router
from auth.routes import router as auth_router

from models import QuestionRequest
from router import process_query

from fastapi import Depends
from auth.dependencies import get_current_user

app = FastAPI()

chat_history = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Smart!"
    }
@app.get("/profile")
def profile(current_user=Depends(get_current_user)):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }

@app.post("/ask")
def ask(request: QuestionRequest,
current_user = Depends(get_current_user)
):

    query = request.question

    print("\n========== CHAT HISTORY ==========")
    print(chat_history)
    print("==================================\n")
    

    answer, sources = process_query(
        query,
        chat_history,
        current_user.id
    )

    chat_history.append({
        "user": query,
        "assistant": answer
    })

    return {
        "answer": answer,
        "sources": sources
    }