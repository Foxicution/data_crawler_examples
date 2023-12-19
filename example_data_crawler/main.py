from io import StringIO
from typing import Any, Callable, Literal

import pandas as pd

from .crawlers import crawl_lrytas

CRAWLERS: dict[str, Callable[..., pd.DataFrame]] = {
    "lrytas": crawl_lrytas,
}


def crawl(
    source: Literal["lrytas"],
    return_format: Literal["csv", "df", "records"] = "csv",
    **kwargs,
) -> pd.DataFrame | str | list[dict[str, Any]]:
    """
    Crawls data from a specified source and returns it in the specified format.

    This function uses a dictionary of crawler functions (`CRAWLERS`) to fetch data
    from various sources. The data is then returned either as a pandas DataFrame
    or as a CSV string, based on the `return_format` argument.

    Args:
        source (str): The key of the source to crawl. Must be one of the keys in `CRAWLERS`.
        return_format (str, optional): The format to return the data in. Can be 'df' for DataFrame
                                       or 'csv' for CSV string. Defaults to 'csv'.
        **kwargs: Additional keyword arguments passed to the crawler function.

    Returns:
        Union[pd.DataFrame, str]: The crawled data. Returns a pandas DataFrame if `return_format`
                                  is 'df', otherwise returns a CSV string.

    Raises:
        ValueError: If the `source` is not a key in `CRAWLERS`.

    Examples:
        Crawling data from 'lrytas' and getting it in DataFrame format:
        >>> data = crawl("lrytas", return_format="df", date_from="2021-01-01", query="vakcinavimas")

        Crawling data from 'lrytas' and getting it as a CSV string:
        >>> csv_data = crawl("lrytas", date_from="2021-01-01", query="vakcinavimas")
    """
    if source not in CRAWLERS:
        raise ValueError(f"Source '{source}' is not supported.")

    data = CRAWLERS[source](**kwargs)

    if return_format == "df":
        return data
    elif return_format == "csv":
        with StringIO() as out:
            data.to_csv(out)
            content = out.getvalue()
        return content
    elif return_format == "records":
        data.to_dict(orient="records")
