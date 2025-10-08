import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from tqdm import tqdm
from WebScraping import config
from utils import setup


logger = setup(loggingfile="logging.log", name="scraper")


session = requests.Session()
session.headers.update(config.headers)

base_url = "https://en.wikipedia.org"


def get_data(url, retries=config.retrying_times, timeout=10):
    for i in range(retries):
        try:
            response = session.get(url, timeout =timeout)
            response.raise_for_status()
            return BeautifulSoup(response.text, "lxml")
        except Exception as e:
            logger.warning(f"Attempt {i+1}/{retries} failed for {url}: {e}")
            time.sleep((2 ** i) + random.random())
    return None



def extract_page_links(soup):
    results = []
    pages_div = soup.find("div", id="mw-pages")
    if pages_div:
        for a in pages_div.select("div.mw-category-group a"):
            href = a.get("href")
            if href and href.startswith("/wiki/") and not href.startswith("/wiki/Category:"):
                results.append((a.get_text(strip=True), base_url + href))
    return results



def find_next_page(soup):
    next_link = soup.find("a", string="next page")
    return base_url + next_link.get("href") if next_link else None


def save_to_csv(file, rows, write_header=False):
    mode = "w" if write_header else "a"
    with open(f"data/{file}", mode, newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["Article_Title", "URL"])
        writer.writerows(rows)


def scrape_category(start_url, output_file=config.output_files["titles_output"]):
    current_url = start_url
    all_results = []

    save_to_csv(output_file, [], write_header=True)

    while current_url:
        logger.info(f"Scraping category page: {current_url}")
        soup = get_data(current_url)
        if soup is None:
            logger.warning(f"Skipping page {current_url} due to fetch errors.")
            break

        results = extract_page_links(soup)
        if results:
            for article in tqdm(results, desc="Articles on page"):
                all_results.append(article)
            save_to_csv(output_file, results)

        current_url = find_next_page(soup)
        time.sleep(config.delay_time + random.random() * 0.5)

    logger.info(f"Total articles collected: {len(all_results)}")
    return all_results


if __name__ == "__main__":
    scrape_category(config.start_url)
