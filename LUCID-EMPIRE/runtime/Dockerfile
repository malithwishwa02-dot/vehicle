# Lucid Empire runtime (scaffold)
FROM python:3.11-slim-bookworm

# System deps
RUN apt-get update && apt-get install -y \
    wget curl git libfaketime xvfb ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy engine & core
COPY ./LUCID-EMPIRE /app/LUCID-EMPIRE

# Install minimal python deps
RUN pip install flask

# FAKETIME
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/faketime/libfaketime.so.1
ENV FAKETIME_DONT_RESET=1

# Expose orchestrator port
EXPOSE 5050

CMD ["python", "/app/LUCID-EMPIRE/app.py"]
