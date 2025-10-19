import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from WebScraping.config import headers, delay_time
from WebScraping.utils import setup
from prefect import task 

logger = setup(loggingfile="text_metadata.log", name=__name__)

session = requests.Session()
session.headers.update(headers)


def fetch_article_text(url):
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)
        return text
    except Exception as e:
        logger.warning(f"error {url}: {e}")
        return ""


def fetch_categories(soup):
    categories = [a.get_text() for a in soup.select("#mw-normal-catlinks ul li a")]
    return categories

@task(retries=2, retry_delay_seconds=3)
def fetch_articles_from_csv(input_csv, output_parquet):
    logger.info(f"loading the titles from {input_csv}")
    df_titles = pd.read_csv(input_csv)

    if df_titles.empty:
        logger.warning("csv is empty")
        return

    full_data = []

    for idx, row in df_titles.iterrows():
        title = row.get("article_title") or row.get("Article_Title") or row.get("Style")
        url = row.get("url") or row.get("URL")

        if not url:
            logger.warning(f"no url is found, skipping: {idx}")
            continue

        logger.info(f"fetching : {title}")

        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")

            text = fetch_article_text(url)
            categories = fetch_categories(soup)

            full_data.append({
                "Title": title,
                "URL": url,
                "Text": text,
                "Categories": categories
            })

        except Exception as e:
            logger.warning(f"Failed {title}: {e}")
            full_data.append({
                "Title": title,
                "URL": url,
                "Text": "",
                "Categories": []
            })

        time.sleep(delay_time + random.random() * 0.5)

    df_full = pd.DataFrame(full_data)

    if not df_full.empty:
        df_full.to_parquet(output_parquet, engine="pyarrow", index=False)
        logger.info(f"saved full articles to {output_parquet} ({len(df_full)} rows)")
    else:
        logger.warning("no data collected, parquet is not getting saved")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv", required=True)
    parser.add_argument("--output_parquet", required=True)
    args = parser.parse_args()

    fetch_articles_from_csv(args.input_csv, args.output_parquet)
