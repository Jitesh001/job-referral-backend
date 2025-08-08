FROM python:3.11-slim

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files into the image
COPY . /app/

# Make entrypoint executable
RUN chmod +x /app/docker-entrypoint.sh

# Set default command
CMD ["bash", "/app/docker-entrypoint.sh"]
