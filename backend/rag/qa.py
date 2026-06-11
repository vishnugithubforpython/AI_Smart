import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

def generate_answer(query, context):

    prompt = f"""
    Answer the question using ONLY the context below.

    If the answer is not found in the context,
    say "I could not find the answer in the provided document."

    Context:
    {context}

    Question:
    {query}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text