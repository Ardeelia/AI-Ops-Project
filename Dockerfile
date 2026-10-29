FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir \
    scikit-learn==1.9.1 xgboost==3.4.1 pandas==3.1.0 joblib==1.6.0 \
    streamlit requests fastapi uvicorn prometheus-fastapi-instrumentator

COPY app.py ui.py cokie.png model.joblib vectorizer.joblib label_encoder.joblib ./

EXPOSE 8000 8501

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run ui.py --server.address=0.0.0.0 --server.port=8501"]