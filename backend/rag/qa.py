from google import genai

client = genai.Client(api_key="AIzaSyD1pD6mTJeGBp5fyintN23votSzrjDwCbA")


def generate_answer(query, context):

    prompt = f"""
    Answer the question using only the context below.

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