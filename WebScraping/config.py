
start_url = "https://en.wikipedia.org/wiki/Category:Architectural_styles"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    )
}

output_files = {
    "titles_output": "data/architectural_styles_pages.csv",
    "full_text_output": "data/architectural_styles_full.parquet",
    "clean_output": "data/architectural_styles_clean.parquet",
    "tfidf_output": "data/architectural_styles_tfidf.parquet",  
}

delay_time = 0.5

retrying_times = 3
