from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query, index, chunks, k=10):

    query_embedding = model.encode([query])

    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, k)

    print("Distances:", distances)
    print("Indices:", indices)

    retrieved_chunks = []

    for distance, idx in zip(distances[0], indices[0]):
        retrieved_chunks.append({
            "text": chunks[idx]["text"],
            "source": chunks[idx]["source"],
            "score": float(distance)
        })
   

    return retrieved_chunks