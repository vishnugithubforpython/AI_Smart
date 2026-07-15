from query_rewriter.prompts import QUERY_REWRITE_PROMPT
from gemini_client import client
from config import GEMINI_MODEL


def rewrite_query(query: str, chat_history):

    # ----------------------------------------
    # Build Recent Conversation History
    # ----------------------------------------

    history = ""

    recent_history = chat_history[-5:]

    for chat in recent_history:

        history += f"""
User: {chat['user']}
Assistant: {chat['assistant']}
"""

    # ----------------------------------------
    # Build Prompt
    # ----------------------------------------

    prompt = f"""
{QUERY_REWRITE_PROMPT}

Conversation History:

{history}

Current User Question:

{query}
"""

    # ----------------------------------------
    # Gemini Rewrite
    # ----------------------------------------

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    rewritten_query = response.text.strip()

    # ----------------------------------------
    # Debug
    # ----------------------------------------

    print("\n========== QUERY REWRITER ==========")
    print(f"Original Query  : {query}")
    print(f"Rewritten Query : {rewritten_query}")
    print("====================================\n")

    return rewritten_query