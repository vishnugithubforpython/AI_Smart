import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

SEARCH_URL = "https://google.serper.dev/search"
NEWS_URL = "https://google.serper.dev/news"


def is_news_query(query: str):
    """
    Detect whether the query is asking about recent events.
    """

    keywords = [
        "today",
        "yesterday",
        "latest",
        "recent",
        "breaking",
        "news",
        "match",
        "score",
        "won",
        "winner",
        "election",
        "stock",
        "weather",
        "earthquake"
    ]

    query = query.lower()

    return any(keyword in query for keyword in keywords)


def search_web(query, num_results=5):
    """
    Search Google or Google News using Serper API.
    """

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query,
        "num": num_results
    }

    # ---------------------------------------
    # Decide Search Type
    # ---------------------------------------

    use_news = is_news_query(query)

    if use_news:
        url = NEWS_URL
        print("\nUsing Google News Search")
    else:
        url = SEARCH_URL
        print("\nUsing Google Search")

    # ---------------------------------------
    # API Call
    # ---------------------------------------

    try:

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

    except Exception as e:

        print("\n========== SERPER ERROR ==========")
        print(e)
        print("==================================\n")

        return []

    # ---------------------------------------
    # Select Correct Results
    # ---------------------------------------

    if use_news:
        items = data.get("news", [])
    else:
        items = data.get("organic", [])

    # ---------------------------------------
    # Remove Unwanted Websites
    # ---------------------------------------

    blocked_domains = [
        "instagram.com",
        "facebook.com",
        "tiktok.com",
        "pinterest.com"
    ]

    search_results = []

    for item in items:

        link = item.get("link", "")

        if any(domain in link for domain in blocked_domains):
            continue

        search_results.append({
            "title": item.get("title", ""),
            "url": link,
            "snippet": item.get("snippet", "")
        })

        if len(search_results) >= num_results:
            break

    # ---------------------------------------
    # Debug
    # ---------------------------------------

    print("\n========== GOOGLE SEARCH ==========")

    for i, result in enumerate(search_results, start=1):

        print(f"\nResult {i}")
        print("Title   :", result["title"])
        print("URL     :", result["url"])
        print("Snippet :", result["snippet"])

    print("\n===================================\n")

    return search_results