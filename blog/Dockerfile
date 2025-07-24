FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Install Python dependencies
RUN pip install flask requests

# Copy application
COPY app.py /app/
COPY templates /app/templates/
COPY static /app/static/

# Expose port
EXPOSE 80

# Start the application
CMD ["python", "app.py"]