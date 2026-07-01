from rag.loader import load_pdf
from rag.splitter import split_text
from rag.embedder import create_embeddings
from rag.vectorstore import create_vectorstore

import faiss
import pickle
import glob

# Automatically find PDF
pdf_files = glob.glob("../sample_data/*.pdf")

if not pdf_files:
    raise FileNotFoundError("No PDF found.")

all_chunks = []
text = []

for pdf_path in pdf_files:

    pdf_text = load_pdf(pdf_path)

    chunks = split_text(pdf_text)

    for chunk in chunks:

        text.append(chunk)

        all_chunks.append({
            "text": chunk,
            "source": pdf_path
        })




print(f"Total Chunks: {len(all_chunks)}")

# Create embeddings
embeddings = create_embeddings(text)

# Create FAISS
index = create_vectorstore(embeddings)

# Save FAISS
faiss.write_index(index, "resume_index.faiss")

# Save chunks
with open("chunks.pkl", "wb") as f:
    pickle.dump(all_chunks, f)

print("Ingestion Completed Successfully!")