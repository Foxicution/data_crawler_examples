import pytest


def test_mock_lrytas_api_response(mock_lrytas_api_response):
    pytest.assume(isinstance(mock_lrytas_api_response, dict))
    pytest.assume(
        tuple(mock_lrytas_api_response.keys())
        == ("articles", "authors", "nextPage", "tags", "totalPages")
    )
