FROM python:3.11-slim
WORKDIR /rdrs

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p data logs data/sandbox data/quarantine

EXPOSE 8000
CMD ["python", "app/main.py"]