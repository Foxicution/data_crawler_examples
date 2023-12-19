import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import chain

import pandas as pd
from httpx import get


def _get_raw_data(page: int, date_from: str | None, query: str | None) -> dict:
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
    }
    if date_from is not None:
        params["dfrom"] = date_from
    if query is not None:
        params["query"] = query
    try:
        return get(
            "https://kolumbus-api.lrytas.lt/api_dev/fe/search/0/",
            params=params,
            headers=headers,
        ).json()
    except Exception as e:
        print(f"Failed to get raw data for {page}: {e}")


def crawl_lrytas(
    date_from: str | None = None,
    query: str | None = None,
    time_limit: int | None = None,
) -> pd.DataFrame:
    """
    Crawls and compiles articles from the lrytas.lt website based on the specified date range and query.
    The function employs multi-threading to fetch pages concurrently. It can be limited by a specified time limit.

    Args:
        date_from (str | None): The starting date for filtering articles, formatted as 'YYYY-MM-DD'. If None,
                                filtering by date is not applied.
        query (str | None): The search query for filtering articles. If None, filtering by query is not applied.
        time_limit (int | None): The maximum time in seconds allowed for the crawling process. If None, the process
                                 continues until all available pages are fetched.

    Returns:
        pd.DataFrame: A DataFrame containing all collected articles. Each row in the DataFrame represents an article,
                      with columns corresponding to the details of the articles as provided by the lrytas.lt API.

    Notes:
        - If the request for the first page fails, an empty DataFrame is returned.
        - If fetching data for a specific page fails, that page is skipped, and the process continues with the next page.
        - If the specified time limit is reached before all pages are fetched, the process is terminated, and data
          collected up to that point is returned.

    Example:
        >>> crawl_lrytas('2021-01-01', 'vakcinavimas')
        (Returns a DataFrame containing articles from lrytas.lt starting from January 1, 2021, related to 'vakcinavimas')
    """
    start_time = time.time()
    first_page = _get_raw_data(0, date_from, query)
    if not first_page:
        return pd.DataFrame()

    total_pages = first_page.get("totalPages", 0)
    print(total_pages)

    data = [first_page.get("articles")]

    with ThreadPoolExecutor(10) as pool:
        futures = {
            pool.submit(_get_raw_data, page, date_from, query): page
            for page in range(1, total_pages)
        }

        for future in as_completed(futures):
            if time_limit is not None and time.time() - start_time > time_limit:
                print("Time limit exceeded during crawling.")
                break

            try:
                page_data = future.result()
                if page_data:
                    data.append(page_data.get("articles"))
            except Exception as e:
                print(f"Failed to get data for page {futures[future]}: {e}")

    return pd.DataFrame(list(chain.from_iterable(filter(None, data))))


if __name__ == "__main__":
    dfrom = "2021-01-01"  # Example date
    q_text = "vakcinavimas"  # Example query
    data = crawl_lrytas(dfrom, q_text)
    data.to_csv("lrytas_data.csv")
