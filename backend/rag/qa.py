import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

def generate_answer(query, context, history):

    history_text = ""

    for chat in history:
        history_text += f"""
User: {chat['user']}
Assistant: {chat['assistant']}
"""

    prompt = f"""
You are a helpful AI assistant.

Use the conversation history and the document context to answer.

If the answer is not found in the context,
say:
"I could not find the answer in the provided document."

Conversation History:
{history_text}

Document Context:
{context}

Current Question:
{query}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text