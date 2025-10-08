import logging
import argparse
import os

def setup(loggingfile="logging.log", name="scraper"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(ch)

        os.makedirs("data", exist_ok=True)
        fh = logging.FileHandler(os.path.join("data", loggingfile))
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(fh)

    return logger

def get_args():
    parser = argparse.ArgumentParser(description="Scrape Wikipedia category pages")
    parser.add_argument(
        "--start-url",
        type=str,
        default="https://en.wikipedia.org/wiki/Category:Architectural_styles",
        help="Starting URL of the Wikipedia category",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default="data/architectural_styles_pages.csv", 
        help="CSV file to save scraped article titles and URLs",
    )
    return parser.parse_args()
