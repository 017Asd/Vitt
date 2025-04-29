# Build stage
FROM python:3.9-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.9-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    zlib1g \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY app/ app/
COPY requirements.txt .

# Create uploads directory and set permissions
RUN mkdir -p app/static/uploads && \
    chmod -R 755 app/static/uploads

# Set environment variables
ENV FLASK_APP=app/app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
# Add a default HF_TOKEN (you should override this when running the container)
ENV HF_TOKEN=""

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app/app.py"]
