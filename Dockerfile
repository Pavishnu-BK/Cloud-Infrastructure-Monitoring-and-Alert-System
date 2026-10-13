# ==============================================================================
# Cloud Infrastructure Monitoring and Automated Alert System
# Production & CI Docker Containerfile
# Base Image: Python 3.11 Slim (Lightweight, Debian-based)
# ==============================================================================

FROM python:3.11-slim

# Set environment variables for non-interactive execution and Python optimization
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    HOST=0.0.0.0 \
    DATABASE_PATH=/app/data/monitoring.db

# Install system dependencies (build-essential/gcc if needed for psutil compilation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy dependency manifest and install Python packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code, templates, and static assets
COPY app.py /app/
COPY monitoring.py /app/
COPY test_app.py /app/
COPY templates/ /app/templates/
COPY static/ /app/static/

# Ensure persistent data directory exists for SQLite database mount
# This directory is mounted via Docker volume: cloud_monitoring_data:/app/data
RUN mkdir -p /app/data

# Declare mount point for persistent data storage
VOLUME ["/app/data"]

# Expose web application port
EXPOSE 5000

# Container healthcheck using built-in Python to poll /health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health').read()" || exit 1

# Start Flask application listening on 0.0.0.0:5000
CMD ["python", "app.py"]
