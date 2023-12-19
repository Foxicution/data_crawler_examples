from example_data_crawler import crawl

if __name__ == "__main__":
    # Crawling all the articles from lrytas.lt; be patient, it takes a while.
    # Also make sure you have enough resources. You'll need ~10GB of RAM.
    # Don't run this, unless you really need the data.
    crawl("lrytas", "df").to_csv("all.csv")
