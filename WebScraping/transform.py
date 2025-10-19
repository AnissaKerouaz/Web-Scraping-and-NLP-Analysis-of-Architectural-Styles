import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from WebScraping.utils import setup  , get_args 
from prefect import task 

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")


logger = setup(loggingfile="logging.log", name=__name__)

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

@task
def clean_parquet(input_path, output_path):
    logger.info(f"Loading full text Parquet from {input_path}...")
    df = pd.read_parquet(f"{input_path}")

    logger.info("cleaning the texts")
    df["Cleaned_Text"] = df["Text"].apply(clean_text)

    logger.info(f"saving data to {output_path}...")
    df.to_parquet(f"{output_path}", index=False)
    logger.info(f"data has {len(df)} rows.")

if __name__ == "__main__":
    args = get_args()
    clean_parquet(args.start_url, args.output_file)