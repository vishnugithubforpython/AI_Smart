from web.search import search_web
from web.fetch import fetch_webpage
from web.extractor import extract_text
from web.reranker import rerank_web
from web.context_builder import build_context
from web_answer import web_answer


def web_pipeline(query):

    # Step 1: Search Google
    search_results = search_web(query)

    documents = []

    # Step 2: Fetch & Extract
    for result in search_results:

        html = fetch_webpage(result["url"])

        if html:
            text = extract_text(html)
        else:
            text = ""

        # Step 3: Fallback to snippet
        if not text:
            text = result["snippet"]

        documents.append({
            "title": result["title"],
            "url": result["url"],
            "text": text
        })

    # Step 4: Re-rank webpages
    documents = rerank_web(
        query,
        documents
    )

    # Step 5: Build context
    context = build_context(
        documents
    )

    # Step 6: Generate answer
    answer = web_answer(
        query,
        context
    )

    return answer