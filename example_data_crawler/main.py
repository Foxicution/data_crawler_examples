from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from threading import Lock
from typing import Any

from lxml.etree import HTML
from requests import get

# Global variables
visited_pages = set()
visited_articles = set()
pages_queue = Queue()
articles_queue = Queue()

lock = Lock()


def query_to_url(query: str) -> str:
    return f"https://www.lrytas.lt/search?q={query}"


BASE_URL = "https://www.lrytas.lt{}"
DATE_FROM = "2021-01-01"
TERM = "vakcinavimas"


def get_articles(page: int) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Origin": "https://www.lrytas.lt",
        "Connection": "keep-alive",
        "Referer": "https://www.lrytas.lt/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Sec-GPC": "1",
    }
    params = {
        "count": "12",
        "kw_count": "12",
        "order": "pubfromdate-",
        "page": str(page),
        "dfrom": DATE_FROM,
        "q_text": TERM,
    }
    try:
        return get(
            "https://kolumbus-api.lrytas.lt/api_dev/fe/search/0/",
            params=params,
            headers=headers,
        ).json()
    except Exception:
        print(f"Failed to get raw data for {page}")


def process_articles_page(articles_page: dict[str, Any]) -> list[tuple[int, int, int]]:
    return [
        (
            article["rating"]["patiko"],
            article["rating"]["neblogai"],
            article["rating"]["nepatiko"],
        )
        for article in articles_page["articles"]
    ]


# def extract_data_from_article(page_html: str) -> tuple[int, int, int]:
#     tree = HTML(page_html)
#     return tuple(
#         int(element.strip())
#         for element in tree.xpath("//div[@class='LArticleEmotions__count']/text()")
#     )


def _process_page(page_url: str):
    with lock:
        print(page_url)
    # global visited_pages, visited_articles, pages_queue, articles_queue
    try:
        response = get(page_url)
        tree = HTML(response.text)
        for page_link in tree.xpath(
            "//a[contains(@class, 'LPagination__button')]/@href"
        ):
            full_page_url = "https://www.lrytas.lt" + page_link
            if full_page_url not in visited_pages:
                pages_queue.put(full_page_url)
                visited_pages.add(full_page_url)
        for article_link in tree.xpath("//a[@class='LPostContent__anchor']/@href"):
            article_url = "https://www.lrytas.lt" + article_link
            if article_url not in visited_articles:
                visited_articles.add(article_url)
                articles_queue.put(article_url)
    except Exception as e:
        print("Error retrieving url:", e)


def main():
    """
    Main function for the web crawling application.

    This function starts the crawling process by initializing the queue of pages to be crawled and the set of visited pages. It then creates a `ThreadPoolExecutor` with a maximum of 10 worker threads and enters a loop that repeatedly submits tasks to the executor until all pages have been crawled. Each task involves fetching a URL from the queue, processing it using the `process_page` function, and adding any new URLs discovered to the queue.

    Args:
        None

    Returns:
        None

    Raises:
        None

    Example usage:
        ```python
        main()

    """
    initial_url = query_to_url("vakcinavimas")
    pages_queue.put(initial_url)
    visited_pages.add(initial_url)
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = set()
        while not pages_queue.empty() or futures:
            # Submit new tasks from the queue
            while not pages_queue.empty() and len(futures) < 10:
                page = pages_queue.get()
                future = executor.submit(process_page, page)
                futures.add(future)
            # Wait for the next future to complete
            done = as_completed(futures, timeout=None)
            for future in done:
                futures.remove(future)
    print("Finished processing all pages.")


if __name__ == "__main__":
    main()
