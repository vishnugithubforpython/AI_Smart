from sentence_transformers import CrossEncoder

# Load Cross Encoder model
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(query, retrieved_chunks, top_k=3):

    pairs = []

    for chunk in retrieved_chunks:
        pairs.append((query, chunk["text"]))

    # Cross Encoder Scores
    scores = reranker.predict(pairs)

    # Add rerank score
    for chunk, score in zip(retrieved_chunks, scores):
        chunk["rerank_score"] = float(score)

    # -----------------------------
    # Fill Missing Scores
    # -----------------------------
    for chunk in retrieved_chunks:

        if "score" not in chunk:
            chunk["score"] = None

        if "bm25_score" not in chunk:
            chunk["bm25_score"] = None

    # Sort
    reranked_chunks = sorted(
        retrieved_chunks,
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked_chunks[:top_k]