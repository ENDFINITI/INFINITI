from flask import Flask, request, jsonify
import hashlib
import json
import os

app = Flask(__name__)
DATA_FILE = 'users.json'  # The file where we will store the users

# Load users from the file (if the file exists)
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save users to the file
def save_users(users):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f)

# Signup route - stores user data
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Load existing users from file
    users = load_users()

    # Check if the username already exists
    if username in users:
        return jsonify({'success': False, 'message': 'Username already exists'}), 400

    # Hash the password using SHA-256 for better security
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    # Add the new user to the users dictionary
    users[username] = hashed_pw

    # Save the updated users data back to the file
    save_users(users)

    return jsonify({'success': True, 'message': 'User created successfully!'}), 200

# Login route - checks if the user exists and the password is correct
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Load existing users from file
    users = load_users()

    # Hash the password provided by the user to compare
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    # Check if the username exists and if the password matches
    if users.get(username) == hashed_pw:
        return jsonify({'success': True, 'message': 'Login successful!'}), 200
    return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)
