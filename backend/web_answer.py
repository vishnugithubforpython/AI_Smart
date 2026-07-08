from gemini_client import client


def web_answer(query, context):

    prompt = f"""
You are an intelligent AI assistant.

Answer the user's question using ONLY the web context below.

If the answer is not present in the context,
say:

"I could not find enough information."

Web Context:

{context}

Question:
{query}

Provide a clear and accurate answer.

At the end, mention the sources.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text