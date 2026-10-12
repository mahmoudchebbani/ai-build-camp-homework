import requests

HEADERS = {"User-Agent": "ai-engineering-buildcamp/1.0 (educational project)"}


def search_wikipedia(query: str) -> list[dict]:
    """Search Wikipedia for pages related to the query."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
    }
    response = requests.get(url, params=params, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()["query"]["search"]


def get_page(title: str) -> str:
    """Fetch the raw wikitext content of a Wikipedia page by its exact title."""
    url = "https://en.wikipedia.org/w/index.php"
    params = {"title": title, "action": "raw"}
    response = requests.get(url, params=params, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.text
