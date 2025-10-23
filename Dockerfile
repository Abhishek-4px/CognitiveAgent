FROM python:3.11-slim

WORKDIR /app

COPY requirements/base.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r base.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
