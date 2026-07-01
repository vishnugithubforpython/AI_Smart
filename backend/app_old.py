from rag.loader import load_pdf
from rag.splitter import split_text
from rag.embedder import create_embeddings
from rag.vectorstore import create_vectorstore
from rag.retriever import retrieve
from rag.qa import generate_answer
import faiss

import glob

chat_history=[]

# Automatically find the PDF inside sample_data
pdf_files = glob.glob("../sample_data/*.pdf")

# Check if a PDF exists
if not pdf_files:
    raise FileNotFoundError("No PDF found in sample_data folder.")

# Use the first PDF found
pdf_path = pdf_files[0]

print(f"Using PDF: {pdf_path}")

# Load PDF
pdf_text = load_pdf(pdf_path)

# Split into chunks
chunks = split_text(pdf_text)

# Create embeddings
embeddings = create_embeddings(chunks)

# Create vector store
index = create_vectorstore(embeddings)


#saving faiss 
faiss.write_index(index, "resume_index.faiss")

print("FAISS index saved!")

#saving chunk of the pdf
import pickle
with open("chunks.pkl","wb")as f:
    pickle.dump(chunks,f)
print("chunks saved")


while True:

    query = input("\nYou: ")

    if query.lower() == "exit":
        print("Goodbye!")
        break

    # Retrieve relevant chunks
    results = retrieve(
        query,
        index,
        chunks
    )

    # Create context
    context = "\n".join(results)

    # Generate answer
    answer = generate_answer(
        query,
        context,
        chat_history
    )

    print("\nAssistant:")
    print(answer)

    # Save conversation
    chat_history.append({
        "user": query,
        "assistant": answer
    })