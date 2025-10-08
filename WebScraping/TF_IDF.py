import pandas as pd
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from config import output_files  
from utils import setup


logger = setup("tfidf.log", name="tfidf")

def compute_tfidf(input_path, output_path, max_features=1000):
    logger.info(f"Loading cleaned text from {input_path}...")
    df = pd.read_parquet(input_path)
    texts = df["Cleaned_Text"].fillna("")

    logger.info(f"Computing TF-IDF (top {max_features} terms)...")
    vectorizer = TfidfVectorizer(max_features=max_features)
    tfidf_matrix = vectorizer.fit_transform(texts)

    feature_names = vectorizer.get_feature_names_out()
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)
    tfidf_df.insert(0, "Title", df["Title"])

    logger.info(f"Saving TF-IDF matrix to {output_path}...")
    tfidf_df.to_parquet(output_path, index=False)
    logger.info(f"Done! TF-IDF matrix has {len(tfidf_df)} rows and {len(feature_names)} features.")

if __name__ == "__main__":
    compute_tfidf(output_files["clean_output"], output_files["tfidf_output"])
