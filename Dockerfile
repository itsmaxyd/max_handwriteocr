# Lightweight Python OCR container with OpenAI GPT-4o
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application script
COPY handwrite_ocr.py .

# Make script executable
RUN chmod +x handwrite_ocr.py

# Create a directory for images
RUN mkdir -p /data

# Default to bash for interactive use
CMD ["/bin/bash"]
