from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

with patch("joblib.load") as mock_load, \
     patch("prometheus_fastapi_instrumentator.Instrumentator.instrument") as mock_inst, \
     patch("prometheus_fastapi_instrumentator.Instrumentator.expose") as mock_exp:
    
    mock_model = MagicMock()
    mock_model.predict.return_value = [0]
    
    mock_vectorizer = MagicMock()
    mock_vectorizer.transform.return_value = "mock_transformed_features"
    
    mock_label_encoder = MagicMock()
    mock_label_encoder.inverse_transform.return_value = ["italian"]
    
    mock_load.side_effect = [mock_model, mock_vectorizer, mock_label_encoder]
    mock_inst.return_value.expose.return_value = None

    from app import app

client = TestClient(app)

def test_predict_endpoint_success():
    payload = {"ingredients": ["garlic", "basil", "olive oil"]}
    response = client.post("/predict", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "cuisine" in data
    assert data["cuisine"] == "italian"

def test_predict_endpoint_invalid_payload():
    payload = {"wrong_key": ["garlic"]}
    response = client.post("/predict", json=payload)
    
    assert response.status_code == 422