from unittest.mock import patch
import pytest
from streamlit.testing.v1 import AppTest

def test_app_initialization():
    """Test that the app loads successfully and renders the main title."""
    at = AppTest.from_file("ui.py").run()
    assert not at.exception
    assert at.title[0].value == "ChefAI Classifier"

def test_ingredient_parsing_and_tags():
    """Test that entering ingredients correctly splits them and generates tag components."""
    at = AppTest.from_file("ui.py").run()

    at.text_area[0].input("garlic, basil, olive oil").run()

    markdown_contents = [element.value for element in at.markdown]
    combined_markdown = " ".join(markdown_contents)
    
    assert "garlic" in combined_markdown
    assert "basil" in combined_markdown
    assert "olive oil" in combined_markdown

@patch("requests.post")
def test_successful_prediction(mock_post):
    """Test clicking the predict button when the API successfully returns a cuisine."""

    class MockResponse:
        status_code = 200
        def json(self):
            return {"cuisine": "italian"}

    mock_post.return_value = MockResponse()

    at = AppTest.from_file("ui.py").run()

    at.text_area[0].input("pasta, tomato, cheese").run()
    at.button[0].click().run()

    assert not at.exception

    markdown_contents = [element.value for element in at.markdown]
    combined_markdown = " ".join(markdown_contents)
    assert "Predicted Cuisine: Italian" in combined_markdown

@patch("requests.post")
def test_api_connection_error(mock_post):
    """Test graceful handling when the backend API connection fails."""
    import requests

    mock_post.side_effect = requests.exceptions.ConnectionError("Connection refused")

    at = AppTest.from_file("ui.py").run()

    at.button[0].click().run()
    
    assert not at.exception

    error_messages = [err.value for err in at.error]
    assert any("Connection Failed" in msg for msg in error_messages)