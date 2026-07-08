from sentence_transformers import CrossEncoder

# Load Cross Encoder model
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(query, retrieved_chunks, top_k=3):

    pairs = []

    for chunk in retrieved_chunks:
        pairs.append((query, chunk["text"]))

    scores = reranker.predict(pairs)

    for chunk, score in zip(retrieved_chunks, scores):
        chunk["rerank_score"] = float(score)

    reranked_chunks = sorted(
        retrieved_chunks,
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked_chunks[:top_k]