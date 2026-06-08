from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(text):
    """
    Splits large text into smaller chunks
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=500
    )

    chunks = splitter.split_text(text)

    return chunks