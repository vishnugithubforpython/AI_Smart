from rag.splitter import split_text
from rag.embedder import create_embeddings
from db.chunk_crud import save_chunks
from rag.vectorstore import (
    create_vectorstore,
    load_index,
    save_index,
    load_metadata,
    save_metadata,
)

import numpy as np


def ingest_document(document_id, text, source):
    """
    Incrementally ingest extracted text into the vector store.

    Parameters
    ----------
    text : str
        Extracted text from any document.
    source : str
        Original document path or filename.
    """

    # -----------------------------
    # Step 1 : Split into chunks
    # -----------------------------
    chunks = split_text(text)

    save_chunks(document_id, chunks)

    if not chunks:
        print("No text found.")
        return

    # -----------------------------
    # Step 2 : Prepare Metadata
    # -----------------------------
    texts = []
    new_metadata = []

    for chunk in chunks:

        texts.append(chunk)

        new_metadata.append(
            {
                "text": chunk,
                "source": source
            }
        )

    # -----------------------------
    # Step 3 : Create Embeddings
    # -----------------------------
    embeddings = create_embeddings(texts)

    embeddings = np.array(embeddings).astype("float32")

    # -----------------------------
    # Step 4 : Load Existing Index
    # -----------------------------
    index = load_index()

    if index is None:

        print("No existing FAISS index found.")
        print("Creating a new index...")

        index = create_vectorstore(embeddings)

    else:

        print("Existing FAISS index found.")
        print("Adding new embeddings...")

        index.add(embeddings)

    # -----------------------------
    # Step 5 : Save Index
    # -----------------------------
    save_index(index)

    # -----------------------------
    # Step 6 : Update Metadata
    # -----------------------------
    metadata = load_metadata()

    metadata.extend(new_metadata)

    save_metadata(metadata)

    # -----------------------------
    # Step 7 : Success Message
    # -----------------------------
    print("\n====================================")
    print("Document Indexed Successfully")
    print(f"Source        : {source}")
    print(f"Chunks Added  : {len(chunks)}")
    print("====================================")