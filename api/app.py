from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# In-memory user database
users = {
    "user@example.com": generate_password_hash("password123")
}

@app.route('/')
def index():
    try:
        if 'user_email' in session:
            return redirect(url_for('dashboard'))
        return render_template('index.html')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        if email in users and check_password_hash(users[email], password):
            session['user_email'] = email
            return jsonify({'message': 'Login successful!'}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    try:
        if 'user_email' not in session:
            return redirect(url_for('index'))
        return render_template('dashboard.html', email=session['user_email'])
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/logout')
def logout():
    try:
        session.pop('user_email', None)
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {str(e)}", 500

# This is the critical part for Vercel
# Export the app as the handler
handler = app