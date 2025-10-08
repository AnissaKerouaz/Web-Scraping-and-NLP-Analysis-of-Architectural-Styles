import pandas as pd
import re
import nltk
import logging
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from WebScraping.config import output_files 

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def clean_text(text):
    if pd.isna(text) or not isinstance(text, str):
        return ""
    
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    tokens = nltk.word_tokenize(text.lower())

    stops = set(stopwords.words("english"))
    tokens = [t for t in tokens if t.isalpha() and t not in stops]

    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    return " ".join(tokens)

def clean_parquet(input_path, output_path):
    logger.info(f"Loading full text Parquet from {input_path}...")
    df = pd.read_parquet(f"data/{input_path}")

    logger.info("Cleaning texts...")
    df["Cleaned_Text"] = df["Text"].apply(clean_text)

    logger.info(f"Saving cleaned dataset to {output_path}...")
    df.to_parquet(f"data/{output_path}", index=False)
    logger.info(f"Done! Cleaned dataset has {len(df)} rows.")

if __name__ == "__main__":
    clean_parquet(output_files["full_text_output"], output_files["clean_output"])
