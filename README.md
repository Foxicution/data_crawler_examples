# Example Data Crawler

## Description

Example Data Crawler is a Python package designed for teaching the basics of web
crawling at CodeAcademy. This project is tailored for beginners and utilizes
Python 3.11, along with lxml and requests libraries, focusing on practical web
data extraction techniques.

## Installation

### Using a package manager

You can install the crawler as a package: Using `pip`:

```sh
pip install example_data_crawler
```

Or using `poetry`:

```sh
poetry add example_data_crawler
```

### Cloning the repository

You can also clone the repository and install the dependencies. Using `poetry`:

```sh
git clone https://github.com/Foxicution/data_crawler_examples
cd data_crawler_examples
poetry install
```

Afterwards you can checkout and run some example scripts, e.g.:

```sh
poetry run python examples/lrytas/by_topic.py
```

## Usage

### As a module

```python
from example_data_crawler import crawl

print(crawl("lrytas", "df", query="vakcinacija", date_from="2023-01-01", time_limit=10))
```

For more examples look in the examples directory.

## Structure

The project is structured as follows:

- `example_data_crawler/`: Main package directory.
  - `__init__.py`: Package initialization file.
  - `crawlers/`: Directory containing individual crawler scripts.
    - `__init__.py`: Initialization file for crawlers module.
    - `lrytas.py`: Crawler for the Lrytas website.
    - `mersedes_crawler.py`: Crawler for the Mercedes website.
  - `definitions.py`: Definitions and utility functions.
  - `dl_image.py`: Script for downloading images.
  - `main.py`: Main script for the crawler package.
- `examples/`: Directory containing example scripts.
  - `lrytas/`: Examples for the Lrytas crawlers.
    - `all.py`: Example script for crawling all data.
    - `by_topic.py`: Example script for crawling by topic.
- `tests/`: Test scripts for the package.
  - `__init__.py`: Initialization file for tests.

## License

This project is licensed under the MIT license.
