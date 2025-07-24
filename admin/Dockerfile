FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Install Python dependencies
RUN pip install flask

# Copy application
COPY app.py /app/
COPY templates /app/templates/

# Create logs directory
RUN mkdir -p /var/log/admin

# Create some log files
RUN echo "[2023-10-01 08:00:00] Admin logged in" > /var/log/admin/admin.log
RUN echo "[2023-10-01 09:15:22] Configuration updated" >> /var/log/admin/admin.log
RUN echo "[2023-10-01 10:30:45] Security scan completed" >> /var/log/admin/admin.log
RUN echo "[2023-10-01 11:45:12] Backup created" >> /var/log/admin/admin.log

# Create the flag in the parent directory of logs
RUN mkdir -p /var/flag
RUN FLAG_SUFFIX=$(openssl rand -hex 16) && \
    echo "FLAG{ssrf_cmd_injection_${FLAG_SUFFIX}}" > /var/flag/flag.txt
RUN chmod 644 /var/flag/flag.txt

# Expose port
EXPOSE 80

# Start the application
CMD ["python", "app.py"]