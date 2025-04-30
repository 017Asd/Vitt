# Development stage
FROM python:3.9-slim as development

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    zlib1g \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p app/static/uploads && \
    chmod -R 755 app/static/uploads

# Development specific settings
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

# Command for development
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

# Production stage
FROM development as production

# Production specific settings
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

# Remove development dependencies if any
RUN pip uninstall -y debugpy

# Add .env file to the container
COPY .env /app/.env

# Command for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
