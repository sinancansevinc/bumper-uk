# Dockerfile

# Use an official Python image as the base
FROM python:3.9-slim

# Install system dependencies for Python packages (such as psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]