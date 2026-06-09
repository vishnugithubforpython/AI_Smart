from rag.loader import load_pdf
from rag.splitter import split_text
from rag.embedder import create_embeddings
from rag.vectorstore import create_vectorstore
from rag.retriever import retrieve

pdf_text = load_pdf("../sample_data/Vishnu-Resume...pdf")

chunks = split_text(pdf_text)

embeddings = create_embeddings(chunks) 

index = create_vectorstore(embeddings)


query = "What cloud technologies does Vishnu know?"

results = retrieve(
    query,
    index,
    chunks
)

for i, result in enumerate(results):
    print(f"\nResult {i+1}:")
    print(result)
