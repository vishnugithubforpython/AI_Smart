import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

SERPER_URL = "https://google.serper.dev/search"


def search_web(query, num_results=5):

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query
    }

    response = requests.post(
        SERPER_URL,
        headers=headers,
        json=payload
    )

    response.raise_for_status()

    data = response.json()

    search_results = []

    for item in data.get("organic", [])[:num_results]:

        search_results.append({
            "title": item.get("title"),
            "url": item.get("link"),
            "snippet": item.get("snippet", "")
        })

    return search_results