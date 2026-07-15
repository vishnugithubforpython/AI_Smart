import re
from rank_bm25 import BM25Okapi


def bm25_search(query, metadata, top_k=10):
    """
    Perform BM25 keyword search over document chunks.
    """

    # ----------------------------------------
    # Build Corpus
    # ----------------------------------------

    corpus = []

    for chunk in metadata:

        tokens = re.findall(
            r"\w+",
            chunk["text"].lower()
        )

        corpus.append(tokens)

    # ----------------------------------------
    # Build BM25 Index
    # ----------------------------------------

    bm25 = BM25Okapi(corpus)

    # ----------------------------------------
    # Tokenize Query
    # ----------------------------------------

    query_tokens = re.findall(
        r"\w+",
        query.lower()
    )

    # ----------------------------------------
    # Compute Scores
    # ----------------------------------------

    scores = bm25.get_scores(query_tokens)

    # ----------------------------------------
    # Sort by Score
    # ----------------------------------------

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:top_k]

    # ----------------------------------------
    # Collect Results
    # ----------------------------------------

    results = []

    for idx in ranked_indices:

        results.append({

            "text": metadata[idx]["text"],

            "source": metadata[idx]["source"],

            "score": None,

            "bm25_score": float(scores[idx])

        })

    return results