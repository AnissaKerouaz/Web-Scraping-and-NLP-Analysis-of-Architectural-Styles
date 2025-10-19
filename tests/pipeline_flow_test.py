import pytest
import pandas as pd
import pandera.pandas as pa
from pandera.pandas import Column , DataFrameSchema, Check

titles_schema = pa.DataFrameSchema({
    "article_title": Column(str, nullable= False),
    "url":Column (str, Check.str_matches(r"^https://") , nullable = False),
})

full_text_schema = pa.DataFrameSchema({
    "Title": Column(str, nullable=False),
    "URL": Column(str, Check.str_matches(r"^https://"), nullable=False),
    "Text": Column(str, Check.str_length(min_value=10)),  # ensure there's actual content
    "Categories": Column(object, nullable=True),
})
clean_schema = pa.DataFrameSchema({
    "Title": Column(str, nullable=False),
    "URL": Column(str, Check.str_matches(r"^https://"), nullable=False),
    "Text": Column(str, nullable=False),
    "Categories": Column(object, nullable=True),
    "Cleaned_Text": Column(str, Check.str_length(min_value=5)),  # cleaned text should not be empty
})
def test_pipeline_data_integrity(tmp_path):
    titles_df = pd.DataFrame({
        "article_title": ["Art Deco", "Modernism"],
        "url": [
            "https://en.wikipedia.org/wiki/Art_Deco",
            "https://en.wikipedia.org/wiki/Modernism"
        ],
    })
    full_df = pd.DataFrame({
        "Title": ["Art Deco", "Modernism"],
        "URL": [
            "https://en.wikipedia.org/wiki/Art_Deco",
            "https://en.wikipedia.org/wiki/Modernism"
        ],
        "Text": ["Art Deco is an architecture style.", "Modernism changed architecture."],
        "Categories": [["Architecture"], ["Art"]],
    })
    clean_df = pd.DataFrame({
        "Title": ["Art Deco", "Modernism"],
        "URL": [
            "https://en.wikipedia.org/wiki/Art_Deco",
            "https://en.wikipedia.org/wiki/Modernism"
        ],
        "Text": ["Art Deco is an architecture style.", "Modernism changed architecture."],
        "Categories": [["Architecture"], ["Art"]],
        "Cleaned_Text": ["art deco architecture style", "modernism change architecture"]
    })

    titles_schema.validate(titles_df)
    full_text_schema.validate(full_df)
    clean_schema.validate(clean_df)

    assert len(titles_df) == len(full_df) == len(clean_df)
    assert all(url.startswith("https://") for url in clean_df["URL"])
    assert clean_df["Cleaned_Text"].apply(lambda x: len(x.split())).min() >= 2


