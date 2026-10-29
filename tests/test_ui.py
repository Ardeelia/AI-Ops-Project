from pathlib import Path
from unittest.mock import patch
import pytest
from streamlit.testing.v1 import AppTest

UI_PATH = str(Path(__file__).parent.parent / "ui.py")

@patch("os.path.exists", return_value=False)
def test_ui_initial_render(mock_exists):
    at = AppTest.from_file(UI_PATH)
    at.run()
    
    assert len(at.title) >= 1
    assert "ChefAI" in at.title[0].value

@patch("os.path.exists", return_value=False)
@patch("requests.post")
def test_ui_prediction_flow(mock_requests_post, mock_exists):
    mock_response = patch("requests.Response").start()
    mock_response.status_code = 200
    mock_response.json.return_value = {"cuisine": "mexican"}
    mock_requests_post.return_value = mock_response

    at = AppTest.from_file(UI_PATH)
    at.run()

    at.text_area[0].set_value("corn tortillas, jalapeno, cilantro")
    
    at.button[0].click()
    at.run()

    rendered_markdown = "".join([el.value for el in at.markdown])
    assert "Predicted Cuisine: Mexican" in rendered_markdown