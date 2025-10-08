from WebScraping.transform import clean_text  

def test_clean_text_basic():
    text = "This is a sample text with [1] citations and (extra info)."
    cleaned = clean_text(text)
    
    assert "[" not in cleaned
    assert "(" not in cleaned
    assert ")" not in cleaned
    
    assert "sample" in cleaned
    assert "text" in cleaned

def test_clean_text_empty_or_none():
    assert clean_text("") == ""
    assert clean_text(None) == ""
