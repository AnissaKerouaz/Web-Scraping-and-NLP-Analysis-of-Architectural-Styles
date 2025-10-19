import logging
import os
from WebScraping.titles_urls import scrape_category
from WebScraping.text_metadata import fetch_articles_from_csv
from WebScraping.transform import clean_parquet
from WebScraping.TF_IDF import compute_tfidf
import WebScraping.config as config
from prefect import flow

log_dir = os.path.join("data", "log")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "pipeline.log")),
        logging.StreamHandler()
    ]
)
@flow(name="pipeline for architecture styles")
def main():
    logging.info("start of pipeline")
    logging.info("scraping titles and urls")
    scrape_category(config.start_url, config.output_files["titles_output"])

    logging.info("fetching full text and metadata")
    fetch_articles_from_csv(
        config.output_files["titles_output"],
        config.output_files["full_text_output"]
    )

    logging.info("cleaning texts")
    clean_parquet(
        config.output_files["full_text_output"],
        config.output_files["clean_output"]
    )

    logging.info("computing tfidf")
    compute_tfidf(
        config.output_files["clean_output"],
        config.output_files["tfidf_output"]
    )

    logging.info("pipeline done")


if __name__ == "__main__":
    main()
