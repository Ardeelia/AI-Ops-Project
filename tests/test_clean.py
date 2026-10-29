from clean_data import clean_batch

def test_clean_batch_normalization_and_filtering():
    sample_batch = {
        "ingredients": [
            ["  Garlic! ", "Fresh Basil.", "123"],
            ["OLIVE -- OIL", "", "  "]
        ]
    }
    
    processed = clean_batch(sample_batch)
    cleaned_lists = processed["ingredients"]
    
    assert "garlic" in cleaned_lists[0]
    assert "fresh basil" in cleaned_lists[0]
    assert "123" not in cleaned_lists[0]
    
    assert "olive  oil" in cleaned_lists[1] or "olive oil" in cleaned_lists[1]
    assert "" not in cleaned_lists[1]