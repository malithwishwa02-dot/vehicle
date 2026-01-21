# ==============================================================================
# PROMETHEUS-CORE Docker Container - Ubuntu 24.04 Build
# Multi-Stage Build: libfaketime compilation + Runtime environment
# Purpose: Time-Shifted Cookie Injection (Method 4) on Linux
# ==============================================================================

# ==============================================================================
# STAGE 1: Builder - Compile libfaketime from source
# ==============================================================================
FROM python:3.11-slim-bookworm AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    make \
    && rm -rf /var/lib/apt/lists/*

# Clone and compile libfaketime
WORKDIR /build
RUN git clone https://github.com/wolfcw/libfaketime.git && \
    cd libfaketime && \
    make && \
    make install PREFIX=/usr/local

# ==============================================================================
# STAGE 2: Runtime - Production Environment
# ==============================================================================
FROM python:3.11-slim-bookworm

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    xvfb \
    iptables \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome Stable
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Copy compiled libfaketime from builder stage
COPY --from=builder /usr/local/lib/faketime /usr/local/lib/faketime
COPY --from=builder /usr/local/bin/faketime /usr/local/bin/faketime

# Configure global time interception via LD_PRELOAD
ENV LD_PRELOAD=/usr/local/lib/faketime/libfaketime.so.1
ENV FAKETIME_DONT_FAKE_MONOTONIC=1

# Create application directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy and configure entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set display for Xvfb
ENV DISPLAY=:99

# Default genesis offset (90 days)
ENV GENESIS_OFFSET_DAYS=90

# Expose any necessary ports
EXPOSE 5000

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["python", "-u", "level9_operations.py"]
