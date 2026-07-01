import faiss
import pickle

from rag.retriever import retrieve
from rag.qa import generate_answer

# Load FAISS
index = faiss.read_index("resume_index.faiss")

# Load chunks
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

chat_history = []

while True:

    query = input("\nYou: ")

    if query.lower() == "exit":
        print("Goodbye!")
        break

    # Retrieve
    results = retrieve(
        query,
        index,
        chunks,
        

    )

    context = "\n".join(
        [item["text"] for item in results]
    )

    # Gemini
    answer = generate_answer(
        query,
        context,
        chat_history
    )

    print("\nAssistant:")
    print(answer)

    # Save memory
    chat_history.append({
        "user": query,
        "assistant": answer,
        "sources": results
    })