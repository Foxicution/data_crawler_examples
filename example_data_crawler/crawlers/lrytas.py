import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import pandas as pd
from httpx import HTTPStatusError, RequestError, get


def _get_raw_data(
    page: int,
    date_from: str | None,
    query: str | None,
    max_retries: int = 5,
    base_delay: float = 5.0,
    max_base_delay: float = 120.0,
) -> dict | None:
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
    retries = 0
    while retries < max_retries:
        try:
            response = get(
                "https://kolumbus-api.lrytas.lt/api_dev/fe/search/0/",
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except RequestError as e:
            print(f"Attempt {retries + 1} failed: {e}")
            time.sleep(min(base_delay * (2**retries), max_base_delay))
            retries += 1
        except HTTPStatusError as e:
            if e.response.status_code == 429:  # Check for 429 specifically
                retry_after = e.response.headers.get("Retry-After")
                if retry_after:
                    try:
                        retry_after = float(retry_after)
                        print(f"Retry after {retry_after}")
                        time.sleep(retry_after)
                    except ValueError:
                        pass  # If the Retry-After header is not a valid number

    print(f"Failed to get raw data after {max_retries} retries")
    return None


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
    print(f"Total pages: {total_pages}")

    data: list[dict[str, Any]] = first_page.get("articles", [])

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
                    data.extend(page_data.get("articles", []))
            except Exception as e:
                print(f"Failed to get data for page {futures[future]}: {e}")

    return pd.DataFrame(data)
