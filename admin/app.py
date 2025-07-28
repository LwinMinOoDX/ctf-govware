#!/usr/bin/env python3
from flask import Flask, request, render_template_string, redirect, url_for
import subprocess
import os

app = Flask(__name__)

# HTML template for the admin panel
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f0f0; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .warning { background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { background-color: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #0056b3; }
        .output { background-color: #f8f9fa; border: 1px solid #e9ecef; padding: 20px; border-radius: 5px; margin-top: 20px; white-space: pre-wrap; font-family: monospace; }
        .nav { display: flex; margin-bottom: 20px; }
        .nav a { padding: 10px 15px; background-color: #007bff; color: white; text-decoration: none; margin-right: 10px; border-radius: 5px; }
        .nav a:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Admin Panel</h1>
        
        <div class="warning">
            <strong>Warning:</strong> This panel is for authorized personnel only. All actions are logged.
        </div>
        
        <div class="nav">
            <a href="/">Dashboard</a>
            <a href="/logs">View Logs</a>
            <a href="/settings">Settings</a>
        </div>
        
        {% if page == 'dashboard' %}
            <h2>Dashboard</h2>
            <p>Welcome to the admin dashboard. Use the navigation above to manage the system.</p>
        {% elif page == 'logs' %}
            <h2>System Logs</h2>
            <p>Available log files:</p>
            <ul>
                <li><strong>admin.log</strong> - Administrative actions and events</li>
                <li><strong>error.log</strong> - System error messages</li>
                <li><strong>access.log</strong> - User access logs</li>
                <li><strong>flag.txt</strong> - Here's the flag but how would you read it?</li>
            </ul>
            <p>View system logs by specifying the log file name:</p>
            
            <form method="POST" action="/logs">
                <div class="form-group">
                    <label for="log_file">Log File:</label>
                    <input type="text" id="log_file" name="log_file" placeholder="admin.log" value="{{ log_file if log_file }}">
                </div>
                <button type="submit">View Logs</button>
            </form>
            
            {% if output %}
            <div class="output">{{ output }}</div>
            {% endif %}
        {% elif page == 'settings' %}
            <h2>System Settings</h2>
            <p>This section is under construction.</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(ADMIN_TEMPLATE, page='dashboard')

@app.route('/logs', methods=['GET', 'POST'])
def logs():
    output = ""
    log_file = ""
    
    if request.method == 'POST':
        log_file = request.form.get('log_file', '')
        
        if log_file:
            # VULNERABLE: Command injection in log file parameter
            # The log_file parameter is directly used in a shell command without proper validation
            command = f"cat /var/log/admin/{log_file}"
            
            try:
                # Execute the command - this is where the vulnerability lies
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5)
                
                output = f"Command executed: {command}\n\n"
                output += result.stdout
                
                if result.stderr:
                    output += "\nErrors:\n" + result.stderr
                    
            except subprocess.TimeoutExpired:
                output = "Command timed out after 5 seconds."
            except Exception as e:
                output = f"Error executing command: {str(e)}"
    
    return render_template_string(ADMIN_TEMPLATE, page='logs', log_file=log_file, output=output)

@app.route('/settings')
def settings():
    return render_template_string(ADMIN_TEMPLATE, page='settings')

@app.route('/health')
def health():
    return '{"status": "healthy", "message": "Admin service is running"}'

if __name__ == '__main__':
    # Only bind to localhost - this makes the admin panel only accessible locally
    app.run(host='0.0.0.0', port=80, debug=False)