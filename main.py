# main.py
import logging
import os
from WebScraping.titles_urls import scrape_category
from WebScraping.text_metadata import fetch_full_text_metadata
from WebScraping.transform import clean_texts
from WebScraping.TF_IDF import compute_tfidf
import WebScraping.config as config
# Ensure log dSrectory exists
os.makedirs("data/logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("data/logs/pipeline.log"),
        logging.StreamHandler()
    ]
)

def main():
    logging.info("Starting the full pipeline...")

    logging.info("Step 1: Scraping titles and URLs")
    scrape_category(config., config.output_files["titles_output"])

    logging.info("Step 2: Fetching full text and metadata")
    fetch_full_text_metadata(config.output_files["titles_output"], config.output_files["full_text_output"])

    logging.info("Step 3: Cleaning texts")
    clean_texts(config.output_files["full_text_output"], config.output_files["clean_output"])

    logging.info("Step 4: Computing TF-IDF")
    compute_tfidf(config.output_files["clean_output"], config.output_files["tfidf_output"])

    logging.info("Pipeline completed successfully!")

if __name__ == "__main__":
    main()
