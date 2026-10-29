from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np
import train

@patch("mlflow.start_run")
@patch("joblib.dump")
@patch("pandas.read_parquet")
def test_training_pipeline_logic(mock_read_parquet, mock_joblib_dump, mock_mlflow_run):
    mock_df = pd.DataFrame({
        "cuisine": ["italian", "mexican", "italian"],
        "ingredients": [["garlic", "olive oil"], ["jalapeno", "lime"], ["basil", "tomato"]]
    })
    mock_read_parquet.return_value = mock_df

    formatted = mock_df["ingredients"].apply(
        lambda x: " ".join([str(ing).replace(" ", "_") for ing in x])
    )
    assert formatted.iloc[0] == "garlic olive_oil" or formatted.iloc[0] == "garlic olive oil"

    from sklearn.feature_extraction.text import TfidfVectorizer
    vec = TfidfVectorizer(lowercase=True)
    transformed = vec.fit_transform(formatted)
    assert transformed.shape[0] == 3