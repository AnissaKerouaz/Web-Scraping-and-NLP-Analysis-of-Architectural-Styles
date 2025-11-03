# 🏛️ Wikipedia Architectural Styles Scraper

Ever wondered how architectural styles are connected? This little Python project scrapes Wikipedia to collect article titles, URLs, full text, and categories for architectural styles — turning scattered pages into structured, analyzable data.

## What It Does

 Gathers all Wikipedia articles under the Architectural Styles category

 Fetches full article text and categories

 Handles multiple pages automatically

 Logs activity, retries failed requests, and respects polite delays

 Saves everything neatly in CSV and Parquet files for easy use

## Tech & Tools

Python

requests + BeautifulSoup for scraping

pandas for data wrangling

tqdm for progress bars

pyarrow for Parquet storage

## How to Use

Clone this repo:

git clone https://github.com/yourusername/architectural-styles-scraper.git
cd architectural-styles-scraper


Install dependencies:

pip install -r requirements.txt


Run the scraper:
Collect article titles and URLs:
python titles_urls.py  
Fetch full text and categories:
python text_metadata.py 


Check the data/ folder for your outputs.
