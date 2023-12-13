import json
from unittest.mock import Mock, patch

import pytest
from requests import Response

from paulius_data_crawler.definitions import test_dir
from paulius_data_crawler.main import main, process_articles_page


@pytest.fixture
def articles_page():
    with open(test_dir / "articles.json") as f:
        content = json.load(f)
    return content


def test_process_articles_page(articles_page):
    assert process_articles_page(articles_page) == [
        (21, 2, 8),
        (35, 5, 228),
        (3, 0, 0),
        (6, 0, 21),
        (0, 0, 0),
        (1, 0, 0),
        (11, 3, 93),
        (6, 2, 1),
        (15, 2, 118),
        (1, 0, 0),
        (3, 1, 1),
        (62, 0, 75),
    ]


def fake_get(url: str) -> Response:
    if not hasattr(fake_get, "call_count"):
        fake_get.call_count = 0
    fake_get.call_count += 1
    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    content = b"<html></html>"
    if url == "https://www.lrytas.lt/search?q=vakcinavimas":
        with open(test_dir / "articles_page.html", "rb") as f:
            content = f.read()
    mock_response.text = content
    return mock_response


def test_process_page():
    with patch("paulius_data_crawler.main.get", side_effect=fake_get) as p:
        main()
        assert p.call_count == 7
