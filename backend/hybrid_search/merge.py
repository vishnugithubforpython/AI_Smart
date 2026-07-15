def merge_results(faiss_results, bm25_results):
    """
    Merge FAISS and BM25 results while removing duplicates.
    """

    merged = {}

    # ----------------------------------
    # Add FAISS Results
    # ----------------------------------
    for chunk in faiss_results:

        key = (chunk["source"], chunk["text"])

        merged[key] = {
            "text": chunk["text"],
            "source": chunk["source"],
            "score": chunk.get("score"),
            "bm25_score": None
        }

    # ----------------------------------
    # Add BM25 Results
    # ----------------------------------
    for chunk in bm25_results:

        key = (chunk["source"], chunk["text"])

        if key in merged:

            # Same chunk found by both searches
            merged[key]["bm25_score"] = chunk.get("bm25_score")

        else:

            # Found only by BM25
            merged[key] = {
                "text": chunk["text"],
                "source": chunk["source"],
                "score": None,
                "bm25_score": chunk.get("bm25_score")
            }

    return list(merged.values())