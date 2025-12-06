FROM python:3.10-slim

WORKDIR /app

# Install system dependencies required by pandas/numpy/matplotlib
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy application code
COPY . /app

# Default working command
CMD ["python"]
