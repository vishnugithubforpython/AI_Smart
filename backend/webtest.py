from web.search import search_web
from web.fetch import fetch_webpage
from web.extractor import extract_text
from web.context_builder import build_context
from web_answer import web_answer
from web.reranker import rerank_web

query = input("Query: ")

# Search
results = search_web(query)

documents = []

# Build documents
for result in results:

    html = fetch_webpage(result["url"])

    if html:
        text = extract_text(html)
    else:
        text = ""

    # Fallback to snippet
    if not text:
        text = result["snippet"]

    documents.append({
        "title": result["title"],
        "url": result["url"],
        "text": text
    })

# Build one context
context = build_context(documents)

documents = rerank_web(
    query,
    documents
)

context = build_context(documents)

# Ask Gemini
answer = web_answer(
    query,
    context
)

print("\n========== WEB ANSWER ==========\n")
print(answer)