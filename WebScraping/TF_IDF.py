import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from WebScraping.config import output_files  
from WebScraping.utils import setup
from prefect import task 


logger = setup("tfidf.log", name="tfidf")
@task
def compute_tfidf(input_path, output_path, max_features=1000):
    logger.info(f"loading cleaned text from {input_path}")
    df = pd.read_parquet(input_path)
    texts = df["Cleaned_Text"].fillna("")

    logger.info(f"computing tfidf (top {max_features} terms)")
    vectorizer = TfidfVectorizer(max_features=max_features)
    tfidf_matrix = vectorizer.fit_transform(texts)

    feature_names = vectorizer.get_feature_names_out()
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)
    tfidf_df.insert(0, "Title", df["Title"])

    logger.info(f"saving tfidf matrix to {output_path}")
    tfidf_df.to_parquet(output_path, index=False)
    logger.info(f"tfidf had {len(tfidf_df)} rows and {len(feature_names)} features")

if __name__ == "__main__":
    compute_tfidf(output_files["clean_output"], output_files["tfidf_output"])
