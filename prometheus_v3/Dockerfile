FROM python:3.10-slim

WORKDIR /app

# Install System Dependencies for LevelDB
RUN apt-get update && apt-get install -y \
    build-essential \
    libleveldb-dev \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
RUN mkdir output logs

EXPOSE 5000

CMD ["python", "app.py"]
