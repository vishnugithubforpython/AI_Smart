from rag.retriever import retrieve
from rag.qa import rag_answer
from rag.reranker import rerank
from web_pipeline import web_pipeline


import faiss
import pickle

from config import RERANK_THRESHOLD

# Load FAISS
index = faiss.read_index("resume_index.faiss")

# Load chunks
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


def process_query(query, chat_history):

    # Step 1: Retrieve Top-K chunks using FAISS
    results = retrieve(
        query,
        index,
        chunks
    )

    # Step 2: Re-rank the retrieved chunks
    results = rerank(
        query,
        results
    )

    # Step 3: Print for debugging
    print("\n========== Retrieved & Re-ranked ==========")

    for i, chunk in enumerate(results, start=1):
        print(f"\nRank {i}")
        print(f"Source        : {chunk['source']}")
        print(f"FAISS Distance: {chunk['score']:.4f}")
        print(f"Re-rank Score : {chunk['rerank_score']:.4f}")

    print("\n===========================================")

    # Current routing (temporary)
    best_distance = results[0]["score"]
    best_rerank = results[0]["rerank_score"]

    print(f"\nBest FAISS Distance : {best_distance:.4f}")
    print(f"Best Re-rank Score  : {best_rerank:.4f}")

    if best_rerank > RERANK_THRESHOLD:
        

        context = "\n".join(
            [item["text"] for item in results]
        )

        answer = rag_answer(
            query,
            context,
            chat_history
        )
        return answer, results
    

    else:

        answer = web_pipeline(query)

    return answer,[]