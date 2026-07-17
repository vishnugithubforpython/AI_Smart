from rag.qa import rag_answer
from rag.reranker import rerank
from query_rewriter.rewrite import rewrite_query
from rag.vectorstore import load_index

from db.chunk_crud import get_chunks_by_user

from hybrid_search.hybrid import hybrid_search

from decision_engine.ai_router import decide_route
from decision_engine.routes import WEB, GENERAL

from web_pipeline import web_pipeline

from config import RERANK_THRESHOLD


def process_query(query, chat_history, user_id):

    # ==================================================
    # Query Rewriter
    # ==================================================

    query = rewrite_query(
        query,
        chat_history
    )

    # ==================================================
    # DOCUMENT SEARCH
    # ==================================================

    print("\n========== DOCUMENT SEARCH ==========\n")

    index = load_index()

    print("Loading chunks from PostgreSQL...")

    chunks = get_chunks_by_user(user_id)

    print("Total chunks:", len(chunks))

    # No documents uploaded
    if not chunks:

        print("No documents found for this user.")

        route = decide_route(query)

        if route == WEB:
            answer = web_pipeline(query)
            return answer, []

        return "You haven't uploaded any documents yet.", []

    # ==================================================
    # Hybrid Search
    # ==================================================

    results = hybrid_search(
        query,
        index,
        chunks
    )

    results = rerank(
        query,
        results
    )

    # No search results
    if not results:

        print("No relevant chunks found.")

        route = decide_route(query)

        if route == WEB:
            answer = web_pipeline(query)
            return answer, []

        return "No relevant information found in your uploaded documents.", []

    print("\n========== Retrieved & Re-ranked ==========")

    for i, chunk in enumerate(results, start=1):

        faiss_score = (
            f"{chunk['score']:.4f}"
            if chunk["score"] is not None
            else "N/A"
        )

        bm25_score = (
            f"{chunk['bm25_score']:.4f}"
            if chunk["bm25_score"] is not None
            else "N/A"
        )

        print(f"\nRank {i}")
        print(f"Source        : {chunk['source']}")
        print(f"FAISS Score   : {faiss_score}")
        print(f"BM25 Score    : {bm25_score}")
        print(f"Re-rank Score : {chunk['rerank_score']:.4f}")

    print("\n===========================================")

    best_rerank = results[0]["rerank_score"]

    print(f"\nBest Re-rank Score : {best_rerank:.4f}")

    # ==================================================
    # DOCUMENT PIPELINE
    # ==================================================

    if best_rerank > RERANK_THRESHOLD:

        print("\n========== DOCUMENT PIPELINE ==========\n")

        context = "\n".join(
            item["text"]
            for item in results
        )

        answer = rag_answer(
            query,
            context,
            chat_history
        )

        return answer, results

    # ==================================================
    # AI ROUTER
    # ==================================================

    print("\nNo relevant document found.")
    print("Routing to AI Router...\n")

    route = decide_route(query)

    print("\n========== AI ROUTER ==========")
    print(f"Selected Route : {route}")
    print("===============================\n")

    # ==================================================
    # WEB PIPELINE
    # ==================================================

    if route == WEB:

        print("\n========== WEB PIPELINE ==========\n")

        answer = web_pipeline(query)

        return answer, []

    # ==================================================
    # GENERAL PIPELINE
    # ==================================================

    print("\n========== GENERAL PIPELINE ==========\n")

    answer = "GENERAL PIPELINE COMING SOON."

    return answer, []