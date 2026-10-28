import pandas as pd
import pyarrow.parquet as pq
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight
import xgboost as xgb
import mlflow
import joblib

try:
    df = pd.read_parquet("data/train_cleaned.parquet")
except TypeError:
    table = pq.read_table("data/train_cleaned.parquet")
    df = pd.DataFrame({
        "cuisine": table["cuisine"].to_pylist(),
        "ingredients": table["ingredients"].to_pylist()
    })

df["formatted_ingredients"] = df["ingredients"].apply(
    lambda x: " ".join([str(ing).replace(" ", "_") for ing in x])
)

vectorizer = TfidfVectorizer(lowercase=True)
X = vectorizer.fit_transform(df["formatted_ingredients"])

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["cuisine"])

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

sample_weights = compute_sample_weight(class_weight="balanced", y=y_train)

params = {
    "n_estimators": 100,
    "max_depth": 6,
    "learning_rate": 0.1,
    "random_state": 42
}

mlflow.set_experiment("yummly_xgboost")

with mlflow.start_run():
    mlflow.log_params(params)
    
    model = xgb.XGBClassifier(**params)
    model.fit(X_train, y_train, sample_weight=sample_weights)
    
    accuracy = model.score(X_val, y_val)
    mlflow.log_metric("val_accuracy", accuracy)
    mlflow.xgboost.log_model(model, "model")

    print(f"Validation Accuracy: {accuracy:.4f}")

joblib.dump(model, "model.joblib")
joblib.dump(vectorizer, "vectorizer.joblib")
joblib.dump(label_encoder, "label_encoder.joblib")
print("Reset complete! Saved fresh model, vectorizer, and label encoder artifacts.")
