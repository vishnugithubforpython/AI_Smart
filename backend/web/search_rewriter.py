from gemini_client import client
from config import GEMINI_MODEL


def rewrite_search_query(query: str) -> str:
    """
    Rewrite the user's query into a better Google search query.
    """

    prompt = f"""
You are an expert Google Search Query Optimizer.

Your job is to rewrite the user's query into the BEST search engine query.

Rules:
- Keep the original intent.
- Expand ambiguous queries.
- Add important keywords if needed.
- Remove unnecessary words.
- Make it suitable for Google Search.
- Do NOT answer the question.
- Return ONLY the rewritten search query.

Examples:

User:
who is cm tamil nadu

Search Query:
Chief Minister of Tamil Nadu 2026 official government

-----------------------

User:
tell about fifa latest match

Search Query:
latest FIFA World Cup 2026 match results

-----------------------

User:
how he become cm

Search Query:
How did C. Joseph Vijay become Chief Minister of Tamil Nadu 2026

-----------------------

User Query:
{query}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text.strip()