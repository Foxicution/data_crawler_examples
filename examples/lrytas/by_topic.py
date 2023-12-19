from example_data_crawler import crawl

if __name__ == "__main__":
    # Crawling all the articles from 2021-01-01 related to 'vakcinacija'
    # and saving to csv file. It takes a while to finish, be patient.
    # In total should have ~220k articles.
    crawl("lrytas", "df", query="vakcinacija", date_from="2021-01-01").to_csv(
        "vakcinacija.csv"
    )
