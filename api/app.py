from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# In-memory user database
users = {
    "user@example.com": generate_password_hash("password123")
}

@app.route('/')
def index():
    if 'user_email' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
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

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', email=session['user_email'])

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("Server starting...")
    print("Demo credentials:")
    print("  Email: user@example.com")
    print("  Password: password123")
    app.run(debug=True, host='0.0.0.0', port=5000)