import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

from WebScraping.config import headers, output_files, delay_time
from WebScraping.utils import setup

logger = setup("text_metadata.log")

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
        logger.warning(f"Failed to fetch {url}: {e}")
        return ""

def fetch_categories(soup):
    categories = [a.get_text() for a in soup.select("#mw-normal-catlinks ul li a")]
    return categories

if __name__ == "__main__":
    input_file = f"data/{output_files['titles_output']}"
    output_file = f"data/{output_files['full_text_output']}"

    logger.info(f"Loading titles from {input_file}")
    df_titles = pd.read_csv(input_file)
    full_data = []

    for idx, row in df_titles.iterrows():
        title = row.get("Article_Title") or row.get("Style")
        url = row["URL"]

        logger.info(f"Fetching: {title}")
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
    df_full.to_parquet(output_file, engine="pyarrow", index=False)
    logger.info(f"Saved full articles to {output_file} ({len(df_full)} rows)")
