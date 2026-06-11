import streamlit as st
import tempfile
import sys
import os

# Add backend folder to Python path
sys.path.append("../backend")

from rag.loader import load_pdf
from rag.splitter import split_text
from rag.embedder import create_embeddings
from rag.vectorstore import create_vectorstore
from rag.retriever import retrieve
from rag.qa import generate_answer


st.set_page_config(page_title="Chat with PDF")

st.title("📄 Chat with PDF")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

query = st.text_input(
    "Ask a question about the PDF"
)

if st.button("Get Answer"):

    if uploaded_file is None:
        st.warning("Please upload a PDF.")

    elif not query:
        st.warning("Please enter a question.")

    else:

        with st.spinner("Processing PDF..."):

            # Save uploaded PDF temporarily
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp_file:

                tmp_file.write(uploaded_file.read())
                pdf_path = tmp_file.name

            # RAG Pipeline
            pdf_text = load_pdf(pdf_path)

            chunks = split_text(pdf_text)

            embeddings = create_embeddings(chunks)

            index = create_vectorstore(embeddings)

            results = retrieve(
                query,
                index,
                chunks
            )

            context = "\n".join(results)

            answer = generate_answer(
                query,
                context
            )

        st.success("Answer Generated!")

        st.write("### Answer")
        st.write(answer)