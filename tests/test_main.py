import json

import pytest

from paulius_data_crawler.definitions import test_dir
from paulius_data_crawler.main import process_articles_page


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
