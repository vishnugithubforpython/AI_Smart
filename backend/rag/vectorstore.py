import faiss
import numpy as np
import os
import pickle

INDEX_PATH = "vector_index.faiss"
CHUNKS_PATH = "metadata.pkl"


def create_vectorstore(embeddings):
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index


def load_index():
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    return None


def save_index(index):
    faiss.write_index(index, INDEX_PATH)


def load_metadata():
    if os.path.exists(CHUNKS_PATH):
        with open(CHUNKS_PATH, "rb") as f:
            return pickle.load(f)
    return []


def save_metadata(metadata):
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(metadata, f)