from sentence_transformers import CrossEncoder

# Load CrossEncoder once
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_web(query, documents, top_k=3):

    if not documents:
        return []

    pairs = []

    for doc in documents:
        pairs.append(
            (query, doc["text"])
        )

    scores = reranker.predict(pairs)

    for doc, score in zip(documents, scores):
        doc["rerank_score"] = float(score)

    reranked_docs = sorted(
        documents,
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked_docs[:top_k]