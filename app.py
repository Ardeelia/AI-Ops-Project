from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Recipe Cuisine Predictor")

model = joblib.load("model.joblib")
vectorizer = joblib.load("vectorizer.joblib")
label_encoder = joblib.load("label_encoder.joblib")

class RecipeRequest(BaseModel):
    ingredients: list[str]

@app.post("/predict")
def predict_cuisine(recipe: RecipeRequest):

    formatted_recipe = " ".join([ing.replace(" ", "_") for ing in recipe.ingredients])
    
    X_input = vectorizer.transform([formatted_recipe])
    pred_idx = model.predict(X_input)[0]
    cuisine_name = label_encoder.inverse_transform([pred_idx])[0]

    return {
        "cuisine": str(cuisine_name)
    }

Instrumentator().instrument(app).expose(app)
