import faiss
import pickle

index = faiss.read_index("resume_index.faiss")

with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

print("Total vectors:", index.ntotal)

print("\nFirst chunk:")
print(chunks[0][:200])