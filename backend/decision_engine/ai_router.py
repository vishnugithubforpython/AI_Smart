from decision_engine.prompts import ROUTER_PROMPT
from decision_engine.routes import DOCUMENT, WEB, GENERAL

from gemini_client import client
from config import GEMINI_MODEL


VALID_ROUTES = {
    DOCUMENT,
    WEB,
    GENERAL
}


def decide_route(query: str):

    prompt = f"""
{ROUTER_PROMPT}

User Question:
{query}

Respond with ONLY ONE WORD:

DOCUMENT
WEB
GENERAL
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    route = response.text.strip().upper()

    print("\n========== AI ROUTER RAW ==========")
    print(route)
    print("===================================\n")

    if route not in VALID_ROUTES:
        route = GENERAL

    return route