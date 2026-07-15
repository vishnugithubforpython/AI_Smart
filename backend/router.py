from rag.qa import rag_answer
from rag.reranker import rerank
from query_rewriter.rewrite import rewrite_query
from rag.vectorstore import load_index, load_metadata

from hybrid_search.hybrid import hybrid_search

from decision_engine.ai_router import decide_route
from decision_engine.routes import DOCUMENT, WEB, GENERAL

from web_pipeline import web_pipeline

from config import RERANK_THRESHOLD


def process_query(query, chat_history):

    # ==================================================
    # Query Rewriter
    # ==================================================

    query = rewrite_query(
        query,
        chat_history
    )

    # ==================================================
    # AI Router (FIRST)
    # ==================================================

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

    if route == GENERAL:

        print("\n========== GENERAL PIPELINE ==========\n")

        answer = "GENERAL PIPELINE COMING SOON."

        return answer, []

    # ==================================================
    # DOCUMENT PIPELINE
    # ==================================================

    print("\n========== DOCUMENT SEARCH ==========\n")

    index = load_index()
    chunks = load_metadata()

    results = hybrid_search(
        query,
        index,
        chunks
    )

    results = rerank(
        query,
        results
    )

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

    print("\nNo relevant documents found.\n")

    answer = "I could not find relevant information in your uploaded documents."

    return answer, []