FROM python:3.9-slim

# Create app directory
WORKDIR /app

# Install Python dependencies
RUN pip install flask

# Copy application
COPY app.py /app/

# Create logs directory
RUN mkdir -p /var/log/app

# Create some log files with sensitive information
RUN echo "[2023-10-01 08:00:00] System started" > /var/log/app/system.log
RUN echo "[2023-10-01 09:15:22] User login: admin" >> /var/log/app/system.log
RUN echo "[2023-10-01 10:30:45] Configuration updated" >> /var/log/app/system.log
RUN echo "[2023-10-01 11:45:12] Backup created" >> /var/log/app/system.log

# Create the flag in the parent directory of logs
RUN mkdir -p /var/flag
RUN FLAG_SUFFIX=$(openssl rand -hex 16) && \
    echo "FLAG{ssrf_cmd_injection_${FLAG_SUFFIX}}" > /var/flag/flag.txt
RUN chmod 644 /var/flag/flag.txt

# Expose port
EXPOSE 80

# Start the application
CMD ["python", "app.py"]