#!/usr/bin/env python3
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "service": "Logs Server",
        "status": "running",
        "endpoints": [
            "/logs",
            "/health"
        ]
    })

@app.route('/logs')
def logs():
    log_file = request.args.get('file', 'system.log')
    log_path = f"/var/log/app/{log_file}"
    
    try:
        if os.path.exists(log_path) and os.path.isfile(log_path):
            with open(log_path, 'r') as f:
                content = f.read()
            return content, 200, {'Content-Type': 'text/plain'}
        else:
            return f"Log file not found: {log_file}", 404, {'Content-Type': 'text/plain'}
    except Exception as e:
        return f"Error reading log file: {str(e)}", 500, {'Content-Type': 'text/plain'}

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "message": "Logs service is running"
    })

if __name__ == '__main__':
    # Only accessible from the internal network
    app.run(host='0.0.0.0', port=80, debug=False)