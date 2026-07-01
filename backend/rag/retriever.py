from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve(query, index, chunks, k=2):

    query_embedding = model.encode([query])

    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, k)
    print("distances:",distances)
    print("infices:",indices)

    retrieved_chunks = [chunks[i] for i in indices[0]]

    return retrieved_chunks 
    