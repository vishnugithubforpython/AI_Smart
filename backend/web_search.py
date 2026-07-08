import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")




def web_search(query):

    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    results = response.json()
    
    search_results = []
    
    for item in results.get("organic", [])[:5]:
        search_results.append({
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "link": item.get("link")
        })

    return search_results

    
