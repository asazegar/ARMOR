FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY mock_backend.py .
CMD ["uvicorn", "mock_backend:app", "--host", "0.0.0.0", "--port", "8000"]