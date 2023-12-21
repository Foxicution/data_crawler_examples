import json
from pathlib import Path

import pytest

mock_dir = Path(__file__).parent / "mocks"


@pytest.fixture
def mock_lrytas_api_response():
    with open(mock_dir / "lrytas.json", "r") as file:
        return json.load(file)
