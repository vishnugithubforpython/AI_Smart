from rag.retriever import retrieve
from hybrid_search.bm25 import bm25_search
from hybrid_search.merge import merge_results


def hybrid_search(query, index, metadata):

    print("\n========== HYBRID SEARCH ==========")

    # FAISS
    faiss_results = retrieve(
        query,
        index,
        metadata
    )

    print(f"FAISS Results : {len(faiss_results)}")

    # BM25
    bm25_results = bm25_search(
        query,
        metadata
    )

    print(f"BM25 Results  : {len(bm25_results)}")

    # Merge
    results = merge_results(
        faiss_results,
        bm25_results
    )

    print(f"Merged Results: {len(results)}")
    print("===================================\n")

    return results