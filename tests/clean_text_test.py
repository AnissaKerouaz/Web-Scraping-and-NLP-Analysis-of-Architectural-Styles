import pytest
import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema, Check
from WebScraping import transform

def test_clean_text_and_output_schema(tmp_path):
    df = pd.DataFrame({
        "Title": ["Modernism"],
        "URL": ["https://en.wikipedia.org/wiki/Modernism"],
        "Text": ["Modernism (Latin: modernus) [1] is a movement in art."]
    })

  
    output_path = tmp_path / "cleaned.parquet"
    df["Cleaned_Text"] = df["Text"].apply(transform.clean_text)
    df.to_parquet(output_path, index=False)


    schema = pa.DataFrameSchema({
        "Title": Column(str),
        "URL": Column(str, Check.str_matches(r"^https://")),
        "Text": Column(str),
        "Cleaned_Text": Column(str, Check.str_length(min_value=5))
    })

    validated = schema.validate(df)


    cleaned_text = validated["Cleaned_Text"].iloc[0]
    assert "[" not in cleaned_text  
    assert "(" not in cleaned_text  
    assert cleaned_text.islower()   
    assert "modernism" in cleaned_text 