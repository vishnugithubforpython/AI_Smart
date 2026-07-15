from web.search import search_web
from web.fetch import fetch_webpage
from web.extractor import extract_text
from web.reranker import rerank_web
from web.context_builder import build_context
from web_answer import web_answer


def web_pipeline(query):

    # -----------------------------
    # Step 1: Search Google
    # -----------------------------
    search_results = search_web(query)

    if not search_results:
        return "I could not find relevant web results."

    documents = []

    # -----------------------------
    # Step 2: Fetch & Extract
    # -----------------------------
    for result in search_results:

        html = fetch_webpage(result["url"])

        extracted_text = ""

        if html:
            extracted_text = extract_text(html)

        snippet = result.get("snippet", "")

        # -----------------------------
        # Combine snippet + extracted text
        # -----------------------------
        if extracted_text:

            text = f"""
Snippet:
{snippet}

Content:
{extracted_text}
"""

        else:

            text = snippet

        documents.append({
            "title": result["title"],
            "url": result["url"],
            "text": text
        })

    # -----------------------------
    # Step 3: Re-rank webpages
    # -----------------------------
    documents = rerank_web(
        query,
        documents
    )

    # -----------------------------
    # Step 4: Build context
    # -----------------------------
    context = build_context(documents)

    # -----------------------------
    # Step 5: Generate Answer
    # -----------------------------
    answer = web_answer(
        query,
        context
    )

    # -----------------------------
    # Debug
    # -----------------------------
    print("\n========== WEB CONTEXT ==========")
    print(context)
    print("=================================\n")

    print("\n========== WEB ANSWER ==========")
    print(answer)
    print("=================================\n")

    return answer