#!/usr/bin/env python3
from flask import Flask, request, render_template, redirect, url_for, jsonify
import requests
import os

app = Flask(__name__, template_folder='/app/blog/templates', static_folder='/app/blog/static')

# Sample blog posts
posts = [
    {
        'id': 1,
        'title': 'Welcome to Our Blog',
        'content': 'This is our first blog post. We hope you enjoy reading our content!',
        'author': 'Admin'
    },
    {
        'id': 2,
        'title': 'Web Security Basics',
        'content': 'Today we\'ll discuss some web security basics including SSRF vulnerabilities.',
        'author': 'Security Expert'
    },
    {
        'id': 3,
        'title': 'Docker for Beginners',
        'content': 'Learn how to use Docker to containerize your applications.',
        'author': 'DevOps Engineer'
    },
    {
        'id': 4,
        'title': 'Hidden Features',
        'content': 'Did you know there\'s an admin panel? Only accessible locally though!',
        'author': 'Admin'
    },
    {
        'id': 5,
        'title': 'CTF Challenges',
        'content': 'Capture The Flag challenges are a great way to learn about security.',
        'author': 'Security Expert'
    }
]

@app.route('/')
def home():
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    # Find the post with the given ID
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        return render_template('error.html', message='Post not found'), 404
    
    # Get the previous and next post IDs for pagination
    prev_id = post_id - 1 if post_id > 1 else None
    next_id = post_id + 1 if post_id < len(posts) else None
    
    return render_template('post.html', post=post, prev_id=prev_id, next_id=next_id)

# VULNERABLE ENDPOINT - SSRF vulnerability in the fetch_url parameter
@app.route('/fetch-next', methods=['GET', 'POST'])
def fetch_next():
    url = request.args.get('url', '')
    
    # VULNERABLE: No validation on the URL - can be used for SSRF
    if url:
        try:
            # This allows attackers to make requests to internal services
            # For single container, admin is accessible at localhost:5001
            if request.method == 'POST':
                # Forward POST data for SSRF attacks
                response = requests.post(url, data=request.form, timeout=3)
            else:
                response = requests.get(url, timeout=3)
            return response.text
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'No URL provided'}), 400

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Blog service is running'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)